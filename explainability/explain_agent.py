class ExplainabilityAgent:
    def generate_explanation(self, agent_results):
        reasons = []

        for agent, result in agent_results.items():
            if result.get("status") == "Risk":
                reasons.append(f"{agent}: {result.get('details')}")

        if not reasons:
            return {
                "summary": "Low Risk",
                "explanation": "All verification checks are consistent. No anomalies detected.",
                "recommendation": "Approve application"
            }

        explanation_text = (
            "The application has been flagged due to the following reasons:\n- "
            + "\n- ".join(reasons)
        )

        return {
            "summary": "High Risk",
            "explanation": explanation_text,
            "recommendation": "Manual audit recommended before approval"
        }
