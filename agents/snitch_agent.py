class SnitchAgent:
    def monitor(self, agent_results):
        anomalies = []

        housing = agent_results.get("Housing Agent", {})
        electricity = agent_results.get("Electricity Agent", {})
        tax = agent_results.get("Tax Agent", {})

        if (
            housing.get("status") == "Risk"
            and electricity.get("status") == "Risk"
            and tax.get("status") == "Risk"
        ):
            anomalies.append(
                "Multiple high-risk indicators detected across departments"
            )

        if not anomalies:
            return {
                "status": "Clear",
                "details": "No cross-department anomalies detected"
            }

        return {
            "status": "Risk",
            "details": "; ".join(anomalies)
        }
