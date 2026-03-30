from core.database.database import *
from core.system.system_info import *

def log_system_data():
    data = collect_system_metrics()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO metrics (cpu, ram, disk, battery)
    VALUES (?, ?, ?, ?)
    """, (data["cpu"], data["ram"], data["disk"], data["battery"]))

    conn.commit()
    conn.close()