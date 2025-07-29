"""
COMPREHENSIVE BREAKDOWN: What Auto-Instrumentation Covers vs What Requires Manual Work
"""

# ===== TRACES & SPANS =====
# AUTO-INSTRUMENTATION PROVIDES:
"""
✅ HTTP request spans (automatically created)
✅ Span timing (start/end)
✅ Basic HTTP attributes:
   - http.method
   - http.url  
   - http.status_code
   - http.route
   - http.user_agent
✅ Parent-child relationships for HTTP requests
✅ Exception recording (if unhandled)
"""

# MANUAL INSTRUMENTATION REQUIRED FOR:
"""
❌ Custom span names
❌ Business logic spans (inside your endpoints)
❌ Custom attributes (like user.id, operation.type)
❌ Span events (like "processing_started")
❌ Nested spans for sub-operations
❌ Custom exception handling
"""

# ===== METRICS =====
# AUTO-INSTRUMENTATION PROVIDES:
"""
✅ Basic HTTP metrics (with FastAPI instrumentation):
   - http_server_duration (request duration histogram)
   - http_server_request_size (request size histogram) 
   - http_server_response_size (response size histogram)
✅ Automatic labeling with method, status_code, route
"""

# MANUAL INSTRUMENTATION REQUIRED FOR:
"""
❌ Custom business metrics (counters, gauges, histograms)
❌ Application-specific metrics (user registrations, purchases, etc.)
❌ Custom metric labels/dimensions
❌ Metric aggregations
"""

# ===== LOGS =====
# AUTO-INSTRUMENTATION PROVIDES:
"""
✅ Log correlation (trace_id, span_id automatically added to logs)
✅ Log export to OTLP endpoint
✅ Structured log format
"""

# MANUAL INSTRUMENTATION REQUIRED FOR:
"""
❌ ALL log messages (logger.info(), logger.error(), etc.)
❌ Log content and formatting  
❌ Log levels and filtering
❌ Custom log attributes
"""
