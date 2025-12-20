import pandas as pd
import os

class HousingAgent:
    def __init__(self, data_path=None):
        # Always resolve path from project root
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "housing.csv")

        self.data = pd.read_csv(data_path)

    def analyze(self, citizen_id):
        record = self.data[self.data["citizen_id"] == citizen_id]

        if record.empty:
            return {"status": "No housing data found"}

        properties = int(record.iloc[0]["properties_owned"])

        if properties > 1:
            return {
                "status": "Risk",
                "details": f"Citizen owns {properties} properties"
            }

        return {
            "status": "Clear",
            "details": "Single property ownership"
        }
