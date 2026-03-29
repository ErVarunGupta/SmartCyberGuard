from core.database import get_connection
import pandas as pd

def fetch_metrics():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 50",
        conn
    )

    conn.close()
    return df