import streamlit as st
import requests
import time
import pandas as pd

# ===============================
# CONFIG
# ===============================
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="UnifiedGov AI | Citizen Verification",
    page_icon="🏛️",
    layout="wide"
)

# ===============================
# STYLES
# ===============================
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-card {
    padding: 30px;
    border-radius: 16px;
    background: linear-gradient(145deg, #1c1f26, #0f1117);
    text-align: center;
}
.big-card h1 {
    font-size: 48px;
    margin-bottom: 0;
}
.big-card p {
    color: #9ca3af;
    margin-top: 0;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
st.markdown("## 🏛️ UnifiedGov AI – Citizen Verification")
st.caption("Cross-department AI-powered fraud detection system")

# ===============================
# MODE SELECTION
# ===============================
mode = st.radio(
    "Select verification mode",
    ["Single Citizen Verification", "Batch Audit (All 100 Citizens)"]
)

# ===============================
# SINGLE MODE
# ===============================
if mode == "Single Citizen Verification":
    citizen_id = st.text_input("Enter Citizen ID (C001 – C100)", value="C001")
    run_btn = st.button("🚀 Run Verification")

    if run_btn:
        with st.spinner("Running autonomous verification workflow..."):
            try:
                response = requests.get(
                    f"{API_URL}/verify/{citizen_id}",
                    timeout=10
                )
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                st.error("Verification failed")
                st.code(str(e))
                st.stop()

        score = data["fraud_score"]
        risk = data["decision"]["summary"]
        explanation = data["decision"]["explanation"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div class="big-card">
                    <h1>{score}%</h1>
                    <p>Fraud Risk Score</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.progress(score / 100)

        with col2:
            if risk == "Low Risk":
                st.success("Low Risk")
            elif risk == "Medium Risk":
                st.warning("Medium Risk")
            else:
                st.error("High Risk")

        with col3:
            st.markdown("### Recommendation")
            st.write(
                "Manual audit recommended"
                if risk == "High Risk"
                else "Approve application"
            )

        with st.expander("📑 Automated Decision Explanation"):
            st.write(explanation)

# ===============================
# BATCH MODE (ALL 100)
# ===============================
else:
    st.markdown("### 🔁 Batch Audit – Full Population Analysis (C001–C100)")
    run_batch = st.button("🚀 Run Full Batch Audit")

    if run_batch:
        citizens = [f"C{str(i).zfill(3)}" for i in range(1, 101)]
        results = []

        with st.status("Running batch verification for all citizens...", expanded=True):
            for cid in citizens:
                try:
                    res = requests.get(
                        f"{API_URL}/verify/{cid}",
                        timeout=10
                    ).json()

                    results.append({
                        "Citizen ID": cid,
                        "Risk Level": res["decision"]["summary"],
                        "Fraud Score": res["fraud_score"]
                    })
                    time.sleep(0.05)  # gentle pacing

                except:
                    continue

        df = pd.DataFrame(results)

        # ===============================
        # SUMMARY METRICS
        # ===============================
        st.markdown("### 📊 Batch Risk Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("High Risk", (df["Risk Level"] == "High Risk").sum())
        col2.metric("Medium Risk", (df["Risk Level"] == "Medium Risk").sum())
        col3.metric("Low Risk", (df["Risk Level"] == "Low Risk").sum())

        # ===============================
        # GRAPH 1: RISK DISTRIBUTION
        # ===============================
        st.markdown("### 📊 Risk Distribution (All Citizens)")

        risk_counts = df["Risk Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk Level", "Count"]

        st.bar_chart(
            risk_counts.set_index("Risk Level"),
            height=300
        )

        # ===============================
        # GRAPH 2: FRAUD SCORE DISTRIBUTION
        # ===============================
        st.markdown("### 📈 Fraud Score Distribution")

        st.bar_chart(
            df["Fraud Score"].value_counts().sort_index(),
            height=300
        )

        # ===============================
        # FULL TABLE
        # ===============================
        st.markdown("### 📋 Full Batch Verification Results")
        st.dataframe(df, use_container_width=True)

        # ===============================
        # IMPACT NOTE
        # ===============================
        st.info(
            "Full population batch audits enable authorities to identify systemic "
            "risk patterns and prioritize high-impact manual investigations."
        )
