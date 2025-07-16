# FastAPI Service

A simple FastAPI application with three different endpoints for testing purposes.

## Endpoints

- **GET /**: Root endpoint with welcome message
- **GET /fast**: A quick, successful response
- **GET /slow**: A response with a 2-second delay
- **GET /error**: Returns a 500 status code and logs an error

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

2. The application will be available at `http://localhost:8000`

3. Access the automatic API documentation at `http://localhost:8000/docs`

## Testing the Endpoints

- **Fast endpoint**: `curl http://localhost:8000/fast`
- **Slow endpoint**: `curl http://localhost:8000/slow`
- **Error endpoint**: `curl http://localhost:8000/error`

## Features

- **Logging**: All endpoints include appropriate logging
- **Error handling**: The `/error` endpoint properly returns HTTP 500 status
- **Delay simulation**: The `/slow` endpoint includes a 2-second delay
- **Auto-documentation**: FastAPI automatically generates API documentation
