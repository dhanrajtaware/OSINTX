def generate_usernames(email):

    usernames = []

    try:

        local_part = email.split("@")[0]

        usernames.append(local_part)

        cleaned = (
            local_part
            .replace(".", "")
            .replace("-", "")
            .replace("_", "")
        )

        usernames.append(cleaned)

        parts = (
            local_part
            .replace("-", ".")
            .replace("_", ".")
            .split(".")
        )

        if len(parts) >= 2:

            first = parts[0]
            last = parts[-1]

            usernames.extend([
                f"{first}{last}",
                f"{first}_{last}",
                f"{first}.{last}",
                f"{last}{first}",
                f"{first[0]}{last}"
            ])

        return list(set(usernames))

    except Exception:

        return []