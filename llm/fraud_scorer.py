def calculate_fraud_score(agent_results):
    """
    Calibrated fraud scoring with confidence accumulation.
    Produces realistic, non-extreme scores.
    """

    BASE_RISK = 5          # everyone has minimal risk
    score = BASE_RISK

    WEIGHTS = {
        "Housing Agent": 25,
        "Electricity Agent": 25,
        "Tax Agent": 20,
        "Snitch Agent": 15
    }

    risk_count = 0

    for agent, result in agent_results.items():
        if not isinstance(result, dict):
            continue

        status = result.get("status")

        if status == "Risk":
            score += WEIGHTS.get(agent, 0)
            risk_count += 1

        elif status == "Unknown":
            score += WEIGHTS.get(agent, 0) * 0.15  # uncertainty penalty

    # 🔹 Confidence boost for multiple corroborating risks
    if risk_count >= 2:
        score += 10
    if risk_count >= 3:
        score += 15

    # 🔹 Soft cap to avoid 100 unless extreme
    score = min(score, 95)

    return int(score)
