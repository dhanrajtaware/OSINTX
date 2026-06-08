import argparse
import os

from modules.email_recon import email_recon
from modules.username_recon import username_recon
from modules.domain_recon import domain_recon
from modules.account_discovery import account_discovery

from utils.banner import show_banner
from utils.risk_engine import calculate_risk
from utils.json_export import save_json
from utils.report_writer import write_report
from utils.splash import boot_sequence
from utils.banner import show_banner

boot_sequence()
show_banner()

os.makedirs("reports", exist_ok=True)

parser = argparse.ArgumentParser(
    description="OSINTX - External Exposure Assessment Tool"
)

parser.add_argument("-e", "--email")
parser.add_argument("-u", "--username")
parser.add_argument("-d", "--domain")

parser.add_argument(
    "--discover",
    help="Account discovery from email"
)

args = parser.parse_args()

results = {}

# =========================
# EMAIL RECON
# =========================

if args.email:

    result = email_recon(args.email)

    results["email"] = result

    print("\n=== EMAIL RECON ===")

    print(f"Email: {result['email']}")
    print(f"Valid: {result['valid']}")

    if result["valid"]:

        print(f"Username: {result['username']}")
        print(f"Domain: {result['domain']}")

        print(
            f"Disposable: "
            f"{'YES' if result['disposable'] else 'NO'}"
        )

        print(
            f"SPF: "
            f"{'✓' if result['spf'] else '✗'}"
        )

        print(
            f"DMARC: "
            f"{'✓' if result['dmarc'] else '✗'}"
        )

        print("\nMX Records:")

        if result["mx"]["records"]:

            for mx in result["mx"]["records"]:
                print(f"- {mx}")

        else:
            print("No MX records found")

# =========================
# USERNAME RECON
# =========================

if args.username:

    result = username_recon(args.username)

    results["username"] = result

    print("\n=== USERNAME RECON ===")

    for site, found in result.items():

        status = (
            "FOUND"
            if found
            else "NOT FOUND"
        )

        print(f"{site}: {status}")

# =========================
# DOMAIN RECON
# =========================

if args.domain:

    result = domain_recon(args.domain)

    results["domain"] = result

    print("\n=== DOMAIN RECON ===")

    for key, value in result.items():

        if key in [
            "security_headers",
            "subdomains"
        ]:
            continue

        print(f"{key}: {value}")

    # Subdomains

    if "subdomains" in result:

        print("\nSubdomains:")

        if result["subdomains"]:

            for subdomain in result[
                "subdomains"
            ][:10]:

                print(
                    f"- {subdomain}"
                )

        else:

            print(
                "No subdomains found"
            )

    # Security Headers

    if "security_headers" in result:

        print("\nSecurity Headers:")

        for header, status in result[
            "security_headers"
        ].items():

            icon = (
                "✓"
                if status
                else "✗"
            )

            print(
                f"{icon} {header}"
            )

if args.discover:

    result = account_discovery(
        args.discover
    )

    results["account_discovery"] = result

    print(
        "\n=== ACCOUNT DISCOVERY ==="
    )

    print(
        "\nGenerated Usernames:"
    )

    for username in result[
        "generated_usernames"
    ]:

        print(f"- {username}")

    print("\nFindings:")

    if result["findings"]:

        for username, sites in result[
            "findings"
        ].items():

            print(
                f"\n{username}"
            )

            for site in sites:

                print(
                    f"  ✓ {site}"
                )

    else:

        print(
            "No public profiles found"
        )

# =========================
# RISK CALCULATION
# =========================

email_valid = False
username_count = 0
missing_headers = 0

disposable = False
spf = False
dmarc = False
mx_present = False

if "email" in results:

    email_valid = results[
        "email"
    ]["valid"]

    email_data = results["email"]

    disposable = email_data.get(
        "disposable",
        False
    )

    spf = email_data.get(
        "spf",
        False
    )

    dmarc = email_data.get(
        "dmarc",
        False
    )

    mx_present = email_data.get(
        "mx",
        {}
    ).get(
        "present",
        False
    )

if "username" in results:

    username_count = sum(
        results["username"].values()
    )

if "domain" in results:

    headers = results[
        "domain"
    ].get(
        "security_headers",
        {}
    )

    missing_headers = sum(
        not status
        for status in headers.values()
    )

risk_result = calculate_risk(
    email_valid=email_valid,
    username_count=username_count,
    missing_headers=missing_headers,
    disposable=disposable,
    spf=spf,
    dmarc=dmarc,
    mx_present=mx_present
)

results["risk"] = risk_result

# =========================
# RISK OUTPUT
# =========================

print("\n=== EXPOSURE RISK ===")

print(
    f"Level: {risk_result['risk']}"
)

print(
    f"Score: {risk_result['score']}"
)

if risk_result["reasons"]:

    print("\nReasons:")

    for reason in risk_result[
        "reasons"
    ]:

        print(f"- {reason}")

# =========================
# REPORTS
# =========================

if results:

    save_json(
        results,
        "reports/report.json"
    )

    write_report(
        results,
        "reports/report.txt"
    )

    print(
        "\n[+] Report saved to reports/report.json"
    )

    print(
        "[+] Report saved to reports/report.txt"
    )