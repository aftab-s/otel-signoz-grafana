#!/bin/bash

# Test Script for FastAPI OpenTelemetry Demo
echo -e "\033[32mFastAPI OpenTelemetry Test Script\033[0m"
echo -e "\033[33mGenerating test traffic to create traces, logs, and metrics\033[0m"

BASE_URL="http://localhost:8000"

echo -e "\033[36mTesting basic endpoints\033[0m"

# Test fast endpoint
echo -e "\033[37mTesting /fast endpoint\033[0m"
if curl -s "$BASE_URL/fast" > /dev/null; then
    echo -e "\033[32mFast endpoint: 200 OK\033[0m"
else
    echo -e "\033[31mFast endpoint failed\033[0m"
fi

# Test slow endpoint
echo -e "\033[37mTesting /slow endpoint\033[0m"
if curl -s "$BASE_URL/slow" > /dev/null; then
    echo -e "\033[32mSlow endpoint: 200 OK\033[0m"
else
    echo -e "\033[31mSlow endpoint failed\033[0m"
fi

# Test error endpoint
echo -e "\033[37mTesting /error endpoint\033[0m"
if curl -s "$BASE_URL/error" > /dev/null 2>&1; then
    echo -e "\033[33mThis should fail\033[0m"
else
    echo -e "\033[32mError endpoint returned expected 500 error\033[0m"
fi

# Test metrics demo endpoint
echo -e "\033[37mTesting /metrics-demo endpoint\033[0m"
if curl -s "$BASE_URL/metrics-demo" > /dev/null; then
    echo -e "\033[32mMetrics demo: 200 OK\033[0m"
else
    echo -e "\033[31mMetrics demo failed\033[0m"
fi

echo -e "\033[36mGenerating load for better metrics\033[0m"

# Generate multiple requests
for i in {1..5}; do
    echo -e "\033[37mLoad test iteration $i/5\033[0m"
    
    curl -s "$BASE_URL/fast" > /dev/null 2>&1
    curl -s "$BASE_URL/fast" > /dev/null 2>&1
    curl -s "$BASE_URL/slow" > /dev/null 2>&1
    curl -s "$BASE_URL/error" > /dev/null 2>&1
    curl -s "$BASE_URL/metrics-demo" > /dev/null 2>&1
    
    sleep 1
done

echo -e "\033[32mTest completed!\033[0m"
echo -e "\033[33mCheck your Observability setup\033[0m"
echo -e "\033[37mYou should see:\033[0m"
echo -e "\033[37m  Traces: Fast (~100ms), Slow (~2000ms), Error (500)\033[0m"
echo -e "\033[37m  Logs: INFO, WARNING, ERROR levels\033[0m"
echo -e "\033[37m  Metrics: Request counts, latency histograms, live users\033[0m"
echo -e "\033[36mService name: fastapi-demo\033[0m"

echo -e "\033[33mAvailable endpoints:\033[0m"
echo -e "\033[37m  GET /         - Root endpoint\033[0m"
echo -e "\033[37m  GET /fast     - Quick response (~100ms)\033[0m"
echo -e "\033[37m  GET /slow     - Slow response (~2000ms)\033[0m"
echo -e "\033[37m  GET /error    - Error response (500)\033[0m"
echo -e "\033[37m  GET /metrics-demo - Custom metrics demo\033[0m"
echo -e "\033[37m  GET /docs     - API documentation\033[0m"
