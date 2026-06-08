from modules.email_intel import (
    check_mx,
    check_spf,
    check_dmarc,
    check_disposable
)


def email_recon(email):

    result = {}

    result["email"] = email

    if "@" not in email:

        result["valid"] = False

        return result

    username, domain = email.split("@")

    result["valid"] = True
    result["username"] = username
    result["domain"] = domain

    result["mx"] = check_mx(domain)

    result["spf"] = check_spf(domain)

    result["dmarc"] = check_dmarc(domain)

    result["disposable"] = check_disposable(domain)

    return result