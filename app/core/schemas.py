"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EnergyReadingCreate(BaseModel):
    sensor_id: str = Field(..., min_length=1, max_length=50)
    timestamp: datetime
    energy_consumption: float = Field(..., ge=0)
    power: float = Field(..., ge=0)
    temperature: Optional[float] = None
    is_anomaly: int = Field(default=0, ge=0, le=1)

class EnergyReadingResponse(BaseModel):
    id: int
    sensor_id: str
    timestamp: datetime
    energy_consumption: float
    power: float
    temperature: Optional[float]
    is_anomaly: int
    class Config:
        from_attributes = True

class PredictionResponse(BaseModel):
    sensor_id: str
    prediction_timestamp: datetime
    predicted_consumption: float
    confidence_interval_lower: Optional[float]
    confidence_interval_upper: Optional[float]
    model_version: str
    class Config:
        from_attributes = True