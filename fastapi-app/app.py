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
    from opentelemetry import trace, _logs
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    
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
    
    print("✅ OpenTelemetry configured successfully")
    print(f"📡 Sending traces to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/traces")
    print(f"📝 Sending logs to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/logs")
    OTEL_ENABLED = True
    
except Exception as e:
    print(f"❌ OpenTelemetry setup failed: {e}")
    print("🔧 App will run without tracing")
    OTEL_ENABLED = False

# Create FastAPI app
app = FastAPI(title="FastAPI Demo", description="Simple FastAPI app with OpenTelemetry tracing")

# Instrument FastAPI
if OTEL_ENABLED:
    try:
        FastAPIInstrumentor.instrument_app(app)
        print("✅ FastAPI instrumentation applied")
    except Exception as e:
        print(f"⚠️ FastAPI instrumentation failed: {e}")

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

if __name__ == "__main__":
    print("🚀 Starting FastAPI application...")
    print(f"🌐 Service: {os.getenv('OTEL_SERVICE_NAME')}")
    print(f"📊 Traces: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}")
    print("📚 API docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
