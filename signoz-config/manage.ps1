# PowerShell script to manage SigNoz observability stack

Write-Host "SigNoz Observability Stack Management" -ForegroundColor Cyan
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

# Function to check if Grafana is running
function Test-GrafanaRunning {
    $grafanaContainers = docker ps --filter "name=grafana" --format "table {{.Names}}" | Where-Object { $_ -ne "NAMES" }
    return $grafanaContainers.Count -gt 0
}

# Function to stop Grafana stack
function Stop-GrafanaStack {
    Write-Host "Stopping Grafana observability stack..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\grafana-config"
    docker-compose down
    Write-Host "Grafana stack stopped." -ForegroundColor Green
}

# Function to start SigNoz
function Start-SigNoz {
    Write-Host "Starting SigNoz observability stack..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\signoz-config\deploy\docker"
    docker-compose up -d
    Write-Host "SigNoz started." -ForegroundColor Green
    Write-Host "SigNoz UI: http://localhost:8080" -ForegroundColor Cyan
}

# Function to stop SigNoz
function Stop-SigNoz {
    Write-Host "Stopping SigNoz observability stack..." -ForegroundColor Yellow
    Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\signoz-config\deploy\docker"
    docker-compose down
    Write-Host "SigNoz stopped." -ForegroundColor Green
}

# Function to show status
function Show-Status {
    Write-Host "`nCurrent Status:" -ForegroundColor Cyan
    Write-Host "===============" -ForegroundColor Cyan
    
    # Check SigNoz
    $signozContainers = docker ps --filter "name=signoz" --format "table {{.Names}}" | Where-Object { $_ -ne "NAMES" }
    if ($signozContainers.Count -gt 0) {
        Write-Host "SigNoz: RUNNING" -ForegroundColor Green
        Write-Host "  - SigNoz UI: http://localhost:8080" -ForegroundColor White
    } else {
        Write-Host "SigNoz: STOPPED" -ForegroundColor Red
    }
    
    # Check Grafana stack
    if (Test-GrafanaRunning) {
        Write-Host "Grafana Stack: RUNNING" -ForegroundColor Green
        Write-Host "  - Grafana UI: http://localhost:3000" -ForegroundColor White
    } else {
        Write-Host "Grafana Stack: STOPPED" -ForegroundColor Red
    }
}

# Main menu
function Show-Menu {
    Write-Host "`nChoose an option:" -ForegroundColor Yellow
    Write-Host "1. Start SigNoz (stops Grafana if running)" -ForegroundColor White
    Write-Host "2. Stop SigNoz" -ForegroundColor White
    Write-Host "3. Switch to Grafana Stack (stops SigNoz, starts Grafana)" -ForegroundColor White
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
            if (Test-GrafanaRunning) {
                Stop-GrafanaStack
                Start-Sleep -Seconds 3
            }
            Start-SigNoz
        }
        "2" {
            Stop-SigNoz
        }
        "3" {
            Stop-SigNoz
            Start-Sleep -Seconds 3
            Write-Host "Starting Grafana Stack..." -ForegroundColor Yellow
            Set-Location "s:\SigNoz\Assignment 2\otel-signoz-grafana\grafana-config"
            docker-compose up -d
            Write-Host "Grafana stack started." -ForegroundColor Green
            Write-Host "Grafana UI: http://localhost:3000 (admin/admin)" -ForegroundColor Cyan
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
        Write-Host "SigNoz Observability Stack Management" -ForegroundColor Cyan
        Write-Host "====================================" -ForegroundColor Cyan
    }
} while ($choice -ne "5")
