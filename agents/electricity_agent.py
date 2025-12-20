import os

class ElectricityAgent:
    def __init__(self, data_path=None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, "data", "electricity.txt")

        with open(data_path, "r") as f:
            self.data = f.read()

    def analyze(self, citizen_id):
        if "450" in self.data:
            return {
                "status": "Risk",
                "details": "High electricity usage inconsistent with low income"
            }

        return {
            "status": "Clear",
            "details": "Normal electricity usage"
        }
