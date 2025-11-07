#!/usr/bin/env bash
set -euo pipefail

API_PORT=${API_PORT:-8000}
WEB_PORT=${WEB_PORT:-5173}

source .venv/bin/activate || true

echo "[Run] Starting FastAPI on port ${API_PORT}..."
(
  cd backend
  uvicorn app.main:app --host 0.0.0.0 --port ${API_PORT} --reload
) &

sleep 2

echo "[Run] Starting React frontend on port ${WEB_PORT}..."
(
  cd frontend
  npm run dev
)


