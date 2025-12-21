from google import genai
import os
import json
from collections import Counter

class ExplainabilityAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = False

        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
                self.enabled = True
                print("✅ Gemini Explainability Agent enabled")
            except Exception as e:
                print("⚠️ Gemini init failed, fallback enabled:", e)
        else:
            print("⚠️ Gemini API key missing, fallback explanations enabled")

    # =================================================
    # 🔹 INDIVIDUAL EXPLANATION (CALLED 100 TIMES)
    # =================================================
    def explain_individual(self, agent_results, score, risk_level):
        if not self.enabled:
            reasons = [
                f"{agent}: {res['details']}"
                for agent, res in agent_results.items()
                if res["status"] != "Clear"
            ]

            if not reasons:
                return (
                    "No inconsistencies were identified across departmental records. "
                    "The citizen profile aligns with declared information."
                )

            return (
                "The verification identified the following contributing factors: "
                + "; ".join(reasons)
                + "."
            )

        prompt = f"""
You are an AI assistant supporting a government verification officer.

Generate a UNIQUE, professional explanation for THIS citizen only.
Rules:
- 2–3 sentences
- Audit-ready language
- No repeated phrasing
- Do NOT invent facts
- Do NOT mention AI or Gemini

Agent Findings:
{json.dumps(agent_results, indent=2)}

Fraud Score: {score}%
Risk Level: {risk_level}

Explain WHY this risk level was assigned.
"""

        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )

        return response.text.strip()

    # =================================================
    # 🔹 BATCH EXPLANATION (CALLED ONCE PER BATCH)
    # =================================================
    def explain_batch(self, batch_results):
        """
        batch_results = list of dicts with keys:
        - Risk Level
        - Fraud Score
        """

        risk_counts = Counter([r["Risk Level"] for r in batch_results])
        avg_score = round(
            sum(r["Fraud Score"] for r in batch_results) / len(batch_results), 1
        )

        if not self.enabled:
            return (
                f"The batch audit evaluated {len(batch_results)} citizen records. "
                f"Most profiles fall under the {max(risk_counts, key=risk_counts.get)} category, "
                f"with an average fraud score of {avg_score}%. "
                "This indicates identifiable risk patterns suitable for prioritized review."
            )

        prompt = f"""
You are an AI assistant summarizing a government batch audit.

Rules:
- Explain SYSTEMIC patterns, not individuals
- Professional, policy-level tone
- 3–4 sentences
- Do NOT invent facts
- Do NOT mention AI or Gemini

Batch Statistics:
- Total Citizens Audited: {len(batch_results)}
- Risk Distribution: {dict(risk_counts)}
- Average Fraud Score: {avg_score}%

Explain the observed risk patterns and their significance.
"""

        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash-exp",
            contents=prompt
        )

        return response.text.strip()
