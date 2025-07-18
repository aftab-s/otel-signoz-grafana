"""
Telemetry configuration examples.

This file demonstrates how easy it is to switch between different
observability backends without changing the main application code.
"""

import os
from telemetry import TelemetryConfig


class SigNozConfig(TelemetryConfig):
    """Configuration for SigNoz observability backend."""
    
    def __init__(self):
        # SigNoz default configuration
        os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
        super().__init__()


class GrafanaConfig(TelemetryConfig):
    """Configuration for Grafana observability stack."""
    
    def __init__(self):
        # Grafana stack configuration (same OTLP endpoints)
        os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
        super().__init__()


class JaegerConfig(TelemetryConfig):
    """Configuration for Jaeger tracing (example)."""
    
    def __init__(self):
        # Example Jaeger configuration
        os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:14268"
        super().__init__()


class CloudConfig(TelemetryConfig):
    """Configuration for cloud observability services (example)."""
    
    def __init__(self):
        # Example cloud provider configuration
        os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        # This would typically be your cloud provider's OTLP endpoint
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://api.your-cloud-provider.com/v1/traces"
        super().__init__()


class DisabledConfig(TelemetryConfig):
    """Configuration that disables telemetry."""
    
    def __init__(self):
        # Set invalid endpoint to disable telemetry
        os.environ["OTEL_SERVICE_NAME"] = "fastapi-demo"
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://disabled:0000"
        super().__init__()


# Configuration selector
def get_config(backend: str = "signoz") -> TelemetryConfig:
    """
    Get telemetry configuration for specified backend.
    
    Args:
        backend: One of 'signoz', 'grafana', 'jaeger', 'cloud', 'disabled'
    
    Returns:
        TelemetryConfig instance for the specified backend
    """
    configs = {
        "signoz": SigNozConfig,
        "grafana": GrafanaConfig,
        "jaeger": JaegerConfig,
        "cloud": CloudConfig,
        "disabled": DisabledConfig,
    }
    
    config_class = configs.get(backend.lower(), SigNozConfig)
    return config_class()


# Example usage:
# To switch to Grafana stack: config = get_config("grafana")
# To switch to SigNoz: config = get_config("signoz") 
# To disable telemetry: config = get_config("disabled")
