import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("glass_production_data.csv")

features = df[
    [
        "furnace_temperature",
        "line_speed",
        "vibration_level",
        "energy_consumption",
        "cullet_ratio",
        "defect_rate",
        "surface_quality_score",
        "predicted_defect_risk"
    ]
]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

model = IsolationForest(contamination=0.04, random_state=42)
df["anomaly_pred"] = model.fit_predict(X_scaled)
df["anomaly_pred"] = df["anomaly_pred"].map({1: "normal", -1: "anomaly"})

df.to_csv("glass_analysis_results.csv", index=False)

print("Analiz tamamlandı: glass_analysis_results.csv")
print(df["anomaly_pred"].value_counts())
