import requests


def get_subdomains(domain):

    subdomains = set()

    try:

        url = f"https://crt.sh/?q=%.{domain}&output=json"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        if response.status_code != 200:
            return []

        data = response.json()

        for entry in data:

            names = entry.get(
                "name_value",
                ""
            )

            for subdomain in names.split("\n"):

                subdomain = (
                    subdomain
                    .strip()
                    .lower()
                )

                if "*" in subdomain:
                    continue

                if domain in subdomain:
                    subdomains.add(subdomain)

        return sorted(subdomains)

    except Exception as e:

        print(
            f"SUBDOMAIN ERROR: {e}"
        )

        return []