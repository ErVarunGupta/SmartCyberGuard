# core/monitor.py

import psutil


def collect_system_metrics():
    """
    Collects real-time system metrics
    Returns a dictionary
    """

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    disk_io = psutil.disk_io_counters()
    battery = psutil.sensors_battery()

    battery_pct = battery.percent if battery else -1
    process_count = len(list(psutil.process_iter()))

    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "disk_read": disk_io.read_bytes,
        "disk_write": disk_io.write_bytes,
        "battery": battery_pct,
        "process_count": process_count
    }

