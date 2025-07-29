# SigNoz Architecture and How It Works

## High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Your App      │    │   SigNoz         │    │   ClickHouse    │
│                 │    │   (OTLP          │    │   (Storage)     │
│ ┌─────────────┐ │    │   Collector)     │    │                 │
│ │OpenTelemetry│ │───▶│                  │───▶│                 │
│ │    SDK      │ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ └─────────────┘ │    │ │ Traces       │ │    │ │   Traces    │ │
│                 │    │ │ Logs         │ │    │ │   Logs      │ │
│                 │    │ │ Metrics      │ │    │ │   Metrics   │ │
│                 │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   SigNoz UI      │
                       │   (Query Engine  │
                       │    + Frontend)   │
                       └──────────────────┘
```

## 1. DATA INGESTION LAYER

### OTLP Collector (Port 4318/4317)
- Receives OTLP data from your applications
- Validates and processes incoming telemetry
- Performs data transformations and enrichment
- Handles batching and buffering

### Data Processing Pipeline
```
Raw OTLP Data → Validation → Transformation → Enrichment → Storage
```

## 2. STORAGE LAYER - ClickHouse

### Why ClickHouse?
- **Columnar database**: Optimized for analytical queries
- **Time-series optimized**: Perfect for telemetry data
- **High compression**: Reduces storage costs
- **Fast aggregations**: Quick dashboard queries
- **Horizontal scaling**: Can handle massive data volumes

### Data Models in ClickHouse

#### Traces Table Structure:
```sql
CREATE TABLE traces (
    timestamp DateTime64,
    trace_id String,
    span_id String,
    parent_span_id String,
    operation_name String,
    service_name String,
    duration_ns UInt64,
    status_code Int32,
    span_kind String,
    attributes Map(String, String),
    events Array(String),
    links Array(String)
) ENGINE = MergeTree()
ORDER BY (service_name, timestamp)
```

#### Logs Table Structure:
```sql
CREATE TABLE logs (
    timestamp DateTime64,
    trace_id String,
    span_id String,
    severity_text String,
    severity_number Int32,
    body String,
    attributes Map(String, String),
    resource_attributes Map(String, String)
) ENGINE = MergeTree()
ORDER BY (timestamp)
```

#### Metrics Table Structure:
```sql
CREATE TABLE metrics (
    timestamp DateTime64,
    name String,
    value Float64,
    attributes Map(String, String),
    resource_attributes Map(String, String),
    metric_type String
) ENGINE = MergeTree()
ORDER BY (name, timestamp)
```

## 3. QUERY ENGINE

### Query Processing Flow
1. **UI Request**: User clicks on dashboard/trace
2. **Query Generation**: Frontend generates ClickHouse SQL
3. **Query Execution**: ClickHouse processes the query
4. **Result Processing**: Data formatted for UI
5. **Response**: JSON sent to frontend

### Example Queries SigNoz Generates

#### Get all traces for a service:
```sql
SELECT 
    trace_id,
    operation_name,
    duration_ns,
    status_code,
    timestamp
FROM traces 
WHERE service_name = 'fastapi-demo'
  AND timestamp BETWEEN '2025-01-01' AND '2025-01-02'
ORDER BY timestamp DESC
LIMIT 100
```

#### Correlate logs with traces:
```sql
SELECT 
    l.timestamp,
    l.body,
    l.severity_text,
    t.operation_name,
    t.duration_ns
