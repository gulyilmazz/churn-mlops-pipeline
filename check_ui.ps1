# UI ve API Durum Kontrolü
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Churn Prediction - Durum Kontrolü" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# API Kontrolü
Write-Host "1. API Kontrolü:" -ForegroundColor Yellow
try {
    $api = Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing -TimeoutSec 2
    Write-Host "   ✓ API ÇALIŞIYOR" -ForegroundColor Green
    Write-Host "   Adres: http://127.0.0.1:8000" -ForegroundColor Gray
    Write-Host "   Dokümantasyon: http://127.0.0.1:8000/docs" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ API ÇALIŞMIYOR" -ForegroundColor Red
    Write-Host "   Hata: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# UI Kontrolü
Write-Host "2. UI Kontrolü:" -ForegroundColor Yellow
try {
    $ui = Invoke-WebRequest -Uri http://localhost:5173 -UseBasicParsing -TimeoutSec 2
    Write-Host "   ✓ UI ÇALIŞIYOR" -ForegroundColor Green
    Write-Host "   Adres: http://localhost:5173" -ForegroundColor Gray
    Write-Host "   Status: $($ui.StatusCode)" -ForegroundColor Gray
} catch {
    Write-Host "   ✗ UI ÇALIŞMIYOR" -ForegroundColor Red
    Write-Host "   Hata: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Port Kontrolü
Write-Host "3. Port Kontrolü:" -ForegroundColor Yellow
$port8000 = netstat -ano | findstr ":8000" | findstr "LISTENING"
$port5173 = netstat -ano | findstr ":5173" | findstr "LISTENING"

if ($port8000) {
    Write-Host "   ✓ Port 8000 (API) kullanımda" -ForegroundColor Green
} else {
    Write-Host "   ✗ Port 8000 (API) kullanılmıyor" -ForegroundColor Red
}

if ($port5173) {
    Write-Host "   ✓ Port 5173 (UI) kullanımda" -ForegroundColor Green
} else {
    Write-Host "   ✗ Port 5173 (UI) kullanılmıyor" -ForegroundColor Red
}

Write-Host ""

# Node Process Kontrolü
Write-Host "4. Node Process Kontrolü:" -ForegroundColor Yellow
$nodeProcesses = Get-Process -Name node -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Host "   ✓ $($nodeProcesses.Count) Node process çalışıyor" -ForegroundColor Green
    $nodeProcesses | ForEach-Object {
        Write-Host "      Process ID: $($_.Id) - Başlangıç: $($_.StartTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "   ✗ Node process bulunamadı" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ÇÖZÜM ÖNERİLERİ" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Tarayıcınızda:" -ForegroundColor Yellow
Write-Host "1. http://localhost:5173 adresine gidin" -ForegroundColor White
Write-Host "2. Eğer sayfa açılmıyorsa, şunları deneyin:" -ForegroundColor White
Write-Host "   - http://127.0.0.1:5173" -ForegroundColor Gray
Write-Host "   - Farklı bir tarayıcı kullanın (Chrome, Firefox, Edge)" -ForegroundColor Gray
Write-Host "   - Tarayıcı cache'ini temizleyin (Ctrl+Shift+Delete)" -ForegroundColor Gray
Write-Host "3. Tarayıcı konsolunu açın (F12) ve hataları kontrol edin" -ForegroundColor White
Write-Host ""
Write-Host "API bağlantısı için:" -ForegroundColor Yellow
Write-Host "- UI'de 'API: Connected' yazısını görmelisiniz" -ForegroundColor White
Write-Host "- Eğer 'Not reachable' görüyorsanız, API'yi başlatın:" -ForegroundColor White
Write-Host "  .\start_api.ps1 veya uvicorn src.api.app:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""

