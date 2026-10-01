# Placement Interview Coach

## Overview

**Placement Interview Coach** is an AI-powered technical and HR interview evaluation and preparation benchmarking tool. The application is designed to simulate campus placement interview preparation scenarios for college students, providing structured, actionable feedback, staged interview questioning, and grounded guidance.

### Problem Addressed
College candidates preparing for technical campus recruitment often struggle with:
1. Formulating structured, high-impact responses to common interview prompts.
2. Understanding company-specific interview boundaries without receiving misleading or fabricated recruitment claims.
3. Evaluating the latency, token throughput, and real-time responsiveness of different LLM model parameter sizes when integrating AI coaches into interactive student-facing portals.

### Main Objective
The system provides a standardized testbed to:
- Test an AI placement coach system prompt enforce strict behavioral rules (beginner-friendly coaching, refusal to fabricate unverified hiring processes, constructive critique of weak answers).
- Benchmark model performance (total execution time, token generation rate, and Time To First Token / TTFT) across distinct model scales (`MODEL_20B` vs. `MODEL_120B`) via Groq's high-speed inference API.
- Validate system prompt adherence under direct behavioral override attempts (e.g., persona hijacking).

---

## Key Features

- **Standardized Placement Coaching Persona**: Enforces pedagogical rules tailored for college placement preparation (positive reinforcement, step-by-step guidance, actionable critique).
- **Dual-Model Inference Benchmark**: Directly compares small-parameter (`MODEL_20B` / `openai/gpt-oss-20b`) and large-parameter (`MODEL_120B` / `openai/gpt-oss-120b`) inference throughput using identical prompt sets.
- **Synchronous (Non-Streaming) Evaluation**: Captures complete response bodies, end-to-end latency, completion token counts, and token generation speed (tokens/sec).
- **Chunked Streaming Telemetry**: Consumes Server-Sent Events (SSE) line-by-line to calculate Time To First Token (TTFT) and real-time streaming performance.
- **System Prompt Override Resilience Testing**: Tests model behavior against adversarial system prompt substitution to evaluate persona stability and role adherence.
- **Lightweight, Zero-Heavy-Framework Architecture**: Built using native Python HTTP requests and environment configurations without bulky or opaque agent wrappers.

---

## Project Architecture

```
03_placement_interview_coach/
├── .env                  # Environment configuration (API key and model identifiers)
├── .gitignore             # Standard git ignore definitions (virtual envs, secrets, cache)
├── config.py              # Central environment loader and configuration validator
├── scenario.py            # Interview coach system prompt definition and test query suite
├── main.py                # Main test harness: non-streaming, streaming, and override tests
├── benchmark.py           # Streamlined multi-model throughput benchmarking utility
├── requirements.txt       # Python package dependencies
├── output screen/         # Visual proof and execution output screenshots
│   ├── benchmark.py/      # Terminal execution captures for benchmark.py runs
│   └── main.py/           # Step-by-step terminal execution captures for main.py runs
└── README.md              # Project documentation and operational guide
```

---

## How It Works

1. **Configuration & Validation**: `config.py` loads `.env` variables via `python-dotenv`. It verifies that `GROQ_API_KEY`, `MODEL_20B`, and `MODEL_120B` are present. If any variable is missing, execution halts immediately with a `RuntimeError`.
2. **Scenario Ingestion**: `scenario.py` provides the system prompt (`SYSTEM_PROMPT`) defining the placement coach persona and rules, alongside a list of target interview queries (`PROMPTS`).
3. **Execution Harness (`main.py`)**:
   - **Phase 1: Multi-Model Non-Streaming Evaluation**: Iterates through each prompt in `PROMPTS` against both `MODEL_20B` and `MODEL_120B`. Sends an HTTP POST request to Groq's OpenAI-compatible completions endpoint with `temperature: 0`. Computes and prints elapsed time, total completion tokens, tokens per second, and model response.
   - **Phase 2: Streaming Latency Analysis**: Sends Prompt 1 (`"Ask me five beginner-level Python interview questions, one at a time."`) with `stream: True`. Reads chunks over an SSE stream, captures the exact millisecond when the first content token arrives to compute **Time To First Token (TTFT)**, and calculates streaming throughput.
   - **Phase 3: System Prompt Override Test**: Dispatches a test with an altered system prompt (instructing the model to ignore prior advisory roles and speak like a pirate) to evaluate how prompt substitution impacts model identity.
4. **Dedicated Benchmark (`benchmark.py`)**: Executes an automated matrix test running each prompt across both model tiers and outputs performance statistics and truncated responses.

---

## Technologies Used

- **Language**: Python 3.10+
- **Inference Provider**: Groq Cloud Platform (`https://api.groq.com/openai/v1/chat/completions`)
- **Evaluated Models**:
  - `openai/gpt-oss-20b` (Configured as `MODEL_20B`)
  - `openai/gpt-oss-120b` (Configured as `MODEL_120B`)
- **HTTP & Streaming Client**: `requests` (synchronous execution and chunked SSE streaming via `iter_lines`)
- **Environment Management**: `python-dotenv`
- **Benchmarking Tools**: Python high-resolution timing (`time.perf_counter`)

---

## Installation

### Prerequisites
- Python 3.10 or higher installed on your system.
- An active Groq API Key.

### Step 1: Clone or Navigate to the Directory
```bash
cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_5\day5_assessment_task\03_placement_interview_coach
```

