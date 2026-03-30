from sklearn.ensemble import IsolationForest
import pandas as pd
import joblib

df = pd.read_csv("data/system_data.csv")

model = IsolationForest(contamination=0.05)
model.fit(df)

joblib.dump(model, "models/anomaly_model.pkl")