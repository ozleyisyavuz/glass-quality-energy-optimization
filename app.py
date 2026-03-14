import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Glass Quality & Energy Optimization", layout="wide")

st.title("AI-Powered Glass Production Quality & Energy Optimization System")
st.write("Cam üretim hattı için kalite, enerji ve risk analizi dashboard'u")

csv_path = Path("glass_analysis_results.csv")

if not csv_path.exists():
    st.error("glass_analysis_results.csv bulunamadı. Önce quality_energy_analysis.py çalıştırılmalı.")
    st.stop()

df = pd.read_csv(csv_path)
df["timestamp"] = pd.to_datetime(df["timestamp"])

total_records = len(df)
anomaly_count = len(df[df["anomaly_pred"] == "anomaly"])
avg_energy = df["energy_consumption"].mean()
avg_quality = df["surface_quality_score"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Kayıt", total_records)
col2.metric("Anomali Sayısı", anomaly_count)
col3.metric("Ortalama Enerji", f"{avg_energy:.2f}")
col4.metric("Ortalama Yüzey Kalitesi", f"{avg_quality:.2f}")

st.subheader("Fırın Sıcaklığı")
st.line_chart(df.set_index("timestamp")["furnace_temperature"])

st.subheader("Enerji Tüketimi")
st.line_chart(df.set_index("timestamp")["energy_consumption"])

st.subheader("Yüzey Kalite Skoru")
st.line_chart(df.set_index("timestamp")["surface_quality_score"])

st.subheader("Yüksek Riskli Kayıtlar")
high_risk = df[df["predicted_defect_risk"] > 50][
    ["timestamp", "predicted_defect_risk", "recommended_action", "anomaly_pred"]
]
st.dataframe(high_risk)

st.subheader("Anomali İçeren Kayıtlar")
st.dataframe(df[df["anomaly_pred"] == "anomaly"])
