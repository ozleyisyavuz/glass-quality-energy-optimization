import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n = 1000
start_time = datetime.now()

timestamps = [start_time + timedelta(minutes=i) for i in range(n)]

furnace_temperature = np.random.normal(1450, 20, n)
line_speed = np.random.normal(100, 5, n)
vibration_level = np.random.normal(2.0, 0.3, n)
energy_consumption = np.random.normal(500, 30, n)
cullet_ratio = np.random.normal(25, 4, n)
defect_rate = np.random.normal(2.5, 0.5, n)
surface_quality_score = np.random.normal(92, 3, n)

anomaly_indices = np.random.choice(n, size=40, replace=False)

furnace_temperature[anomaly_indices] += np.random.uniform(30, 60, size=40)
vibration_level[anomaly_indices] += np.random.uniform(0.8, 1.5, size=40)
energy_consumption[anomaly_indices] += np.random.uniform(40, 90, size=40)
defect_rate[anomaly_indices] += np.random.uniform(1.5, 4.0, size=40)
surface_quality_score[anomaly_indices] -= np.random.uniform(5, 12, size=40)

predicted_defect_risk = (
    (furnace_temperature - 1450) * 0.05 +
    (vibration_level - 2.0) * 8 +
    (energy_consumption - 500) * 0.03 +
    (defect_rate - 2.5) * 10 -
    (surface_quality_score - 92) * 1.2
)

predicted_defect_risk = np.clip(predicted_defect_risk, 0, 100)

recommended_action = []

for i in range(n):
    if predicted_defect_risk[i] > 70:
        recommended_action.append("Reduce furnace temperature and inspect line vibration")
    elif predicted_defect_risk[i] > 50:
        recommended_action.append("Optimize cullet ratio and monitor quality")
    else:
        recommended_action.append("System operating in normal range")

df = pd.DataFrame({
    "timestamp": timestamps,
    "furnace_temperature": furnace_temperature,
    "line_speed": line_speed,
    "vibration_level": vibration_level,
    "energy_consumption": energy_consumption,
    "cullet_ratio": cullet_ratio,
    "defect_rate": defect_rate,
    "surface_quality_score": surface_quality_score,
    "predicted_defect_risk": predicted_defect_risk,
    "recommended_action": recommended_action
})

df.to_csv("glass_production_data.csv", index=False)
print("Veri oluşturuldu: glass_production_data.csv")
