#!/bin/bash

# FastAPI + OpenTelemetry + SigNoz Setup and Run Script
echo -e "\033[32mStarting FastAPI with OpenTelemetry\033[0m"

# Install dependencies
echo -e "\033[33mInstalling Python dependencies\033[0m"
pip install -r requirements.txt

# Set environment variables
echo -e "\033[33mSetting up OpenTelemetry environment variables\033[0m"
export OTEL_SERVICE_NAME="fastapi-demo"
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
export OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
export OTEL_RESOURCE_ATTRIBUTES="service.name=fastapi-demo"

echo -e "\033[32mEnvironment variables set successfully\033[0m"

# Run the application
echo -e "\033[32mStarting FastAPI application\033[0m"
echo -e "\033[36mApplication will be available at http://localhost:8000\033[0m"
echo -e "\033[36mSigNoz UI: http://localhost:8080\033[0m"

python main.py
