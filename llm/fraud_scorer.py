def calculate_fraud_score(agent_results):
    score = 0

    for result in agent_results.values():
        if result.get("status") == "Risk":
            score += 30

    return min(score, 100)

