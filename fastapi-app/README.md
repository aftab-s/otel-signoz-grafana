## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```
   
   **Or use the setup script:**
   ```powershell
   # Windows PowerShell:
   PowerShell.exe -ExecutionPolicy Bypass -File .\run.ps1
   # Or if already allowed: .\run.ps1
   ```
   ```bash
   # Linux/Mac:
   chmod +x run.sh && ./run.sh
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
```powershell
# Windows PowerShell:
PowerShell.exe -ExecutionPolicy Bypass -File .\test-telemetry.ps1
# Or if already allowed: .\test-telemetry.ps1
```
```bash
# Linux/Mac:
chmod +x test-telemetry.sh && ./test-telemetry.sh
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