from fastapi import FastAPI, HTTPException
import time
import logging
import uvicorn
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set default environment variables if not set
if not os.getenv("OTEL_SERVICE_NAME"):
    os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
if not os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"

# OpenTelemetry setup
try:
    from opentelemetry import trace, _logs, metrics
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    import random
    
    # Configure the resource
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME"),
        "service.version": "1.0.0",
    })
    
    # Configure tracing
    trace.set_tracer_provider(TracerProvider(resource=resource))
    
    # Configure the OTLP trace exporter
    otlp_trace_exporter = OTLPSpanExporter(
        endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/traces"
    )
    
    # Add the span processor
    span_processor = BatchSpanProcessor(otlp_trace_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
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
    
    # Add OpenTelemetry handler to the root logger
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    
    # Configure metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/metrics"),
        export_interval_millis=5000,  # Export every 5 seconds
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)
    
    # Get a meter
    meter = metrics.get_meter("fastapi-demo-meter")
    
    # Create metrics
    request_counter = meter.create_counter(
        "http_requests_total",
        description="Total number of HTTP requests",
        unit="1"
    )
    
    request_duration_histogram = meter.create_histogram(
        "http_request_duration_seconds",
        description="HTTP request duration in seconds",
        unit="s"
    )
    
    live_users_gauge = meter.create_up_down_counter(
        "live_users_count",
        description="Number of live users currently active",
        unit="1"
    )
    
    print("OpenTelemetry configured successfully")
    print(f"Sending traces to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/traces")
    print(f"Sending logs to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/logs")
    print(f"Sending metrics to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/metrics")
    OTEL_ENABLED = True
    
except Exception as e:
    print(f"OpenTelemetry setup failed: {e}")
    print("App will run without tracing")
    OTEL_ENABLED = False
    # Create dummy metrics objects to avoid errors
    request_counter = None
    request_duration_histogram = None
    live_users_gauge = None

# Create FastAPI app
app = FastAPI(title="FastAPI Demo", description="Simple FastAPI app with OpenTelemetry tracing")

# Instrument FastAPI
if OTEL_ENABLED:
    try:
        FastAPIInstrumentor.instrument_app(app)
        print("FastAPI instrumentation applied")
    except Exception as e:
        print(f"FastAPI instrumentation failed: {e}")

# Middleware to track request metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Record metrics if OpenTelemetry is enabled
    if OTEL_ENABLED and request_counter and request_duration_histogram:
        # Increment request counter
        request_counter.add(1, {
            "method": request.method,
            "endpoint": str(request.url.path),
            "status_code": str(response.status_code)
        })
        
        # Record request duration
        request_duration_histogram.record(duration, {
            "method": request.method,
            "endpoint": str(request.url.path),
            "status_code": str(response.status_code)
        })
        
        # Simulate live users count (random between 10-100)
        live_users_count = random.randint(10, 100)
        live_users_gauge.add(live_users_count - 50)  # Simulate fluctuation around 50
    
    return response

@app.get("/")
async def root():
    """Root endpoint"""
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI with OpenTelemetry!", "service": os.getenv("OTEL_SERVICE_NAME")}

@app.get("/fast")
async def fast_endpoint():
    """A quick, successful response"""
    logger.info("Fast endpoint called")
    return {"message": "This is a fast response", "status": "success", "endpoint": "fast"}

@app.get("/slow")
async def slow_endpoint():
    """A response with a 2-second delay"""
    logger.warning("Slow endpoint called - starting delay")
    time.sleep(2)  # 2-second delay
    logger.info("Slow endpoint - delay completed")
    return {"message": "This is a slow response after 2 seconds", "status": "success", "endpoint": "slow"}

@app.get("/error")
async def error_endpoint():
    """Returns a 500 status code"""
    logger.error("Error endpoint called - simulating server error")
    raise HTTPException(status_code=500, detail="Internal Server Error - This is a simulated error")

@app.get("/metrics-demo")
async def metrics_demo():
    """Endpoint to demonstrate custom metrics"""
    logger.info("Metrics demo endpoint called")
    
    if OTEL_ENABLED and request_counter:
        # Create some custom metrics for demonstration
        demo_counter = meter.create_counter(
            "demo_operations_total",
            description="Total demo operations performed",
            unit="1"
        )
        
        demo_gauge = meter.create_up_down_counter(
            "demo_active_connections",
            description="Number of active demo connections",
            unit="1"
        )
        
        # Record some demo metrics
        demo_counter.add(1, {"operation": "demo_call", "user_type": "demo"})
        demo_gauge.add(random.randint(1, 5), {"connection_type": "demo"})
        
        return {
            "message": "Custom metrics recorded successfully",
            "metrics_recorded": [
                "demo_operations_total",
                "demo_active_connections"
            ],
            "status": "success"
        }
    else:
        return {
            "message": "Metrics not available - OpenTelemetry not configured",
            "status": "disabled"
        }

if __name__ == "__main__":
    print("Starting FastAPI application...")
    print(f"Service: {os.getenv('OTEL_SERVICE_NAME')}")
    print(f"Traces: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}")
    print("API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
