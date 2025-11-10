import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from app.models.energy_data import energy_usage  # If your model file is named differently, adjust this import.

async def generate_synthetic_data(db: AsyncSession, num_sensors: int = 3, days: int = 7):
    """
    Generate synthetic hourly energy usage data for the last `days` days.
    """
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    timestamps = pd.date_range(start=start_time, end=end_time, freq='H')

    records = []
    for sensor_id in range(1, num_sensors + 1):
        # day–night pattern + noise
        base_usage = 50 + 20 * np.sin(2 * np.pi * (timestamps.hour / 24))
        noise = np.random.normal(0, 5, len(timestamps))
        usage = base_usage + noise + np.random.randint(0, 10)
        for ts, val in zip(timestamps, usage):
            records.append({"sensor_id": sensor_id, "timestamp": ts, "usage": float(val)})

    await db.execute(insert(energy_usage), records)
    await db.commit()

    print(f"✅ Inserted {len(records)} records for {num_sensors} sensors.")
