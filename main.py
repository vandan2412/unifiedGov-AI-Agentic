from orchestrator.jules import JulesOrchestrator
from agents.housing_agent import HousingAgent
from agents.electricity_agent import ElectricityAgent

if __name__ == "__main__":
    agents = {
        "Housing Agent": HousingAgent(),
        "Electricity Agent": ElectricityAgent()
    }

    jules = JulesOrchestrator(agents)

    result = jules.run_verification("C123")

    print("FINAL AGENT OUTPUT:")
    for agent, output in result.items():
        print(f"{agent}: {output}")

