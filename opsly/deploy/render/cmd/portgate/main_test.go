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

func TestOnlyOwnershipConflictGetsRetry(t *testing.T){
 code3:=exec.Command("sh","-c","exit 3").Run()
 if !ownershipConflict(code3,"ERROR: serve failed · startup ownership lease · Another swarm serve is already running"){t.Fatal("valid contention must retry")}
 if ownershipConflict(code3,"invalid config"){t.Fatal("unrelated exit must not retry")}
 if ownershipConflict(errors.New("generic"),"startup ownership lease"){t.Fatal("generic failure must not retry")}
}

func TestGateFailClosedBeforeRuntime(t *testing.T){
 ctx,cancel:=context.WithCancel(context.Background());defer cancel()
 l,s,err:=serveHTTP(ctx,"0")
 if err==nil{s.Close();l.Close();t.Fatal("port zero should fail")}
 l,s,err=serveHTTP(ctx,"19271");if err!=nil{t.Skipf("unavailable test port: %v",err)}
 defer s.Close();defer l.Close()
 client:=&http.Client{Timeout:3*time.Second}
 for _,tc:=range []struct{path string;want int}{{"/_opsly/gate/live",200},{"/_opsly/gate/ready",503},{"/v1/rpc",503}}{
  resp,e:=client.Get("http://127.0.0.1:19271"+tc.path);if e!=nil{t.Fatal(e)}
  io.Copy(io.Discard,resp.Body);resp.Body.Close()
  if resp.StatusCode!=tc.want{t.Fatalf("%s returned %d, expected %d",tc.path,resp.StatusCode,tc.want)}
 }
}

func TestChildRetriesLockThenStopsOnOtherExit(t *testing.T){
 dir:=t.TempDir();marker:=filepath.Join(dir,"count")
 script:=filepath.Join(dir,"fake-sw.sh")
 scriptText:="#!/bin/sh\nif [ ! -f '"+marker+"' ]; then echo x > '"+marker+"'; echo 'startup ownership lease' >&2; exit 3; fi\nexit 2\n"
 if err:=os.WriteFile(script,[]byte(scriptText),0700);err!=nil{t.Fatal(err)}
 err:=runChild(context.Background(),script,nil,time.Millisecond)
 if err==nil||!strings.Contains(err.Error(),"not a retryable"){t.Fatalf("expected fatal second error after lock retry, got: %v",err)}
 if _,err:=os.Stat(marker);err!=nil{t.Fatalf("expected retry marker: %v",err)}
}

func TestConfigErrorNeverRetries(t *testing.T){
 ctx,cancel:=context.WithTimeout(context.Background(),2*time.Second);defer cancel()
 err:=runChild(ctx,"sh",[]string{"-c","echo bad config >&2; exit 3"},time.Millisecond)
 if err==nil||!strings.Contains(err.Error(),"not a retryable"){t.Fatalf("must refuse non-lock failure: %v",err)}
}
