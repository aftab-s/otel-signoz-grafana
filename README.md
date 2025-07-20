# FastAPI Observability Stack Comparison

**A comprehensive demonstration comparing SigNoz and Grafana observability stacks with a modular FastAPI application.**

This project showcases a FastAPI application with **complete OpenTelemetry instrumentation** that can seamlessly switch between two observability backends without any code changes.

## Prerequisites

- **Docker & Docker Compose**: For observability stacks
- **Python 3.8+**: For FastAPI application
- **8GB RAM**: Recommended for running both stacks
- **Available Ports**: 3000, 4317, 4318, 8000, 8080, 9090

## Project Overview

This project demonstrates modern observability practices by implementing a FastAPI application with complete OpenTelemetry instrumentation. 

## Demo Videos

| SigNoz | Grafana |
|-------------|--------------|
| 🎥 [**Watch SigNoz Demo**](https://drive.google.com/file/d/1WJF-EsMRLip3iqa79NBHyjZw-uzA2imD/view?usp=sharing)<br>*Navigating SigNoz for this project* | 🎥 [**Watch Grafana Demo**](https://drive.google.com/file/d/1bm940MBtyqH2A9FC5dxhgy3AG-2Wj-Dm/view?usp=sharing)<br>*Navigating Grafana Stack for this project* |

> 📖 **New to observability platforms?** Check out the [**Navigation Guide**](./Navigation.md) for a beginner-friendly walkthrough of both SigNoz and Grafana interfaces.

## Project Structure

```
otel-signoz-grafana/
├── fastapi-app/                  # FastAPI application
│   ├── main.py                   # Application logic
│   ├── telemetry.py              # OpenTelemetry setup
│   ├── requirements.txt          # Python dependencies
│   ├── run.ps1 /.sh              # Setup scripts
│   ├── test-telemetry.ps1/.sh    # Test scripts
│   └── README.md                 # App-specific documentation
├── grafana-config/               # Complete Grafana observability stack
│   ├── docker-compose.yaml       # Grafana + Prometheus + Loki + Tempo
│   ├── grafana/                  # Dashboards and provisioning
│   └── *.yaml                    # Service configurations
└── signoz-config/                # SigNoz deployment configuration
    └── deploy/                   # Docker deployment files
```

## Quick Start

### Option 1: SigNoz

```bash
# 1. Start SigNoz
cd signoz-config/deploy/docker
docker-compose up -d

# 2. Run FastAPI application (assuming you are in signoz-config/deploy/docker directory)
cd ../../../fastapi-app

# Windows:
PowerShell.exe -ExecutionPolicy Bypass -File .\run.ps1

# Linux/Mac:
chmod +x run.sh && ./run.sh

# 3. Generate test data
# Windows:
PowerShell.exe -ExecutionPolicy Bypass -File .\test-telemetry.ps1

# Linux/Mac:
chmod +x test-telemetry.sh && ./test-telemetry.sh

# 4. View results
# SigNoz UI: http://localhost:8080
# Application: http://localhost:8000
```

### Option 2: Grafana Stack (For Comparison)

```bash
# 1. Start Grafana observability stack
cd grafana-config
docker-compose up -d

# 2. Run FastAPI application (same commands as above)
cd ../fastapi-app
# Use same run.ps1 or run.sh commands

# 3. Generate test data (same commands as above)
# Use same test-telemetry scripts

# 4. View results
# Grafana UI: http://localhost:3000 (admin/admin)
# Application: http://localhost:8000
```

## Backend Switching

**The same FastAPI application works with both backends:**

```bash
# For Grafana stack
cd grafana-config && docker-compose up -d
cd ../fastapi-app && python main.py

# For SigNoz stack  
cd signoz-config/deploy/docker && docker-compose up -d
cd ../../../fastapi-app && python main.py
```

**No code changes required!** The application automatically sends telemetry to whichever backend is running.

## Observability Features

### API Endpoints for Testing
| Endpoint | Response Time | Purpose |
|----------|---------------|---------|
| `GET /` | Instant | Basic connectivity |
| `GET /fast` | ~100ms | Normal operations |
| `GET /slow` | ~2000ms | Latency testing |
| `GET /error` | Instant | Error tracking |
| `GET /metrics-demo` | Instant | Custom metrics |

### Generated Telemetry Data
- **Traces**: Different duration patterns for analysis
- **Logs**: INFO, WARNING, ERROR levels with trace correlation
- **Metrics**: Request counts, latency histograms, custom business metrics

## Technology Stack

### Application Layer
- **FastAPI**: Modern Python web framework
- **OpenTelemetry**: Vendor-neutral observability instrumentation
- **Python 3.8+**: Compatible with modern Python versions

### Grafana Stack
- **Grafana**: Visualization and dashboards
- **Prometheus**: Metrics collection and storage
- **Loki**: Log aggregation and querying
- **Tempo**: Distributed tracing backend
- **OTEL Collector**: Telemetry data pipeline
- **Docker**: Containerized deployment

### SigNoz Stack
- **SigNoz**: All-in-one observability platform
- **ClickHouse**: Time-series database
- **Docker**: Containerized deployment

### Cross-Platform Application Scripts
```bash
cd fastapi-app

# Windows
.\run.ps1                    # Setup and run application
.\test-telemetry.ps1        # Generate test traffic

# Linux/Mac
./run.sh                    # Setup and run application  
./test-telemetry.sh         # Generate test traffic
```

## Testing Scenarios

### Load Testing
```bash
# Generate realistic traffic patterns
cd fastapi-app

# Windows
PowerShell.exe -ExecutionPolicy Bypass -File .\test-telemetry.ps1

# Linux/Mac  
./test-telemetry.sh
```

### Manual Testing
```bash
# Test different endpoints
curl http://localhost:8000/fast      # Normal response
curl http://localhost:8000/slow      # High latency
curl http://localhost:8000/error     # Error handling
curl http://localhost:8000/metrics-demo  # Custom metrics
```

## Documentations

> - **[Navigation.md](./Navigation.md)**: Beginner-friendly guide to navigating SigNoz and Grafana interfaces
> - **[Internal Strategy Memo : SigNoz vs. Grafana Stack](https://docs.google.com/document/d/1SpcPD3XoHWwqCjcA2Mg-yedPRkBPtJ9y4llgNwwEc-g/edit?usp=sharing)**: Task 2

