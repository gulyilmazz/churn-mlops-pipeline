# API Test Scripti
Write-Host "=== API Health Check ===" -ForegroundColor Cyan
try {
    $health = Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing
    Write-Host "✓ Health Check: OK" -ForegroundColor Green
    Write-Host "  Response: $($health.Content)"
} catch {
    Write-Host "✗ Health Check Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Sample Data Test ===" -ForegroundColor Cyan
try {
    $sample = Invoke-WebRequest -Uri http://127.0.0.1:8000/sample -UseBasicParsing
    $sampleData = $sample.Content | ConvertFrom-Json
    Write-Host "✓ Sample Endpoint: OK" -ForegroundColor Green
    Write-Host "  Features count: $($sampleData.features.PSObject.Properties.Count)"
} catch {
    Write-Host "✗ Sample Endpoint Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== Prediction Test ===" -ForegroundColor Cyan
$testData = @{
    features = @{
        "Gender" = "Female"
        "Age" = 35
        "Tenure in Months" = 24
        "Monthly Charge" = 75.0
    }
} | ConvertTo-Json -Depth 10

try {
    $pred = Invoke-WebRequest -Uri http://127.0.0.1:8000/predict -Method POST -Body $testData -ContentType "application/json" -UseBasicParsing
    $result = $pred.Content | ConvertFrom-Json
    Write-Host "✓ Prediction: OK" -ForegroundColor Green
    Write-Host "  Predicted Label: $($result.pred_label)"
    Write-Host "  Probability: $([math]::Round($result.pred_proba_yes * 100, 2))%"
} catch {
    Write-Host "✗ Prediction Failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n=== API Dokümantasyonu ===" -ForegroundColor Cyan
Write-Host "http://127.0.0.1:8000/docs" -ForegroundColor Yellow

