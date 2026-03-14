import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Glass Quality & Energy Optimization", layout="wide")

st.title("AI-Powered Glass Production Quality & Energy Optimization System")
st.markdown(
    "Cam üretim hattı için **kalite riski**, **enerji tüketimi**, **anomali tespiti** ve **operatör karar desteği** sunan dashboard"
)

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
high_risk_count = len(df[df["predicted_defect_risk"] > 70])
avg_temp = df["furnace_temperature"].mean()

st.subheader("Genel Performans Göstergeleri")
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Kayıt", total_records)
col2.metric("Anomali Sayısı", anomaly_count)
col3.metric("Yüksek Riskli Kayıt", high_risk_count)

col4, col5, col6 = st.columns(3)
col4.metric("Ortalama Enerji Tüketimi", f"{avg_energy:.2f}")
col5.metric("Ortalama Yüzey Kalitesi", f"{avg_quality:.2f}")
col6.metric("Ortalama Fırın Sıcaklığı", f"{avg_temp:.2f}")

st.markdown("---")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Fırın Sıcaklığı Takibi")
    st.line_chart(df.set_index("timestamp")["furnace_temperature"])

    st.subheader("Enerji Tüketimi Takibi")
    st.line_chart(df.set_index("timestamp")["energy_consumption"])

with right_col:
    st.subheader("Yüzey Kalite Skoru")
    st.line_chart(df.set_index("timestamp")["surface_quality_score"])

    st.subheader("Tahmini Kusur Riski")
    st.line_chart(df.set_index("timestamp")["predicted_defect_risk"])

st.markdown("---")

st.subheader("Yüksek Riskli Üretim Kayıtları")
high_risk = df[df["predicted_defect_risk"] > 50][
    ["timestamp", "predicted_defect_risk", "recommended_action", "anomaly_pred"]
]
st.dataframe(high_risk, use_container_width=True)

st.subheader("Anomali İçeren Kayıtlar")
anomalies = df[df["anomaly_pred"] == "anomaly"][
    [
        "timestamp",
        "furnace_temperature",
        "energy_consumption",
        "surface_quality_score",
        "predicted_defect_risk",
        "recommended_action",
    ]
]
st.dataframe(anomalies, use_container_width=True)

st.subheader("Operatör İçin Önerilen Aksiyonlar")
recommended_summary = df["recommended_action"].value_counts().reset_index()
recommended_summary.columns = ["Recommended Action", "Count"]
st.dataframe(recommended_summary, use_container_width=True)
