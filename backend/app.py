print("🔥 backend/app.py LOADED")

from fastapi import FastAPI
import os
import json
from collections import Counter
from google import genai

# ==================================================
# FASTAPI APP (ROUTES MUST BE TOP-LEVEL)
# ==================================================

app = FastAPI(title="UnifiedGov AI – Antigravity Backend")

# --------------------------------------------------
# HEALTH
# --------------------------------------------------
@app.get("/")
def health():
    return {"status": "Backend running"}

# --------------------------------------------------
# VERIFY SINGLE CITIZEN
# --------------------------------------------------
@app.get("/verify/{citizen_id}")
def verify(citizen_id: str):
    try:
        return jules.verify(citizen_id)
    except Exception as e:
        return {
            "error": "Backend execution failed",
            "details": str(e)
        }

# --------------------------------------------------
# BATCH VERIFY (ALL 100)
# --------------------------------------------------
@app.get("/batch")
def batch():
    return jules.verify_all()

# ==================================================
# DATA
# ==================================================

DATA_DIR = "data"

# ==================================================
# AGENTS
# ==================================================

class HousingAgent:
    def __init__(self):
        with open(f"{DATA_DIR}/housing.csv") as f:
            self.rows = f.readlines()

    def analyze(self, citizen_id):
        for r in self.rows:
            cid, props = r.strip().split(",")
            if cid == citizen_id:
                props = int(props)
                if props >= 2:
                    return {"status": "Risk", "details": f"Owns {props} properties"}
                return {"status": "Clear", "details": "Single property"}
        return {"status": "Unknown", "details": "Housing data missing"}


class ElectricityAgent:
    def __init__(self):
        with open(f"{DATA_DIR}/electricity.txt") as f:
            self.lines = f.readlines()

    def analyze(self, citizen_id):
        for l in self.lines:
            if citizen_id in l:
                try:
                    usage = int(l.split(":")[1])
                except:
                    return {"status": "Unknown", "details": "Invalid electricity data"}
                if usage > 400:
                    return {"status": "Risk", "details": f"High usage ({usage})"}
                return {"status": "Clear", "details": f"Normal usage ({usage})"}
        return {"status": "Unknown", "details": "Electricity data missing"}


class TaxAgent:
    def __init__(self):
        with open(f"{DATA_DIR}/tax.json") as f:
            self.data = json.load(f)

    def analyze(self, citizen_id):
        for r in self.data:
            if r["citizen_id"] == citizen_id:
                income = r.get("declared_income")
                if income is None:
                    return {"status": "Unknown", "details": "Income not declared"}
                if income < 200000:
                    return {"status": "Risk", "details": f"Low income ({income})"}
                return {"status": "Clear", "details": f"Declared income ({income})"}
        return {"status": "Unknown", "details": "Tax data missing"}


class SnitchAgent:
    def analyze(self, agent_results):
        risks = sum(1 for r in agent_results.values() if r["status"] == "Risk")
        if risks >= 2:
            return {"status": "Risk", "details": "Cross-department inconsistency"}
        return {"status": "Clear", "details": "No major inconsistencies"}

# ==================================================
# SCORING
# ==================================================

def calculate_fraud_score(agent_results):
    score = 5
    weights = {
        "Housing Agent": 25,
        "Electricity Agent": 25,
        "Tax Agent": 20,
        "Snitch Agent": 15
    }

    risk_count = 0

    for agent, res in agent_results.items():
        if res["status"] == "Risk":
            score += weights.get(agent, 0)
            risk_count += 1
        elif res["status"] == "Unknown":
            score += weights.get(agent, 0) * 0.25  # ✅ CHANGED HERE

    if risk_count >= 2:
        score += 10
    if risk_count >= 3:
        score += 15

    return min(int(score), 95)

# ==================================================
# EXPLAINABILITY (GEMINI + SAFE FALLBACK)
# ==================================================
class ExplainabilityAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = False

        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.enabled = True
                print("✅ Gemini enabled")
            except Exception as e:
                print("⚠️ Gemini init failed:", e)
        else:
            print("⚠️ Gemini disabled – fallback explanations")

    def explain(self, agent_results, score, risk):
        # Fallback (no Gemini)
        if not self.enabled:
            reasons = [
                f"{agent}: {res['details']}"
                for agent, res in agent_results.items()
                if res["status"] == "Risk"
            ]
            if not reasons:
                return "No inconsistencies detected across departments."
            return "Risk factors identified: " + "; ".join(reasons)

        # Gemini-powered explanation
        prompt = f"""
You are an AI assistant helping a government officer.

Based ONLY on the agent reports below, write a concise,
professional, audit-ready explanation (2–3 sentences).
Do not invent facts. Use unique phrasing.

Agent Results:
{json.dumps(agent_results, indent=2)}

Fraud Score: {score}
Risk Level: {risk}
"""
        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )

        return response.text.strip()


    # ---------- BATCH ----------
    def explain_batch(self, batch_results):
        risk_counts = Counter([r["Risk Level"] for r in batch_results])
        avg_score = round(
            sum(r["Fraud Score"] for r in batch_results) / len(batch_results), 1
        )

        if not self.enabled:
            return (
                f"The batch audit reviewed {len(batch_results)} citizens. "
                f"Most profiles fall under {max(risk_counts, key=risk_counts.get)} risk, "
                f"with an average fraud score of {avg_score}%."
            )

        prompt = f"""
Summarize the following government batch audit:
- Explain population-level risk patterns
- Do NOT discuss individuals
- Professional policy tone
- 3–4 sentences

Batch Summary:
Total Citizens: {len(batch_results)}
Risk Distribution: {dict(risk_counts)}
Average Fraud Score: {avg_score}%
"""
        resp = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )
        return resp.text.strip()

# ==================================================
# ORCHESTRATOR (JULES)
# ==================================================
class Jules:
    def __init__(self):
        self.h = HousingAgent()
        self.e = ElectricityAgent()
        self.t = TaxAgent()
        self.s = SnitchAgent()
        self.explainer = ExplainabilityAgent()

    def verify(self, cid):
        agent_results = {
            "Housing Agent": self.h.analyze(cid),
            "Electricity Agent": self.e.analyze(cid),
            "Tax Agent": self.t.analyze(cid),
        }

        agent_results["Snitch Agent"] = self.s.analyze(agent_results)

        score = calculate_fraud_score(agent_results)

        if score > 60:
            risk = "High Risk"
        elif score > 25:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        explanation = self.explainer.explain(agent_results, score, risk)

        return {
            "citizen_id": cid,
            "fraud_score": score,
            "decision": {
                "summary": risk,
                "explanation": explanation
            },
            "agent_results": agent_results
        }


jules = Jules()