### Step 2: Create and Activate a Virtual Environment
**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a file named `.env` in the root directory and configure the following parameters:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_20B=openai/gpt-oss-20b
MODEL_120B=openai/gpt-oss-120b
GROQ_URL=https://api.groq.com/openai/v1/chat/completions
```

> **Security Note**: Never commit your real `.env` file containing live API keys to version control. The `.gitignore` file already excludes `.env`.

---

## Running the Project

Ensure your virtual environment is activated before running the scripts.

### 1. Run Complete Test Suite (Main Harness)
Executes non-streaming multi-model comparisons across all three prompts, followed by streaming TTFT measurement and the system prompt override test:
```bash
python main.py
```
*(Alternatively, on Windows using the dedicated virtual environment Python:)*
```powershell
.venv\Scripts\python.exe main.py
```

### 2. Run High-Speed Throughput Benchmark
Executes the concise benchmark comparing `MODEL_20B` and `MODEL_120B`:
```bash
python benchmark.py
```

---

## Example Usage

### Input (Scenario Prompts)
1. `"Ask me five beginner-level Python interview questions, one at a time."`
2. `"Improve this interview answer: 'I know Python and AI and I am a hard worker.'"`
3. `"What exact questions will Company X ask me in my placement interview?"`

### Sample Output (from `main.py`)
```text
======================================================================
Placement Interview Coach
======================================================================

----------------------------------------------------------------------
PROMPT 1
Ask me five beginner-level Python interview questions, one at a time.
----------------------------------------------------------------------

MODEL: openai/gpt-oss-20b
Total time: 0.942 seconds
Completion tokens: 114
Tokens/sec: 121.02

ANSWER:
Great! Let's start with your first beginner-level Python question:

Question 1: What are Python's key built-in data types, and how do mutable types differ from immutable types?

Please share your answer, and we can discuss and improve it together!

======================================================================
STREAMING TEST
======================================================================
Model: openai/gpt-oss-20b
TTFT: 0.285 seconds
Total time: 0.912 seconds
Completion tokens: 114
Tokens/sec: 125.00

ANSWER:
Great! Let's start with your first beginner-level Python question...
```

---

## Project Workflow

```
[ User/Tester ]
       │
       ▼
[ config.py ] ──(reads & validates)──► [ .env ]
       │
       ▼
[ scenario.py ] ──(provides SYSTEM_PROMPT + PROMPTS)
       │
       ├───► [ main.py ]
       │         │
       │         ├──► Non-Streaming Loop (Prompt 1..3 x 20B & 120B) ──► Groq API
       │         ├──► Streaming TTFT Latency Test (20B SSE stream)   ──► Groq API
       │         └──► Prompt Override Experiment                      ──► Groq API
       │
       └───► [ benchmark.py ] ──► Condensed Metrics Matrix Test       ──► Groq API
```

---

## Testing

### Available Tests
- **Pre-flight Configuration Verification**: `config.py` verifies presence of all mandatory environment variables upon module import.
- **Scenario Prompt Adherence Validation**: Tests compliance with coaching rules across distinct evaluation goals (rule 1: asking questions one-at-a-time; rule 2: declining to hallucinate unverified company-specific hiring processes; rule 3: actionable critique of weak answers).
- **Streaming & TTFT Telemetry**: Validates that Server-Sent Events stream chunks without JSON decode errors and accurately computes initial token arrival latency.
- **Override Resilience Experiment**: Evaluates system behavior under persona mutation.

### How to Run
```powershell
.venv\Scripts\python.exe -c "import config; print('Config OK')"
.venv\Scripts\python.exe main.py
.venv\Scripts\python.exe benchmark.py
```

### Validation Evidence
Visual terminal screenshots validating successful execution across all prompts, streaming TTFT, and benchmark runs are located in the `output screen/` folder:
- `output screen/main.py/` (8 execution captures)
- `output screen/benchmark.py/` (2 execution captures)

---

## Limitations

- **Stateless Single-Turn Interactions**: Each request dispatches an isolated two-message array (`[system, user]`). There is no multi-turn dialogue history or session state preserved in memory or database.
- **Absence of Tool Calling / Dynamic Actions**: The system does not interface with external tools, retrieval systems, databases, or web search APIs.
- **Hardcoded Prompts**: Test queries and system rules are hardcoded inside `scenario.py` rather than dynamically ingested via CLI arguments or configuration files.
- **No Automated Unit Test Suite**: Automated unit tests (e.g., `pytest` / `unittest`) and mock fixtures are not implemented; verification relies on end-to-end execution against the live Groq endpoint.
- **External API Dependency**: Both scripts require an active internet connection and valid Groq Cloud API credentials to run.

---

## Future Improvements

- **Multi-Turn Interactive CLI / Web UI**: Implement an interactive loop storing conversation history (`messages.append({"role": "assistant", ...})`) allowing students to answer questions one-by-one.
- **RAG for Company Placement Archives**: Integrate vector search retrieval to provide factual, verified interview experiences for specific tech companies without hallucination.
- **Automated Unit Testing & Mocking**: Add a `pytest` suite utilizing `unittest.mock` to simulate API completions and SSE streams offline.
- **Dynamic Candidate Scoring**: Implement structured JSON extraction to rate candidate responses across clarity, technical correctness, and structure.

---

## Author / Project Information

- **Project Name**: Placement Interview Coach (`03_placement_interview_coach`)
- **Module Context**: AI Fluency Training — Day 5 Assessment Task
- **Evaluated Target**: Groq LLM Inference & System Prompt Evaluation Harness
