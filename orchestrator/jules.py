class JulesOrchestrator:
    def __init__(self, agents):
        """
        agents: dict of agent_name -> agent_instance
        """
        self.agents = agents

    def run_verification(self, citizen_id):
        print(f"\n[JULES] Starting verification for Citizen ID: {citizen_id}\n")

        results = {}

        for name, agent in self.agents.items():
            print(f"[JULES] Activating {name}...")
            results[name] = agent.analyze(citizen_id)
            print(f"[JULES] {name} completed.\n")

        print("[JULES] All agents completed. Compiling results...\n")
        return results
