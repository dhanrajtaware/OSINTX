import argparse
import os

from modules.email_recon import email_recon
from modules.username_recon import username_recon
from modules.domain_recon import domain_recon
from utils.banner import show_banner
from utils.risk_engine import calculate_risk
from utils.json_export import save_json
from utils.report_writer import write_report

show_banner()

os.makedirs("reports", exist_ok=True)

parser = argparse.ArgumentParser(
    description="OSINTX - External Exposure Assessment Tool"
)

parser.add_argument("-e", "--email")
parser.add_argument("-u", "--username")
parser.add_argument("-d", "--domain")

args = parser.parse_args()

results = {}

# Email Recon
if args.email:
    result = email_recon(args.email)
    results["email"] = result

    print("\n=== EMAIL RECON ===")
    print(f"Email: {result['email']}")
    print(f"Valid: {result['valid']}")
    print(f"Username: {result['username']}")

# Username Recon
if args.username:
    result = username_recon(args.username)
    results["username"] = result

    print("\n=== USERNAME RECON ===")

    for site, found in result.items():
        status = "FOUND" if found else "NOT FOUND"
        print(f"{site}: {status}")

# Domain Recon
# Domain Recon
if args.domain:
    result = domain_recon(args.domain)
    results["domain"] = result

    print("\n=== DOMAIN RECON ===")

    for key, value in result.items():

        if key in ["security_headers", "subdomains"]:
            continue

        print(f"{key}: {value}")

    # Subdomains
    if "subdomains" in result:

        print("\nSubdomains:")

        if result["subdomains"]:

            for subdomain in result["subdomains"][:10]:
                print(f"- {subdomain}")

        else:
            print("No subdomains found")

    # Security Headers
    if "security_headers" in result:

        print("\nSecurity Headers:")

        for header, status in result["security_headers"].items():

            icon = "✓" if status else "✗"

            print(f"{icon} {header}")
            
email_valid = False
username_count = 0
missing_headers = 0

if "email" in results:
    email_valid = results["email"]["valid"]

if "username" in results:
    username_count = sum(
        results["username"].values()
    )

if "domain" in results:

    headers = results["domain"].get(
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
    missing_headers=missing_headers
)

results["risk"] = risk_result

if results:

    save_json(
        results,
        "reports/report.json"
    )

    write_report(
        results,
        "reports/report.txt"
    )

    print("\n[+] Report saved to reports/report.json")
    print("[+] Report saved to reports/report.txt")