import os
import joblib
import pandas as pd
import sys
# from skops.io import load

from schema.feature_schema import FEATURE_ORDER
from core.ids.rule_engine import rule_based_detection

# project_root = smart_laptop_analyzer/
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

BASE_DIR = os.path.join(PROJECT_ROOT, "models")

# model = joblib.load(os.path.join(BASE_DIR, "rf_model.pkl"))

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

model = joblib.load(resource_path("models/rf_model.pkl"))
scaler = joblib.load(resource_path("models/scaler.pkl"))

# model = load(resource_path("models/rf_model.skops"), trusted=True)
# scaler = load(resource_path("models/scaler.skops"), trusted=True)


# scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))

# Map ML output to labels
LABEL_MAP = {
    0: "normal",
    1: "possible_dos"
}

def predict_attack(features: dict, src_ip: str) -> str:
    """
    Returns: 'normal' or 'possible_dos'
    """

    # 1️⃣ RULE-BASED DETECTION (FAST + SAFE)
    rule_alert = rule_based_detection(features, src_ip)
    if rule_alert:
        return rule_alert

    # 2️⃣ ML FALLBACK (SAFE MODE)
    try:
        row = [features.get(f, 0) for f in FEATURE_ORDER]
        df = pd.DataFrame([row], columns=FEATURE_ORDER)

        df = df.fillna(0)  # safety
        scaled = scaler.transform(df)

        pred = model.predict(scaled)[0]
        return LABEL_MAP.get(pred, "normal")

    except Exception as e:
        # NEVER crash real-time IDS
        print("[ML ERROR]", e)
        return "normal"
