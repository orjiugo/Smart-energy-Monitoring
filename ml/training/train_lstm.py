# ml/train_lstm.py
"""
LSTM model training for IoT-Enabled Smart Energy Monitoring
Author: Rosemary Chiamaka Orjiugo
"""

import os
import pandas as pd
import numpy as np
import psycopg2
from sqlalchemy import create_engine, text
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib

# -----------------------------
# 1️⃣ Connect to PostgreSQL
# -----------------------------
db_url = os.environ.get("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL environment variable not found.")

print("Connecting to database...")
engine = create_engine(db_url)
query = "SELECT sensor_id, timestamp, usage FROM energy_usage ORDER BY timestamp ASC;"
df = pd.read_sql(query, engine)

print(f"Loaded {len(df)} rows from energy_usage")

# -----------------------------
# 2️⃣ Data Preprocessing
# -----------------------------
# Ensure timestamps are datetime and sort by time
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Pick one sensor for training first (e.g., sensor 1)
sensor_id = 1
sensor_df = df[df["sensor_id"] == sensor_id].copy()
sensor_df = sensor_df.set_index("timestamp").resample("H").mean().interpolate()

values = sensor_df["usage"].values.reshape(-1, 1)

scaler = MinMaxScaler()
scaled = scaler.fit_transform(values)

# Save scaler for later
os.makedirs("ml/models", exist_ok=True)
joblib.dump(scaler, "ml/models/scaler.pkl")

# -----------------------------
# 3️⃣ Sequence Generation
# -----------------------------
def create_sequences(data, seq_len=24):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

SEQ_LEN = 24
X, y = create_sequences(scaled, SEQ_LEN)

print(f"Training samples: {X.shape[0]}")

# -----------------------------
# 4️⃣ LSTM Model
# -----------------------------
model = Sequential([
    LSTM(64, input_shape=(SEQ_LEN, 1), return_sequences=False),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")

# -----------------------------
# 5️⃣ Train Model
# -----------------------------
early_stop = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)

history = model.fit(
    X, y,
    epochs=50,
    batch_size=32,
    verbose=1,
    callbacks=[early_stop]
)

# -----------------------------
# 6️⃣ Save Model
# -----------------------------
model.save("ml/models/lstm_model.h5")
print("✅ Model trained and saved successfully at ml/models/lstm_model.h5")

# -----------------------------
# 7️⃣ Optional: Save metrics
# -----------------------------
final_loss = history.history['loss'][-1]
metrics = {"final_loss": float(final_loss), "samples": len(df)}
pd.DataFrame([metrics]).to_json("ml/reports/metrics.json", orient="records", indent=4)

print(f"Final training loss: {final_loss:.4f}")
