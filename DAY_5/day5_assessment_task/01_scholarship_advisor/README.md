# Scholarship Advisor: LLM Inference & Benchmarking Pipeline

## Overview

The **Scholarship Advisor** project is an applied LLM evaluation and benchmarking suite designed to analyze, compare, and measure the performance of large language models acting in the domain-specific role of an academic and scholarship guidance advisor.

Students frequently navigate complex financial aid workflows that involve arithmetic discounts, strict eligibility rules, and rigorous documentation checklists. This project addresses the challenge of evaluating how models of different parameter scales (`openai/gpt-oss-20b` and `openai/gpt-oss-120b`, hosted via Groq's high-speed inference endpoints) handle:
1. **Mathematical reasoning**: Calculating net payable fees after applying percentage-based scholarship awards.
2. **Hallucination resistance**: Refusing to guarantee government awards without specific scheme guidelines.
3. **Structured synthesis**: Formulating comprehensive document verification checklists.
4. **Latency and throughput**: Measuring total round-trip time, tokens per second (TPS), and time-to-first-token (TTFT) across non-streaming and streaming modes.
5. **System prompt adherence & steerability**: Testing prompt injection/override robustness using a pirate persona override test.

---

## Key Features

- **Dual-Model Inference Comparison**: Evaluates and compares performance metrics between `MODEL_20B` (`openai/gpt-oss-20b`) and `MODEL_120B` (`openai/gpt-oss-120b`).
- **REST-Based Direct Inference**: Implements clean, low-overhead HTTP REST client calls to Groq's OpenAI-compatible completions API using Python `requests`.
- **Streaming & TTFT Measurement**: Measures Server-Sent Events (SSE) stream chunks to capture Time-To-First-Token (TTFT) and calculate streaming tokens per second.
- **Quantitative Performance Benchmarking**: Tracks response latency (seconds), completion token count, and generation throughput (tokens/sec) at `temperature=0` for reproducibility.
- **Rule-Constrained System Prompting**: Enforces 5 explicit operational rules (factual restraint, arithmetic disclosure, missing-information queries, and length limits).
- **System Prompt Override Stress-Testing**: Validates role steerability and override susceptibility using an adversarial persona switch experiment.

---

## Project Architecture

```text
01_scholarship_advisor/
├── .env                       # Environment configuration with API keys and model designations
├── .gitignore                 # Git ignore rules for virtual environments, secrets, and caches
├── requirements.txt           # Python package dependencies
├── config.py                  # Environment loader and configuration verification
├── scenario.py                # Domain definitions: system prompt, scenario name, and test prompts
├── main.py                    # Primary test harness: batch, streaming (TTFT), and override tests
├── benchmark.py               # Comparative benchmarking script outputting throughput metrics
└── output screen/             # Verified terminal execution capture screenshots
    ├── benchmark.py/          # Execution evidence for benchmark.py runs
    │   ├── Screenshot 2026-10-01 213738.png
    │   ├── Screenshot 2026-10-01 213744.png
    │   └── Screenshot 2026-10-01 213747.png
    └── main.py/               # Execution evidence for main.py runs
        ├── Screenshot 2026-10-01 213510.png
        ├── Screenshot 2026-10-01 213534.png
        ├── Screenshot 2026-10-01 213541.png
        ├── Screenshot 2026-10-01 213547.png
        └── Screenshot 2026-10-01 213552.png
```

---

## How It Works

1. **Configuration Initialization**: `config.py` loads environment variables (`GROQ_API_KEY`, `MODEL_20B`, `MODEL_120B`, `GROQ_URL`) using `python-dotenv`. It enforces fail-fast assertions if keys or model names are absent.
2. **Scenario Formulation**: `scenario.py` defines the scholarship advisor persona, the 5 operational constraints, and 3 standard test prompts covering math, eligibility inquiry, and document verification.
3. **Execution Modes**:
   - **Non-Streaming Inference (`main.py` / `benchmark.py`)**: Submits JSON payloads to the completions endpoint, records end-to-end wall-clock latency via `time.perf_counter()`, extracts token usage metrics from the JSON response, and calculates generation throughput.
   - **Streaming Inference (`main.py`)**: Opens a streaming HTTP connection (`stream=True`), iterates over SSE data chunks (`data: {...}`), captures the exact elapsed time when the first token content chunk arrives (TTFT), reconstructs the full message, and logs final streaming throughput.
   - **System Prompt Override Test (`main.py`)**: Dispatches a competing prompt directive instructing the model to disregard its advisor role and adopt a pirate persona, assessing model adherence under role conflicts.

---

## Technologies Used

- **Language**: Python 3.10+
- **Inference Provider**: Groq Cloud Platform (`https://api.groq.com/openai/v1/chat/completions`)
- **Language Models**:
  - `openai/gpt-oss-20b` (Configured as `MODEL_20B`)
  - `openai/gpt-oss-120b` (Configured as `MODEL_120B`)
- **HTTP Client**: `requests` (synchronous HTTP request dispatching and chunked streaming)
- **Environment Management**: `python-dotenv`
- **Benchmarking Tools**: Python standard library `time` (`time.perf_counter`) and `json`
- **Agent Framework**: None (Pure direct API integration without LangChain, LlamaIndex, or AutoGen)
- **External Tools / Function Calling**: Not implemented

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Git

### Setup Instructions

1. Clone or navigate to the project directory:
   ```bash
   cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_5\day5_assessment_task\01_scholarship_advisor
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

4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

Create a `.env` file in the root of the project directory. Populate it with the required settings:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_20B=openai/gpt-oss-20b
MODEL_120B=openai/gpt-oss-120b
GROQ_URL=https://api.groq.com/openai/v1/chat/completions
```

> **Note**: `GROQ_URL` defaults to `https://api.groq.com/openai/v1/chat/completions` if omitted, but `GROQ_API_KEY`, `MODEL_20B`, and `MODEL_120B` are strictly required by `config.py`.

---

## Running the Project

Ensure your virtual environment is active and `.env` is configured.

### 1. Run the Main Evaluation Harness
Executes prompt evaluations across both models, performs a streaming TTFT test, and runs the system prompt override experiment:

```powershell
python main.py
```

### 2. Run the Benchmark Script
Executes comparative throughput benchmarking across both models for all three evaluation prompts:

```powershell
python benchmark.py
```

---

## Example Usage

### Running `python benchmark.py`

#### Terminal Output:
```text
======================================================================
SCHOLARSHIP ADVISOR BENCHMARK
======================================================================

PROMPT:
A course costs Rs. 18,000 and I received a 15% scholarship. What amount should I pay? Show the calculation.

MODEL: openai/gpt-oss-20b
Time: 0.754 seconds
Tokens: 111
Tokens/sec: 147.22
Answer: **Calculation**

1. Scholarship amount:
   \(18,000 \times 0.15 = 2,700\)

2. Amount to pay:
   \(18,000 - 2,700 = 15,300\)

**You should pay Rs. 15,300.**

MODEL: openai/gpt-oss-120b
Time: 0.877 seconds
Tokens: 157
Tokens/sec: 179.10
Answer: **Calculation**

1. Find the scholarship amount:
   \(15\% \times 18{,}000 = 0.15 \times 18{,}000 = 2{,}700\) rupees

2. Subtract the scholarship from the full cost:
   \(18{,}000 - 2{,}700 = 15{,}300\) rupees

**Amount you need to pay:** **R
```

### Running Streaming Test in `python main.py`

#### Terminal Output:
```text
======================================================================
STREAMING TEST
======================================================================
Model: openai/gpt-oss-20b
TTFT: 0.496 seconds
Total time: 0.561 seconds
Completion tokens: 111
Tokens/sec: 197.88

ANSWER:
**Calculation**

1. Scholarship amount:
   \(18,000 \times 0.15 = 2,700\)

2. Amount to pay:
   \(18,000 - 2,700 = 15,300\)

**You should pay Rs. 15,300.**
```

---

## Project Workflow

```mermaid
flowchart TD
    A[Start: python main.py / benchmark.py] --> B[config.py: Load & Validate .env]
    B --> C[scenario.py: Load SYSTEM_PROMPT & PROMPTS]
    C --> D[Iterate Over Evaluation Prompts]
    
    subgraph NonStreamingPipeline [Non-Streaming Pipeline]
        D --> E[Construct HTTP POST Payload: stream=False, temp=0]
        E --> F[Send Request to Groq API via requests.post]
        F --> G[Parse JSON Response & usage metadata]
        G --> H[Calculate Latency, Token Count, and TPS]
        H --> I[Print Response Content and Metrics]
    end

    subgraph StreamingPipeline [Streaming Pipeline (main.py only)]
        I --> J[Construct HTTP POST Payload: stream=True]
        J --> K[Send Request to Groq API with stream=True]
        K --> L[Iterate SSE Chunks data: ... ]
        L --> M[Capture TTFT on First Content Chunk]
        M --> N[Accumulate Content Chunks & Extract usage]
        N --> O[Print TTFT, Total Time, and Streaming TPS]
    end

    subgraph OverridePipeline [Prompt Override Pipeline (main.py only)]
        O --> P[Inject Override System Prompt: Pirate Persona]
        P --> Q[Send Request with Prompt 1]
        Q --> R[Print Overridden Pirate Output]
    end
    
    R --> S[End Execution]
```

---

## Testing

- **Automated Test Suite (`pytest` / `unittest`)**: Not implemented.
- **Manual Verification**: Performed via command-line execution of `main.py` and `benchmark.py`.
- **Recorded Test Evidence**:
  - `output screen/main.py/`: 5 full-screen captures showing end-to-end execution of prompt evaluation, streaming TTFT analysis, and override validation.
  - `output screen/benchmark.py/`: 3 full-screen captures showing throughput, latency, and token generation benchmarks across both models.
- **Validation Scope**:
  1. Validates mathematical correctness in deduction formulas ($18,000 - 15\% = 15,300$).
  2. Validates refusal to give definitive false guarantees on eligibility queries without criteria.
  3. Validates document checklist formulation under length constraints.
  4. Validates model responsiveness and TTFT latency.

---

## Limitations

1. **No Autonomous Agent Loop**: The project is a linear inference pipeline. It does not implement multi-turn conversational memory, autonomous planning, or tool-calling loops.
2. **Deterministic Arithmetic Handled Entirely by LLM**: Calculations are performed by the generative neural network without external calculator verification or tool execution (e.g., Python execution sandbox).
3. **No Retries or Backoff Logic**: Network calls via `requests.post` lack retry mechanisms (e.g., `urllib3.util.retry.Retry`), leaving executions vulnerable to transient HTTP 429 or 503 errors.
4. **Synchronous Execution**: Requests are executed sequentially using blocking synchronous calls; concurrent evaluations using `asyncio` or `aiohttp` are not implemented.
5. **No Automated Test Framework**: Verification relies entirely on terminal execution inspection and screenshot captures without assert-based unit or integration test suites.
6. **Hardcoded Model Names**: Fixed to specific model configurations (`openai/gpt-oss-20b` and `openai/gpt-oss-120b`).

---

## Future Improvements

- **External Tool Integration**: Implement function calling for a verified arithmetic tool and live scholarship eligibility database lookups.
- **Async Execution**: Migrate from synchronous `requests` to asynchronous `httpx` or `aiohttp` for parallel model benchmarking.
- **Automated Evaluation Suite**: Build a `pytest` harness with evaluation assertions for hallucination rate, formatting compliance, and latency SLAs.
- **Dynamic Memory and Chat History**: Implement a stateful multi-turn conversational session allowing students to ask iterative follow-up questions.
- **Guardrails Framework**: Implement NeMo Guardrails or Llama Guard to prevent system prompt override exploits like the pirate persona override test demonstrated in `main.py`.

---

## Author / Project Information

- **Workspace / Repository**: `01_scholarship_advisor` (Part of `AI_FLUENCY_TRAINING / DAY_5 / day5_assessment_task`)
- **Author Identity**: GOKULAKRISHNA-S (`7376251CS187`)
- **Execution Environment**: Windows PowerShell, Python virtual environment (`.venv`), Groq Cloud API.
