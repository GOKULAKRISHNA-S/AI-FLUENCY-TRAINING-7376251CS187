# Local LLM VRAM & System Memory Estimator

A cross-platform hardware detection and memory profiling tool for running Large Language Models (LLMs) locally. Built for **Day 4 of the AI Fluency Training**, this tool inspects host CPU architecture, physical RAM, and GPU VRAM to compute precision-aware model footprint benchmarks across varying context lengths and quantization levels.

---

## Overview

Deploying open-weights LLMs on local consumer and developer workstations requires matching model architecture, parameter count, quantization schemes, and context window demands against physical memory limitations. Under-provisioning memory leads to out-of-memory (OOM) crashes or aggressive OS swapping, degrading tokens-per-second throughput to near-zero.

This project solves the model provisioning and capacity planning problem by:
1. Detecting operating system details, processor architecture, physical RAM, and discrete GPU VRAM.
2. Calculating exact weight sizing across common GGUF/k-quantizations (`Q3_K_M` to `FP16`).
3. Estimating Key-Value (KV) cache allocation for Grouped-Query Attention (GQA) architectures across 4K to 128K context windows.
4. Applying a 10% runtime overhead margin (activations, memory fragmentation, CUDA/host runtimes).
5. Outputting a categorized hardware feasibility verdict (`fits comfortably`, `fits, but tight`, `does NOT fit`) and providing an optimal model recommendation for daily workloads.

---

## Key Features

- **Multi-OS Hardware Detection**:
  - **Windows**: Native Win32 API access using `ctypes` (`GlobalMemoryStatusEx`) with fallback to `wmic computersystem`. Dedicated VRAM inspection via `wmic path Win32_VideoController`.
  - **macOS (Darwin)**: Memory and CPU brand discovery via `os.sysconf` and `sysctl` (`hw.memsize`, `machdep.cpu.brand_string`).
  - **Linux**: Memory discovery via `os.sysconf` page-size calculations.
  - **NVIDIA GPU Support**: Direct query of dedicated VRAM via `nvidia-smi` CLI parsing.
- **Hardware-Specific Budget Allocations**:
  - *Apple Silicon Unified Memory*: Allocates 75% of total system RAM to model execution, reserving 25% for macOS and background applications.
  - *Discrete GPU*: Allocates 90% of dedicated VRAM, reserving 10% for driver and display surface overhead.
  - *Standard System RAM (CPU Inference / iGPU)*: Allocates 70% of physical RAM, reserving 30% for OS processes and applications.
- **Quantization Precision Profiles**:
  - Effective bytes-per-parameter mapping for `FP16` (2.00 B/param), `Q8_0` (1.00 B/param), `Q6_K` (0.81 B/param), `Q5_K_M` (0.68 B/param), `Q4_K_M` (0.57 B/param), and `Q3_K_M` (0.43 B/param), accounting for GGUF block metadata.
- **Dynamic KV-Cache Sizing**:
  - Estimates memory overhead for modern Grouped-Query Attention (GQA) models at 0.02 GB per 1 Billion parameters per 1,000 tokens of context.
- **Automated Sizing Benchmarks**:
  - Tiered model analysis from 1.5B (Qwen small) to 70B (Server-class Llama).
  - Context scaling analysis for 8B models across 4K, 8K, 32K, and 128K context lengths.
  - Quantization comparison for 8B models across 5 precision tiers.
- **Automated Suitability Recommendation**:
  - Selects the largest high-performing model that safely fits within the hardware budget.

---

## Project Architecture

```
day4_lab/
├── .venv/               # Virtual environment directory (optional / local)
├── requirements.txt     # Python package dependencies
├── vram_estimate.py     # Main hardware detection, estimation, and benchmarking engine
├── README.md            # Project overview and execution instructions
└── analysis.md          # In-depth technical, architectural, and mathematical analysis
```

---

## How It Works

