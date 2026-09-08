#!/usr/bin/env bash
set -euo pipefail

trap 'docker compose -f compose.test.yml down -v --remove-orphans >/dev/null 2>&1' EXIT

docker compose -f compose.test.yml up \
  --build \
  --exit-code-from test \
  --attach test \
  --no-log-prefix
