# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from core import (
    set_seed, load_data, detect_events, build_model,
    generate_events, fast_timeseries, inject, detect, metrics
)

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Water Intelligence System", layout="wide")

# ---------------------------
# STYLING
# ---------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: #e2e8f0;
}

.block-container {
    padding-top: 1rem;
}

.top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.05);
    padding: 12px 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.control-panel {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 14px;
    text-align: center;
}

.alert {
    background: rgba(239,68,68,0.2);
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.success {
    background: rgba(34,197,94,0.2);
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="top-bar">
    <h2>Water Intelligence Control System</h2>
    <span>Real-time monitoring and anomaly detection</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# CONTROL PANEL
# ---------------------------
st.markdown('<div class="control-panel">', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

seed = col1.number_input("Seed", value=42)
threshold = col2.slider("Detection Sensitivity", 1.0, 10.0, 3.5)
buildings = col3.slider("Number of Buildings", 1, 10, 5)
days = col4.slider("Simulation Duration (days)", 3, 14, 7)
run = col5.button("Run System")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------
if "campus" not in st.session_state:
    st.session_state.campus = None

# ---------------------------
# RUN PIPELINE
# ---------------------------
if run:

    with st.spinner("Running simulation..."):

        set_seed(seed)

        df = load_data("WEUSEDTO")
        events = detect_events(df, threshold)
        model = build_model(events)

        all_df = []

        for b in range(buildings):
            ev = []
            for d in pd.date_range("2025-01-01", periods=days):
                ev.extend(generate_events(model, d))

            ts = fast_timeseries(ev)
            ts = inject(ts)
            ts = detect(ts, threshold)

            ts["building"] = f"B{b+1}"
            all_df.append(ts)

        st.session_state.campus = pd.concat(all_df)

# ---------------------------
# DISPLAY RESULTS
# ---------------------------
if st.session_state.campus is not None:

    campus = st.session_state.campus

    # KPIs
    cm, acc, recall = metrics(campus)

    c1, c2, c3 = st.columns(3)

    c1.markdown(f'<div class="card"><h2>{acc:.2f}</h2><p>Model Accuracy</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h2>{len(campus["building"].unique())}</h2><p>Buildings</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><h2>{len(campus)}</h2><p>Data Points</p></div>', unsafe_allow_html=True)

    # ALERTS
    st.markdown("## Anomaly Alerts")

    alerts = campus[campus["pred"] != "Normal"]

    if len(alerts) > 0:
        for _, row in alerts.head(5).iterrows():
            st.markdown(
                f'<div class="alert">{row["timestamp"]} → {row["pred"]}</div>',
                unsafe_allow_html=True
            )
    else:
        st.markdown('<div class="success">No anomalies detected</div>', unsafe_allow_html=True)

    # BUILDING VIEW
    st.markdown("## Building Analysis")

    selected = st.selectbox(
        "Select Building",
        campus["building"].unique(),
        key="building_select"
    )

    bdf = campus[campus["building"] == selected]

    # MAIN GRAPH
    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(bdf["timestamp"], bdf["consumption"], label="Consumption")

    anomalies = bdf[bdf["pred"] != "Normal"]
    ax.scatter(anomalies["timestamp"], anomalies["consumption"], label="Anomalies")

    ax.legend()
    ax.set_title(f"{selected} - Water Consumption and Detected Events")

    st.pyplot(fig)

    # SCORE GRAPH
    fig2, ax2 = plt.subplots(figsize=(12,4))
    ax2.plot(bdf["timestamp"], bdf["score"])
    ax2.set_title("Anomaly Score")

    st.pyplot(fig2)

    # PERFORMANCE
    st.markdown("## Model Performance")

    st.dataframe(cm)
    st.json(recall)

    st.success("System execution completed")