from fastapi import FastAPI
import os
import json
from google import genai

# ===============================
# FASTAPI APP
# ===============================
app = FastAPI(title="UnifiedGov AI – Antigravity Backend")

DATA_DIR = "data"

# ===============================
# AGENTS
# ===============================

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


# ===============================
# SCORING
# ===============================

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
            score += weights.get(agent, 0) * 0.15

    if risk_count >= 2:
        score += 10
    if risk_count >= 3:
        score += 15

    return min(int(score), 95)


# ===============================
# EXPLAINABILITY (SAFE)
# ===============================

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
                print("⚠️ Gemini failed, fallback:", e)
        else:
            print("⚠️ Gemini disabled – fallback explanations")

    def explain(self, agent_results, score, risk):
        if not self.enabled:
            reasons = [
                f"{a}: {r['details']}"
                for a, r in agent_results.items()
                if r["status"] != "Clear"
            ]
            if not reasons:
                return "No inconsistencies detected across departments."
            return "Risk factors identified: " + "; ".join(reasons)

        prompt = f"""
Explain the following fraud assessment for a government officer.
Agent Results:
{json.dumps(agent_results, indent=2)}
Fraud Score: {score}
Risk Level: {risk}
"""
        resp = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )
        return resp.text.strip()


# ===============================
# ORCHESTRATOR
# ===============================

class Jules:
    def __init__(self):
        self.h = HousingAgent()
        self.e = ElectricityAgent()
        self.t = TaxAgent()
        self.s = SnitchAgent()
        self.x = ExplainabilityAgent()

    def verify(self, cid):
        results = {
            "Housing Agent": self.h.analyze(cid),
            "Electricity Agent": self.e.analyze(cid),
            "Tax Agent": self.t.analyze(cid)
        }
        results["Snitch Agent"] = self.s.analyze(results)

        score = calculate_fraud_score(results)
        risk = "High Risk" if score > 60 else "Medium Risk" if score > 25 else "Low Risk"

        return {
            "citizen_id": cid,
            "fraud_score": score,
            "decision": {
                "summary": risk,
                "explanation": self.x.explain(results, score, risk)
            },
            "agent_results": results
        }


jules = Jules()

# ===============================
# API
# ===============================

@app.get("/")
def health():
    return {"status": "Backend running"}

@app.get("/verify/{citizen_id}")
def verify(citizen_id: str):
    return jules.verify(citizen_id)
