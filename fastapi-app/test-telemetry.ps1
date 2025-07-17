# Test Script for FastAPI OpenTelemetry Demo
Write-Host "FastAPI OpenTelemetry Test Script" -ForegroundColor Green
Write-Host "Generating test traffic to create traces, logs, and metrics..." -ForegroundColor Yellow

$baseUrl = "http://localhost:8000"

Write-Host "Testing basic endpoints..." -ForegroundColor Cyan

# Test fast endpoint
Write-Host "Testing /fast endpoint..." -ForegroundColor White
try {
    $response = Invoke-WebRequest "$baseUrl/fast" -UseBasicParsing
    Write-Host "Fast endpoint: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Fast endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test slow endpoint
Write-Host "Testing /slow endpoint..." -ForegroundColor White
try {
    $response = Invoke-WebRequest "$baseUrl/slow" -UseBasicParsing
    Write-Host "Slow endpoint: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Slow endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test error endpoint
Write-Host "Testing /error endpoint..." -ForegroundColor White
try {
    $response = Invoke-WebRequest "$baseUrl/error" -UseBasicParsing
    Write-Host "This should fail..." -ForegroundColor Yellow
} catch {
    Write-Host "Error endpoint returned expected 500 error" -ForegroundColor Green
}

# Test metrics demo endpoint
Write-Host "Testing /metrics-demo endpoint..." -ForegroundColor White
try {
    $response = Invoke-WebRequest "$baseUrl/metrics-demo" -UseBasicParsing
    Write-Host "Metrics demo: $($response.StatusCode)" -ForegroundColor Green
} catch {
    Write-Host "Metrics demo failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Generating load for better metrics..." -ForegroundColor Cyan

# Generate multiple requests
for ($i = 1; $i -le 5; $i++) {
    Write-Host "Load test iteration $i/5..." -ForegroundColor White
    
    try { Invoke-WebRequest "$baseUrl/fast" -UseBasicParsing | Out-Null } catch {}
    try { Invoke-WebRequest "$baseUrl/fast" -UseBasicParsing | Out-Null } catch {}
    try { Invoke-WebRequest "$baseUrl/slow" -UseBasicParsing | Out-Null } catch {}
    try { Invoke-WebRequest "$baseUrl/error" -UseBasicParsing | Out-Null } catch {}
    try { Invoke-WebRequest "$baseUrl/metrics-demo" -UseBasicParsing | Out-Null } catch {}
    
    Start-Sleep -Seconds 1
}

Write-Host "Test completed!" -ForegroundColor Green
Write-Host "Check your SigNoz dashboard at http://localhost:8080" -ForegroundColor Yellow
Write-Host "You should see:" -ForegroundColor White
Write-Host "  Traces: Fast (~100ms), Slow (~2000ms), Error (500)" -ForegroundColor White
Write-Host "  Logs: INFO, WARNING, ERROR levels" -ForegroundColor White
Write-Host "  Metrics: Request counts, latency histograms, live users" -ForegroundColor White
Write-Host "Service name: fastapi-demo" -ForegroundColor Cyan

Write-Host "Available endpoints:" -ForegroundColor Yellow
Write-Host "  GET /         - Root endpoint" -ForegroundColor White
Write-Host "  GET /fast     - Quick response (~100ms)" -ForegroundColor White  
Write-Host "  GET /slow     - Slow response (~2000ms)" -ForegroundColor White
Write-Host "  GET /error    - Error response (500)" -ForegroundColor White
Write-Host "  GET /metrics-demo - Custom metrics demo" -ForegroundColor White
Write-Host "  GET /docs     - API documentation" -ForegroundColor White
