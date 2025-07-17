# FastAPI with OpenTelemetry for SigNoz

A comprehensive FastAPI application demonstrating full observability with OpenTelemetry integration, sending **traces**, **logs**, and **metrics** to SigNoz for monitoring and analysis.

## What This Demo Shows

This project demonstrates how to instrument a FastAPI application with OpenTelemetry to achieve complete observability:

- Distributed Tracing: Track request flows and performance
- Structured Logging: Centralized log collection with trace correlation
- Custom Metrics: Business and technical metrics (Counter, Histogram, Gauge)
- Full Integration: Complete SigNoz integration with HTTP protocol
- Real-world Examples: Multiple endpoints showcasing different patterns

## Prerequisites

Before starting, ensure you have:

- **Python 3.8+** (tested with Python 3.11.4 and 3.12.4)
- **SigNoz** running locally (see [SigNoz Installation](#signoz-installation))
- **PowerShell** (for Windows users) or **Bash** (for Linux/Mac)
- **Git** for cloning the repository

## Quick Start Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/aftab-s/otel-signoz-grafana.git
cd otel-signoz-grafana/fastapi-app
```

### Step 2: Install SigNoz (if not already installed)

**Option A: Docker Compose (Recommended)**
```bash
git clone -b develop https://github.com/SigNoz/signoz.git
cd signoz/deploy/
./install.sh
```

**Option B: Docker Compose Manual**
```bash
# Download docker-compose file
curl -sL https://github.com/SigNoz/signoz/raw/develop/deploy/docker/clickhouse-setup/docker-compose.yaml > docker-compose.yaml

# Start SigNoz
docker-compose up -d
```

**Verify SigNoz is running:**
- SigNoz UI: http://localhost:8080
- OTLP Receiver: http://localhost:4318

### Step 3: Set Up Python Environment

**Option A: Using Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv fastapi-otel-env

# Activate virtual environment
# Windows PowerShell:
fastapi-otel-env\Scripts\Activate.ps1
# Windows Command Prompt:
fastapi-otel-env\Scripts\activate.bat
# Linux/Mac:
source fastapi-otel-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Option B: Using Global Python**
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

**Option A: Using PowerShell Script (Windows - Recommended)**
```powershell
PowerShell.exe -ExecutionPolicy Bypass -File run.ps1
```

**Option B: Manual Setup**
```bash
# Set environment variables
# Windows PowerShell:
$env:OTEL_SERVICE_NAME = "fastapi-demo"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
$env:OTEL_RESOURCE_ATTRIBUTES = "service.name=fastapi-demo"

# Linux/Mac:
export OTEL_SERVICE_NAME=fastapi-demo
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_RESOURCE_ATTRIBUTES=service.name=fastapi-demo

# Run the application
python app.py
```

### Step 5: Generate Test Data

**Option A: Using Test Script (Recommended)**
```powershell
PowerShell.exe -ExecutionPolicy Bypass -File test-telemetry.ps1
```

**Option B: Manual Testing**
```bash
# Test different endpoints
curl http://localhost:8000/fast
curl http://localhost:8000/slow
curl http://localhost:8000/error
curl http://localhost:8000/metrics-demo

# Windows PowerShell:
Invoke-WebRequest http://localhost:8000/fast
Invoke-WebRequest http://localhost:8000/slow
Invoke-WebRequest http://localhost:8000/error
Invoke-WebRequest http://localhost:8000/metrics-demo
```

### Step 6: View Results in SigNoz

1. **Open SigNoz Dashboard**: http://localhost:8080
2. **Explore the data** in different sections:
   - **Services**: See `fastapi-demo` service
   - **Traces**: View request traces with different latencies
   - **Logs**: See structured logs with different levels
   - **Metrics**: Monitor request rates, latencies, and custom metrics

## 📁 Project Structure

```
fastapi-app/
├── app.py                    # Main FastAPI application with OpenTelemetry
├── requirements.txt          # Python dependencies
├── run.ps1                  # PowerShell setup and run script
├── test-telemetry.ps1       # Test script to generate telemetry data
├── README.md                # This comprehensive guide
├── METRICS.md               # Detailed metrics documentation
└── TROUBLESHOOTING.md       # Common issues and solutions
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

## 🔗 Application Endpoints

Once running, the application will be available at `http://localhost:8000` with these endpoints:

| Endpoint | Method | Description | Purpose |
|----------|--------|-------------|---------|
| `/` | GET | Root endpoint with welcome message | Basic connectivity test |
| `/fast` | GET | Quick response (~100ms) | Test normal operations and fast metrics |
| `/slow` | GET | Response with 2-second delay | Test latency monitoring and slow metrics |
| `/error` | GET | Returns HTTP 500 error | Test error tracking and error metrics |
| `/metrics-demo` | GET | Demonstrates custom metrics | Test custom business metrics |
| `/docs` | GET | Swagger UI API documentation | Interactive API exploration |
| `/redoc` | GET | ReDoc API documentation | Alternative API documentation |

### What Each Endpoint Generates

**`/fast` endpoint:**
- Trace: ~100ms duration
- Log: INFO level message
- Metrics: Request count, fast duration

**`/slow` endpoint:**
- Trace: ~2000ms duration  
- Logs: WARNING (start) + INFO (complete)
- Metrics: Request count, slow duration

**`/error` endpoint:**
- Trace: Error trace with 500 status
- Log: ERROR level message
- Metrics: Request count, error status

**`/metrics-demo` endpoint:**
- Trace: Normal trace
- Log: INFO level message
- Metrics: Custom demo counter and gauge

## Testing and Validation

### Automated Testing

The repository includes a comprehensive test script that generates various telemetry patterns:

```powershell
# Run the test script
PowerShell.exe -ExecutionPolicy Bypass -File test-telemetry.ps1
```

**What the test script does:**
- Tests all endpoints systematically
- Generates load to create interesting metric patterns
- Validates endpoint responses
- Creates diverse trace, log, and metric data

### Manual Testing

You can also test individual endpoints manually:

```bash
# Basic connectivity
curl http://localhost:8000/

# Test fast response
curl http://localhost:8000/fast

# Test slow response (takes 2 seconds)
curl http://localhost:8000/slow

# Test error handling
curl http://localhost:8000/error

# Test custom metrics
curl http://localhost:8000/metrics-demo

# View API documentation
open http://localhost:8000/docs
```

**PowerShell equivalent:**
```powershell
Invoke-WebRequest http://localhost:8000/
Invoke-WebRequest http://localhost:8000/fast
Invoke-WebRequest http://localhost:8000/slow
Invoke-WebRequest http://localhost:8000/error
Invoke-WebRequest http://localhost:8000/metrics-demo
```

### Load Testing

Generate multiple requests to see interesting patterns:

```powershell
# Generate 10 iterations of mixed traffic
for ($i=1; $i -le 10; $i++) {
    Invoke-WebRequest http://localhost:8000/fast
    Invoke-WebRequest http://localhost:8000/slow
    try { Invoke-WebRequest http://localhost:8000/error } catch {}
    Invoke-WebRequest http://localhost:8000/metrics-demo
    Start-Sleep 1
}
```

## Viewing Results in SigNoz

### SigNoz Dashboard Access

1. **Open SigNoz Dashboard**: Navigate to http://localhost:8080
   - If first time, you may need to sign up with an email
   - Use any email (no verification required for local setup)

2. **Navigate to Different Sections**: Use the left sidebar to explore

### Traces Section

**What to look for:**
- Go to **"Traces"** in the left sidebar
- Filter by service name: `fastapi-demo`
- Look for traces with different patterns:
  - **Fast traces**: ~100ms duration from `/fast` endpoint
  - **Slow traces**: ~2000ms duration from `/slow` endpoint  
  - **Error traces**: HTTP 500 status from `/error` endpoint
  - **Normal traces**: Various durations from other endpoints

**Key metrics in traces:**
- Request duration
- HTTP status codes
- Request paths
- Error details (for failed requests)

### Logs Section

**What to look for:**
- Go to **"Logs"** in the left sidebar
- Filter by service name: `fastapi-demo`
- Look for logs with different severity levels:
  - INFO logs: "Fast endpoint called", "Root endpoint called", "Metrics demo endpoint called"
  - WARNING logs: "Slow endpoint called - starting delay"
  - ERROR logs: "Error endpoint called - simulating server error"

**Log correlation:**
- Each log entry should include a trace ID
- Click on a trace ID to see the corresponding trace
- This enables trace-log correlation for debugging

### Metrics Section

**What to look for:**
- Go to **"Metrics"** or **"Dashboard"** in the left sidebar
- Filter by service name: `fastapi-demo`
- Available metrics:

#### Core HTTP Metrics
- **`http_requests_total`** (Counter)
  - Total HTTP requests by method, endpoint, and status code
  - Useful for: Request volume, error rates, endpoint popularity

- **`http_request_duration_seconds`** (Histogram)  
  - Request latency distribution
  - Useful for: P50/P95/P99 percentiles, SLA monitoring

#### Business Metrics
- **`live_users_count`** (Gauge)
  - Simulated live user count (fluctuates 10-100)
  - Useful for: Monitoring concurrent users

- **`demo_operations_total`** (Counter)
  - Custom business operations from `/metrics-demo`
  - Useful for: Business-specific tracking

- **`demo_active_connections`** (Gauge)
  - Custom connection pool simulation
  - Useful for: Resource monitoring

### Creating Custom Dashboards

**Create a comprehensive dashboard:**

1. **Go to Dashboards** → **New Dashboard**
2. **Add panels for:**
   - Request rate: `rate(http_requests_total[5m])`
   - Error rate: `rate(http_requests_total{status_code=~"5.."}[5m])`
   - Latency percentiles: `histogram_quantile(0.95, http_request_duration_seconds)`
   - Live users: `live_users_count`

3. **Set up alerts** for:
   - High error rate (>5%)
   - High latency (>1s P95)
   - Low request volume

## Configuration Details

### Environment Variables

The application uses these environment variables:

| Variable | Default Value | Description |
|----------|---------------|-------------|
| `OTEL_SERVICE_NAME` | `fastapi-demo` | Service name in SigNoz |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318` | SigNoz OTLP endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | Protocol for data export |
| `OTEL_RESOURCE_ATTRIBUTES` | `service.name=fastapi-demo` | Additional service attributes |

**Setting environment variables:**

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

### OpenTelemetry Configuration

| Component | Endpoint | Export Interval | Protocol |
|-----------|----------|-----------------|----------|
| **Traces** | `http://localhost:4318/v1/traces` | Real-time | HTTP/Protobuf |
| **Logs** | `http://localhost:4318/v1/logs` | Real-time | HTTP/Protobuf |
| **Metrics** | `http://localhost:4318/v1/metrics` | 5 seconds | HTTP/Protobuf |

## Features

This FastAPI application demonstrates:

- Complete Observability: Full traces, logs, and metrics integration
- Automatic Instrumentation: FastAPI requests are automatically traced
- Structured Logging: Application logs with trace correlation
- Custom Metrics: Counter, Histogram, and Gauge implementations
- HTTP Protocol: Uses HTTP instead of gRPC for better compatibility
- Error Handling: Graceful fallback if OpenTelemetry setup fails
- Multiple Test Scenarios: Different endpoints for various observability patterns
- Cross-Platform: Works on Windows, Linux, and macOS
- Python 3.8+ Compatible: Tested with Python 3.11.4 and 3.12.4
- Production Ready: Follows OpenTelemetry best practices
- Comprehensive Documentation: Detailed setup and troubleshooting guides

## Troubleshooting

### Common Issues

#### 1. SigNoz Not Accessible
**Problem**: Cannot access http://localhost:8080
**Solutions**:
```bash
# Check if SigNoz containers are running
docker ps | grep signoz

# If not running, start SigNoz
cd signoz/deploy/
docker-compose up -d

# Check logs if issues persist
docker-compose logs
```

#### 2. Application Won't Start
**Problem**: Python application fails to start
**Solutions**:
```bash
# Check Python version (must be 3.8+)
python --version

# Install dependencies
pip install -r requirements.txt

# Check if port 8000 is available
netstat -an | grep :8000
```

#### 3. No Data in SigNoz
**Problem**: Traces/logs/metrics not appearing
**Solutions**:
1. **Check application logs** for OpenTelemetry setup messages:
   ```
   OpenTelemetry configured successfully
   Sending traces to: http://localhost:4318/v1/traces
   Sending logs to: http://localhost:4318/v1/logs
   Sending metrics to: http://localhost:4318/v1/metrics
   ```

2. **Verify SigNoz OTLP endpoint**:
   ```bash
   curl http://localhost:4318/v1/traces
   # Should return: 405 Method Not Allowed (this is expected)
   ```

3. **Check environment variables**:
   ```powershell
   # PowerShell
   echo $env:OTEL_SERVICE_NAME
   echo $env:OTEL_EXPORTER_OTLP_ENDPOINT
   
   # Linux/Mac
   echo $OTEL_SERVICE_NAME
   echo $OTEL_EXPORTER_OTLP_ENDPOINT
   ```

4. **Generate test traffic**:
   ```bash
   curl http://localhost:8000/fast
   ```

#### 4. PowerShell Execution Policy
**Problem**: Cannot run PowerShell scripts
**Solution**:
```powershell
# Run with bypass (recommended for testing)
PowerShell.exe -ExecutionPolicy Bypass -File run.ps1

# Or set execution policy (requires admin)
Set-ExecutionPolicy RemoteSigned
```

#### 5. Port Already in Use
**Problem**: Port 8000 already occupied
**Solutions**:
```bash
# Find process using port 8000
netstat -ano | findstr :8000
# Or on Linux/Mac:
lsof -i :8000

# Kill the process or change port in app.py
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use different port
```

### Debug Mode

**Enable console output for debugging**:
```powershell
# See traces in console
$env:OTEL_TRACES_EXPORTER = "console"

# See logs in console  
$env:OTEL_LOGS_EXPORTER = "console"

# See metrics in console
$env:OTEL_METRICS_EXPORTER = "console"

python app.py
```

### Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ is installed: `python --version`
- [ ] SigNoz is running: http://localhost:8080 accessible
- [ ] Dependencies installed: `pip list | grep opentelemetry`
- [ ] Port 8000 is free: `netstat -an | grep :8000`
- [ ] Environment variables set: `echo $OTEL_SERVICE_NAME`
- [ ] Application starts without errors
- [ ] Test endpoints respond: `curl http://localhost:8000/fast`
- [ ] OpenTelemetry setup messages appear in logs

## Additional Resources

### Documentation
- **METRICS.md**: Detailed metrics implementation guide
- **TROUBLESHOOTING.md**: Comprehensive troubleshooting guide
- **OpenTelemetry Python**: https://opentelemetry.io/docs/instrumentation/python/
- **SigNoz Documentation**: https://signoz.io/docs/

### Related Repositories
- **SigNoz**: https://github.com/SigNoz/signoz
- **OpenTelemetry Python**: https://github.com/open-telemetry/opentelemetry-python

### Community Support
- **SigNoz Slack**: https://signoz.io/slack
- **OpenTelemetry Community**: https://opentelemetry.io/community/

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Update documentation as needed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Success Indicators

**If everything is working correctly, you should see:**

**Application startup messages:**
```
OpenTelemetry configured successfully
Sending traces to: http://localhost:4318/v1/traces
Sending logs to: http://localhost:4318/v1/logs  
Sending metrics to: http://localhost:4318/v1/metrics
FastAPI instrumentation applied
Starting FastAPI application...
```

**SigNoz dashboard shows:**
- Service named `fastapi-demo` in Services section
- Traces with varying durations (100ms, 2000ms, errors)
- Logs with INFO, WARNING, ERROR levels
- Metrics for requests, latency, and custom business metrics

**Test endpoints respond:**
- http://localhost:8000/ → Welcome message
- http://localhost:8000/fast → Quick response
- http://localhost:8000/slow → 2-second delay
- http://localhost:8000/error → 500 error
- http://localhost:8000/metrics-demo → Custom metrics
- http://localhost:8000/docs → API documentation

**You now have a complete observability setup with FastAPI + OpenTelemetry + SigNoz!**
