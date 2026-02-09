import os
import sys

# ✅ Add project root to PYTHONPATH
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from core.monitor import collect_system_metrics
import joblib
import pandas as pd

# Load model
model = joblib.load("models/model.pkl")

print("Model expects:", model.n_features_in_)
print("Feature names:", model.feature_names_in_)

# Collect metrics
metrics = collect_system_metrics()
print("Raw metrics:", metrics)

# Build feature row (TEMP – just for test)
row = {
    "cpu_usage": metrics.get("cpu", 0),
    "ram_usage": metrics.get("ram", 0),
    "disk_usage": metrics.get("disk", 0),
    "disk_read": metrics.get("disk_read", 0),
    "disk_write": metrics.get("disk_write", 0),
    "battery_percent": metrics.get("battery", 0),
    "process_count": metrics.get("process_count", 0),
    "heavy_process_count": 0  # TEMP placeholder
}

df = pd.DataFrame([row])
print("DF columns:", df.columns.tolist())

# Try prediction
pred = model.predict(df)[0]
print("Prediction:", pred)
