import os

class ElectricityAgent:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base_dir, "data", "electricity.txt")

        with open(data_path, "r") as f:
            self.data = f.read()

    def analyze(self, citizen_id):
        for line in self.data.splitlines():
            if citizen_id in line:
                if "not available" in line:
                    return {
                        "status": "Unknown",
                        "details": "Electricity data not available"
                    }

                if "usage" in line:
                    try:
                        usage = int(line.split(":")[1].split()[0])
                    except Exception:
                        return {
                            "status": "Unknown",
                            "details": "Invalid electricity data format"
                        }

                    if usage > 400:
                        return {
                            "status": "Risk",
                            "details": f"High electricity usage: {usage} units"
                        }

                    return {
                        "status": "Clear",
                        "details": f"Normal electricity usage: {usage} units"
                    }

        return {
            "status": "Unknown",
            "details": "Electricity record not found"
        }
