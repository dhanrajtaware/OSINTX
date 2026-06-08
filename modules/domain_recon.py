import socket
import requests
import whois

from modules.security_headers import analyze_headers
from modules.subdomain_enum import get_subdomains


def domain_recon(domain):

    result = {}

    # DNS Resolution
    try:
        result["ip"] = socket.gethostbyname(domain)

    except Exception as e:
        print(f"DNS ERROR: {e}")
        result["ip"] = "Not Resolved"

    # WHOIS Lookup
    try:
        w = whois.whois(domain)

        result["registrar"] = w.registrar
        result["creation_date"] = str(w.creation_date)

    except Exception as e:
        print(f"WHOIS ERROR: {e}")

        result["registrar"] = "Unknown"
        result["creation_date"] = "Unknown"

    # HTTP Headers + Security Headers
    try:
        response = requests.get(
            f"https://{domain}",
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        result["server"] = response.headers.get(
            "Server",
            "Unknown"
        )

        result["powered_by"] = response.headers.get(
            "X-Powered-By",
            "Not Exposed"
        )

        result["security_headers"] = analyze_headers(
            response.headers
        )

    except Exception as e:

        print(f"HTTP ERROR: {e}")

        result["server"] = "Unknown"
        result["powered_by"] = "Unknown"

        result["security_headers"] = {
            "HSTS": False,
            "CSP": False,
            "X-Frame-Options": False,
            "X-Content-Type-Options": False
        }

    result["subdomains"] = get_subdomains(domain)
    return result