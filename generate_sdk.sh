#!/usr/bin/env bash
set -euo pipefail

SPEC_URL=${1:-http://localhost:8000/openapi.json}
OUT_DIR=${2:-healthcare_sdk}

npx --yes @openapitools/openapi-generator-cli generate \
  -i "$SPEC_URL" \
  -g python \
  -o "$OUT_DIR"

echo "SDK generated at $OUT_DIR"


