import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="UnifiedGov AI", layout="wide")

st.title("🧠 UnifiedGov AI – Agentic Governance Platform")
st.caption("Stitch Frontend | Antigravity Backend | Multi-Agent AI")

# ---------------- SINGLE VERIFICATION ----------------
st.header("🔍 Verify Single Citizen")

citizen_id = st.text_input(
    "Enter Citizen ID (C001 – C100)",
    placeholder="C023"
)

if st.button("Run Verification"):
    if citizen_id:
        res = requests.get(f"{API_URL}/verify/{citizen_id}")

        if res.status_code != 200:
            st.error("Backend error. Check Antigravity service.")
        else:
            try:
                data = res.json()
            except Exception:
                st.error("Invalid response from backend")
                st.text(res.text)
                st.stop()

            if "error" in data:
                st.error(data["error"])
                st.text(data["details"])
            else:
                st.subheader(f"Fraud Risk Score: {data['fraud_score']}%")
                st.write("### Explanation")
                st.write(data["decision"]["explanation"])
                st.success(
                    f"Recommendation: {data['decision']['recommendation']}"
                )

                with st.expander("View Agent Outputs"):
                    st.json(data["agent_results"])
    else:
        st.warning("Please enter a Citizen ID")

# ---------------- BATCH ANALYSIS ----------------
st.header("📊 Batch Analysis (All Citizens)")

if st.button("Run Batch Processing"):
    res = requests.get(f"{API_URL}/batch-run").json()

    st.metric("Total Citizens", res["total_citizens"])

    st.subheader("Risk Distribution")
    st.bar_chart(res["risk_distribution"])

st.divider()

# ---------------- SYSTEM METRICS ----------------
st.header("⚙️ System Metrics")

if st.button("View System Info"):
    res = requests.get(f"{API_URL}/metrics").json()
    st.json(res)
