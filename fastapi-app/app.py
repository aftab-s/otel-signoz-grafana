from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import time
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI Service", description="A simple FastAPI service with different endpoints")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the FastAPI service"}

@app.get("/fast")
async def fast_endpoint():
    """A quick, successful response"""
    logger.info("Fast endpoint called")
    return {"message": "This is a fast response", "status": "success"}

@app.get("/slow")
async def slow_endpoint():
    """A response with a 2-second delay"""
    logger.info("Slow endpoint called - starting delay")
    time.sleep(2)  # 2-second delay
    logger.info("Slow endpoint - delay completed")
    return {"message": "This is a slow response after 2 seconds", "status": "success"}

@app.get("/error")
async def error_endpoint():
    """Returns a 500 status code and logs an error"""
    logger.error("Error endpoint called - simulating server error")
    raise HTTPException(status_code=500, detail="Internal Server Error - This is a simulated error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
