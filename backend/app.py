from fastapi import FastAPI
import random
import csv
import os

from orchestrator.jules import JulesOrchestrator
from agents.housing_agent import HousingAgent
from agents.electricity_agent import ElectricityAgent
from agents.tax_agent import TaxAgent
from agents.snitch_agent import SnitchAgent
from explainability.explain_agent import ExplainabilityAgent
from llm.fraud_scorer import calculate_fraud_score

app = FastAPI(title="UnifiedGov AI – Antigravity Backend")

# Load citizens
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOUSING_PATH = os.path.join(BASE_DIR, "data", "housing.csv")

citizens = []
with open(HOUSING_PATH) as f:
    reader = csv.DictReader(f)
    citizens = [row["citizen_id"] for row in reader]

agents = {
    "Housing Agent": HousingAgent(),
    "Electricity Agent": ElectricityAgent(),
    "Tax Agent": TaxAgent()
}

jules = JulesOrchestrator(agents)
snitch = SnitchAgent()
explainer = ExplainabilityAgent()


@app.get("/verify/{citizen_id}")
def verify_citizen(citizen_id: str):
    try:
        results = jules.run_verification(citizen_id)
        results["Snitch Agent"] = snitch.monitor(results)

        fraud_score = calculate_fraud_score(results)
        explanation = explainer.generate_explanation(results)

        return {
            "citizen_id": citizen_id,
            "fraud_score": fraud_score,
            "decision": explanation,
            "agent_results": results
        }
    except Exception as e:
        return {
            "error": "Backend execution failed",
            "details": str(e)
        }


@app.get("/batch-run")
def batch_run():
    summary = {"High Risk": 0, "Low Risk": 0}

    for cid in citizens:
        results = jules.run_verification(cid)
        results["Snitch Agent"] = snitch.monitor(results)
        explanation = explainer.generate_explanation(results)

        summary[explanation["summary"]] += 1

    return {
        "total_citizens": len(citizens),
        "risk_distribution": summary
    }


@app.get("/metrics")
def metrics():
    return {
        "total_citizens": len(citizens),
        "agents": list(agents.keys()) + ["Snitch Agent", "Explainability Agent"],
        "capabilities": [
            "Multi-agent verification",
            "Cross-department anomaly detection",
            "Fraud scoring",
            "Explainable decisions"
        ]
    }