FROM logs l
JOIN traces t ON l.trace_id = t.trace_id
WHERE l.trace_id = '7f8e9d2c1b3a4f5e6789012345abcdef'
ORDER BY l.timestamp
```

## 4. FRONTEND/UI LAYER

### React-based Frontend
- **Traces Explorer**: Query and visualize traces
- **Logs Explorer**: Search and filter logs
- **Metrics Dashboard**: Create custom dashboards
- **Alerts Manager**: Set up alerting rules
- **Service Map**: Visualize service dependencies

### Real-time Features
- **WebSocket connections**: Live updates
- **Streaming queries**: Real-time dashboards
- **Auto-refresh**: Keep data current

## 5. DATA FLOW IN YOUR PROJECT

### When you call GET /slow:

1. **Application Layer**:
   ```python
   # Your FastAPI app generates telemetry
   logger.warning("Slow endpoint called")  # Creates log with trace_id
   # Auto-instrumentation creates span
   # Middleware records metrics
   ```

2. **OpenTelemetry SDK**:
   ```
   Traces → BatchSpanProcessor → OTLPSpanExporter → HTTP POST
   Logs → BatchLogProcessor → OTLPLogExporter → HTTP POST  
   Metrics → PeriodicMetricReader → OTLPMetricExporter → HTTP POST
   ```

3. **SigNoz Ingestion** (Port 4318):
   ```
   POST /v1/traces   ← Span data
   POST /v1/logs     ← Log data  
   POST /v1/metrics  ← Metric data
   ```

4. **Data Processing**:
   ```
   OTLP JSON → Validation → Schema mapping → ClickHouse INSERT
   ```

5. **Storage in ClickHouse**:
   ```sql
   -- Trace record
   INSERT INTO traces VALUES (
     '2025-01-29 10:30:15',
     '7f8e9d2c1b3a4f5e6789012345abcdef',
     'a1b2c3d4e5f6789',
     '',
     'GET /slow',
     'fastapi-demo',
     2003000000,  -- 2.003 seconds in nanoseconds
     200,
     'SERVER',
     {'http.method': 'GET', 'http.route': '/slow'},
     [],
     []
   )
   ```

6. **UI Query**:
   ```sql
   -- When you open SigNoz UI
   SELECT * FROM traces 
   WHERE service_name = 'fastapi-demo' 
   ORDER BY timestamp DESC 
   LIMIT 50
   ```

## 6. ADVANCED FEATURES

### Sampling
```yaml
# In SigNoz config
sampling:
  default_strategy:
    type: probabilistic
    param: 0.1  # Sample 10% of traces
```

### Retention Policies
```sql
-- Automatic data cleanup
ALTER TABLE traces 
ADD TTL timestamp + INTERVAL 30 DAY  -- Keep traces for 30 days
```

### Alerting Engine
```yaml
# Alert rules stored in ClickHouse
alerts:
  - name: "High Error Rate"
    query: "SELECT count(*) FROM traces WHERE status_code >= 400"
    threshold: 10
    evaluation_interval: "1m"
```

## 7. PERFORMANCE OPTIMIZATIONS

### Data Ingestion
- **Batching**: Reduces network overhead
- **Compression**: gzip/zstd compression
- **Buffering**: Handles traffic spikes

### Query Optimization  
- **Indexes**: Optimized for time-series queries
- **Materialized views**: Pre-computed aggregations
- **Caching**: Query result caching
- **Partitioning**: Data organized by time ranges

### Storage Optimization
- **Compression**: ClickHouse's built-in compression
- **Compaction**: Background data optimization
- **Sharding**: Distribute data across nodes

## 8. DEPLOYMENT ARCHITECTURE

### Single Node (Your Setup)
```
┌─────────────────────────────────────┐
│           Docker Container          │
│                                     │
│  ┌─────────────┐ ┌─────────────────┐│
│  │   SigNoz    │ │   ClickHouse    ││
│  │   Backend   │ │   Database      ││
│  └─────────────┘ └─────────────────┘│
│                                     │
│  ┌─────────────────────────────────┐│
│  │        SigNoz UI                ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### Production Cluster
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  SigNoz      │    │  ClickHouse  │    │  ClickHouse  │
│  Collector   │───▶│   Node 1     │    │   Node 2     │
│              │    │              │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                              │                │
                              └────────────────┘
                                     │
                    ┌──────────────────────────────┐
                    │       Load Balancer          │
                    └──────────────────────────────┘
                                     │
                    ┌──────────────────────────────┐
                    │       SigNoz UI              │
                    └──────────────────────────────┘
```

This is the complete picture of how SigNoz processes your OpenTelemetry data from ingestion to visualization!
