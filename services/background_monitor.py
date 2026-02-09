# services/background_monitor.py
# --------------------------------
# SmartCyberGuard Background Agent
# --------------------------------

# ===== SINGLE INSTANCE (WINDOWS KERNEL MUTEX via ctypes) =====
import sys
import ctypes

kernel32 = ctypes.windll.kernel32

mutex = kernel32.CreateMutexW(
    None,
    True,   # initial owner (CRITICAL)
    "SmartCyberGuard_BackgroundMonitor"
)

ERROR_ALREADY_EXISTS = 183

if kernel32.GetLastError() == ERROR_ALREADY_EXISTS:
    sys.exit(0)

# ===== STANDARD IMPORTS =====
import os
import time
import threading
import pandas as pd
import joblib

# ===== PATH HANDLING (SOURCE + PYINSTALLER) =====
if hasattr(sys, "_MEIPASS"):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ===== PROJECT IMPORTS =====
from core.monitor import collect_system_metrics
from core.predictor import predict_system_state
from core.ids.network_sniffer import start_sniffing
from utils.logger import log_alert

# ===== RESOURCE PATH HELPER =====
def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(BASE_DIR, relative_path)

# ===== LOAD ML MODEL (FAIL-SAFE) =====
model = None
try:
    model = joblib.load(resource_path("models/model.pkl"))
    log_alert(
        alert_type="MODEL_LOADED",
        source="AGENT",
        extra_info="ML model loaded successfully"
    )
except Exception as e:
    log_alert(
        alert_type="MODEL_FALLBACK",
        source="AGENT",
        extra_info=str(e)
    )

# ===== START IDS ENGINE (DAEMON THREAD) =====
ids_thread = threading.Thread(
    target=start_sniffing,
    daemon=True
)
ids_thread.start()

log_alert(
    alert_type="IDS_STARTED",
    source="AGENT",
    extra_info="IDS engine running"
)

# ===== MAIN BACKGROUND LOOP (NEVER EXIT) =====
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

        # 2 = HANG RISK
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
        log_alert(
            alert_type="AGENT_ERROR",
            source="AGENT",
            extra_info=str(e)
        )
        time.sleep(5)
