import psutil
import joblib
import time
import os
import numpy as np
import pandas as pd
from collections import defaultdict

# Path handling
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

# Load trained model
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully")

# Label mapping
LABEL_MAP = {
    0: "🟢 Normal",
    1: "🟡 High Load",
    2: "🔴 Hang Risk"
}

print("⚡ Real-time system monitoring started... Press CTRL+C to stop.\n")

def get_top_heavy_processes(limit=3):
    ignore_processes = {
        "System Idle Process",
        "System",
        "Registry",
        "Idle"
    }

    proc_usage = []
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
        try:
            name = proc.info['name']
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_percent']

            if (
                name not in ignore_processes
                and cpu is not None
                and cpu > 1
            ):
                proc_usage.append((name, cpu, mem))
        except:
            pass

    proc_usage.sort(key=lambda x: x[1], reverse=True)
    return proc_usage[:limit]


try:
    while True:
        # Collect live system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        disk_io = psutil.disk_io_counters()
        disk_read = disk_io.read_bytes
        disk_write = disk_io.write_bytes

        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else -1

        processes = list(psutil.process_iter())
        process_count = len(processes)

        heavy_process_count = 0
        for proc in processes:
            try:
                if proc.cpu_percent(interval=0.1) > 10:
                    heavy_process_count += 1
            except:
                pass

        # Prepare input for model
        features = pd.DataFrame([{
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "disk_usage": disk_usage,
            "disk_read": disk_read,
            "disk_write": disk_write,
            "battery_percent": battery_percent,
            "process_count": process_count,
            "heavy_process_count": heavy_process_count
        }])

        # Prediction
        prediction = model.predict(features)[0]
        state = LABEL_MAP[prediction]

        print(
            f"CPU:{cpu_usage:5.1f}% | "
            f"RAM:{ram_usage:5.1f}% | "
            f"DISK:{disk_usage:5.1f}% | "
            f"STATE: {state}"
        )

        # SMART ALERTS & RECOMMENDATIONS
        if prediction == 1:  # High Load
            print("⚠️  Recommendation: System under high load.")
            heavy_apps = get_top_heavy_processes()
            for name, cpu, mem in heavy_apps:
                print(f"   🔧 Consider closing: {name} (CPU {cpu:.1f}%, RAM {mem:.1f}%)")

        elif prediction == 2:  # Hang Risk
            print("🚨 ALERT: High risk of system hang!")
            print("   🔴 Suggested actions:")
            print("   - Save your work immediately")
            print("   - Close heavy applications")
            print("   - Restart system if needed")


        time.sleep(5)

except KeyboardInterrupt:
    print("\n⛔ Real-time monitoring stopped.")
