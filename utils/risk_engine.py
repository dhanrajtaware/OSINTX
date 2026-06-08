def calculate_risk(
    email_valid=False,
    username_count=0,
    missing_headers=0,
    disposable=False,
    spf=False,
    dmarc=False,
    mx_present=False
):

    score = 0
    reasons = []

    # Email Checks

    if disposable:
        score += 3
        reasons.append(
            "Disposable email provider detected"
        )

    if not spf:
        score += 1
        reasons.append(
            "SPF record missing"
        )

    if not dmarc:
        score += 1
        reasons.append(
            "DMARC record missing"
        )

    if not mx_present:
        score += 2
        reasons.append(
            "No MX records found"
        )

    # Username Exposure

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

    # Domain Security

    if missing_headers >= 2:
        score += 2
        reasons.append(
            "Missing security headers"
        )

    # Final Rating

    if score >= 7:
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