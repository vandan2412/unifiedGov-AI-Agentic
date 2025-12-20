import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator.jules import JulesOrchestrator
from agents.housing_agent import HousingAgent
from agents.electricity_agent import ElectricityAgent
from explainability.explain_agent import ExplainabilityAgent

if __name__ == "__main__":
    agents = {
        "Housing Agent": HousingAgent(),
        "Electricity Agent": ElectricityAgent()
    }

    jules = JulesOrchestrator(agents)
    agent_results = jules.run_verification("C123")

    explainer = ExplainabilityAgent()
    explanation = explainer.generate_explanation(agent_results)

    print("\n=== FINAL DECISION REPORT ===")
    print(f"Risk Level: {explanation['summary']}")
    print(f"\nExplanation:\n{explanation['explanation']}")
    print(f"\nRecommendation: {explanation['recommendation']}")
