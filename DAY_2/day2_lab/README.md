# AI Fluency Training: Day 2 Lab — Reasoning Techniques and Agentic Workflows

## Overview

This repository contains the implementation and experimental evaluation for Day 2 of the AI Fluency Training program. The project investigates how advanced prompt engineering paradigms and agentic reasoning architectures overcome the inherent limitations of standard Large Language Models (LLMs)—specifically hallucinations, arithmetic inaccuracies, and inability to query private external data.

The project demonstrates three progressive AI paradigms:
1. **Chain-of-Thought (CoT) Reasoning**: Forcing explicit intermediate reasoning steps to improve problem-solving accuracy over direct zero-shot generation.
2. **Self-Consistency Sampling**: Running multiple diverse reasoning paths at higher temperature and aggregating candidate answers via majority voting.
3. **ReAct AI Agent with Tool Calling**: Combining reasoning and acting in a multi-turn autonomous execution loop equipped with external tools (a private database retriever and an AST-based arithmetic calculator).

---

## Key Features

- **Multi-Provider LLM Configuration**: Centralized API client supporting local deployment via Ollama and cloud inference via Groq or Hugging Face through OpenAI-compatible interfaces.
- **AST-Based Safe Calculator Tool**: Secure mathematical expression evaluation using Python's Abstract Syntax Tree (`ast`), rejecting dangerous arbitrary execution such as `eval()`.
- **Domain-Specific Tool Integration**: Private mock database lookup tool (`get_course_fee`) mapping course codes (`CS101`, `AI202`, `DS303`) to proprietary fee structures.
- **Autonomous Multi-Step ReAct Agent Loop**: Iterative model-tool loop implementing tool-call dispatch, argument parsing, Groq metadata sanitization, observation feedback, and configurable step bounds (`max_steps`).
- **Chain-of-Thought Comparison Harness**: Side-by-side benchmarking comparing direct answer generation against structured, numbered step-by-step reasoning across arithmetic, counting, and logic tasks.
- **Self-Consistency Majority Voting Engine**: Stochastic multi-path generator sampling candidate responses at non-zero temperature (`0.8`) with automated regex-free answer extraction and frequency aggregation via `collections.Counter`.
- **ReAct Execution Tracing**: Dedicated trace harness exposing the step-by-step reasoning, action dispatch, and observation progression for complex comparative queries.

---

## Project Architecture

```
day2_lab/
├── .env                       # Local environment configuration (API keys & provider settings)
├── .gitignore                  # Git exclusions (.env, .venv, __pycache__, etc.)
├── agent.py                   # ReAct agent loop implementation and fee assistant evaluation
├── config.py                  # Client setup, provider switching, private course fee data, queries
├── cot_compare.py             # Direct vs. Chain-of-Thought comparison script
├── react_trace.py             # Trace script demonstrating multi-step agent reasoning
├── requirements.txt           # Python dependencies (openai, python-dotenv)
├── self_consistency.py        # Self-consistency majority voting over CoT samples
├── tools.py                   # Tool definitions, schemas, and safe AST evaluation engine
└── output_screen/             # Verified execution output screenshots
    ├── cot_compare/           # Execution screenshots for cot_compare.py
    │   ├── Screenshot 2026-09-22 211719.png
    │   └── Screenshot 2026-09-22 211734.png
    ├── react_trace/           # Execution screenshot for react_trace.py
    │   └── Screenshot 2026-09-22 211856.png
    └── self_resistency/       # Execution screenshot for self_consistency.py
        └── Screenshot 2026-09-22 211935.png
```

---

## How It Works

The repository operates through three distinct execution workflows:

### 1. Chain-of-Thought Comparison (`cot_compare.py`)
1. Loads benchmark reasoning questions covering multi-step arithmetic, combination counting, and relational ordering.
2. Queries the model with `DIRECT_PROMPT` (`temperature=0`) instructing it to output only the final answer without reasoning.
3. Queries the model with `COT_PROMPT` (`temperature=0`) instructing it to decompose the problem into numbered steps and append `Final Answer: <answer>`.
4. Outputs the direct response alongside the step-by-step trace to contrast reasoning depth and intermediate verification.

