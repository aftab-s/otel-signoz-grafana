# FastAPI with OpenTelemetry for SigNoz

A FastAPI application instrumented with OpenTelemetry to send telemetry data to SigNoz for observability and monitoring.

## Overview

This project demonstrates how to instrument a FastAPI application with OpenTelemetry to send traces to SigNoz running locally. The setup follows the official SigNoz documentation and is compatible with Python 3.12.4.

## Prerequisites

- Python 3.8 or newer (tested with Python 3.12.4)
- SigNoz running locally (typically on port 4318 for HTTP)
- PowerShell (for Windows users)

## Project Structure

```
fastapi-app/
├── app.py              # FastAPI application with OpenTelemetry instrumentation
├── requirements.txt    # Python dependencies
├── run.ps1            # PowerShell script for easy setup and running
└── README.md          # This file
```

## Quick Start

### Option 1: Using the PowerShell Script (Recommended)

1. **Run the setup script:**
   ```powershell
   PowerShell.exe -ExecutionPolicy Bypass -File run.ps1
   ```

   This script will:
   - Install all required dependencies
   - Set up environment variables
   - Start the FastAPI application with OpenTelemetry

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install opentelemetry-instrumentation-fastapi
   ```

2. **Set environment variables:**
   ```powershell
   # Windows PowerShell
   $env:OTEL_SERVICE_NAME = "fastapi-demo"
   $env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
   $env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
   $env:OTEL_RESOURCE_ATTRIBUTES = "service.name=fastapi-demo"
   ```

   ```bash
   # Linux/Mac
   export OTEL_SERVICE_NAME=fastapi-demo
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
   export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
   export OTEL_RESOURCE_ATTRIBUTES=service.name=fastapi-demo
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

## Application Endpoints

Once running, the application will be available at `http://localhost:8000` with these endpoints:

- **`GET /`** - Root endpoint with welcome message
- **`GET /fast`** - Quick response (for testing normal operations)
- **`GET /slow`** - Response with 2-second delay (for testing latency monitoring)
- **`GET /error`** - Returns HTTP 500 error (for testing error tracking)

### API Documentation

FastAPI automatically generates API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the Setup

### Generate Test Traffic

Use these curl commands to generate different types of traces:

```bash
# Test normal operation
curl http://localhost:8000/fast

# Test latency monitoring
curl http://localhost:8000/slow

# Test error tracking
curl http://localhost:8000/error
```

### PowerShell equivalent:
```powershell
Invoke-WebRequest http://localhost:8000/fast
Invoke-WebRequest http://localhost:8000/slow
Invoke-WebRequest http://localhost:8000/error
```

## Viewing Traces in SigNoz

1. **Open SigNoz Dashboard**: Navigate to http://localhost:3301 (default SigNoz UI port)

2. **Check Services**: 
   - Go to the **Services** tab
   - Look for the service named `fastapi-demo`

3. **View Traces**:
   - Go to the **Traces** tab
   - Filter by service name `fastapi-demo`
   - You should see traces with different patterns:
     - Fast traces (~100ms)
     - Slow traces (~2000ms)
     - Error traces (HTTP 500)

## Configuration Details

### OpenTelemetry Configuration

- **Service Name**: `fastapi-demo`
- **Exporter Endpoint**: `http://localhost:4318` (HTTP protocol)
- **Protocol**: `http/protobuf`
- **Instrumentation**: Automatic FastAPI instrumentation

### Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `OTEL_SERVICE_NAME` | `fastapi-demo` | Name of your service in SigNoz |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318` | SigNoz OTLP HTTP endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | Protocol for sending traces |
| `OTEL_RESOURCE_ATTRIBUTES` | `service.name=fastapi-demo` | Additional service attributes |

## Features

- ✅ **Automatic Instrumentation**: FastAPI requests are automatically traced
- ✅ **HTTP Protocol**: Uses HTTP instead of gRPC for better compatibility
- ✅ **Error Handling**: Graceful fallback if OpenTelemetry setup fails
- ✅ **Multiple Test Scenarios**: Different endpoints for testing various observability patterns
- ✅ **Python 3.12 Compatible**: Tested with the latest Python version
- ✅ **Comprehensive Logging**: Detailed logging for setup and operation status

## Troubleshooting

### Common Issues

1. **Traces not appearing in SigNoz:**
   - Verify SigNoz is running on port 4318
   - Check that environment variables are set correctly
   - Look for OpenTelemetry setup messages in the application logs

2. **Application won't start:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version`
   - Verify port 8000 is not already in use

3. **Environment variables not working:**
   - On Windows, make sure to use PowerShell, not Command Prompt
   - Restart your terminal after setting environment variables
   - Verify variables are set: `echo $env:OTEL_SERVICE_NAME` (PowerShell)

### Debug Mode

To see traces in the console for debugging:

```powershell
$env:OTEL_TRACES_EXPORTER = "console"
python app.py
```

This will print traces to the terminal instead of sending them to SigNoz.

### Application Logs

The application provides detailed logging:
- ✅ `OpenTelemetry configured successfully` - Setup completed
- ✅ `FastAPI instrumentation applied` - Automatic tracing enabled
- ⚠️ `OpenTelemetry setup failed` - Check your configuration
- 📦 `OpenTelemetry packages not installed` - Run pip install

## Dependencies

The project uses these main dependencies:

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **opentelemetry-distro**: OpenTelemetry distribution
- **opentelemetry-exporter-otlp**: OTLP exporter for SigNoz
- **opentelemetry-instrumentation-fastapi**: FastAPI automatic instrumentation

## Reference

This implementation follows the official SigNoz documentation:
- https://signoz.io/docs/instrumentation/opentelemetry-fastapi/

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your SigNoz installation
3. Review the application logs for detailed error messages
