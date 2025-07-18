# FastAPI + OpenTelemetry + SigNoz Setup and Run Script
Write-Host "Starting FastAPI with OpenTelemetry..." -ForegroundColor Green

# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Set environment variables
Write-Host "Setting up OpenTelemetry environment variables..." -ForegroundColor Yellow
$env:OTEL_SERVICE_NAME = "fastapi-demo"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
$env:OTEL_RESOURCE_ATTRIBUTES = "service.name=fastapi-demo"

Write-Host "Environment variables set successfully" -ForegroundColor Green

# Run the application
Write-Host "Starting FastAPI application..." -ForegroundColor Green
Write-Host "Application will be available at http://localhost:8000" -ForegroundColor Cyan
Write-Host "API documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host "SigNoz UI: http://localhost:8080" -ForegroundColor Cyan

python main.py