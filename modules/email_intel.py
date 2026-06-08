import dns.resolver


def check_mx(domain):

    try:
        records = dns.resolver.resolve(
            domain,
            "MX"
        )

        return {
            "present": True,
            "records": [
                str(record.exchange)
                for record in records
            ]
        }

    except Exception:
        return {
            "present": False,
            "records": []
        }


def check_spf(domain):

    try:
        records = dns.resolver.resolve(
            domain,
            "TXT"
        )

        for record in records:

            txt = "".join(
                record.strings[0]
                .decode()
            )

            if txt.startswith(
                "v=spf1"
            ):
                return True

        return False

    except Exception:
        return False


def check_dmarc(domain):

    try:

        records = dns.resolver.resolve(
            f"_dmarc.{domain}",
            "TXT"
        )

        for record in records:

            txt = "".join(
                record.strings[0]
                .decode()
            )

            if txt.startswith(
                "v=DMARC1"
            ):
                return True

        return False

    except Exception:
        return False
    
def check_disposable(domain):

    try:

        with open(
            "data/disposable_domains.txt",
            "r",
            encoding="utf-8"
        ) as f:

            domains = {
                line.strip().lower()
                for line in f
            }

        return domain.lower() in domains

    except Exception:
        return False