"""
Example showing how main.py would look with MANUAL instrumentation instead of auto-instrumentation
"""

from fastapi import FastAPI, HTTPException, Request
import time
import logging
import uvicorn
import random
from telemetry import setup_telemetry_manual, record_request, create_metric, is_telemetry_enabled
from opentelemetry import trace

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Demo", description="Simple FastAPI app with MANUAL OpenTelemetry tracing")

# Setup telemetry WITHOUT auto-instrumentation
telemetry_manager = setup_telemetry_manual(app)

# Get tracer for manual span creation
tracer = trace.get_tracer("fastapi-demo-tracer")

@app.middleware("http")
async def tracing_and_metrics_middleware(request: Request, call_next):
    """
    MANUAL middleware that creates spans AND records metrics
    This replaces the auto-instrumentation functionality
    """
    # MANUAL: Create span manually
    with tracer.start_as_current_span(
        name=f"{request.method} {request.url.path}",
        kind=trace.SpanKind.SERVER
    ) as span:
        
        # MANUAL: Add span attributes
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.url", str(request.url))
        span.set_attribute("http.route", request.url.path)
        span.set_attribute("http.user_agent", request.headers.get("user-agent", ""))
        
        start_time = time.time()
        
        try:
            # Process the request
            response = await call_next(request)
            
            # MANUAL: Add response attributes to span
            span.set_attribute("http.status_code", response.status_code)
            span.set_status(trace.Status(trace.StatusCode.OK))
            
            return response
            
        except Exception as e:
            # MANUAL: Handle exceptions in spans
            span.set_status(trace.Status(
                trace.StatusCode.ERROR, 
                description=str(e)
            ))
            span.record_exception(e)
            raise
            
        finally:
            # Record metrics (this part stays similar)
            duration = time.time() - start_time
            record_request(
                method=request.method,
                endpoint=str(request.url.path),
                status_code=getattr(response, 'status_code', 500),
                duration=duration
            )


@app.get("/")
async def root():
    """
    MANUAL instrumentation example - adding custom spans and attributes
    """
    # MANUAL: Create custom child span
    with tracer.start_as_current_span("root_endpoint_processing") as span:
        logger.info("Root endpoint called")
        
        # MANUAL: Add custom attributes
        span.set_attribute("endpoint.type", "greeting")
        span.set_attribute("endpoint.version", "v1")
        
        # MANUAL: Create sub-operation span
        with tracer.start_as_current_span("get_service_info") as sub_span:
            sub_span.set_attribute("operation", "config_lookup")
            service_name = telemetry_manager.config.service_name
            sub_span.set_attribute("service.name", service_name)
        
        # MANUAL: Add event to span
        span.add_event("response_prepared", {
            "message_length": len("Hello from FastAPI with OpenTelemetry!"),
            "service": service_name
        })
        
        return {
            "message": "Hello from FastAPI with OpenTelemetry!", 
            "service": service_name
        }


@app.get("/fast")
async def fast_endpoint():
    """Simple endpoint - minimal manual instrumentation"""
    with tracer.start_as_current_span("fast_endpoint_processing") as span:
        logger.info("Fast endpoint called")
        
        span.set_attribute("endpoint.category", "performance_demo")
        span.set_attribute("expected_duration", "fast")
        
        return {
            "message": "This is a fast response", 
            "status": "success", 
            "endpoint": "fast"
        }


@app.get("/slow")
async def slow_endpoint():
    """MANUAL instrumentation with nested spans for slow operations"""
    with tracer.start_as_current_span("slow_endpoint_processing") as span:
        logger.warning("Slow endpoint called - starting delay")
        
        span.set_attribute("endpoint.category", "performance_demo")
        span.set_attribute("expected_duration", "slow")
        span.set_attribute("delay_seconds", 2)
        
        # MANUAL: Create span for the delay operation
        with tracer.start_as_current_span("artificial_delay") as delay_span:
            delay_span.set_attribute("delay.type", "sleep")
            delay_span.set_attribute("delay.duration", 2.0)
            delay_span.add_event("delay_started")
            
            time.sleep(2)  # 2s delay
            
            delay_span.add_event("delay_completed")
        
        logger.info("Slow endpoint - delay completed")
        span.add_event("response_ready")
        
        return {
            "message": "This is a slow response after 2 seconds", 
            "status": "success", 
            "endpoint": "slow"
        }


@app.get("/error")
async def error_endpoint():
    """MANUAL error handling and span status management"""
    with tracer.start_as_current_span("error_endpoint_processing") as span:
        logger.error("Error endpoint called - simulating server error")
        
        span.set_attribute("endpoint.category", "error_demo")
        span.set_attribute("error.type", "simulated")
        
        # MANUAL: Set span status and record exception
        span.add_event("error_simulation_started")
        
        try:
            # Simulate some processing before error
            with tracer.start_as_current_span("pre_error_processing") as sub_span:
                sub_span.set_attribute("processing.step", "validation")
                sub_span.add_event("validation_failed")
                
                # Create the exception
                error = HTTPException(
                    status_code=500, 
                    detail="Internal Server Error - This is a simulated error"
                )
                
                # MANUAL: Record exception in span
                span.record_exception(error)
                span.set_status(trace.Status(
                    trace.StatusCode.ERROR,
                    description="Simulated server error"
                ))
                
                raise error
                
        except HTTPException:
            # Re-raise the HTTP exception
            raise


@app.get("/metrics-demo")
async def metrics_demo():
    """MANUAL instrumentation with custom metrics and detailed tracing"""
    with tracer.start_as_current_span("metrics_demo_processing") as span:
        logger.info("Metrics demo endpoint called")
        
        span.set_attribute("endpoint.category", "metrics_demo")
        span.set_attribute("telemetry.enabled", is_telemetry_enabled())
        
        if is_telemetry_enabled():
            # MANUAL: Create span for metrics creation
            with tracer.start_as_current_span("create_custom_metrics") as metrics_span:
                metrics_span.set_attribute("metrics.count", 2)
                
                # Create custom metrics
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
                
                metrics_span.add_event("metrics_created")
            
            # MANUAL: Create span for recording metrics
            with tracer.start_as_current_span("record_metrics") as record_span:
                random_value = random.randint(1, 5)
                record_span.set_attribute("random_value", random_value)
                
                # Recording demo metrics
                if demo_counter:
                    demo_counter.add(1, {"operation": "demo_call", "user_type": "demo"})
                    record_span.add_event("counter_incremented")
                    
                if demo_gauge:
                    demo_gauge.add(random_value, {"connection_type": "demo"})
                    record_span.add_event("gauge_updated", {"value": random_value})
            
            span.set_attribute("metrics.recorded", True)
            return {
                "message": "Custom metrics recorded successfully",
                "metrics_recorded": [
                    "demo_operations_total",
                    "demo_active_connections"
                ],
                "status": "success"
            }
        else:
            span.set_attribute("metrics.recorded", False)
            span.add_event("telemetry_disabled")
            return {
                "message": "Metrics not available - OpenTelemetry not configured",
                "status": "disabled"
            }


if __name__ == "__main__":
    print("Starting FastAPI application with MANUAL instrumentation")
    print(f"Service: {telemetry_manager.config.service_name}")
    print(f"Traces: {telemetry_manager.config.otlp_endpoint}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
