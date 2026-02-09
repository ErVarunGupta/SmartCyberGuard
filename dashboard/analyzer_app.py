import os
import sys
import time
import threading
import streamlit as st
import pandas as pd
import joblib

# ===============================
# PROJECT ROOT (IMPORT SAFE)
# ===============================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ===============================
# PROJECT IMPORTS
# ===============================
from core.monitor import collect_system_metrics
from core.ids.network_sniffer import start_sniffing
from utils.logger import log_alert

# ===============================
# STREAMLIT CONFIG
# ===============================
st.set_page_config(
    page_title="SmartCyberGuard",
    layout="wide"
)

st.title("🛡️ SmartCyberGuard – Laptop Health Analyzer")

# ===============================
# LOAD ML MODEL (SAFE)
# ===============================
MODEL = None
MODEL_ERROR = None

try:
    MODEL = joblib.load(os.path.join(PROJECT_ROOT, "models", "model.pkl"))
except Exception as e:
    MODEL_ERROR = str(e)

# ===============================
# SHARED STATE
# ===============================
if "ids_started" not in st.session_state:
    st.session_state.ids_started = False

if "metrics" not in st.session_state:
    st.session_state.metrics = {}

# ===============================
# IDS THREAD (START ONCE)
# ===============================
def start_ids_once():
    if not st.session_state.ids_started:
        t = threading.Thread(target=start_sniffing, daemon=True)
        t.start()
        st.session_state.ids_started = True
        log_alert(
            alert_type="IDS_STARTED",
            source="UI",
            extra_info="IDS thread started from Streamlit"
        )

start_ids_once()

# ===============================
# COLLECT METRICS
# ===============================
def get_metrics():
    try:
        m = collect_system_metrics()
        return {
            "cpu_usage": m.get("cpu", 0.0),
            "ram_usage": m.get("ram", 0.0),
            "disk_usage": m.get("disk", 0.0),
            "disk_read": m.get("disk_read", 0),
            "disk_write": m.get("disk_write", 0),
            "battery_percent": m.get("battery", 0),
            "process_count": m.get("process_count", 0),
            "heavy_process_count": 0  # placeholder (future)
        }
    except Exception as e:
        log_alert(
            alert_type="METRICS_ERROR",
            source="UI",
            extra_info=str(e)
        )
        return None

# ===============================
# UI LOOP (SAFE REFRESH)
# ===============================
refresh = st.sidebar.slider(
    "Refresh interval (seconds)",
    min_value=2,
    max_value=10,
    value=5
)

placeholder = st.empty()

while True:
    data = get_metrics()

    with placeholder.container():
        if not data:
            st.error("Failed to collect system metrics")
            time.sleep(refresh)
            continue

        df = pd.DataFrame([data])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CPU %", data["cpu_usage"])
        col2.metric("RAM %", data["ram_usage"])
        col3.metric("Disk %", data["disk_usage"])
        col4.metric("Battery %", data["battery_percent"])

        st.subheader("📊 System Metrics")
        st.dataframe(df, use_container_width=True)

        st.subheader("🧠 ML Prediction")

        if MODEL_ERROR:
            st.error(f"ML model not loaded: {MODEL_ERROR}")
        else:
            try:
                pred = MODEL.predict(df)[0]
                state = {
                    0: "Normal",
                    1: "High Load",
                    2: "Hang Risk"
                }.get(pred, "Unknown")

                if pred == 2:
                    st.error(f"⚠️ {state}")
                elif pred == 1:
                    st.warning(f"⚠️ {state}")
                else:
                    st.success(f"✅ {state}")

            except Exception as e:
                st.error(f"Prediction failed: {e}")

    time.sleep(refresh)
