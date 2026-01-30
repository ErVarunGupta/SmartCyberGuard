import time
import os
import winsound
from plyer import notification

LOG_FILE = "logs/alerts.log"

CRITICAL_ALERT_KEYWORDS = [
    "HANG",
    "HANG_RISK",
    "INTRUSION",
    "DOS",
    "ATTACK",
    "BLOCKED"
]

def is_critical_alert(log_line: str) -> bool:
    log_upper = log_line.upper()
    return any(keyword in log_upper for keyword in CRITICAL_ALERT_KEYWORDS)

def notify(alert_text: str):
    # Beep (short & sharp)
    winsound.Beep(1500, 700)

    # Desktop popup
    notification.notify(
        title="🚨 Smart Laptop Analyzer Alert",
        message=alert_text,
        timeout=6
    )

def watch_alerts():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if line:
                if is_critical_alert(line):
                    notify(line.strip())
            else:
                time.sleep(1)

if __name__ == "__main__":
    watch_alerts()
