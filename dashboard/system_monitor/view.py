import streamlit as st
import joblib
import pandas as pd
import os
import time

from core.monitor import collect_system_metrics
from core.predictor import predict_system_state
from core.health import calculate_health_score
from core.mitigation import get_auto_mitigation_suggestions

from dashboard.components.metrics import render_metrics
from dashboard.components.tables import get_top_heavy_processes, render_resource_table
from dashboard.components.alerts import render_alerts
from dashboard.components.sidebar import load_sidebar_settings
from utils.logger import log_alert

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
SETTINGS_PATH = os.path.join(BASE_DIR, "config", "settings.json")

LABEL_MAP = {
    0: "🟢 Normal",
    1: "🟡 High Load",
    2: "🔴 Hang Risk"
}

# -------------------------------------------------
# MAIN RENDER FUNCTION
# -------------------------------------------------
def render_system_monitor(refresh_interval=5):

    st.header("💻 System Performance Monitor")

    # Sidebar settings (already loaded once)
    settings = load_sidebar_settings(SETTINGS_PATH)

    # Load ML model once
    model = None
    try:
        model = joblib.load(MODEL_PATH)
    except:
        st.warning("⚠️ ML model not available, using rule-based prediction")

    # 🔥 IMPORTANT: PLACEHOLDER (NO FLICKER)
    placeholder = st.empty()

    # -------------------------------------------------
    # LOOP (CONTROLLED REFRESH)
    # -------------------------------------------------
    while True:
        with placeholder.container():

            # 1️⃣ Collect metrics
            metrics = collect_system_metrics()

            cpu = metrics["cpu"]
            ram = metrics["ram"]
            disk = metrics["disk"]
            battery = metrics["battery"]
            process_count = metrics["process_count"]

            # 2️⃣ Heavy processes (ONLY ONCE)
            heavy_df = get_top_heavy_processes()
            heavy_process_count = len(heavy_df)

            # 3️⃣ Feature vector
            features = pd.DataFrame([{
                "cpu_usage": cpu,
                "ram_usage": ram,
                "disk_usage": disk,
                "disk_read": metrics["disk_read"],
                "disk_write": metrics["disk_write"],
                "battery_percent": battery,
                "process_count": process_count,
                "heavy_process_count": heavy_process_count
            }])

            # 4️⃣ Prediction
            pred, ml_available = predict_system_state(model, features)
            state = LABEL_MAP[pred]

            # 5️⃣ Health score
            health_score, health_label = calculate_health_score(
                cpu, ram, disk, pred
            )

            # 6️⃣ UI METRICS
            render_metrics(cpu, ram, disk, battery)

            st.markdown(f"### Current State: **{state}**")
            st.markdown(
                f"""
                ### 🧠 System Health Score  
                **{health_score}/100 — {health_label}**
                """
            )

            # 7️⃣ Alerts
            render_alerts(
                pred=pred,
                hang_alert_enabled=settings["hang_alert_enabled"],
                alert_interval=settings["alert_interval"],
                show_xai=False
            )

            # 8️⃣ Log alerts (background audit)
            if pred == 2 and settings["hang_alert_enabled"]:
                log_alert(
                    alert_type="HANG_RISK",
                    cpu=cpu,
                    ram=ram,
                    disk=disk,
                    battery=battery,
                    extra_info="ML" if ml_available else "RULE"
                )

            # 9️⃣ Recommendations
            st.subheader("🛠️ Recommended Actions")
            for s in get_auto_mitigation_suggestions(cpu, ram, disk, pred, battery):
                st.write(f"• {s}")

            # 🔟 Resource table (ONLY ONE)
            render_resource_table(heavy_df)

        # ⏱️ CONTROLLED REFRESH (NO PAGE RELOAD)
        time.sleep(refresh_interval)
