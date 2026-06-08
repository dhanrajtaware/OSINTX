import requests

def username_recon(username):
    sites = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://reddit.com/user/{username}",
        "Instagram": f"https://instagram.com/{username}"
    }

    results = {}

    for site, url in sites.items():
        try:
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            results[site] = response.status_code == 200

        except:
            results[site] = False

    return results