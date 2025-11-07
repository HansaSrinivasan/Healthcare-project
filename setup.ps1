Param(
  [string]$Python = "python"
)

Write-Host "[Setup] Creating Python venv..."
& $Python -m venv .venv
if ($LASTEXITCODE -ne 0) { throw "Failed to create venv" }

Write-Host "[Setup] Activating venv..."
./.venv/Scripts/Activate.ps1

Write-Host "[Setup] Installing backend dependencies..."
pip install -r backend/requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Failed to install backend deps" }

Write-Host "[Setup] Installing frontend dependencies..."
Push-Location frontend
npm install --silent
if ($LASTEXITCODE -ne 0) { Pop-Location; throw "Failed to install frontend deps" }
Pop-Location

Write-Host "[Setup] Seeding sample data..."
python scripts/seed.py

Write-Host "[Setup] Done."


