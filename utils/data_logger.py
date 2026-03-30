import csv
import os

FILE_PATH = "data/system_logs.csv"

def log_system_data(metrics):
    file_exists = os.path.isfile(FILE_PATH)

    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "cpu", "ram", "disk", "battery",
                "disk_read", "disk_write", "process_count"
            ])

        writer.writerow([
            metrics["cpu"],
            metrics["ram"],
            metrics["disk"],
            metrics["battery"],
            metrics["disk_read"],
            metrics["disk_write"],
            metrics["process_count"]
        ])