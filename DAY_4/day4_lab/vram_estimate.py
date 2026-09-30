import os
import platform
import subprocess
import ctypes
"""Day 4: estimate the memory a model needs, and whether it fits your machine.
Works seamlessly across macOS, Windows, and Linux.
"""
# Approximate bytes per parameter for common precisions (GGUF k-quants include
# a little block metadata, so these are effective rates, not the nominal bit depth).
BYTES_PER_PARAM = {
    "FP16":   2.00,
    "Q8_0":   1.00,
    "Q6_K":   0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}
# Rough KV-cache cost for a modern grouped-query-attention model with an FP16
# cache: about 0.02 GB for every 1B parameters per 1K tokens of context used.
# Older multi-head models can be several times higher. Treat this as an estimate.
KV_GB_PER_B_PER_1K = 0.02
OVERHEAD = 1.10          # runtime, activations and fragmentation: about 10%
def get_system_memory_gb():
    """Detect total physical RAM in GB across Windows, macOS, and Linux."""
    system_os = platform.system()
    # 1. Windows: Native Win32 API via ctypes (GlobalMemoryStatusEx)
    if system_os == "Windows":
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return round(stat.ullTotalPhys / (1024 ** 3), 1)
        except Exception:
            pass
        # Windows Fallback: wmic command
        try:
            out = subprocess.check_output(
                ["wmic", "computersystem", "get", "TotalPhysicalMemory"],
                stderr=subprocess.DEVNULL
            ).decode()
            lines = [line.strip() for line in out.splitlines() if line.strip().isdigit()]
            if lines:
                return round(int(lines[0]) / (1024 ** 3), 1)
        except Exception:
            pass
    # 2. macOS & Linux: os.sysconf
    try:
        pages = os.sysconf("SC_PHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
        return round((pages * page_size) / (1024 ** 3), 1)
    except (AttributeError, ValueError):
        pass
    # 3. macOS Fallback: sysctl hw.memsize
    if system_os == "Darwin":
        try:
            out = subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip()
            return round(int(out) / (1024 ** 3), 1)
        except Exception:
            pass
    # 4. Optional psutil library if installed
    try:
        import psutil  # type: ignore[import-not-found]
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except ImportError:
        pass
    # Default fallback if everything fails
    return 8.0
def get_gpu_vram_gb():
    """Detect dedicated GPU VRAM (NVIDIA / AMD) if available on Windows or Linux."""
    # Method 1: Check nvidia-smi
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        if out:
            # First GPU's memory in MB converted to GB
            first_gpu_mb = float(out.splitlines()[0])
            return round(first_gpu_mb / 1024, 1), "NVIDIA GPU (Dedicated VRAM)"
    except Exception:
        pass
    # Method 2: On Windows, query via WMIC for display adapter RAM
    if platform.system() == "Windows":
        try:
            out = subprocess.check_output(
                ["wmic", "path", "Win32_VideoController", "get", "AdapterRAM,Name"],
                stderr=subprocess.DEVNULL
            ).decode()
            for line in out.splitlines()[1:]:
                parts = line.strip().split()
                if parts and parts[0].isdigit():
                    bytes_val = int(parts[0])
                    # Ignore tiny values (< 512MB often basic display or shared)
                    if bytes_val > 512 * 1024 * 1024:
                        vram_gb = round(bytes_val / (1024 ** 3), 1)
                        gpu_name = " ".join(parts[1:]) if len(parts) > 1 else "Dedicated GPU"
                        return vram_gb, gpu_name
        except Exception:
            pass
    return None, None
def get_chip_info():
    """Retrieve chip/processor name across platforms."""
    system_os = platform.system()
    if system_os == "Darwin":
        try:
            return subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        except Exception:
            pass
    elif system_os == "Windows":
        try:
            return os.environ.get("PROCESSOR_IDENTIFIER", platform.processor() or "Windows PC")
        except Exception:
            pass
    return platform.processor() or platform.machine()
def estimate(params_b, precision="Q4_K_M", context_k=8):
    """Return (weights_gb, kv_gb, total_gb) for a model of params_b billion parameters."""
    if precision not in BYTES_PER_PARAM:
        raise ValueError(f"Unknown precision {precision}. Choose from {list(BYTES_PER_PARAM)}")
    weights_gb = params_b * BYTES_PER_PARAM[precision]
    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K
    total_gb = (weights_gb + kv_gb) * OVERHEAD
    return weights_gb, kv_gb, total_gb
def verdict(total_gb, available_gb):
    if total_gb <= available_gb * 0.7:
        return "fits comfortably"
    if total_gb <= available_gb:
        return "fits, but tight"
    return "does NOT fit"
def report(name, params_b, precision, context_k, available_gb):
    weights, kv, total = estimate(params_b, precision, context_k)
    v = verdict(total, available_gb)
    print(f"{name:<22} {precision:<7} {params_b:>5.1f}B  ctx {context_k:>3}K  "
          f"weights {weights:>6.2f} GB  kv {kv:>5.2f} GB  total {total:>6.2f} GB  "
          f"-> {v}")
    return v, total
if __name__ == "__main__":
    system_os = platform.system()
    total_ram_gb = get_system_memory_gb()
    chip_name = get_chip_info()
    os_name = f"{system_os} {platform.release()} ({platform.machine()})"
    # Detect hardware configuration (Dedicated GPU vs Apple Silicon Unified vs System RAM)
    gpu_vram_gb, gpu_name = get_gpu_vram_gb()
    if system_os == "Darwin":
        memory_type = "Apple Silicon Unified Memory (CPU + GPU Shared)"
        # On Mac Unified Memory, reserve ~25% for macOS and other running apps
        usable_gb = round(total_ram_gb * 0.75, 1)
        budget_explanation = f"{usable_gb} GB (reserving 25% for macOS & background apps)"
    elif gpu_vram_gb:
        memory_type = f"Discrete GPU: {gpu_name} ({gpu_vram_gb} GB VRAM)"
        # If running on dedicated GPU, we can use ~90% of dedicated VRAM
        usable_gb = round(gpu_vram_gb * 0.90, 1)
        budget_explanation = f"{usable_gb} GB (dedicated GPU VRAM minus driver overhead)"
    else:
        memory_type = "Standard System RAM (CPU Inference / Shared iGPU)"
        # On Windows/Linux running on CPU/RAM, reserve ~30% for Windows & apps
        usable_gb = round(total_ram_gb * 0.70, 1)
        budget_explanation = f"{usable_gb} GB (reserving 30% for {system_os} & apps)"
    print("=" * 72)
    print("                      SYSTEM HARDWARE DETECTION")
    print("=" * 72)
    print(f"OS:                 {os_name}")
    print(f"Processor:          {chip_name}")
    print(f"System RAM:         {total_ram_gb} GB")
    print(f"Memory Type:        {memory_type}")
    print(f"Recommended Budget: {budget_explanation}")
    print("=" * 72)
    print()
    models_to_test = [
        ("Qwen small", 1.5, "Q4_K_M", 8),
        ("Granite / Qwen mid", 8.0, "Q4_K_M", 8),
        ("Mid at FP16", 8.0, "FP16", 8),
        ("Large local (Command-R/Qwen)", 30.0, "Q4_K_M", 8),
        ("Server class (Llama 70B)", 70.0, "Q4_K_M", 8),
    ]
    print("--- MODEL COMPATIBILITY BENCHMARK ---")
    recommendations = []
    for name, params, prec, ctx in models_to_test:
        status, total = report(name, params, prec, ctx, usable_gb)
        if status in ("fits comfortably", "fits, but tight"):
            recommendations.append((name, params, prec, status, total))
    print("\nSame 8B model, different context lengths:")
    for context_k in (4, 8, 32, 128):
        report("8B agent", 8.0, "Q4_K_M", context_k, usable_gb)
    print("\nSame 8B model, different quantizations:")
    for precision in ("Q3_K_M", "Q4_K_M", "Q5_K_M", "Q8_0", "FP16"):
        report("8B agent", 8.0, precision, 8, usable_gb)
    print("\n" + "=" * 72)
    print("                    SUITABILITY RECOMMENDATION")
    print("=" * 72)
    if recommendations:
        best_model = recommendations[-1]
        print(f"Based on your hardware ({usable_gb} GB usable budget):")
        for name, params, prec, status, total in recommendations:
            symbol = "✓ [Ideal]" if status == "fits comfortably" else "⚠️ [Tight]"
            print(f"  {symbol} {name} ({params}B, {prec}) - Uses {total:.1f} GB ({status})")
        print(f"\n-> Recommended sweet spot for daily work: '{best_model[0]}' ({best_model[1]}B, {best_model[2]})")
    else:
        print(f"Available budget ({usable_gb} GB) is low. Consider smaller models (<= 3B Q4_K_M).")
    print("=" * 72)