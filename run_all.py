import subprocess
import sys
import os
import time

PYTHON = sys.executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def start(cmd, name):
    print(f"[+] Starting {name}...")
    return subprocess.Popen(
        cmd,
        cwd=BASE_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

if __name__ == "__main__":
    processes = []

    processes.append(start(
        [PYTHON, "services/background_monitor.py"],
        "Background Monitor"
    ))

    time.sleep(1)

    processes.append(start(
        [PYTHON, "services/alert_notifier.py"],
        "Alert Notifier"
    ))

    time.sleep(1)

    processes.append(start(
        [PYTHON, "-m", "streamlit", "run", "app.py"],
        "Dashboard"
    ))

    print("\n✅ SmartCyberGuard fully started")
    print("❌ Close this window to stop everything")

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n[!] Shutting down...")
        for p in processes:
            p.terminate()
