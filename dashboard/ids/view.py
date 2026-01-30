import streamlit as st
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(BASE_DIR, "logs", "alerts.log")

def render_ids_dashboard(refresh_interval=3, reset_logs=False):

    st_autorefresh(
        interval=refresh_interval * 1000,
        key="ids_refresh"
    )

    st.header("🛡️ Cyber-Guard IDPS Dashboard")
    st.caption("Real-Time Intrusion Detection & Prevention")

    if reset_logs:
        open(LOG_FILE, "w").close()
        st.success("Monitoring reset successfully")

    if not os.path.exists(LOG_FILE):
        st.info("No IDS logs found")
        return

    rows = []

    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            try:
                # Only IDS logs
                if "| IDS |" not in line:
                    continue

                parts = [p.strip() for p in line.split("|")]

                time = parts[0]
                label = parts[2]

                src_ip = ""
                action = ""

                for p in parts:
                    if p.startswith("SRC_IP="):
                        src_ip = p.replace("SRC_IP=", "")
                    if p.startswith("ACTION="):
                        action = p.replace("ACTION=", "")

                rows.append([time, label, src_ip, action])

            except:
                pass

    df = pd.DataFrame(rows, columns=["time", "label", "src_ip", "action"])

    # ---------------- METRICS ----------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📦 Packets", len(df))

    c2.metric(
        "⚠️ Alerts",
        len(df[df.label != "normal"])
    )

    c3.metric(
        "⛔ Blocked IPs",
        df[df.action == "BLOCKED"].src_ip.nunique()
    )

    c4.metric(
        "🌍 Unique IPs",
        df.src_ip.nunique()
    )


    st.subheader("🚨 Live Events")

    def highlight(row):
        if row["action"] == "BLOCKED":
            return ["background-color:#ff4b4b"] * 4
        if row["label"] != "normal":
            return ["background-color:#ffcccc"] * 4
        return [""] * 4

    st.dataframe(
        df.tail(50).style.apply(highlight, axis=1),
        use_container_width=True,
        height=450
    )
