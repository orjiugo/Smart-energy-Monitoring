"""General utility functions"""
from datetime import datetime, timedelta
import numpy as np

def generate_time_range(start: datetime, end: datetime, interval_seconds: int):
    current = start
    while current <= end:
        yield current
        current += timedelta(seconds=interval_seconds)

def calculate_statistics(values: list) -> dict:
    if not values:
        return {"mean": 0, "std": 0, "min": 0, "max": 0}
    arr = np.array(values)
    return {
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }