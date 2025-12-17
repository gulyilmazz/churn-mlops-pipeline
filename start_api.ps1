# API'yi başlatma scripti
Write-Host "Churn Prediction API başlatılıyor..." -ForegroundColor Green
Write-Host "API adresi: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Virtual environment'ı aktif et
& .\venv\Scripts\Activate.ps1

# API'yi başlat
uvicorn src.api.app:app --reload --port 8000

