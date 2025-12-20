def calculate_fraud_score(agent_results):
    score = 0

    for agent, result in agent_results.items():
        if not isinstance(result, dict):
            continue

        status = result.get("status")

        if status == "Risk":
            score += 30
        elif status == "Unknown":
            score += 10  # uncertainty adds mild risk

    return min(score, 100)
