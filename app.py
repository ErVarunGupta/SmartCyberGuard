import streamlit as st
import sys
import os
import time

# ---------------- PATH SETUP ----------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart System & Security Monitor",
    layout="wide"
)

st.title("🚀 Smart Laptop Analyzer + Cyber Guard")

# ---------------- IMPORT CORE ----------------
from core.database import create_table, get_connection
from core.data_logger import log_system_data

# Create DB table (IMPORTANT)
create_table()


# conn = get_connection()
# cursor = conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# st.write(cursor.fetchall())
# conn.close()

# ---------------- GLOBAL LOGGING SYSTEM ----------------
# This ensures analytics always works

if "last_log_time" not in st.session_state:
    st.session_state.last_log_time = 0

# Log data every 5 seconds
if time.time() - st.session_state.last_log_time > 5:
    try:
        log_system_data()
    except Exception as e:
        st.error(f"Logging Error: {e}")
    st.session_state.last_log_time = time.time()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("⚙️ Controls")

active_tab = st.sidebar.radio(
    "Select Module",
    [
        "💻 System Monitor",
        "🛡️ Intrusion Detection",
        "🧹 Smart File Cleaner",
        "🤖 AI Assistant"   # ✅ FIXED (removed space)
    ]
)

# Default values
sys_refresh = None
ids_refresh = None
ids_reset = False

# ---------------- SYSTEM MONITOR ----------------
if active_tab == "💻 System Monitor":
    st.sidebar.subheader("💻 System Monitor Settings")

    sys_refresh = st.sidebar.slider(
        "Refresh System Monitor (sec)",
        min_value=3,
        max_value=30,
        value=5,
        step=1
    )

# ---------------- IDS ----------------
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

# 💻 SYSTEM MONITOR
if active_tab == "💻 System Monitor":
    from dashboard.system_monitor.view import render_system_monitor

    render_system_monitor(refresh_interval=sys_refresh)

# 🛡️ IDS
elif active_tab == "🛡️ Intrusion Detection":
    from dashboard.ids.view import render_ids_dashboard

    render_ids_dashboard(
        refresh_interval=ids_refresh,
        reset_logs=ids_reset
    )

# 🤖 AI ASSISTANT
elif active_tab == "🤖 AI Assistant":
    from dashboard.chatbot.view import render_chatbot

    render_chatbot()

# 🧹 FILE CLEANER
elif active_tab == "🧹 Smart File Cleaner":
    from dashboard.file_cleaner.view import render_file_cleaner

    render_file_cleaner()