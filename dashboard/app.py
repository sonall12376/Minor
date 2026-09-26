import os
import requests
import streamlit as st

API_URL = os.getenv("MINOR_API_URL", "http://localhost:8000/api/v1")
st.set_page_config(page_title="Minor MLOps Dashboard", layout="wide")
st.title("Minor — MLOps Model Monitoring")
st.caption("Mid-term dashboard: production batches, drift status and model health")

def api_get(path):
    try:
        r = requests.get(f"{API_URL}{path}", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return None

history = api_get("/history") or []
drift = api_get("/drift")

c1, c2, c3 = st.columns(3)
c1.metric("Production Batches", len(history))
c2.metric("Drift Status", "DRIFT DETECTED" if drift and drift.get("is_drift_detected") else "NO DRIFT")
c3.metric("Health Score", f"{drift.get('health_score', 100):.1f}" if drift else "—")

st.divider()
st.subheader("Recent Production Batches")
if history:
    st.dataframe(history, use_container_width=True)
else:
    st.info("No batches yet. Start FastAPI and POST /api/v1/production.")

st.subheader("Latest Drift")
if drift:
    st.json(drift)
else:
    st.info("No drift result available yet.")
