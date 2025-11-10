# app/services/predict_lstm.py
import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

try:
    from tensorflow.keras.models import load_model
except Exception:
    # If TF isn't available at import time, the route will fall back to baseline.
    load_model = None  # type: ignore

MODEL_PATH = "ml/models/lstm_model.h5"
SCALER_PATH = "ml/models/scaler.pkl"


def _get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set")
    return create_engine(db_url, future=True)


def fetch_recent_usage_for_sensor(engine, sensor_id: int, hours: int = 48) -> pd.DataFrame:
    """SQLAlchemy 2.x compatible fetch using a connection + text()."""
    start = datetime.utcnow() - timedelta(hours=hours)

    sql = text("""
        SELECT timestamp, usage
        FROM energy_usage
        WHERE sensor_id = :sid
          AND timestamp >= :start
        ORDER BY timestamp ASC
    """)

    with engine.connect() as conn:
        rows = conn.execute(sql, {"sid": sensor_id, "start": start}).mappings().all()

    if not rows:
        return pd.DataFrame(columns=["timestamp", "usage"])

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def _load_scaler(y: np.ndarray):
    """Load a saved scaler if present, else fit a simple MinMax scaler inline."""
    scaler = None
    if os.path.exists(SCALER_PATH):
        try:
            with open(SCALER_PATH, "rb") as f:
                scaler = pickle.load(f)
        except Exception:
            scaler = None

    if scaler is None:
        # Minimal embedded scaler
        class _MinMax:
            def fit(self, a): 
                self.mi = float(np.min(a)); self.ma = float(np.max(a) + 1e-9)
            def transform(self, a): 
                return (a - self.mi) / (self.ma - self.mi)
            def inverse_transform(self, a): 
                return a * (self.ma - self.mi) + self.mi
        scaler = _MinMax()
        scaler.fit(y.reshape(-1, 1))
    return scaler


def _recursive_forecast(model, history_norm: np.ndarray, horizon: int, scaler) -> List[float]:
    """
    history_norm: shape (history, 1), already normalized.
    Returns list of denormalized predictions (len=horizon).
    """
    window = history_norm.copy().reshape(1, history_norm.shape[0], 1)
    preds = []
    for _ in range(horizon):
        yhat = model.predict(window, verbose=0)  # shape (1, 1) or (1, horizon) depending on model
        if yhat.ndim == 2:
            next_norm = float(yhat[0, 0])
        else:
            next_norm = float(yhat.squeeze())
        preds.append(next_norm)
        # slide window
        window = np.concatenate([window[:, 1:, :], np.array(next_norm).reshape(1, 1, 1)], axis=1)
    # inverse scale
    preds = np.array(preds).reshape(-1, 1)
    preds = scaler.inverse_transform(preds).ravel().tolist()
    return preds


def generate_lstm_prediction(sensor_id: int, hours_history: int = 48, horizon: int = 24) -> Optional[List[Dict]]:
    """
    Load the last `hours_history` points for `sensor_id`, normalize, run LSTM recursively,
    and return list of {timestamp, prediction}.
    Returns None if model cannot be used (caller should fall back).
    """
    if load_model is None or not os.path.exists(MODEL_PATH):
        # TensorFlow not importable or no model file
        return None

    engine = _get_engine()
    df = fetch_recent_usage_for_sensor(engine, sensor_id, hours_history)

    if df.empty or len(df) < hours_history:
        return None

    # Prepare series
    y = df["usage"].astype(float).values
    scaler = _load_scaler(y)
    y_norm = scaler.transform(y.reshape(-1, 1)).reshape(-1, 1)  # (n,1)

    history_norm = y_norm[-hours_history:]  # (history,1)

    # Load model
    try:
        model = load_model(MODEL_PATH)
    except Exception:
        return None

    # Forecast horizon recursively
    preds = _recursive_forecast(model, history_norm, horizon, scaler)

    # Build timestamps for next 24 hours
    last_ts = pd.to_datetime(df["timestamp"].iloc[-1])
    future_ts = [last_ts + timedelta(hours=i + 1) for i in range(horizon)]

    out = [{"timestamp": ts.isoformat(), "prediction": float(p)} for ts, p in zip(future_ts, preds)]
    return out
