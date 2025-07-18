# Modular FastAPI with OpenTelemetry

This FastAPI application demonstrates a clean, modular approach to integrating observability using OpenTelemetry. The application separates business logic from telemetry concerns, making it easy to maintain and switch between different observability backends.

## Architecture

### 🏗️ Modular Structure

```
fastapi-app/
├── main.py                 # ✨ Clean FastAPI application (business logic only)
├── telemetry.py           # 📊 Complete telemetry/observability module  
├── telemetry_configs.py   # ⚙️ Configuration examples for different backends
├── app.py                 # 📜 Original monolithic version (for reference)
├── requirements.txt       # 📦 Python dependencies
└── run.ps1               # 🚀 PowerShell startup script
```

### 🎯 Key Benefits

1. **Separation of Concerns**: Business logic and telemetry are completely decoupled
2. **Easy Backend Switching**: Change observability backend without touching app code
3. **Maintainable**: Clear boundaries between application and infrastructure concerns
4. **Testable**: Can easily disable telemetry for testing or run with different configs
5. **Production Ready**: Robust error handling and graceful degradation

## 📊 Telemetry Features

### Traces
- Automatic FastAPI instrumentation
- Custom span creation with context managers
- Distributed tracing across service boundaries

### Metrics
- HTTP request counters with labels (method, endpoint, status)
- Request duration histograms
- Live user count gauge (simulated)
- Custom business metrics creation

### Logs
- Structured logging with OpenTelemetry correlation
- Automatic log export to observability backend
- Contextual information in traces

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run with SigNoz (Default)
```bash
# Start SigNoz first, then:
python main.py
```

### 3. Run with Grafana Stack
```bash
# Start Grafana stack first, then:
python main.py
```

The application automatically detects the running observability backend via OTLP endpoints.

## 🔧 Configuration

### Environment Variables
```bash
OTEL_SERVICE_NAME="fastapi-demo"              # Service name
OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"  # OTLP endpoint
```

### Backend-Specific Configs
The `telemetry_configs.py` file shows how to configure for different backends:

```python
from telemetry_configs import get_config
from telemetry import TelemetryManager

# Switch to different backends
signoz_config = get_config("signoz")     # SigNoz
grafana_config = get_config("grafana")   # Grafana Stack  
jaeger_config = get_config("jaeger")     # Jaeger
disabled_config = get_config("disabled") # No telemetry
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with basic info
- `GET /health` - Health check with telemetry status
- `GET /telemetry-status` - Detailed telemetry information

### Demo Endpoints  
- `GET /fast` - Quick response (< 100ms)
- `GET /slow` - Delayed response (2s) for testing
- `GET /error` - Simulated error (500) for error tracking
- `GET /metrics-demo` - Custom metrics demonstration
- `GET /business-logic` - Example business logic with metrics

### Interactive Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📈 Observability Examples

### Custom Tracing
```python
from telemetry import trace_operation

# Trace business operations
with trace_operation("data_processing", {"user_id": 123, "operation": "analysis"}):
    # Your business logic here
    result = process_data()
    return result
```

### Custom Metrics
```python
from telemetry import create_metric

# Create business metrics
user_count = create_metric("active_users", "Number of active users", "gauge")
order_count = create_metric("orders_total", "Total orders processed", "counter")

# Record values
user_count.add(50, {"region": "us-east"})
order_count.add(1, {"product": "widget", "status": "completed"})
```

### Conditional Telemetry
```python
from telemetry import is_telemetry_enabled

if is_telemetry_enabled():
    # Only create metrics if telemetry is available
    performance_metric = create_metric("performance_score", "Performance metric")
    performance_metric.add(95.5)
```

## 🔄 Switching Backends

### SigNoz ➡️ Grafana
1. Stop SigNoz: `docker-compose down` (in signoz-config/deploy/docker)
2. Start Grafana: `docker-compose up -d` (in grafana-config)  
3. Restart FastAPI app - **no code changes needed!**

### Grafana ➡️ SigNoz
1. Stop Grafana: `docker-compose down` (in grafana-config)
2. Start SigNoz: `docker-compose up -d` (in signoz-config/deploy/docker)
3. Restart FastAPI app - **no code changes needed!**

## 🛠️ Development vs Production

### Development Mode
- Telemetry enabled with local backends
- Detailed logging and tracing
- Custom metrics for debugging

### Production Mode  
- Optimized telemetry configuration
- Error handling and graceful degradation
- Performance monitoring metrics

### Testing Mode
```python
from telemetry_configs import get_config
from telemetry import TelemetryManager

# Disable telemetry for testing
config = get_config("disabled")
telemetry = TelemetryManager(config)
```

## 📊 Comparison: Before vs After

### Before (Monolithic - app.py)
- ❌ 226 lines mixing business logic with telemetry
- ❌ Hard to maintain and test
- ❌ Difficult to switch observability backends  
- ❌ Telemetry code scattered throughout application

### After (Modular - main.py + telemetry.py)
- ✅ Clean separation: ~100 lines business logic + ~250 lines telemetry module
- ✅ Easy to maintain and test each component separately
- ✅ Switch backends without changing application code
- ✅ Reusable telemetry module across projects

## 🔍 Error Handling

The modular design includes robust error handling:

- **Telemetry Failures**: App continues running without observability
- **Backend Unavailable**: Graceful degradation with logging
- **Configuration Errors**: Clear error messages and fallback behavior
- **Import Errors**: Safe fallbacks when OpenTelemetry packages are missing

## 🚦 Status Monitoring

Check telemetry status at runtime:

```bash
curl http://localhost:8000/telemetry-status
```

Response:
```json
{
  "telemetry": {
    "enabled": true,
    "service_name": "fastapi-demo",
    "otlp_endpoint": "http://localhost:4318",
    "components": {
      "tracing": true,
      "metrics": true, 
      "logging": true
    }
  },
  "endpoints": {
    "traces": "http://localhost:4318/v1/traces",
    "logs": "http://localhost:4318/v1/logs", 
    "metrics": "http://localhost:4318/v1/metrics"
  }
}
```

## 🎓 Best Practices Demonstrated

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: Telemetry manager can be injected/mocked
3. **Configuration Management**: Environment-based configuration
4. **Error Handling**: Graceful degradation when telemetry unavailable
5. **Context Managers**: Clean resource management for tracing
6. **Factory Pattern**: Flexible metric creation
7. **Singleton Pattern**: Global telemetry manager instance

This modular approach makes it easy to maintain, test, and scale your observability setup while keeping your business logic clean and focused.
