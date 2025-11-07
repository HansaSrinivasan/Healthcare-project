Param(
  [int]$ApiPort = 8000,
  [int]$WebPort = 5173
)

./.venv/Scripts/Activate.ps1

Write-Host "[Run] Starting FastAPI on port $ApiPort..."
Start-Process powershell -ArgumentList "-NoProfile","-Command","uvicorn app.main:app --host 0.0.0.0 --port $ApiPort --reload" -WorkingDirectory "backend"

Start-Sleep -Seconds 2

Write-Host "[Run] Starting React frontend on port $WebPort..."
Push-Location frontend
npm run dev
Pop-Location


