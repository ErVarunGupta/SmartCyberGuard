import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


st.set_page_config(
    page_title="Smart System & Security Monitor",
    layout="wide"
)

st.title("🚀 Smart Laptop Analyzer + Cyber Guard")

# -------------------------------------------------
# GLOBAL SIDEBAR
# -------------------------------------------------
st.sidebar.header("⚙️ Controls")

active_tab = st.sidebar.radio(
    "Select Module",
    ["💻 System Monitor", "🛡️ Intrusion Detection"]
)

# Default values
sys_refresh = None
ids_refresh = None
ids_reset = False

# ---------------- SYSTEM MONITOR CONTROLS ----------------
if active_tab == "💻 System Monitor":
    st.sidebar.subheader("💻 System Monitor Settings")

    sys_refresh = st.sidebar.slider(
        "Refresh System Monitor (sec)",
        min_value=3,
        max_value=30,
        value=5,
        step=1
    )

# ---------------- IDS CONTROLS ----------------
elif active_tab == "🛡️ Intrusion Detection":
    st.sidebar.subheader("🛡️ IDS Settings")

    ids_refresh = st.sidebar.slider(
        "Refresh IDS Dashboard (sec)",
        min_value=1,
        max_value=10,
        value=3,
        step=1
    )

    ids_reset = st.sidebar.button("🔄 Reset Monitoring")

# -------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------
if active_tab == "💻 System Monitor":
    from dashboard.system_monitor.view import render_system_monitor
    render_system_monitor(refresh_interval=sys_refresh)

elif active_tab == "🛡️ Intrusion Detection":
    from dashboard.ids.view import render_ids_dashboard
    render_ids_dashboard(
        refresh_interval=ids_refresh,
        reset_logs=ids_reset
    )
