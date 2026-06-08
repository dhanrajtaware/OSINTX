def analyze_headers(headers):

    checks = {
        "HSTS": "Strict-Transport-Security",
        "CSP": "Content-Security-Policy",
        "X-Frame-Options": "X-Frame-Options",
        "X-Content-Type-Options": "X-Content-Type-Options"
    }

    results = {}

    for name, header in checks.items():
        results[name] = header in headers

    return results