# PowerShell script to manage Grafana observability stack

Write-Host "Grafana Observability Stack Management" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Function to check if Docker is running
function Test-DockerRunning {
    try {
        docker version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to check if SigNoz is running
function Test-SigNozRunning {
    $signozContainers = docker ps --filter "name=signoz" --format "table {{.Names}}" | Where-Object { $_ -ne "NAMES" }
    return $signozContainers.Count -gt 0
}

# Function to stop SigNoz
function Stop-SigNoz {
    Write-Host "Stopping SigNoz services..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\signoz-config\deploy\docker"
    docker-compose down
    Write-Host "SigNoz stopped." -ForegroundColor Green
}

# Function to start Grafana stack
function Start-GrafanaStack {
    Write-Host "Starting Grafana observability stack..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\grafana-config"
    docker-compose up -d
    Write-Host "Grafana stack started." -ForegroundColor Green
    Write-Host "Grafana UI: http://localhost:3000 (admin/admin)" -ForegroundColor Cyan
}

# Function to stop Grafana stack
function Stop-GrafanaStack {
    Write-Host "Stopping Grafana observability stack..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\grafana-config"
    docker-compose down
    Write-Host "Grafana stack stopped." -ForegroundColor Green
}

# Function to show status
function Show-Status {
    Write-Host "`nCurrent Status:" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan
    
    # Check SigNoz
    if (Test-SigNozRunning) {
        Write-Host "SigNoz: RUNNING" -ForegroundColor Green
    } else {
        Write-Host "SigNoz: STOPPED" -ForegroundColor Red
    }
    
    # Check Grafana stack
    $grafanaContainers = docker ps --filter "name=grafana" --format "table {{.Names}}" | Where-Object { $_ -ne "NAMES" }
    if ($grafanaContainers.Count -gt 0) {
        Write-Host "Grafana Stack: RUNNING" -ForegroundColor Green
        Write-Host "  - Grafana UI: http://localhost:3000" -ForegroundColor White
        Write-Host "  - Prometheus: http://localhost:9090" -ForegroundColor White
        Write-Host "  - Loki: http://localhost:3100" -ForegroundColor White
        Write-Host "  - Tempo: http://localhost:3200" -ForegroundColor White
    } else {
        Write-Host "Grafana Stack: STOPPED" -ForegroundColor Red
    }
}

# Main menu
function Show-Menu {
    Write-Host "`nChoose an option:" -ForegroundColor Yellow
    Write-Host "1. Start Grafana Stack (stops SigNoz if running)" -ForegroundColor White
    Write-Host "2. Stop Grafana Stack" -ForegroundColor White
    Write-Host "3. Switch to SigNoz (stops Grafana, starts SigNoz)" -ForegroundColor White
    Write-Host "4. Show Status" -ForegroundColor White
    Write-Host "5. Exit" -ForegroundColor White
    Write-Host ""
}

# Check if Docker is running
if (-not (Test-DockerRunning)) {
    Write-Host "Error: Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Main loop
do {
    Show-Status
    Show-Menu
    $choice = Read-Host "Enter your choice (1-5)"
    
    switch ($choice) {
        "1" {
            if (Test-SigNozRunning) {
                Stop-SigNoz
                Start-Sleep -Seconds 3
            }
            Start-GrafanaStack
        }
        "2" {
            Stop-GrafanaStack
        }
        "3" {
            Stop-GrafanaStack
            Start-Sleep -Seconds 3
            Write-Host "Starting SigNoz..." -ForegroundColor Yellow
            Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\signoz-config\deploy\docker"
            docker-compose up -d
            Write-Host "SigNoz started." -ForegroundColor Green
            Write-Host "SigNoz UI: http://localhost:8080" -ForegroundColor Cyan
        }
        "4" {
            # Status already shown at the top of loop
        }
        "5" {
            Write-Host "Goodbye!" -ForegroundColor Green
            break
        }
        default {
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
        }
    }
    
    if ($choice -ne "5") {
        Write-Host "`nPress any key to continue..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        Clear-Host
        Write-Host "Grafana Observability Stack Management" -ForegroundColor Cyan
        Write-Host "====================================" -ForegroundColor Cyan
    }
} while ($choice -ne "5")
