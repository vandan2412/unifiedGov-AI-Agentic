class ExplainabilityAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = False

        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.enabled = True
                print("✅ Gemini explainability enabled")
            except Exception as e:
                print("⚠️ Gemini init failed, using fallback:", e)
        else:
            print("⚠️ Gemini disabled – using fallback explanations")

    def explain(self, agent_results, score, risk_level):
        if not self.enabled:
            reasons = [
                f"{agent}: {res['details']}"
                for agent, res in agent_results.items()
                if res["status"] != "Clear"
            ]

            if not reasons:
                return (
                    "The verification process did not identify any inconsistencies "
                    "across available department records. The citizen profile "
                    "aligns with declared information."
                )

            return (
                "The application was evaluated across multiple departments. "
                "The following factors contributed to the assessed risk: "
                + "; ".join(reasons)
                + "."
            )

        prompt = f"""
You are an AI assistant helping a government officer.

Based ONLY on the following agent reports, generate:
- A concise explanation (2–3 sentences)
- Professional, audit-ready language
- Unique phrasing
- Do NOT invent facts

Agent Reports:
{json.dumps(agent_results, indent=2)}

Fraud Score: {score}%
Risk Level: {risk_level}
"""

        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )

        return response.text.strip()
