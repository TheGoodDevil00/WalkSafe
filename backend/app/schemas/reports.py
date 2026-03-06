from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    user_hash: str
    lat: float
    lon: float
    incident_type: str
    description: Optional[str] = None

class ReportResponse(ReportCreate):
    id: int
    confidence_score: float
    timestamp: datetime
