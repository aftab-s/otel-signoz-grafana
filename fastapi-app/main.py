from fastapi import FastAPI, HTTPException, Request
import time
import logging
import uvicorn
import random
from telemetry import setup_telemetry, record_request, create_metric, is_telemetry_enabled

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Demo", description="Simple FastAPI app with OpenTelemetry tracing")

# this handles all OpenTelemetry configuration
telemetry_manager = setup_telemetry(app)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    # Middleware to track request metrics using the telemetry module
    start_time = time.time()
    
    # process the request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Record metrics using telemetry module
    record_request(
        method=request.method,
        endpoint=str(request.url.path),
        status_code=response.status_code,
        duration=duration
    )
    
    return response


@app.get("/")
async def root():
    # Root endpoint
    logger.info("Root endpoint called")
    return {"message": "Hello from FastAPI with OpenTelemetry!", "service": telemetry_manager.config.service_name}


@app.get("/fast")
async def fast_endpoint():
    # fast endpoint
    logger.info("Fast endpoint called")
    return {"message": "This is a fast response", "status": "success", "endpoint": "fast"}


@app.get("/slow")
async def slow_endpoint():
    # slow endpoint with 2s delay
    logger.warning("Slow endpoint called - starting delay")
    time.sleep(2)  # 2s delay
    logger.info("Slow endpoint - delay completed")
    return {"message": "This is a slow response after 2 seconds", "status": "success", "endpoint": "slow"}


@app.get("/error")
async def error_endpoint():
    # Error endpoint - Returns "500" status code
    logger.error("Error endpoint called - simulating server error")
    raise HTTPException(status_code=500, detail="Internal Server Error - This is a simulated error")


@app.get("/metrics-demo")
async def metrics_demo():
    # Endpoint to demonstrate custom metrics
    logger.info("Metrics demo endpoint called")
    
    if is_telemetry_enabled():
        # custom metrics for demonstration
        demo_counter = create_metric(
            "demo_operations_total",
            "Total demo operations performed",
            "counter"
        )
        
        demo_gauge = create_metric(
            "demo_active_connections",
            "Number of active demo connections",
            "gauge"
        )
        
        # Recording demo metrics
        if demo_counter:
            demo_counter.add(1, {"operation": "demo_call", "user_type": "demo"})
            
        if demo_gauge:
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
    print("Starting FastAPI application")
    print(f"Service: {telemetry_manager.config.service_name}")
    print(f"Traces: {telemetry_manager.config.otlp_endpoint}")
    uvicorn.run(app, host="0.0.0.0", port=8000)