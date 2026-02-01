# -*- coding: utf-8 -*-
"""
Intrusion Detection System - Corrected & Production Ready
Compatible with latest pandas & sklearn
"""

import os
import time
import joblib
from skops.io import dump
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# FILE PATHS
# =========================
DATA_PATH = "data/kddcup.data_10_percent.gz"
NAMES_PATH = "data/kddcup.names"
ATTACK_PATH = "data/training_attack_types"

# =========================
# LOAD FEATURE NAMES
# =========================
with open(NAMES_PATH, "r") as f:
    print(f.read())

cols = """duration,protocol_type,service,flag,src_bytes,dst_bytes,land,
wrong_fragment,urgent,hot,num_failed_logins,logged_in,num_compromised,
root_shell,su_attempted,num_root,num_file_creations,num_shells,
num_access_files,num_outbound_cmds,is_host_login,is_guest_login,count,
srv_count,serror_rate,srv_serror_rate,rerror_rate,srv_rerror_rate,
same_srv_rate,diff_srv_rate,srv_diff_host_rate,dst_host_count,
dst_host_srv_count,dst_host_same_srv_rate,dst_host_diff_srv_rate,
dst_host_same_src_port_rate,dst_host_srv_diff_host_rate,
dst_host_serror_rate,dst_host_srv_serror_rate,dst_host_rerror_rate,
dst_host_srv_rerror_rate"""

columns = [c.strip() for c in cols.split(",")]
columns.append("target")

print("Total columns:", len(columns))

# =========================
# ATTACK MAPPING
# =========================
with open(ATTACK_PATH, "r") as f:
    print(f.read())

attack_map = {
    "normal": "normal",
    "back": "dos", "land": "dos", "neptune": "dos", "pod": "dos",
    "smurf": "dos", "teardrop": "dos",
    "ipsweep": "probe", "nmap": "probe", "portsweep": "probe", "satan": "probe",
    "ftp_write": "r2l", "guess_passwd": "r2l", "imap": "r2l",
    "multihop": "r2l", "phf": "r2l", "spy": "r2l",
    "warezclient": "r2l", "warezmaster": "r2l",
    "buffer_overflow": "u2r", "loadmodule": "u2r",
    "perl": "u2r", "rootkit": "u2r"
}

# =========================
# LOAD DATASET (GZIP SAFE)
# =========================
df = pd.read_csv(
    DATA_PATH,
    names=columns,
    compression="gzip",
    header=None
)

print("Dataset shape:", df.shape)

# =========================
# TARGET LABEL
# =========================
df["Attack Type"] = df["target"].apply(lambda x: attack_map[x.rstrip(".")])

# =========================
# CLEANING
# =========================
df = df.dropna(axis=1)
df = df.loc[:, df.nunique() > 1]

# =========================
# CORRELATION (NUMERIC ONLY)
# =========================
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

plt.figure(figsize=(14, 10))
sns.heatmap(corr, cmap="coolwarm")
plt.title("Feature Correlation Heatmap")
plt.show()

# =========================
# DROP HIGHLY CORRELATED FEATURES
# =========================
drop_cols = [
    "num_root",
    "srv_serror_rate",
    "srv_rerror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
    "dst_host_same_srv_rate"
]

df.drop(columns=[c for c in drop_cols if c in df.columns], inplace=True)

# =========================
# ENCODING
# =========================
protocol_map = {"icmp": 0, "tcp": 1, "udp": 2}
flag_map = {
    "SF": 0, "S0": 1, "REJ": 2, "RSTR": 3, "RSTO": 4,
    "SH": 5, "S1": 6, "S2": 7, "RSTOS0": 8, "S3": 9, "OTH": 10
}

df["protocol_type"] = df["protocol_type"].map(protocol_map)
df["flag"] = df["flag"].map(flag_map)

df.drop(columns=["service", "target"], inplace=True)

# =========================
# MODELING
# =========================
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

X = df.drop("Attack Type", axis=1)
y = df["Attack Type"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.33, random_state=42
)

model = RandomForestClassifier(n_estimators=30, random_state=42)

start = time.time()
model.fit(X_train, y_train)
print("Training time:", time.time() - start)

print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))

# =========================
# SAVE MODEL
# =========================
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/rf_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

os.makedirs("models", exist_ok=True)

dump(model, "models/rf_model.skops")
dump(scaler, "models/scaler.skops")

print("✅ Model & Scaler saved using skops")

print("✅ Model & Scaler saved successfully")
