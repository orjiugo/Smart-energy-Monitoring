import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy import text
from typing import Dict, List

def fetch_recent_usage(conn, sensor_id: int, hours: int = 48) -> pd.DataFrame:
    """
    Fetch the most recent readings for a sensor from the database.
    """
    sql = text("""
        SELECT timestamp, usage
        FROM energy_usage
        WHERE sensor_id = :sid
          AND timestamp >= (NOW() AT TIME ZONE 'UTC' - INTERVAL :hrs)
        ORDER BY timestamp
    """)
    rows = conn.execute(sql, {"sid": sensor_id, "hrs": f"{hours} hours"}).mappings().all()
    if not rows:
        return pd.DataFrame(columns=["timestamp", "usage"])
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df.set_index("timestamp").asfreq("H").interpolate()

def predict_next_24_naive(df: pd.DataFrame) -> List[Dict]:
    """
    Predict the next 24 hours of usage using a simple rule:
    Repeat the pattern from the last 24 hours.
    """
    now_utc = pd.Timestamp.utcnow().floor("H")
    future_index = pd.date_range(now_utc + pd.Timedelta(hours=1), periods=24, freq="H")

    if len(df) >= 24:
        last24 = df["usage"].iloc[-24:].to_numpy()
        forecast = last24  # simple repeat of last 24 hours
    else:
        mean_val = float(df["usage"].mean()) if len(df) else 60.0
        forecast = np.full(24, mean_val)

    return [
        {"timestamp": ts.to_pydatetime(), "predicted_usage": float(val)}
        for ts, val in zip(future_index, forecast)
    ]
