# FastAPI OpenTelemetry SigNoz Demo

A complete observability demonstration showing how to instrument a FastAPI application with OpenTelemetry and send traces, logs, and metrics to SigNoz.

## Quick Start (TL;DR)

```bash
# 1. Clone the repository
git clone https://github.com/aftab-s/otel-signoz-grafana.git
cd otel-signoz-grafana/fastapi-app

# 2. Install and start SigNoz (if not already running)
git clone -b develop https://github.com/SigNoz/signoz.git
cd signoz/deploy/
./install.sh

# 3. Run the FastAPI demo
PowerShell.exe -ExecutionPolicy Bypass -File run.ps1

# 4. Generate test data
PowerShell.exe -ExecutionPolicy Bypass -File test-telemetry.ps1

# 5. View results in SigNoz
# Open http://localhost:8080 and explore Traces, Logs, and Metrics
```

## Repository Structure

```
otel-signoz-grafana/
├── fastapi-app/                 # Main FastAPI application
│   ├── app.py                   # FastAPI app with OpenTelemetry
│   ├── requirements.txt         # Python dependencies
│   ├── run.ps1                  # Setup and run script
│   ├── test-telemetry.ps1       # Test data generation script
│   ├── README.md                # Comprehensive setup guide
│   ├── METRICS.md               # Metrics implementation details
│   └── TROUBLESHOOTING.md       # Common issues and solutions
└── signoz-config/               # SigNoz configuration (if needed)
```

## What This Demo Shows

This project demonstrates a complete observability setup with:

### Distributed Tracing
- Request flow tracking
- Performance monitoring
- Error trace capture
- Cross-service correlation (when extended)

### Structured Logging  
- Centralized log collection
- Trace-log correlation
- Different log levels (INFO, WARNING, ERROR)
- Structured log format

### Custom Metrics
- **Counter**: `http_requests_total` - Request volume tracking
- **Histogram**: `http_request_duration_seconds` - Latency distribution
- **Gauge**: `live_users_count` - Live user simulation
- **Business Metrics**: Custom counters and gauges

### Real-World Endpoints
- `/fast` - Normal operation simulation (~100ms)
- `/slow` - High latency simulation (~2000ms)  
- `/error` - Error handling demonstration (HTTP 500)
- `/metrics-demo` - Custom metrics showcase

## Technology Stack

- **Application**: FastAPI (Python web framework)
- **Instrumentation**: OpenTelemetry Python SDK
- **Observability Platform**: SigNoz (open-source APM)
- **Protocol**: OTLP over HTTP
- **Deployment**: Docker (SigNoz), Local Python (FastAPI)

## Detailed Documentation

For comprehensive setup instructions, troubleshooting, and advanced configuration:

**[fastapi-app/README.md](./fastapi-app/README.md)** - Complete setup guide

## Demo Scenarios

### Scenario 1: Normal Operations
```bash
curl http://localhost:8000/fast
# Generates: Fast trace (~100ms) + INFO log + request metrics
```

### Scenario 2: Performance Issues
```bash
curl http://localhost:8000/slow
# Generates: Slow trace (~2000ms) + WARNING/INFO logs + latency metrics
```

### Scenario 3: Error Handling
```bash
curl http://localhost:8000/error
# Generates: Error trace (500 status) + ERROR log + error metrics
```

### Scenario 4: Business Metrics
```bash
curl http://localhost:8000/metrics-demo
# Generates: Custom business metrics + trace + INFO log
```

## Expected Results in SigNoz

After running the demo and generating test data, you should see:

### Services Tab
- Service named `fastapi-demo`
- Request rate, error rate, and latency overview

### Traces Tab  
- Traces with different duration patterns
- Error traces with stack traces
- Distributed tracing spans

### Logs Tab
- Structured logs with trace correlation
- Different log levels and messages
- Searchable and filterable logs

### Metrics Tab
- Request volume and rate metrics
- Latency percentile distributions  
- Custom business metrics
- Live user count simulation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with both FastAPI and SigNoz
5. Update documentation
6. Submit a pull request

## License

MIT License - feel free to use this demo for learning and development.

## Need Help?

- **Setup Issues**: Check [TROUBLESHOOTING.md](./fastapi-app/TROUBLESHOOTING.md)
- **Metrics Questions**: See [METRICS.md](./fastapi-app/METRICS.md)
- **SigNoz Help**: Visit [SigNoz Documentation](https://signoz.io/docs/)
- **OpenTelemetry**: Check [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)

---

**Happy Observing! This demo provides a solid foundation for implementing observability in your own applications.**
