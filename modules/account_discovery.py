from modules.username_generator import generate_usernames
from modules.username_recon import username_recon


def account_discovery(email):

    usernames = generate_usernames(email)

    findings = {}

    for username in usernames:

        results = username_recon(username)

        found_sites = []

        for site, exists in results.items():

            if exists:
                found_sites.append(site)

        if found_sites:

            findings[username] = found_sites

    return {
        "generated_usernames": usernames,
        "findings": findings
    }