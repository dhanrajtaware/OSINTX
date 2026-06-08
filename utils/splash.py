import os
import time


def clear_screen():

    os.system(
        "cls" if os.name == "nt" else "clear"
    )


def boot_sequence():

    clear_screen()

    modules = [
        "Recon Engine",
        "Correlation Engine",
        "Risk Engine",
        "Reporting Engine"
    ]

    print("\nInitializing OSINTX Core...\n")

    for module in modules:

        print(
            f"[BOOT] Loading {module}..."
        )

        time.sleep(0.4)

        print(
            f"[ OK ] {module} Loaded\n"
        )

    time.sleep(1)

    clear_screen()