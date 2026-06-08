def calculate_risk(email_valid=False,
                   username_count=0,
                   missing_headers=0):

    score = 0
    reasons = []

    if email_valid:
        score += 1

    if username_count >= 3:
        score += 4
        reasons.append(
            "Username found on multiple platforms"
        )

    elif username_count >= 1:
        score += 2
        reasons.append(
            "Username publicly exposed"
        )

    if missing_headers >= 2:
        score += 2
        reasons.append(
            "Missing important security headers"
        )

    if score >= 6:
        risk = "HIGH"

    elif score >= 3:
        risk = "MEDIUM"

    else:
        risk = "LOW"

    return {
        "risk": risk,
        "score": score,
        "reasons": reasons
    }