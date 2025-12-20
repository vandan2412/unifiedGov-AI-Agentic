import sys
import os
import random
import csv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.jules import JulesOrchestrator
from agents.housing_agent import HousingAgent
from agents.electricity_agent import ElectricityAgent
from agents.tax_agent import TaxAgent
from agents.snitch_agent import SnitchAgent
from explainability.explain_agent import ExplainabilityAgent
from llm.fraud_scorer import calculate_fraud_score


def load_citizens():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    housing_path = os.path.join(base_dir, "data", "housing.csv")

    citizens = []
    with open(housing_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            citizens.append(row["citizen_id"])

    return citizens


if __name__ == "__main__":
    # Load all citizen IDs
    citizens = load_citizens()

    # Pick one random citizen for demo
    citizen_id = random.choice(citizens)

    print(f"\n🔍 Verifying Citizen ID: {citizen_id}")

    agents = {
        "Housing Agent": HousingAgent(),
        "Electricity Agent": ElectricityAgent(),
        "Tax Agent": TaxAgent()
    }

    jules = JulesOrchestrator(agents)
    agent_results = jules.run_verification(citizen_id)

    # Snitch agent
    snitch = SnitchAgent()
    agent_results["Snitch Agent"] = snitch.monitor(agent_results)

    # Fraud score
    fraud_score = calculate_fraud_score(agent_results)

    # Explainability
    explainer = ExplainabilityAgent()
    explanation = explainer.generate_explanation(agent_results)

    print("\n=== FINAL DECISION REPORT ===")
    print(f"Fraud Risk Score: {fraud_score}%")
    print(f"Risk Level: {explanation['summary']}")
    print(f"\nExplanation:\n{explanation['explanation']}")
    print(f"\nRecommendation: {explanation['recommendation']}")
