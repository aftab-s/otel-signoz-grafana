# Grafana Observability Stack

This directory contains a complete Grafana-based observability stack that can receive the same telemetry data from your FastAPI application without any code changes.

## Architecture

The Grafana stack consists of:

- **OpenTelemetry Collector**: Receives OTLP data on the same ports as SigNoz (4317/4318)
- **Prometheus**: Metrics storage and querying
- **Loki**: Log aggregation and storage  
- **Tempo**: Distributed tracing backend
- **Grafana**: Unified visualization and dashboards

## Quick Start

1. **Stop SigNoz** (if running):
   ```powershell
   cd "s:\SigNoz\Assignment 2\otel-signoz-grafana\signoz-config\deploy\docker"
   docker-compose down
   ```

2. **Start Grafana Stack**:
   ```powershell
   cd "s:\SigNoz\Assignment 2\otel-signoz-grafana\grafana-config"
   docker-compose up -d
   ```

3. **Run your FastAPI application** (no code changes needed):
   ```powershell
   cd "s:\SigNoz\Assignment 2\otel-signoz-grafana\fastapi-app"
   .\run.ps1
   ```

4. **Access Grafana UI**:
   - URL: http://localhost:3000
   - Username: admin
   - Password: admin

## Service Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| Grafana UI | http://localhost:3000 | Main dashboard interface |
| Prometheus | http://localhost:9090 | Metrics query interface |
| Loki | http://localhost:3100 | Logs API |
| Tempo | http://localhost:3200 | Tracing backend |
| OTLP gRPC | http://localhost:4317 | Same as SigNoz |
| OTLP HTTP | http://localhost:4318 | Same as SigNoz |

## Key Features

### Metrics (Prometheus)
- HTTP request rates and latency
- Custom business metrics (counters, histograms, gauges)
- System and application performance metrics
- Alert rules and thresholds

### Logs (Loki)
- Structured and unstructured log ingestion
- Label-based log filtering and searching
- Log aggregation and retention policies
- Integration with traces for correlation

### Traces (Tempo)
- Distributed request tracing
- Service dependency mapping
- Performance bottleneck identification
- Trace to logs/metrics correlation

### Visualization (Grafana)
- Pre-configured dashboards for FastAPI metrics
- Unified view of metrics, logs, and traces
- Alerting and notification capabilities
- Explore interface for ad-hoc analysis

## Data Flow

```
FastAPI App → OTLP (4317/4318) → OpenTelemetry Collector → {Prometheus, Loki, Tempo} → Grafana
```

## Comparison with SigNoz

| Feature | SigNoz | Grafana Stack |
|---------|--------|---------------|
| Setup Complexity | Medium | Medium |
| UI Experience | Integrated | Flexible |
| Query Language | ClickHouse SQL | PromQL, LogQL, TraceQL |
| Storage Backend | ClickHouse | Prometheus/Loki/Tempo |
| Community | Growing | Mature |
| Alerting | Built-in | Advanced |
| Customization | Limited | Extensive |

## Testing the Setup

1. Generate test traffic:
   ```powershell
   cd "s:\SigNoz\Assignment 2\otel-signoz-grafana\fastapi-app"
   .\test-telemetry.ps1
   ```

2. View data in Grafana:
   - Navigate to Dashboards → FastAPI Application Observability
   - Use Explore to query metrics, logs, and traces directly
   - Check data sources connectivity in Configuration → Data Sources

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure SigNoz is stopped before starting Grafana stack
2. **Data Not Appearing**: Check OpenTelemetry Collector logs: `docker logs grafana-otel-collector`
3. **Dashboard Empty**: Verify data sources are connected and receiving data

### Useful Commands

```powershell
# Check all services status
docker-compose ps

# View collector logs
docker logs grafana-otel-collector -f

# Restart specific service
docker-compose restart otel-collector

# Clean up everything
docker-compose down -v
```

## Dashboard Features

The included FastAPI dashboard provides:

- **Request Rate**: Real-time request throughput
- **Response Time**: 95th percentile latency monitoring
- **Error Rate**: HTTP 5xx error percentage
- **Endpoint Performance**: Per-endpoint metrics breakdown
- **Application Logs**: Structured log viewing with filtering

## Next Steps

1. **Customize Dashboards**: Modify `grafana/dashboards/fastapi-dashboard.json`
2. **Add Alerting**: Configure alert rules in Grafana
3. **Extend Metrics**: Add custom business metrics to your application
4. **Performance Tuning**: Adjust retention periods and storage settings

This setup provides a production-ready alternative to SigNoz while maintaining the same data ingestion endpoints, allowing for easy comparison between the two observability platforms.
