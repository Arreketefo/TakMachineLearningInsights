import logging
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import settings
from .schemas import CoTEvent, CoTResponse
from .auth import get_api_key
from .ml_processor import MLProcessor

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML processor
ml_processor = MLProcessor()

@app.get("/")
async def root():
    """Root endpoint that returns basic API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/v1/process_cot", response_model=CoTResponse)
async def process_cot(
    event: CoTEvent,
    api_key: str = Security(get_api_key)
):
    """Process a CoT event and detect anomalies"""
    try:
        # Process the CoT event
        logger.info(f"Processing CoT event: {event.event_id}")

        # Extract features and detect anomalies
        result = ml_processor.process_event(event)

        # Create enriched response
        response = CoTResponse(
            event_id=event.event_id,
            is_anomaly=result["is_anomaly"],
            anomaly_score=result["anomaly_score"],
            enriched_cot=result["enriched_cot"]
        )

        logger.info(f"Successfully processed event {event.event_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing CoT event: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))