def email_recon(email):
    result = {
        "email": email,
        "valid": "@" in email,
        "username": email.split("@")[0] if "@" in email else None
    }

    return result