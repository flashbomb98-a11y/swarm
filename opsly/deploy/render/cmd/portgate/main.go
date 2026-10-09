// Command portgate implements a safe Render port-first handoff for the
// Division Swarm runtime. It never terminates an existing owner or edits a DB.
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

const backendAddress = "127.0.0.1:18941"

type tailWriter struct { buf []byte }
func (w *tailWriter) Write(p []byte) (int,error) {
 w.buf=append(w.buf,p...)
 if len(w.buf)>16384 { w.buf=append([]byte(nil),w.buf[len(w.buf)-16384:]...) }
 return len(p),nil
}

func ownershipConflict(err error, output string) bool {
 var exit *exec.ExitError
 return errors.As(err,&exit) && exit.ExitCode()==3 &&
  (strings.Contains(output,"startup ownership lease") || strings.Contains(output,"Another swarm serve is already running"))
}

func serveHTTP(ctx context.Context, port string) (net.Listener,*http.Server,error) {
 n,err:=strconv.Atoi(port);if err!=nil || n<1 || n>65535{return nil,nil,fmt.Errorf("invalid public port")}
 listener,err:=net.Listen("tcp",fmt.Sprintf("0.0.0.0:%d",n));if err!=nil{return nil,nil,err}
 backend:=&url.URL{Scheme:"http",Host:backendAddress}
 proxy:=httputil.NewSingleHostReverseProxy(backend)
 proxy.Transport=&http.Transport{DialContext:(&net.Dialer{Timeout:2*time.Second}).DialContext, ResponseHeaderTimeout:25*time.Second,IdleConnTimeout:30*time.Second}
 proxy.ErrorHandler=func(w http.ResponseWriter,_ *http.Request,_ error){http.Error(w,"Swarm runtime not ready",http.StatusServiceUnavailable)}
 mux:=http.NewServeMux()
 mux.HandleFunc("/_opsly/gate/live",func(w http.ResponseWriter,r *http.Request){
  if r.Method!="GET"{w.WriteHeader(http.StatusMethodNotAllowed);return}
  w.Header().Set("Content-Type","text/plain")
  io.WriteString(w,"gate-alive\n")
 })
 mux.HandleFunc("/_opsly/gate/ready",func(w http.ResponseWriter,r *http.Request){
  if r.Method!="GET"{w.WriteHeader(http.StatusMethodNotAllowed);return}
  c,e:=net.DialTimeout("tcp",backendAddress,400*time.Millisecond)
  if e!=nil{http.Error(w,"runtime not ready",503);return}
  c.Close();io.WriteString(w,"backend-listening\n")
 })
 mux.Handle("/",proxy)
 server:=&http.Server{Handler:mux,ReadHeaderTimeout:6*time.Second,IdleTimeout:35*time.Second}
 go func(){if e:=server.Serve(listener);e!=nil && !errors.Is(e,http.ErrServerClosed){log.Printf("gate server error: %v",e)}}()
 go func(){<-ctx.Done();stop,cancel:=context.WithTimeout(context.Background(),4*time.Second);defer cancel();server.Shutdown(stop)}()
 return listener,server,nil
}

func runChild(ctx context.Context, executable string, args []string, retryDelay time.Duration) error {
 for attempts:=0;;attempts++{
  if ctx.Err()!=nil{return ctx.Err()}
  cmd:=exec.Command(executable,args...)
  cmd.Env=os.Environ()
  output:=&tailWriter{}
  cmd.Stdout=io.MultiWriter(os.Stdout,output)
  cmd.Stderr=io.MultiWriter(os.Stderr,output)
  if e:=cmd.Start();e!=nil{return fmt.Errorf("swarm start failed: %w",e)}
  done:=make(chan error,1)
  go func(){done<-cmd.Wait()}()
  var err error
  select{
  case err=<-done:
  case <-ctx.Done():
   if cmd.Process!=nil{cmd.Process.Signal(syscall.SIGTERM)}
   select{case <-done:case <-time.After(6*time.Second):if cmd.Process!=nil{cmd.Process.Kill()};<-done}
   return ctx.Err()
  }
  if err==nil{return errors.New("swarm exited unexpectedly with no error")}
  if !ownershipConflict(err,string(output.buf)){return fmt.Errorf("swarm failure is not a retryable ownership lock: %w",err)}
  log.Printf("previous Swarm process still owns PostgreSQL store; retrying after orderly handoff (attempt %d)",attempts+1)
  timer:=time.NewTimer(retryDelay)
  select{case <-ctx.Done():timer.Stop();return ctx.Err();case <-timer.C:}
 }
}

func main(){
 if len(os.Args)<2{log.Fatal("usage: opsly-portgate ./swarm serve <args>")}
 ctx,stop:=signal.NotifyContext(context.Background(),syscall.SIGTERM,syscall.SIGINT)
 defer stop()
 port:=os.Getenv("PORT");if port==""{port="10000"}
 ln,server,err:=serveHTTP(ctx,port);if err!=nil{log.Fatalf("gate listener: %v",err)}
 defer func(){server.Close();ln.Close()}()
 log.Printf("port gate listening on :%s; Swarm is private until DB store ownership is acquired",port)
 if err=runChild(ctx,os.Args[1],os.Args[2:],3*time.Second);ctx.Err()==nil{log.Fatalf("Swarm runtime terminated: %v",err)}
}