The execution flow of [vram_estimate.py](file:///c:/Users/gokul/Documents/AI_FLUENCY_TRAINING/DAY_4/day4_lab/vram_estimate.py) operates in five distinct phases:

1. **Hardware Inspection**:
   - Detects host OS, CPU processor identifier, physical RAM, and any discrete GPU VRAM via native system libraries or system CLI tools.
2. **Budget Determination**:
   - Evaluates whether execution targets Apple Silicon Unified Memory, a discrete GPU, or System RAM (CPU/iGPU), establishing the safe maximum memory threshold (`usable_gb`).
3. **Memory Modeling**:
   - For any model configuration (Parameter count $P$ in billions, precision $b$, context $C$ in K tokens):
     $$\text{Weights (GB)} = P \times \text{BytesPerParam}(b)$$
     $$\text{KV Cache (GB)} = P \times C \times 0.02$$
     $$\text{Total Memory (GB)} = (\text{Weights} + \text{KV Cache}) \times 1.10$$
4. **Feasibility Evaluation**:
   - Evaluates total memory against `usable_gb`:
     - $\le 70\%$ usable budget: `fits comfortably`
     - $> 70\%$ and $\le 100\%$ usable budget: `fits, but tight`
     - $> 100\%$ usable budget: `does NOT fit`
5. **Reporting and Recommendations**:
   - Prints formatted tabular summaries and highlights the best fitting model for daily use.

---

## Technologies Used

- **Language**: Python 3.10+
- **Standard Library Modules**:
  - `ctypes`: Direct invocation of Windows Win32 API (`kernel32.dll` `GlobalMemoryStatusEx`).
  - `platform`: Cross-platform OS detection, release, machine architecture, and processor querying.
  - `subprocess`: Non-blocking invocation of hardware diagnostic utilities (`nvidia-smi`, `wmic`, `sysctl`).
  - `os`: Access to environment variables (`PROCESSOR_IDENTIFIER`) and POSIX memory page sizes (`os.sysconf`).
- **Dependencies** (from [requirements.txt](file:///c:/Users/gokul/Documents/AI_FLUENCY_TRAINING/DAY_4/day4_lab/requirements.txt)):
  - `openai>=1.40.0`: Required for standard AI Fluency training client interactions (reserved/shared across lab modules).
  - `python-dotenv>=1.0.0`: Environment variable management.
  - `requests`: HTTP networking library.
  - `psutil` *(optional fallback)*: Fallback memory detection if installed in environment.

---

## Installation

### Prerequisites
- Python 3.10 or higher installed.

### Setup Instructions

1. Navigate to the project directory:
   ```bash
   cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_4\day4_lab
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

No external API keys (e.g., `OPENAI_API_KEY`) or cloud services are strictly required to run [vram_estimate.py](file:///c:/Users/gokul/Documents/AI_FLUENCY_TRAINING/DAY_4/day4_lab/vram_estimate.py), as it executes purely offline against local hardware.

However, if using the environment across other training lab scripts sharing [requirements.txt](file:///c:/Users/gokul/Documents/AI_FLUENCY_TRAINING/DAY_4/day4_lab/requirements.txt):
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## Running the Project

Run the memory estimator script using the following command:

```bash
python vram_estimate.py
```

*Note on Windows Terminal Encoding*: Because the script outputs Unicode status symbols (`✓` and `⚠️`), Windows consoles operating under Windows-1252 / `cp1252` encoding should run:
```powershell
$env:PYTHONIOENCODING="utf-8"
python vram_estimate.py
```

---

## Example Usage and Output

Below is an authentic execution output captured from a standard Windows 11 workstation (Intel Core i5 / 8 GB physical RAM):

```text
========================================================================
                      SYSTEM HARDWARE DETECTION
========================================================================
OS:                 Windows 11 (AMD64)
Processor:          Intel64 Family 6 Model 140 Stepping 1, GenuineIntel
System RAM:         7.7 GB
Memory Type:        Standard System RAM (CPU Inference / Shared iGPU)
Recommended Budget: 5.4 GB (reserving 30% for Windows & apps)
========================================================================

--- MODEL COMPATIBILITY BENCHMARK ---
Qwen small             Q4_K_M    1.5B  ctx   8K  weights   0.85 GB  kv  0.24 GB  total   1.20 GB  -> fits comfortably
Granite / Qwen mid     Q4_K_M    8.0B  ctx   8K  weights   4.56 GB  kv  1.28 GB  total   6.42 GB  -> does NOT fit
Mid at FP16            FP16      8.0B  ctx   8K  weights  16.00 GB  kv  1.28 GB  total  19.01 GB  -> does NOT fit
Large local (Command-R/Qwen) Q4_K_M   30.0B  ctx   8K  weights  17.10 GB  kv  4.80 GB  total  24.09 GB  -> does NOT fit
Server class (Llama 70B) Q4_K_M   70.0B  ctx   8K  weights  39.90 GB  kv 11.20 GB  total  56.21 GB  -> does NOT fit

Same 8B model, different context lengths:
8B agent               Q4_K_M    8.0B  ctx   4K  weights   4.56 GB  kv  0.64 GB  total   5.72 GB  -> does NOT fit
8B agent               Q4_K_M    8.0B  ctx   8K  weights   4.56 GB  kv  1.28 GB  total   6.42 GB  -> does NOT fit
8B agent               Q4_K_M    8.0B  ctx  32K  weights   4.56 GB  kv  5.12 GB  total  10.65 GB  -> does NOT fit
8B agent               Q4_K_M    8.0B  ctx 128K  weights   4.56 GB  kv 20.48 GB  total  27.54 GB  -> does NOT fit

Same 8B model, different quantizations:
8B agent               Q3_K_M    8.0B  ctx   8K  weights   3.44 GB  kv  1.28 GB  total   5.19 GB  -> fits, but tight
8B agent               Q4_K_M    8.0B  ctx   8K  weights   4.56 GB  kv  1.28 GB  total   6.42 GB  -> does NOT fit
8B agent               Q5_K_M    8.0B  ctx   8K  weights   5.44 GB  kv  1.28 GB  total   7.39 GB  -> does NOT fit
8B agent               Q8_0      8.0B  ctx   8K  weights   8.00 GB  kv  1.28 GB  total  10.21 GB  -> does NOT fit
8B agent               FP16      8.0B  ctx   8K  weights  16.00 GB  kv  1.28 GB  total  19.01 GB  -> does NOT fit

========================================================================
                    SUITABILITY RECOMMENDATION
========================================================================
Based on your hardware (5.4 GB usable budget):
  ✓ [Ideal] Qwen small (1.5B, Q4_K_M) - Uses 1.2 GB (fits comfortably)

-> Recommended sweet spot for daily work: 'Qwen small' (1.5B, Q4_K_M)
========================================================================
```

---

## Project Workflow

```
[Start Execution]
       │
       ▼
[Detect System OS & CPU] ──> (ctypes / platform / sysctl)
       │
       ▼
[Detect Physical RAM & GPU VRAM] ──> (GlobalMemoryStatusEx / nvidia-smi / wmic)
       │
       ▼
[Compute Usable Memory Budget] ──> Apply 25% (Mac), 10% (GPU), or 30% (CPU) OS Headroom
       │
       ▼
[Simulate Model Footprints]
  ├── Multi-Model Scale: 1.5B, 8B, 30B, 70B
  ├── Context Scaling: 4K, 8K, 32K, 128K
  └── Quantization Levels: Q3_K_M, Q4_K_M, Q5_K_M, Q8_0, FP16
       │
       ▼
[Apply Verdict Classification]
  ├── <= 70% Budget  ──> "fits comfortably"
  ├── <= 100% Budget ──> "fits, but tight"
  └── > 100% Budget  ──> "does NOT fit"
       │
       ▼
[Generate Recommendation & Summary Output]
```

---

## Testing

- **Automated Test Suites**: Not implemented in the workspace (no `pytest` or `unittest` test suites are present).
- **Manual Verification & Testing**:
  - The script was executed end-to-end using Python 3.14 on Windows 11.
  - Validated native Win32 memory reporting accuracy (7.7 GB total physical RAM reported via `GlobalMemoryStatusEx`).
  - Validated fallback branches and calculation logic against manual mathematical derivations.
  - Validated character encoding constraints across terminal standard output streams.

---

## Limitations

1. **Static KV-Cache Heuristic**: Assumes a constant $0.02\text{ GB} / 1\text{B params} / 1\text{K ctx}$ based on modern Grouped-Query Attention (GQA) architectures. Older Multi-Head Attention (MHA) models (e.g., original LLaMA-1) consume significantly more KV memory.
2. **Fixed 10% Runtime Overhead**: Uses a static 1.10 multiplier for activations and fragmentation. In high-concurrency batch processing or extremely large activation tensors, actual overhead can exceed 15-20%.
3. **No CLI Arguments**: Model benchmarks and context windows are hardcoded inside the `if __name__ == "__main__":` block rather than accepting interactive flags or dynamic CLI inputs (`argparse`).
4. **Terminal Encoding Sensitivity**: The use of unicode literals (`✓` and `⚠️`) in terminal prints triggers a `UnicodeEncodeError` in standard Windows cmd shells defaulting to Windows-1252 unless `PYTHONIOENCODING=utf-8` or UTF-8 code pages (`chcp 65001`) are set.
5. **No Dynamic MoE (Mixture of Experts) Handling**: Treats parameter count uniformly as dense parameters. MoE architectures (e.g., Mixtral 8x7B) require full parameter sizing for weights but activate only a subset for computation.

---

## Future Improvements

1. **Interactive CLI / GUI**: Implement `argparse` or `click` to allow users to evaluate custom models (e.g., `--params 14 --precision Q5_K_M --context 16`).
2. **MoE Model Support**: Distinguish between total storage parameters and active parameters for accurate activation and compute modeling.
3. **Cross-Platform UTF-8 Handling**: Replace unicode checkmarks with ASCII fallbacks (`[PASS]` / `[WARN]`) or invoke `sys.stdout.reconfigure(encoding='utf-8')` to prevent encoding crashes on default Windows consoles.
4. **Comprehensive Unit Testing**: Implement unit test cases verifying mathematical accuracy, parameter lookup tables, and OS detection fallbacks using `pytest`.

---

## Author / Project Information

- **Program**: AI Fluency Training — Day 4 Lab
- **Author**: GOKULAKRISHNA-S
- **Workspace**: `AI-FLUENCY-TRAINING-7376251CS187`
