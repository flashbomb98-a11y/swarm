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
		Type                    string `yaml:"type"`
		Name                    string `yaml:"name"`
		Runtime                 string `yaml:"runtime"`
		Plan                    string `yaml:"plan"`
		Region                  string `yaml:"region"`
		Repo                    string `yaml:"repo"`
		Branch                  string `yaml:"branch"`
		AutoDeployTrigger       string `yaml:"autoDeployTrigger"`
		BuildCommand            string `yaml:"buildCommand"`
		StartCommand            string `yaml:"startCommand"`
		HealthCheckPath         string `yaml:"healthCheckPath"`
		MaxShutdownDelaySeconds int    `yaml:"maxShutdownDelaySeconds"`
		EnvVars                 []struct {
			Key           string `yaml:"key"`
			Value         string `yaml:"value"`
			Sync          *bool  `yaml:"sync"`
			GenerateValue bool   `yaml:"generateValue"`
		} `yaml:"envVars"`
	} `yaml:"services"`
}

func TestRootBlueprintIsFreeNeonOnly(t *testing.T) {
	raw, err := os.ReadFile(filepath.Join("..", "..", "..", "render.yaml"))
	if err != nil {
		t.Fatal(err)
	}
	var b blueprint
	decoder := yaml.NewDecoder(strings.NewReader(string(raw)))
	decoder.KnownFields(true)
	if err := decoder.Decode(&b); err != nil {
		t.Fatal(err)
	}
	if len(b.Services) != 1 {
		t.Fatalf("expected one service, got %d", len(b.Services))
	}
	s := b.Services[0]
	if s.Type != "web" || s.Name != "opsly-new-buyer-intent" || s.Runtime != "go" || s.Plan != "free" || s.Region != "frankfurt" {
		t.Fatal("blueprint must create only named free Go service in Frankfurt")
	}
	if s.Repo != "https://github.com/flashbomb98-a11y/swarm" || s.Branch != "master" || s.StartCommand != "bash opsly/deploy/render/start.sh" || s.AutoDeployTrigger != "off" {
		t.Fatal("repo, branch, start command or auto deploy mode changed")
	}
	if !strings.Contains(s.BuildCommand, "go build -o opsly-portgate") || s.HealthCheckPath != "/_opsly/gate/ready" {
		t.Fatal("port gate build and readiness check must be configured")
	}
	type value struct {
		text string
		sync *bool
		generated bool
	}
	vars := map[string]value{}
	for _, v := range s.EnvVars {
		vars[v.Key] = value{v.Value, v.Sync, v.GenerateValue}
	}
	for _, name := range []string{"DB_HOST", "DB_NAME", "DB_USER", "DB_PASSWORD", "SWARM_API_TOKEN"} {
		if _, ok := vars[name]; !ok {
			t.Fatalf("missing %s", name)
		}
	}
	pass := vars["DB_PASSWORD"]
	if pass.text != "" || pass.sync == nil || *pass.sync {
		t.Fatal("Neon DB password must be entered via secure Render prompt, not checked into Git")
	}
	if !vars["SWARM_API_TOKEN"].generated || vars["SWARM_API_TOKEN"].text != "" {
		t.Fatal("API token must be generated securely in Render")
	}
	if vars["DB_HOST"].text != "ep-dawn-silence-b193cq88.c-5.eu-central-1.aws.neon.tech" || strings.Contains(vars["DB_HOST"].text, "pooler") {
		t.Fatal("must use exact direct Neon backend rather than pooled connection")
	}
	if vars["DB_NAME"].text != "neondb" || vars["DB_USER"].text != "neondb_owner" {
		t.Fatal("unexpected Neon database or role")
	}
}
