from fastapi import APIRouter, Query
import datetime as dt
import os
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, text

from app.services.predict_baseline import fetch_recent_usage, predict_next_24_naive
from app.services.predict_lstm import generate_lstm_prediction

ENGINE = create_engine(os.environ["DATABASE_URL"], future=True)
router = APIRouter(prefix="/api", tags=["energy"])

@router.get("/predict")
def predict_next_24(sensor_id: int = Query(1, ge=1, description="Sensor ID to forecast")):
    """
    Predict the next 24 hours of usage for the given sensor.
    Priority:
    1. LSTM model prediction (if available)
    2. Baseline repeat-last-24h fallback
    """

    # Try LSTM model first
    lstm_forecast = generate_lstm_prediction(sensor_id=sensor_id, hours_history=48, horizon=24)

    if lstm_forecast is not None:
        return {
            "sensor_id": sensor_id,
            "model": "lstm",
            "horizon_hours": 24,
            "generated_at_utc": dt.datetime.utcnow(),
            "predictions": lstm_forecast,
        }

    # Fallback: baseline
    with ENGINE.connect() as conn:
        df = fetch_recent_usage(conn, sensor_id=sensor_id, hours=48)
        preds = predict_next_24_naive(df)
        return {
            "sensor_id": sensor_id,
            "model": "baseline_repeat_last_24h",
            "horizon_hours": 24,
            "generated_at_utc": dt.datetime.utcnow(),
            "predictions": preds,
        }
