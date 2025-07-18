"""
OpenTelemetry telemetry configuration module.

This module handles all observability setup including traces, logs, and metrics.
It provides a clean interface for the main application to use without coupling
the business logic to the telemetry implementation.
"""

import os
import logging
import time
import random
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelemetryConfig:
    """Configuration class for telemetry setup."""
    
    def __init__(self):
        # Set default environment variables if not set
        if not os.getenv("OTEL_SERVICE_NAME"):
            os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        if not os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT"):
            os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
        
        self.service_name = os.getenv("OTEL_SERVICE_NAME")
        self.otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
        self.service_version = "1.0.0"


class TelemetryManager:
    """Manages OpenTelemetry setup and provides telemetry functionality."""
    
    def __init__(self, config: TelemetryConfig):
        self.config = config
        self.enabled = False
        self.meter = None
        
        # Metrics
        self.request_counter = None
        self.request_duration_histogram = None
        self.live_users_gauge = None
        
        self._setup_telemetry()
    
    def _setup_telemetry(self):
        """Initialize OpenTelemetry components."""
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
            
            # Configure the resource
            resource = Resource.create({
                "service.name": self.config.service_name,
                "service.version": self.config.service_version,
            })
            
            # Configure tracing
            trace.set_tracer_provider(TracerProvider(resource=resource))
            
            # Configure the OTLP trace exporter
            otlp_trace_exporter = OTLPSpanExporter(
                endpoint=f"{self.config.otlp_endpoint}/v1/traces"
            )
            
            # Add the span processor
            span_processor = BatchSpanProcessor(otlp_trace_exporter)
            trace.get_tracer_provider().add_span_processor(span_processor)
            
            # Configure logging
            logger_provider = LoggerProvider(resource=resource)
            _logs.set_logger_provider(logger_provider)
            
            # Configure the OTLP log exporter
            otlp_log_exporter = OTLPLogExporter(
                endpoint=f"{self.config.otlp_endpoint}/v1/logs"
            )
            
            # Add the log processor
            log_processor = BatchLogRecordProcessor(otlp_log_exporter)
            logger_provider.add_log_record_processor(log_processor)
            
            # Add OpenTelemetry handler to the root logger
            handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
            logging.getLogger().addHandler(handler)
            
            # Configure metrics
            metric_reader = PeriodicExportingMetricReader(
                OTLPMetricExporter(endpoint=f"{self.config.otlp_endpoint}/v1/metrics"),
                export_interval_millis=5000,  # Export every 5 seconds
            )
            meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
            metrics.set_meter_provider(meter_provider)
            
            # Get a meter
            self.meter = metrics.get_meter("fastapi-demo-meter")
            
            # Create metrics
            self.request_counter = self.meter.create_counter(
                "http_requests_total",
                description="Total number of HTTP requests",
                unit="1"
            )
            
            self.request_duration_histogram = self.meter.create_histogram(
                "http_request_duration_seconds",
                description="HTTP request duration in seconds",
                unit="s"
            )
            
            self.live_users_gauge = self.meter.create_up_down_counter(
                "live_users_count",
                description="Number of live users currently active",
                unit="1"
            )
            
            print("OpenTelemetry configured successfully")
            print(f"Sending traces to: {self.config.otlp_endpoint}/v1/traces")
            print(f"Sending logs to: {self.config.otlp_endpoint}/v1/logs")
            print(f"Sending metrics to: {self.config.otlp_endpoint}/v1/metrics")
            self.enabled = True
            
        except Exception as e:
            print(f"OpenTelemetry setup failed: {e}")
            print("App will run without tracing")
            self.enabled = False
    
    def instrument_fastapi(self, app):
        """Instrument FastAPI application with OpenTelemetry."""
        if not self.enabled:
            return
        
        try:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
            FastAPIInstrumentor.instrument_app(app)
            print("FastAPI instrumentation applied")
        except Exception as e:
            print(f"FastAPI instrumentation failed: {e}")
    
    def record_request_metrics(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics."""
        if not self.enabled or not self.request_counter or not self.request_duration_histogram:
            return
        
        labels = {
            "method": method,
            "endpoint": endpoint,
            "status_code": str(status_code)
        }
        
        # Increment request counter
        self.request_counter.add(1, labels)
        
        # Record request duration
        self.request_duration_histogram.record(duration, labels)
        
        # Simulate live users count (random between 10-100)
        if self.live_users_gauge:
            live_users_count = random.randint(10, 100)
            self.live_users_gauge.add(live_users_count - 50)  # Simulate fluctuation around 50
    
    def create_custom_metric(self, name: str, description: str, metric_type: str = "counter", unit: str = "1"):
        """Create a custom metric."""
        if not self.enabled or not self.meter:
            return None
        
        try:
            if metric_type == "counter":
                return self.meter.create_counter(name, description=description, unit=unit)
            elif metric_type == "histogram":
                return self.meter.create_histogram(name, description=description, unit=unit)
            elif metric_type == "gauge":
                return self.meter.create_up_down_counter(name, description=description, unit=unit)
            else:
                print(f"Unknown metric type: {metric_type}")
                return None
        except Exception as e:
            print(f"Failed to create custom metric {name}: {e}")
            return None


# Global telemetry manager instance
_telemetry_manager: Optional[TelemetryManager] = None


def get_telemetry_manager() -> TelemetryManager:
    """Get or create the global telemetry manager instance."""
    global _telemetry_manager
    if _telemetry_manager is None:
        config = TelemetryConfig()
        _telemetry_manager = TelemetryManager(config)
    return _telemetry_manager


def setup_telemetry(app) -> TelemetryManager:
    """Setup telemetry for FastAPI application."""
    telemetry = get_telemetry_manager()
    telemetry.instrument_fastapi(app)
    return telemetry


# Convenience functions for easy usage
def record_request(method: str, endpoint: str, status_code: int, duration: float):
    """Record HTTP request metrics."""
    get_telemetry_manager().record_request_metrics(method, endpoint, status_code, duration)


def create_metric(name: str, description: str, metric_type: str = "counter", unit: str = "1"):
    """Create a custom metric."""
    return get_telemetry_manager().create_custom_metric(name, description, metric_type, unit)


def is_telemetry_enabled() -> bool:
    """Check if telemetry is enabled."""
    return get_telemetry_manager().enabled
