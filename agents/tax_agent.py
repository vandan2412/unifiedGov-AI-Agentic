import json
import os

class TaxAgent:
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "tax.json")

        with open(data_path, "r") as f:
            self.data = json.load(f)
    def analyze(self, citizen_id):
        record = next(
            (r for r in self.data if r.get("citizen_id") == citizen_id),
            None
        )

        if not record:
            return {"status": "No tax data found"}

        income = record.get("declared_income", 0)

        if income < 200000:
            return {
                "status": "Risk",
                "details": f"Low declared income: ₹{income}"
            }

        return {
            "status": "Clear",
            "details": f"Declared income: ₹{income}"
        }
