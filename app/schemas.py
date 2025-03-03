from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class CoTEvent(BaseModel):
    event_id: str = Field(..., description="Unique identifier for the CoT event")
    type: str = Field(..., description="Type of the CoT event")
    time: datetime = Field(..., description="Timestamp of the event")
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    speed: Optional[float] = Field(None, description="Speed in m/s")
    course: Optional[float] = Field(None, description="Course in degrees")
    additional_data: Optional[Dict] = Field(default={}, description="Additional CoT data")

class CoTResponse(BaseModel):
    event_id: str
    is_anomaly: bool
    anomaly_score: float
    enriched_cot: Dict
