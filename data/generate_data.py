import random
import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NUM_CITIZENS = 100
citizens = [f"C{str(i).zfill(3)}" for i in range(1, NUM_CITIZENS + 1)]

housing_data = []
electricity_data = []
tax_data = []

for cid in citizens:
    # Assign a risk type deterministically but mixed
    risk_type = random.choice(["low", "medium", "high", "sparse"])

    # ---------------- HOUSING (100/100 guaranteed) ----------------
    if risk_type == "high":
        properties_owned = random.randint(2, 4)
    elif risk_type == "medium":
        properties_owned = random.choice([1, 2])
    else:
        properties_owned = random.choice([0, 1])

    housing_data.append([
        cid,
        properties_owned
    ])

    # ---------------- ELECTRICITY (100/100 guaranteed) ----------------
    if risk_type == "low":
        usage = random.randint(80, 180)
        electricity_data.append(
            f"Citizen {cid} average monthly electricity usage: {usage} units"
        )

    elif risk_type == "medium":
        usage = random.randint(200, 350)
        electricity_data.append(
            f"Citizen {cid} average monthly electricity usage: {usage} units"
        )

    elif risk_type == "high":
        usage = random.randint(400, 700)
        electricity_data.append(
            f"Citizen {cid} average monthly electricity usage: {usage} units"
        )

    else:  # sparse
        electricity_data.append(
            f"Citizen {cid} electricity data not available"
        )

    # ---------------- TAX (100/100 guaranteed) ----------------
    if risk_type == "low":
        income = random.randint(400000, 900000)
    elif risk_type == "medium":
        income = random.randint(200000, 350000)
    elif risk_type == "high":
        income = random.randint(50000, 150000)
    else:
        income = None  # sparse but record exists

    tax_data.append({
        "citizen_id": cid,
        "declared_income": income
    })

# ---------------- WRITE FILES ----------------

# housing.csv
with open(os.path.join(BASE_DIR, "housing.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["citizen_id", "properties_owned"])
    writer.writerows(housing_data)

# electricity.txt
with open(os.path.join(BASE_DIR, "electricity.txt"), "w") as f:
    for line in electricity_data:
        f.write(line + "\n")

# tax.json
with open(os.path.join(BASE_DIR, "tax.json"), "w") as f:
    json.dump(tax_data, f, indent=2)

print("✅ SUCCESS: 100 citizens (C001–C100) written to ALL datasets")
