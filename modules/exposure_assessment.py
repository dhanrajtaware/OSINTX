def assess_exposure(email_data, username_data):
    score = 0
    reasons = []

    if email_data.get("valid"):
        score += 2
        reasons.append("Valid email identified")

    found_accounts = sum(username_data.values())

    if found_accounts >= 3:
        score += 5
        reasons.append("Username reused on multiple platforms")

    elif found_accounts >= 1:
        score += 2
        reasons.append("Username found online")

    return {
        "score": score,
        "reasons": reasons
    }