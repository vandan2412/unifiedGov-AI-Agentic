import random
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NUM_CITIZENS = 100

citizens = [f"C{str(i).zfill(3)}" for i in range(1, NUM_CITIZENS + 1)]

housing_rows = []
electricity_lines = []
tax_records = []

for cid in citizens:
    risk_type = random.choice(["low", "medium", "high", "sparse"])

    # ---- HOUSING ----
    if risk_type == "high":
        properties = random.randint(2, 4)
    else:
        properties = random.choice([0, 1])

    housing_rows.append([cid, properties])

    # ---- ELECTRICITY ----
    if risk_type == "low":
        usage = random.randint(80, 180)
    elif risk_type == "medium":
        usage = random.randint(200, 350)
    elif risk_type == "high":
        usage = random.randint(400, 700)
    else:
        usage = None  # sparse

    if usage:
        electricity_lines.append(
            f"Citizen {cid} average monthly electricity usage: {usage} units"
        )

    # ---- TAX ----
    if risk_type == "low":
        income = random.randint(400000, 900000)
    elif risk_type == "medium":
        income = random.randint(200000, 350000)
    elif risk_type == "high":
        income = random.randint(50000, 150000)
    else:
        continue  # sparse tax data

    tax_records.append({
        "citizen_id": cid,
        "declared_income": income
    })

# Write housing.csv
with open(os.path.join(BASE_DIR, "housing.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["citizen_id", "properties_owned"])
    writer.writerows(housing_rows)

# Write electricity.txt
with open(os.path.join(BASE_DIR, "electricity.txt"), "w") as f:
    for line in electricity_lines:
        f.write(line + "\n")

# Write tax.json
with open(os.path.join(BASE_DIR, "tax.json"), "w") as f:
    json.dump(tax_records, f, indent=2)

print("✅ Generated housing.csv, electricity.txt, and tax.json with 100 citizens")
