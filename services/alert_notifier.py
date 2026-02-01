import time
import os
import winsound
from plyer import notification

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "alerts.log")


def beep():
    winsound.Beep(2000, 400)
    winsound.Beep(1800, 300)


def notify(msg):
    notification.notify(
        title="🚨 Smart Cyber Guard Alert",
        message=msg,
        timeout=5
    )
    beep()


def watch_alerts():
    if not os.path.exists(LOG_FILE):
        return

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        f.seek(0, os.SEEK_END)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue

            line_lower = line.lower()

            # 🔥 robust trigger
            if "possible_dos" in line_lower or "hang_risk" in line_lower:
                notify(line.strip())


if __name__ == "__main__":
    watch_alerts()
