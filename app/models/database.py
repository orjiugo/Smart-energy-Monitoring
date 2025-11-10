"""SQLAlchemy ORM models for database tables"""
from sqlalchemy import Column, Integer, Float, DateTime, String, Index
from sqlalchemy.sql import func
from app.db.base import Base

class EnergyReading(Base):
    __tablename__ = "energy_readings"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    energy_consumption = Column(Float, nullable=False)
    power = Column(Float, nullable=False)
    temperature = Column(Float, nullable=True)
    is_anomaly = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (
        Index('idx_sensor_timestamp', 'sensor_id', 'timestamp'),
        Index('idx_timestamp', 'timestamp'),
    )

class EnergyPrediction(Base):
    __tablename__ = "energy_predictions"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String(50), nullable=False, index=True)
    prediction_timestamp = Column(DateTime(timezone=True), nullable=False)
    predicted_consumption = Column(Float, nullable=False)
    actual_consumption = Column(Float, nullable=True)
    confidence_interval_lower = Column(Float, nullable=True)
    confidence_interval_upper = Column(Float, nullable=True)
    model_version = Column(String(50), default="1.0.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (Index('idx_pred_sensor_timestamp', 'sensor_id', 'prediction_timestamp'),)