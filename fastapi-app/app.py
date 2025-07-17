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
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    
    # Configure the tracer provider
    resource = Resource.create({
        "service.name": os.getenv("OTEL_SERVICE_NAME"),
        "service.version": "1.0.0",
    })
    
    trace.set_tracer_provider(TracerProvider(resource=resource))
    
    # Configure the OTLP exporter
    otlp_exporter = OTLPSpanExporter(
        endpoint=f"{os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}/v1/traces"
    )
    
    # Add the span processor
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    print("✅ OpenTelemetry configured successfully")
    print(f"📡 Sending traces to: {os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT')}")
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
    logger.info("Slow endpoint called - starting delay")
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
