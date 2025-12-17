# Proje Durum Kontrolü
Write-Host "`n=== Churn Prediction Project Status ===" -ForegroundColor Cyan
Write-Host ""

# API Kontrolü
Write-Host "API Status:" -ForegroundColor Yellow
try {
    $apiHealth = Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing -TimeoutSec 2
    if ($apiHealth.StatusCode -eq 200) {
        Write-Host "  ✓ API is running" -ForegroundColor Green
        Write-Host "    URL: http://127.0.0.1:8000" -ForegroundColor Gray
        Write-Host "    Docs: http://127.0.0.1:8000/docs" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ API is not responding" -ForegroundColor Red
}

Write-Host ""

# UI Kontrolü
Write-Host "UI Status:" -ForegroundColor Yellow
try {
    $ui = Invoke-WebRequest -Uri http://localhost:5173 -UseBasicParsing -TimeoutSec 2
    if ($ui.StatusCode -eq 200) {
        Write-Host "  ✓ UI is running" -ForegroundColor Green
        Write-Host "    URL: http://localhost:5173" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ✗ UI is not responding" -ForegroundColor Red
}

Write-Host ""

# Port Kontrolü
Write-Host "Port Status:" -ForegroundColor Yellow
$port8000 = netstat -ano | findstr ":8000" | findstr "LISTENING"
$port5173 = netstat -ano | findstr ":5173" | findstr "LISTENING"

if ($port8000) {
    Write-Host "  ✓ Port 8000 (API) is in use" -ForegroundColor Green
} else {
    Write-Host "  ✗ Port 8000 (API) is not in use" -ForegroundColor Red
}

if ($port5173) {
    Write-Host "  ✓ Port 5173 (UI) is in use" -ForegroundColor Green
} else {
    Write-Host "  ✗ Port 5173 (UI) is not in use" -ForegroundColor Red
}

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "Open your browser and go to: http://localhost:5173" -ForegroundColor Yellow
Write-Host ""

