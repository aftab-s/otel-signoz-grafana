# Troubleshooting Logs in SigNoz

## The Problem You Were Having

Your FastAPI application was only sending **traces** to SigNoz, but not **logs**. This is a common issue because OpenTelemetry requires separate configuration for traces and logs.

## What Was Missing

1. **Log Exporter Configuration**: Your app only had trace exporter, not log exporter
2. **Logging Handler**: No OpenTelemetry logging handler was attached to Python's logging system
3. **Log Endpoints**: SigNoz needs logs sent to `/v1/logs` endpoint

## What I Fixed

### 1. Added Log Export Configuration

```python
# Configure logging
logger_provider = LoggerProvider(resource=resource)
_logs.set_logger_provider(logger_provider)

# Configure the OTLP log exporter
otlp_log_exporter = OTLPLogExporter(
    endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/logs"
)

# Add the log processor
log_processor = BatchLogRecordProcessor(otlp_log_exporter)
logger_provider.add_log_record_processor(log_processor)
```

### 2. Added OpenTelemetry Logging Handler

```python
# Add OpenTelemetry handler to the root logger
handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
```

## How to Verify Logs Are Working

### 1. Check Application Startup
When you start the app, you should see:
```
✅ OpenTelemetry configured successfully
📡 Sending traces to: http://localhost:4318/v1/traces
📝 Sending logs to: http://localhost:4318/v1/logs
```

### 2. Generate Test Traffic
```powershell
# Generate different types of logs
Invoke-WebRequest http://localhost:8000/fast    # INFO log
Invoke-WebRequest http://localhost:8000/slow    # WARNING + INFO logs
Invoke-WebRequest http://localhost:8000/error   # ERROR log
```

### 3. Check SigNoz Dashboard

1. **Open SigNoz**: Go to http://localhost:3301
2. **Go to Logs Section**: Click on "Logs" in the left sidebar
3. **Filter by Service**: Filter by service name "fastapi-demo"
4. **Look for Log Levels**: You should see:
   - 🟢 INFO logs from `/fast` endpoint
   - 🟡 WARNING logs from `/slow` endpoint  
   - 🔴 ERROR logs from `/error` endpoint

### 4. Expected Log Messages

You should see logs like:
- `"Root endpoint called"`
- `"Fast endpoint called"`
- `"Slow endpoint called - starting delay"`
- `"Slow endpoint - delay completed"`
- `"Error endpoint called - simulating server error"`

## Common Issues and Solutions

### Issue 1: Logs Not Appearing
**Problem**: Logs still not showing in SigNoz
**Solutions**:
1. Check SigNoz is running: `docker ps | findstr signoz`
2. Verify endpoint: Make sure SigNoz OTLP receiver is on port 4318
3. Check application logs for errors during OpenTelemetry setup

### Issue 2: Only Some Logs Appearing
**Problem**: Only certain log levels showing
**Solutions**:
1. Check log level configuration in SigNoz
2. Verify logging handler level: `LoggingHandler(level=logging.NOTSET)`
3. Check if log filtering is applied in SigNoz UI

### Issue 3: Logs Missing Context
**Problem**: Logs appear but without trace correlation
**Solutions**:
1. Ensure both trace and log exporters use same resource configuration
2. Check that service.name is consistent between traces and logs
3. Verify trace context is being propagated

## Debug Mode

To see logs in console for debugging:
```powershell
$env:OTEL_LOGS_EXPORTER = "console"
python app.py
```

This will print logs to terminal instead of sending to SigNoz.

## Environment Variables for Logging

Make sure these are set:
```powershell
$env:OTEL_SERVICE_NAME = "fastapi-demo"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
$env:OTEL_RESOURCE_ATTRIBUTES = "service.name=fastapi-demo"
```

## Expected SigNoz Log Structure

Your logs should appear with these fields:
- **Timestamp**: When the log was created
- **Service Name**: `fastapi-demo`
- **Log Level**: INFO, WARNING, ERROR
- **Message**: The actual log message
- **Trace ID**: Links logs to traces (if available)
- **Span ID**: Links logs to specific spans

## Verification Checklist

- [ ] Application starts without OpenTelemetry errors
- [ ] Console shows "Sending logs to: http://localhost:4318/v1/logs"
- [ ] SigNoz logs section shows service "fastapi-demo"
- [ ] Different log levels appear after hitting endpoints
- [ ] Logs contain proper service name and timestamps
- [ ] Logs are correlated with traces (same trace ID)