### 2. Self-Consistency Sampling (`self_consistency.py`)
1. Submits a reasoning question to the LLM using the Chain-of-Thought prompt across $N=5$ independent stochastic completions at `temperature=0.8`.
2. Extracts the final answer string from each completion by scanning from the bottom of the response for the `Final Answer:` prefix.
3. Aggregates the extracted candidates using `collections.Counter`.
4. Selects the most frequent answer as the consensus winner.

### 3. ReAct Autonomous Agent Loop (`agent.py` & `react_trace.py`)
1. Initializes conversation memory with a system prompt detailing available tools, constraints, and the user's inquiry.
2. Invokes the LLM with tool schemas (`get_course_fee`, `calculator`).
3. Evaluates model response:
   - If the model produces direct text without tool calls, the loop terminates and returns the response.
   - If the model requests one or more tool calls, the assistant's request is recorded into memory.
4. Executes the requested tools locally:
   - Strips channel artifacts if present (e.g. `<|...|>`).
   - Parses JSON arguments and invokes matching functions in `TOOL_FUNCTIONS`.
   - Captures string outputs as observations.
5. Appends tool results with `role: "tool"` and the corresponding `tool_call_id` to the conversation history.
6. Re-invokes the LLM with the updated history. The cycle repeats until the agent concludes reasoning or hits `max_steps`.

---

## Technologies Used

- **Language**: Python 3.10+
- **LLM Providers Supported**:
  - **Groq** (`https://api.groq.com/openai/v1`) — Cloud inference (default active in lab)
  - **Ollama** (`http://localhost:11434/v1`) — Local inference
  - **Hugging Face** (`https://router.huggingface.co/v1`) — Serverless inference router
- **Default Models**:
  - Groq / Hugging Face: `openai/gpt-oss-20b`
  - Ollama: `qwen2.5:1.5b`
- **Core Libraries**:
  - `openai>=1.40.0`: Unified client for OpenAI-compatible inference and function calling
  - `python-dotenv>=1.0.0`: Environment variable management
- **Standard Library Modules**:
  - `ast` and `operator`: Safe mathematical AST parsing and binary/unary operation evaluation
  - `json`: Tool argument decoding
  - `collections.Counter`: Frequency tabulation for majority voting

---

## Installation

### Prerequisites
- Python 3.10 or higher installed.
- Valid API credentials for Groq or Hugging Face, or a local running Ollama instance.

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```powershell
   cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_2\day2_lab
   ```

2. **Create and activate a virtual environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
     .\.venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

---

## Environment Variables

Create a `.env` file in the root of the project directory based on your chosen provider:

```ini
# Provider selection: "groq", "ollama", or "huggingface"
PROVIDER=groq

# API Key corresponding to the provider
GROQ_API_KEY=your_groq_api_key_here

# Optional: HF_TOKEN if PROVIDER=huggingface
# HF_TOKEN=your_huggingface_token_here

# Model identifier
MODEL=openai/gpt-oss-20b
```

> [!CAUTION]
> Never commit your real API keys or `.env` file to version control. The `.gitignore` file is configured to exclude `.env`.

---

## Running the Project

Ensure the virtual environment is activated before executing any script.

### 1. Test Tools Engine
Run sanity checks on the safe calculator and fee lookup dictionary:
```powershell
python tools.py
```

### 2. Run Chain-of-Thought Comparison
Run the side-by-side prompt engineering experiment:
```powershell
python cot_compare.py
```

### 3. Run Self-Consistency Majority Voting
Sample multiple stochastic reasoning chains and aggregate consensus:
```powershell
python self_consistency.py
```

### 4. Run AI Agent Evaluation
Run the autonomous ReAct agent across the standard test queries:
```powershell
python agent.py
```

### 5. Run ReAct Trace Demonstration
Inspect a detailed step-by-step action and observation trace for a multi-step query:
```powershell
python react_trace.py
```

---

## Example Usage

