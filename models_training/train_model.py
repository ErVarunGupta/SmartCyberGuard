import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Path handling
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "system_data_labeled.csv")

# Load dataset
df = pd.read_csv(DATA_FILE)

# Features and target
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

X = df[FEATURES]
y = df["label"]

# Train-test split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("✅ Random Forest model trained successfully\n")
print(f"🎯 Accuracy: {accuracy * 100:.2f}%\n")

print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("🧩 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))



MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
joblib.dump(model, MODEL_PATH)

print(f"\n💾 Model saved successfully at: {MODEL_PATH}")