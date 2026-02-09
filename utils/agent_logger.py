import os
import datetime

LOG_FILE = os.path.join(os.environ.get("TEMP", "."), "smartcyberguard_agent.log")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")
