import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "alerts.log")

os.makedirs(LOG_DIR, exist_ok=True)

# -------------------------------------------------
# UNIFIED LOGGER (SYSTEM + IDS)
# -------------------------------------------------
def log_alert(
    alert_type: str,
    source: str = "SYSTEM",
    cpu: float = 0.0,
    ram: float = 0.0,
    disk: float = 0.0,
    battery: float = 0.0,
    src_ip: str | None = None,
    action: str | None = None,
    extra_info: str = ""
):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    parts = [ts, source, alert_type]

    if source == "SYSTEM":
        parts.extend([
            f"CPU={cpu:.1f}%",
            f"RAM={ram:.1f}%",
            f"DISK={disk:.1f}%",
            f"BATTERY={battery:.0f}%"
        ])

    if src_ip:
        parts.append(f"SRC_IP={src_ip}")

    if action:
        parts.append(f"ACTION={action}")

    if extra_info:
        parts.append(extra_info)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(" | ".join(parts) + "\n")


# -------------------------------------------------
# BACKWARD COMPATIBILITY FOR IDS
# -------------------------------------------------
def log_event(label, src_ip, action=None):
    """
    IDS legacy wrapper → calls unified logger
    """
    log_alert(
        alert_type=label,
        source="IDS",
        src_ip=src_ip,
        action=action
    )
