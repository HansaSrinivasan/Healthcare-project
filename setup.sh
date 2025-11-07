#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3}"

echo "[Setup] Creating Python venv..."
$PYTHON -m venv .venv
source .venv/bin/activate

echo "[Setup] Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "[Setup] Installing frontend dependencies..."
pushd frontend >/dev/null
npm install --silent
popd >/dev/null

echo "[Setup] Seeding sample data..."
python scripts/seed.py

echo "[Setup] Done."


