Param(
  [switch]$Install,
  [switch]$StartAll
)

if ($Install) {
  Write-Host "🔧 Installing backend & frontend dependencies..."
  python -m venv .venv
  .\.venv\Scripts\Activate
  pip install --upgrade pip
  pip install -r backend/requirements.txt
  Push-Location frontend
  npm install
  Pop-Location
  Write-Host "✅ Installation complete."
}

if ($StartAll) {
  Write-Host "🚀 Starting backend, worker, and frontend..."
  Start-Process powershell -ArgumentList '-NoExit','-Command",".\.venv\Scripts\Activate; uvicorn backend.app.main:app --reload --port 8000"'
  Start-Process powershell -ArgumentList '-NoExit','-Command",".\.venv\Scripts\Activate; python backend/app/worker/worker.py"'
  Start-Process powershell -ArgumentList '-NoExit','-Command',"cd frontend; npm run dev"
}
