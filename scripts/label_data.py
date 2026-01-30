import pandas as pd
import os

# Path handling (safe)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "system_data.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "system_data_labeled.csv")

# Load dataset
df = pd.read_csv(DATA_FILE)

# Labeling function
def assign_label(row):
    cpu = row["cpu_usage"]
    ram = row["ram_usage"]

    if cpu < 60 and ram < 70:
        return 0  # Normal
    elif (60 <= cpu <= 85) or (70 <= ram <= 85):
        return 1  # High Load
    else:
        return 2  # Hang Risk

# Apply labeling
df["label"] = df.apply(assign_label, axis=1)

# Save labeled dataset
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Dataset labeled successfully!")
print(df["label"].value_counts())
