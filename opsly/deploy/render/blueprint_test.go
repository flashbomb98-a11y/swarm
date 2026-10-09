package render

import (
  "os"
  "path/filepath"
  "strings"
  "testing"

  "gopkg.in/yaml.v3"
)

type blueprint struct {
  Services []struct {
    Type string `yaml:"type"`
    Name string `yaml:"name"`
    Runtime string `yaml:"runtime"`
    Plan string `yaml:"plan"`
    Region string `yaml:"region"`
    Repo string `yaml:"repo"`
    Branch string `yaml:"branch"`
    BuildCommand string `yaml:"buildCommand"`
    StartCommand string `yaml:"startCommand"`
    HealthCheckPath string `yaml:"healthCheckPath"`
    EnvVars []struct {
      Key string `yaml:"key"`
      Value string `yaml:"value"`
      Sync *bool `yaml:"sync"`
      GenerateValue bool `yaml:"generateValue"`
    } `yaml:"envVars"`
  } `yaml:"services"`
}

func TestRootBlueprintIsFreeNeonOnly(t *testing.T) {
  p := filepath.Join("..","..","..","render.yaml")
  raw, err := os.ReadFile(p)
  if err != nil {t.Fatal(err)}
  var b blueprint
  decoder := yaml.NewDecoder(strings.NewReader(string(raw)))
  decoder.KnownFields(true)
  if err := decoder.Decode(&b);err!=nil {t.Fatal(err)}
  if len(b.Services)!=1 {t.Fatalf("expected one service, got %d", len(b.Services))}
  s:=b.Services[0]
  if s.Type!="web"||s.Name!="opsly-new-buyer-intent"||s.Runtime!="go"||s.Plan!="free"||s.Region!="frankfurt"{
     t.Fatal("blueprint must create only named free Go service in Frankfurt")
  }
  if s.Repo!="https://github.com/flashbomb98-a11y/swarm"||s.Branch!="master"||s.StartCommand!="bash opsly/deploy/render/start.sh"{
    t.Fatal("repo, branch or start command changed")
  }
  if !strings.Contains(s.BuildCommand,"go build -o opsly-portgate")||s.HealthCheckPath!="/_opsly/gate/ready"{
    t.Fatal("port gate build and readiness check must be configured")
  }
  vars:=map[string]struct{value string; sync *bool; gen bool}{}
  for _, v := range s.EnvVars{
    vars[v.Key]=struct{value string;sync *bool; gen bool}{v.Value,v.Sync,v.GenerateValue}
  }
  for _,name:=range []string{"DB_HOST","DB_NAME","DB_USER","DB_PASSWORD","SWARM_API_TOKEN"}{
    if _, ok:=vars[name];!ok{t.Fatalf("missing %s",name)}
  }
  pass:=vars["DB_PASSWORD"]
  if pass.Value!=""||pass.Sync==nil||*pass.Sync{
    t.Fatal("Neon DB password must be entered via secure Render prompt, not checked into Git")
  }
  if !vars["SWARM_API_TOKEN"].gen||vars["SWARM_API_TOKEN"].value!=""{
    t.Fatal("API token must be generated securely in Render")
  }
  if vars["DB_HOST"].value!="ep-dawn-silence-b193cq88.c-5.eu-central-1.aws.neon.tech"||strings.Contains(vars["DB_HOST"].value,"pooler"){
     t.Fatal("must use exact direct Neon backend rather than pooled connection")
  }
  if vars["DB_NAME"].value!="neondb"||vars["DB_USER"].value!="neondb_owner"{
     t.Fatal("unexpected Neon database or role")
  }
}
