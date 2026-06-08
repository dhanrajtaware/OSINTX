def write_report(results, filename):

    with open(filename, "w", encoding="utf-8") as f:

        f.write("OSINTX REPORT\n")
        f.write("=" * 40)
        f.write("\n\n")

        for section, data in results.items():

            f.write(f"[{section.upper()}]\n")

            if isinstance(data, dict):

                for key, value in data.items():
                    f.write(
                        f"{key}: {value}\n"
                    )

            else:
                f.write(f"{data}\n")

            f.write("\n")