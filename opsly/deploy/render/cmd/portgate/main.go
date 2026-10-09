// Command portgate enables a fail-closed, non-overlapping Render handoff for
// Division Swarm's single-owner PostgreSQL runtime. It does not release locks.
package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"os/exec"
	"os/signal"
	"strconv"
	"strings"
	"syscall"
	"time"
)

const internalAddress = "127.0.0.1:18941"
const retryDelay = 3 * time.Second

type tailWriter struct{ buf []byte }

func (w *tailWriter) Write(p []byte) (int, error) {
	w.buf = append(w.buf, p...)
	if len(w.buf) > 16384 {
		w.buf = append([]byte(nil), w.buf[len(w.buf)-16384:]...)
	}
	return len(p), nil
}

func ownershipConflict(exitErr error, output string) bool {
	var err *exec.ExitError
	return errors.As(exitErr, &err) && err.ExitCode() == 3 && (strings.Contains(output, "startup ownership lease") || strings.Contains(output, "Another swarm serve is already running"))
}

func serveHTTP(ctx context.Context, port string) (net.Listener, *http.Server, error) {
	n, err := strconv.Atoi(port)
	if err != nil || n < 1 || n > 65535 {
		return nil, nil, fmt.Errorf("invalid public port")
	}
	listener, err := net.Listen("tcp", fmt.Sprintf("0.0.0.0:%d", n))
	if err != nil {
		return nil, nil, err
	}
	backend := &url.URL{Scheme: "http", Host: internalAddress}
	proxy := httputil.NewSingleHostReverseProxy(backend)
	proxy.Transport = &http.Transport{DialContext: (&net.Dialer{Timeout: 2 * time.Second}).DialContext, ResponseHeaderTimeout: 25 * time.Second, IdleConnTimeout: 30 * time.Second}
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, e error) {
		http.Error(w, "Swarm runtime not ready", http.StatusServiceUnavailable)
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/_opsly/gate/live", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}
		w.Header().Set("Content-Type", "text/plain")
		io.WriteString(w, "gate-alive\n")
	})
	mux.HandleFunc("/_opsly/gate/ready", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			w.WriteHeader(http.StatusMethodNotAllowed)
			return
		}
		c, e := net.DialTimeout("tcp", internalAddress, 400*time.Millisecond)
		if e != nil {
			http.Error(w, "runtime not ready", 503)
			return
		}
		c.Close()
		io.WriteString(w, "backend-listening\n")
	})
	mux.Handle("/", proxy)
	server := &http.Server{Handler: mux, ReadHeaderTimeout: 6 * time.Second, IdleTimeout: 35 * time.Second}
	go func() {
		e := server.Serve(listener)
		if e != nil && e != http.ErrServerClosed {
			log.Printf("gate server error: %v", e)
		}
	}()
	go func() {
		<-ctx.Done()
		stop, cancel := context.WithTimeout(context.Background(), 4*time.Second)
		defer cancel()
		server.Shutdown(stop)
	}()
	return listener, server, nil
}

func runChild(ctx context.Context, executable string, args []string, delay time.Duration) error {
	for attempts := 0; ; attempts++ {
		if ctx.Err() != nil {
			return ctx.Err()
		}
		cmd := exec.Command(executable, args...)
		cmd.Env = os.Environ()
		out := &tailWriter{}
		cmd.Stdout = io.MultiWriter(os.Stdout, out)
		cmd.Stderr = io.MultiWriter(os.Stderr, out)
		if err := cmd.Start(); err != nil {
			return fmt.Errorf("swarm start failed: %w", err)
		}
		done := make(chan error, 1)
		go func() { done <- cmd.Wait() }()
		var err error
		select {
		case err = <-done:
		case <-ctx.Done():
			if cmd.Process != nil {
				cmd.Process.Signal(syscall.SIGTERM)
			}
			select {
			case <-done:
			case <-time.After(6 * time.Second):
				if cmd.Process != nil {
					cmd.Process.Kill()
				}
				<-done
			}
			return ctx.Err()
		}
		if err == nil {
			return fmt.Errorf("swarm exited unexpectedly with no error")
		}
		if !ownershipConflict(err, string(out.buf)) {
			return fmt.Errorf("swarm exited without retryable ownership conflict: %w", err)
		}
		log.Printf("swarm store ownership held by previous deployment; waiting for clean release (attempt %d)", attempts+1)
		timer := time.NewTimer(delay)
		select {
		case <-ctx.Done():
			timer.Stop()
			return ctx.Err()
		case <-timer.C:
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		log.Fatal("usage: portgate ./swarm serve <args>")
	}
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGTERM, syscall.SIGINT)
	defer stop()
	port := os.Getenv("PORT")
	if port == "" {
		port = "10000"
	}
	ln, server, err := serveHTTP(ctx, port)
	if err != nil {
		log.Fatalf("gate listener: %v", err)
	}
	defer func() { server.Close(); ln.Close() }()
	log.Printf("render handoff gate bound to :%s; forwarding only after Swarm backend starts", port)
	err = runChild(ctx, os.Args[1], os.Args[2:], retryDelay)
	if ctx.Err() == nil {
		log.Printf("fatal runtime: %v", err)
		os.Exit(1)
	}
}
