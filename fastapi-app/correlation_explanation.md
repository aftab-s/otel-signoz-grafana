# CORRELATION EXAMPLE: What happens when you call GET /slow

## 1. TRACE DATA
```
Trace ID: 7f8e9d2c1b3a4f5e6789012345abcdef
└── Span ID: a1b2c3d4e5f6789
    ├── Span Name: "GET /slow"
    ├── Attributes:
    │   ├── http.method = "GET"
    │   ├── http.url = "http://localhost:8000/slow"
    │   ├── http.route = "/slow"
    │   ├── http.status_code = 200
    │   └── duration = 2.003s
    └── Events: [span_start, span_end]
```

## 2. LOG DATA (Automatically Correlated)
```
Log Entry 1:
├── Timestamp: 2025-07-29T10:30:15.123Z
├── Level: WARNING
├── Message: "Slow endpoint called - starting delay"
├── trace_id: 7f8e9d2c1b3a4f5e6789012345abcdef  ← AUTOMATIC CORRELATION
├── span_id: a1b2c3d4e5f6789                    ← AUTOMATIC CORRELATION
└── resource.service.name: "fastapi-demo"

Log Entry 2:
├── Timestamp: 2025-07-29T10:30:17.126Z
├── Level: INFO
├── Message: "Slow endpoint - delay completed"
├── trace_id: 7f8e9d2c1b3a4f5e6789012345abcdef  ← SAME TRACE_ID
├── span_id: a1b2c3d4e5f6789                    ← SAME SPAN_ID
└── resource.service.name: "fastapi-demo"
```

## 3. METRICS DATA (Correlated by Labels)
```
Metric: http_requests_total
├── Value: +1
├── Labels:
│   ├── method = "GET"        ← MATCHES trace attribute
│   ├── endpoint = "/slow"    ← MATCHES trace attribute
│   └── status_code = "200"   ← MATCHES trace attribute
└── Timestamp: 2025-07-29T10:30:17.126Z

Metric: http_request_duration_seconds
├── Value: 2.003
├── Labels:
│   ├── method = "GET"
│   ├── endpoint = "/slow"
│   └── status_code = "200"
└── Timestamp: 2025-07-29T10:30:17.126Z
```

## 4. HOW SIGNOZ/GRAFANA USES THIS FOR CORRELATION

### In SigNoz:
- Click on a trace → See all logs with matching trace_id
- Click on a log → Jump to the trace that contains it
- Filter metrics by endpoint → See traces for that endpoint

### In Grafana:
- Correlate metrics spikes with traces
- Jump from dashboard panels to trace details
- Filter logs by trace_id to debug specific requests

## 5. CORRELATION FLOW IN YOUR CODE

```python
# When this happens in main.py:
@app.get("/slow")
async def slow_endpoint():
    logger.warning("Slow endpoint called - starting delay")  # Gets trace_id automatically
    time.sleep(2)
    logger.info("Slow endpoint - delay completed")           # Gets same trace_id
    return response

# Your middleware records metrics:
record_request(
    method="GET",           # Will match trace attribute
    endpoint="/slow",       # Will match trace attribute  
    status_code=200,        # Will match trace attribute
    duration=2.003
)
```

The magic is that OpenTelemetry automatically maintains the "active context" throughout the request, so:
- All logs get the current trace_id/span_id
- All metrics are recorded with matching attributes
- Everything can be correlated together!
