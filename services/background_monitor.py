# services/background_monitor.py
import pandas as pd
import time
import joblib
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from core.monitor import collect_system_metrics
from core.predictor import predict_system_state
from utils.logger import log_alert

# -------------------------------
# LOAD ML MODEL (SAFE)
# -------------------------------
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

model = None
try:
    model = joblib.load(MODEL_PATH)
    print("✅ ML model loaded")
except Exception:
    print("⚠️ ML model not available, using rule-based mode")

print("🚀 Unified Background Agent started")

# -------------------------------
# START IDS ENGINE
# -------------------------------
from core.ids.network_sniffer import start_sniffing
import threading

ids_thread = threading.Thread(target=start_sniffing, daemon=True)
ids_thread.start()

print("🛡️ IDS engine started")

# -------------------------------
# SYSTEM PERFORMANCE MONITOR LOOP
# -------------------------------
print("🟢 System performance monitor started")

while True:
    try:
        metrics = collect_system_metrics()

        features_df = pd.DataFrame([{
            "cpu_usage": metrics["cpu"],
            "ram_usage": metrics["ram"],
            "disk_usage": metrics["disk"],
            "disk_read": metrics["disk_read"],
            "disk_write": metrics["disk_write"],
            "battery_percent": metrics["battery"],
            "process_count": metrics["process_count"],
        }])

        pred, ml_available = predict_system_state(model, features_df)


        # 2 = Hang Risk
        if pred == 2:
            log_alert(
                alert_type="HANG_RISK",
                cpu=metrics["cpu"],
                ram=metrics["ram"],
                disk=metrics["disk"],
                battery=metrics["battery"],
                source="SYSTEM",
                extra_info="ML" if ml_available else "RULE"
            )

        time.sleep(5)

    except Exception as e:
        print("⚠️ System monitor error:", e)
        time.sleep(5)
