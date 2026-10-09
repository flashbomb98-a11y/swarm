package main

import (
	"context"
	"errors"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

func TestOwnershipConflictOnlyWhenRetryable(t *testing.T) {
	code3 := exec.Command("sh", "-c", "exit 3").Run()
	if !ownershipConflict(code3, "ERROR: serve failed · startup ownership lease · Another swarm serve is already running") {
		t.Fatal("lock refusal must be retryable")
	}
	if ownershipConflict(code3, "bad config") {
		t.Fatal("unrelated exit must fail closed")
	}
	if ownershipConflict(errors.New("not an exit error"), "startup ownership lease") {
		t.Fatal("invalid exit must fail closed")
	}
}

func TestGateRoutesSafelyBeforeBackend(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	listener, server, err := serveHTTP(ctx, "0")
	if err == nil {
		server.Close()
		listener.Close()
		t.Fatal("port 0 must fail")
	}
	listener, server, err = serveHTTP(ctx, "19271")
	if err != nil {
		t.Skipf("unable to bind port: %v", err)
	}
	defer server.Close()
	defer listener.Close()
	client := &http.Client{Timeout: 3 * time.Second}
	for _, tc := range []struct {
		path string
		want int
	}{{"/_opsly/gate/live", 200}, {"/_opsly/gate/ready", 503}, {"/v1/rpc", 503}} {
		req, _ := http.NewRequest(http.MethodGet, "http://127.0.0.1:19271"+tc.path, nil)
		resp, e := client.Do(req)
		if e != nil {
			t.Fatal(e)
		}
		io.Copy(io.Discard, resp.Body)
		resp.Body.Close()
		if resp.StatusCode != tc.want {
			t.Fatalf("%s got %d want %d", tc.path, resp.StatusCode, tc.want)
		}
	}
}

func TestChildRetriesOnlyOwnerConflictThenSucceeds(t *testing.T) {
	dir := t.TempDir()
	marker := filepath.Join(dir, "count")
	script := filepath.Join(dir, "child.sh")
	content := "#!/bin/sh\nif [ ! -f '" + marker + "' ]; then echo x > '" + marker + "'; echo 'startup ownership lease' >&2; exit 3; fi\nexit 0\n"
	if err := os.WriteFile(script, []byte(content), 0700); err != nil {
		t.Fatal(err)
	}
	err := runChild(context.Background(), script, nil, time.Millisecond)
	if err == nil || !strings.Contains(err.Error(), "exited unexpectedly") {
		t.Fatalf("expected graceful child-exit detection, got %v", err)
	}
}

func TestChildNonOwnerFailureDoesNotRetry(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	err := runChild(ctx, "sh", []string{"-c", "echo bad config >&2; exit 3"}, time.Millisecond)
	if err == nil || !strings.Contains(err.Error(), "without retryable ownership conflict") {
		t.Fatalf("expected fatal mismatch: %v", err)
	}
}
