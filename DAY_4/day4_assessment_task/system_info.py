import platform
import shutil


def get_ram():

    try:

        import psutil

        memory = psutil.virtual_memory()

        return memory.total / (1024 ** 3)

    except ImportError:

        return None


def get_gpu_windows():

    try:

        import subprocess

        command = [
            "powershell",
            "-Command",
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,AdapterRAM"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as error:

        return str(error)


def main():

    print("=" * 70)
    print("DAY 4 — SYSTEM INFORMATION")
    print("=" * 70)

    print(
        "\nOperating System:",
        platform.system(),
        platform.release()
    )

    print(
        "Machine:",
        platform.machine()
    )

    print(
        "Processor:",
        platform.processor()
    )

    ram = get_ram()

    if ram:

        print(
            f"RAM: {ram:.2f} GB"
        )

    else:

        print(
            "RAM: Install psutil to read automatically."
        )

    print("\nGPU Information:")
    print("-" * 70)

    print(
        get_gpu_windows()
    )


if __name__ == "__main__":
    main()