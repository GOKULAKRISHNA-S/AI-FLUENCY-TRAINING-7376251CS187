import shutil
import subprocess


def run_command(command):

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as error:

        return f"ERROR: {error}"


def main():

    print("=" * 80)
    print("DAY 4 — OLLAMA CHECK")
    print("=" * 80)

    ollama = shutil.which("ollama")

    if ollama is None:

        print(
            "\nOllama was not found in PATH."
        )

        print(
            "Install Ollama first, then reopen PowerShell."
        )

        return

    print(
        "\nOllama executable:",
        ollama
    )

    print("\nOllama Version")
    print("-" * 80)

    print(
        run_command(
            ["ollama", "--version"]
        )
    )

    print("\nInstalled Models")
    print("-" * 80)

    print(
        run_command(
            ["ollama", "list"]
        )
    )

    print("\nRunning Models")
    print("-" * 80)

    print(
        run_command(
            ["ollama", "ps"]
        )
    )


if __name__ == "__main__":
    main()