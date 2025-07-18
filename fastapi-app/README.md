## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Test the endpoints:**
   ```bash
   curl http://localhost:8000/fast
   curl http://localhost:8000/slow
   curl http://localhost:8000/error
   ```

## API Endpoints

| Endpoint | Description | Purpose |
|----------|-------------|---------|
| `GET /` | Welcome message | Basic connectivity |
| `GET /fast` | Quick response (~100ms) | Normal operations |
| `GET /slow` | 2-second delay | Latency testing |
| `GET /error` | HTTP 500 error | Error tracking |
| `GET /metrics-demo` | Custom metrics demo | Business metrics |
| `GET /docs` | Swagger UI | API documentation |

## Backend Switching

**Works with both SigNoz and Grafana without code changes:**

```bash
# SigNoz (default)
python main.py  # Uses http://localhost:4318

# Grafana Stack  
python main.py  # Same endpoints, different backend
```

**Environment variables:**
```bash
OTEL_SERVICE_NAME=fastapi-demo
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

## Testing

**Generate test traffic:**
```bash
.\test-telemetry.ps1  # PowerShell script
```

**Or manual testing:**
```bash
# Load test
for i in {1..5}; do
  curl http://localhost:8000/fast
  curl http://localhost:8000/slow
  curl http://localhost:8000/error
done
```