import psutil
import pandas as pd
import time
import os
from datetime import datetime

# Output CSV file
DATA_FILE = "data/system_data.csv"

# Create CSV with header if not exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "timestamp",
        "cpu_usage",
        "ram_usage",
        "disk_usage",
        "disk_read",
        "disk_write",
        "battery_percent",
        "process_count",
        "heavy_process_count"
    ])
    df.to_csv(DATA_FILE, index=False)

print("📊 System data collection started... Press CTRL+C to stop.")

# Previous disk IO (for per-second calculation)
prev_disk = psutil.disk_io_counters()

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cpu_usage = psutil.cpu_percent(interval=1)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Disk IO calculation
        current_disk = psutil.disk_io_counters()
        disk_read = current_disk.read_bytes - prev_disk.read_bytes
        disk_write = current_disk.write_bytes - prev_disk.write_bytes
        prev_disk = current_disk

        # Battery (handle desktop case)
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else -1

        # Process info
        processes = list(psutil.process_iter())
        process_count = len(processes)

        heavy_process_count = 0
        for proc in processes:
            try:
                if proc.cpu_percent(interval=0.1) > 10:
                    heavy_process_count += 1
            except:
                pass

        # Append data
        row = {
            "timestamp": timestamp,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "disk_usage": disk_usage,
            "disk_read": disk_read,
            "disk_write": disk_write,
            "battery_percent": battery_percent,
            "process_count": process_count,
            "heavy_process_count": heavy_process_count
        }

        df = pd.DataFrame([row])
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)

        print(f"[{timestamp}] CPU:{cpu_usage}% RAM:{ram_usage}% DISK:{disk_usage}%")

        time.sleep(5)

except KeyboardInterrupt:
    print("\n⛔ Data collection stopped by user.")
