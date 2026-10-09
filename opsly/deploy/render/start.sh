#!/usr/bin/env bash
# OPSLY New Division Swarm, single-owner Render runtime.
# Port-first handoff: gate opens Render port, Swarm waits on old DB owner's exit.
# The gate returns 503 for the API until Swarm is actually available.
# Does NOT delete data, terminate prior owners or bypass PostgreSQL locks.
# Requires build: go build -o swarm ./cmd/swarm && go build -o opsly-portgate ./opsly/deploy/render/cmd/portgate
set -euo pipefail

for name in DB_HOST DB_NAME DB_USER DB_PASSWORD SWARM_API_TOKEN; do
  if [[ -z "${!name:-}" ]]; then
    printf 'OPSLY start blocked: required environment variable %s is missing\n' "$name" >&2
    exit 78
  fi
done

if [[ ! "${PORT:-10000}" =~ ^[0-9]+$ ]]; then
  printf 'OPSLY start blocked: invalid PORT\n' >&2
  exit 78
fi

umask 077
cat > /tmp/opsly-new-swarm.yaml <<EOF
store:
  backend: postgres
database:
  host: ${DB_HOST}
  port: 5432
  name: ${DB_NAME}
  user: ${DB_USER}
  sslmode: require
  pool_size: 8
  password_env: DB_PASSWORD
runtime:
  fan_out_workers: 2
  recovery_on_startup: true
EOF
printf '%s' "$SWARM_API_TOKEN" > /tmp/opsly-new-swarm-token
unset SWARM_API_TOKEN

exec ./opsly-portgate ./swarm serve opsly/buyer-intent-hunter \
  --config /tmp/opsly-new-swarm.yaml \
  --store postgres \
  --api-token-file /tmp/opsly-new-swarm-token \
  --api-listen-addr "127.0.0.1:18941" \
  --mcp-listen-addr 127.0.0.1:8082