### 1. ReAct Agent Trace Output (`python react_trace.py`)
```
QUESTION: Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much? 

--- the agent's actions and observations ---
   step 1: get_course_fee({'course_code': 'CS101'}) -> 12000
   step 2: get_course_fee({'course_code': 'AI202'}) -> 18000
   step 3: get_course_fee({'course_code': 'DS303'}) -> 15000
   step 4: calculator({'expression': '45000*0.75'}) -> 33750.0
   step 5: calculator({'expression': '33750-27000'}) -> 6750

FINAL ANSWER: The pair **CS101 + AI202** with the 10 % scholarship is cheaper.

- **CS101 + AI202 (10 % scholarship)**: ₹27 000
- **CS101 + AI202 + DS303 (25 % scholarship)**: ₹33 750

**Difference**: ₹6 750.
```

### 2. Self-Consistency Output (`python self_consistency.py`)
```
=== SELF-CONSISTENCY | provider: groq | model: openai/gpt-oss-20b ===

QUESTION: A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs. 15,000. She gets a 15% scholarship on the total and pays the rest in 4 equal instalments. How much is each instalment?

   run 1: ** Rs. 9,562.50 per instalment.
   run 2: 9562.50
   run 3: ** 9,562.50 rupees per instalment.
   run 4: ** Rs. 9,562.50 per instalment.
   run 5: 9,562.50 rupees per instalment.

Majority answer (2 of 5 runs): ** Rs. 9,562.50 per instalment.
```

---

## Project Workflow

```
[ User Inquiry ]
       │
       ▼
[ config.py: Provider & Model Initialized ]
       │
       ├─────────────────────────┬─────────────────────────┐
       │                         │                         │
       ▼                         ▼                         ▼
[ cot_compare.py ]      [ self_consistency.py ]       [ agent.py / react_trace.py ]
 Direct vs CoT           Sample 5 Paths (T=0.8)        ReAct Loop (max_steps=6..8)
 Prompting               Extract Final Answer          LLM Reasoning & Tool Calls
 Zero-Shot vs Steps      Counter Majority Vote         Tool Dispatch -> tools.py
                                                       Return Final Synthesis
```

---

## Testing

- **Automated Unit Testing Framework**: *Not implemented*. (No `pytest` or `unittest` suite exists in the project).
- **Embedded Script Verifications**:
  - `tools.py`: Validates uppercase/lowercase key handling in `get_course_fee` and operator precedence in `calculator`.
  - `cot_compare.py`: Validates model capability on arithmetic, counting, and logic problems under different prompting schemes.
  - `self_consistency.py`: Validates stability of mathematical extraction across multiple runs.
  - `agent.py`: Validates tool dispatch and direct non-tool completion handling.

---

## Limitations

1. **Exact String Match Sensitivity in Self-Consistency**: Majority voting in `self_consistency.py` uses raw string matching (`Counter(answers)`). As observed during execution, semantically identical answers with minor variations (e.g. `9562.50` vs `** Rs. 9,562.50 per instalment.`) fail to cluster together.
2. **Fixed Hardcoded Knowledge Base**: Course fees are stored in an in-memory dictionary in `config.py` rather than a persistent database or dynamic API.
3. **No Retries or Backoff**: Network or rate-limit errors during LLM inference are not caught with retry loops.
4. **Hardcoded Step Bounds**: The ReAct agent enforces a fixed ceiling (`max_steps=6` or `8`). Tasks requiring additional iterations will terminate abruptly.
5. **No Parallel Tool Execution**: Although the OpenAI API supports parallel tool calling, tool executions are processed sequentially in a single synchronous loop.

---

## Future Improvements

- **Numeric & Semantic Answer Normalization**: Implement regex or numerical parsing in `self_consistency.py` to extract float values prior to running `Counter`.
- **Database Backend Integration**: Replace `COURSE_FEES` dictionary with SQLite or PostgreSQL database queries via parameterized tools.
- **Dynamic Step Limits and Exponential Backoff**: Add resilience mechanisms around OpenAI API calls using `tenacity`.
- **Automated Regression Suite**: Introduce formal unit and integration test suites using `pytest`.

---

## Author / Project Information

- **Author**: GOKULAKRISHNA-S (`gokulakrishzna.s@gmail.com`)
- **Program**: AI Fluency Training — Day 2 Lab
- **Repository Branch**: `main`
