# scripts/retrain_model.py

import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------------------------------------------------
# PATHS
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "system_data_labeled.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
BACKUP_MODEL_PATH = os.path.join(BASE_DIR, "models", "model_backup.pkl")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
print("📥 Loading latest dataset...")
df = pd.read_csv(DATA_PATH)

FEATURES = [
    "cpu_usage",
    "ram_usage",
    "disk_usage",
    "disk_read",
    "disk_write",
    "battery_percent",
    "process_count",
    "heavy_process_count"
]

TARGET = "label"

X = df[FEATURES]
y = df[TARGET]

# -------------------------------------------------
# TRAIN / TEST SPLIT
# -------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------------------------
# TRAIN MODEL
# -------------------------------------------------
print("🤖 Retraining model...")
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# -------------------------------------------------
# EVALUATION
# -------------------------------------------------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"🎯 New model accuracy: {acc * 100:.2f}%")

# -------------------------------------------------
# SAFE REPLACEMENT
# -------------------------------------------------
if acc >= 0.85:
    if os.path.exists(MODEL_PATH):
        os.replace(MODEL_PATH, BACKUP_MODEL_PATH)

    joblib.dump(model, MODEL_PATH)
    print("✅ Model updated successfully")
else:
    print("❌ Accuracy too low. Model not replaced.")
