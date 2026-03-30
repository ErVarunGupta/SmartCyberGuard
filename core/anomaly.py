import joblib

model = joblib.load("models/anomaly_model.pkl")

def detect(data):
    return model.predict([data])[0]