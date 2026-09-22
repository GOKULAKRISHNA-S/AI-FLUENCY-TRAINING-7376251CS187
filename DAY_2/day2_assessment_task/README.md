# AI Fluency Training — Day 2: Reasoning, Agentic Tracing, and Prompting Evaluation

## Overview

This repository contains the Day 2 assessment project for the **AI Fluency Training** program. The project explores and evaluates foundational patterns in Large Language Model (LLM) reasoning and agentic workflows using the Groq API (OpenAI-compatible client) and Python.

### Problem Addressed
When solving complex multi-step reasoning problems—such as travel budget planning combined with environmental decision-making—plain zero-shot language model queries can suffer from arithmetic hallucinations, lack of transparency, inability to retrieve external facts, and inconsistent outputs across stochastic samplings.

### Main Objective
The primary objective of this project is to implement, compare, and analyze four core paradigms of modern LLM interaction:
1. **Direct Zero-Shot Prompting (`agent.py`)**: Querying the model without intermediate reasoning instructions or external tool access.
2. **Chain-of-Thought (CoT) Prompting vs. Direct Prompting (`cot_compare.py`)**: Comparing naive output generation against step-by-step reasoning constraints on identical arithmetic budget queries.
3. **Self-Consistency and Sampling Sensitivity (`self_consistency.py`)**: Evaluating the output stability and variation of the LLM across repeated runs at differing temperature settings (`temperature=0.7` vs. `temperature=0.0`).
4. **ReAct Paradigm Simulation (`react_trace.py`)**: Modeling an explicit, step-by-step **Reasoning + Acting (ReAct)** trace (`Thought -> Action -> Observation -> Thought -> Final Answer`) combining arithmetic cost calculation and contextual weather data retrieval tools.

---

## Key Features

- **Centralized Client & Configuration (`config.py`)**: Environment-based configuration using `python-dotenv` and the OpenAI Python SDK routed through Groq's low-latency API endpoint.
- **Deterministic Tool Modules (`tools.py`)**:
  - `calculate_trip_cost`: Computes categorized and aggregate travel expenses (travel, lodging, food, local transport).
  - `get_weather`: Deterministic dictionary lookup providing temperature, weather conditions, and rain probability for specified cities.
- **Direct Prompt Baseline (`agent.py`)**: Implements baseline query submission to measure zero-shot response quality.
- **Prompt Engineering Comparison (`cot_compare.py`)**: Head-to-head empirical comparison evaluating structural differences between direct prompt responses and explicit step-by-step Chain-of-Thought prompting.
- **Stochasticity & Consistency Benchmark (`self_consistency.py`)**: Executes 5-run sample sets at both exploratory (`0.7`) and deterministic (`0.0`) temperatures to observe formatting variance and numerical consistency.
- **Simulated ReAct Execution Trace (`react_trace.py`)**: A programmatic walkthrough of the ReAct pattern decomposing multi-modal constraints (financial budgeting + weather-based attire advice) into sequential thought, action, and observation states.
- **Execution Artifacts (`output_screen/`)**: Verified visual screenshots documenting terminal executions for all experimental scripts.

---

## Project Architecture

```
day2_assessment_task/
├── .env                  # Environment configuration (GROQ_API_KEY)
├── .gitignore            # Git ignore rules for virtualenvs, caches, and secrets
├── requirements.txt      # Python package dependencies (openai, python-dotenv)
├── config.py             # Groq client initialization and model definition
├── tools.py              # Tool definitions (calculate_trip_cost, get_weather)
├── agent.py              # Baseline zero-shot prompting script
├── cot_compare.py        # Direct vs. Chain-of-Thought prompt comparison
├── self_consistency.py   # Multi-run sampling experiment across temperatures
├── react_trace.py        # Programmatic ReAct reasoning-action trace simulation
├── README.md             # Project documentation and quickstart guide
├── analysis.md           # In-depth technical and academic evaluation document
└── output_screen/        # Captured terminal execution screenshots
    ├── cot_compare/      # Screenshots of cot_compare.py execution
    ├── react_trace/      # Screenshots of react_trace.py execution
    └── self_consistency/ # Screenshots of self_consistency.py execution
```

---

## How It Works

1. **Configuration Stage**:
   - `config.py` calls `load_dotenv()` to read `GROQ_API_KEY` from `.env`.
   - It validates that `GROQ_API_KEY` is present, raising a `ValueError` if missing.
   - It initializes an `OpenAI` client pointing to `https://api.groq.com/openai/v1` with model target `openai/gpt-oss-20b`.

2. **Direct Execution (`agent.py`)**:
   - Submits an unaugmented budget calculation question to the LLM via `client.chat.completions.create`.
   - The LLM performs end-to-end generation and outputs its answer directly to standard output.

3. **Comparative Evaluation (`cot_compare.py`)**:
   - Executes `direct_prompt()`: Submits the raw question.
   - Executes `reasoning_prompt()`: Appends explicit meta-prompts instructing the model to break calculations into clear steps and provide a concise reasoning summary followed by the final answer.
   - Prints both outputs side-by-side to compare structure and accuracy.

4. **Self-Consistency Experimentation (`self_consistency.py`)**:
   - Defines a standardized budget evaluation prompt.
   - Invokes `run_experiment(0.7)`: Queries the model 5 consecutive times at sampling temperature `0.7` to observe variance in formatting and numerical results.
   - Invokes `run_experiment(0.0)`: Queries the model 5 consecutive times at temperature `0.0` (greedy decoding) to observe determinism.

5. **ReAct Trace Workflow (`react_trace.py`)**:
   - Defines a dual-objective problem: determine if a 2-day Chennai trip fits a ₹10,000 budget and decide if an umbrella is needed.
   - **Step 1 (Thought)**: Identifies need for cost calculation and weather lookup.
   - **Step 2 & 3 (Action & Observation)**: Calls `calculate_trip_cost(...)` from `tools.py`; captures exact cost totals (`₹10,400`).
   - **Step 4 (Thought)**: Evaluates budget difference (`₹400 over`) and notes the remaining umbrella query.
   - **Step 5 & 6 (Action & Observation)**: Calls `get_weather("Chennai")`; retrieves temperature (`29°C`), condition (`Cloudy`), and rain probability (`60%`).
   - **Step 7 & Final Answer**: Reasons over the 60% precipitation risk to advise carrying an umbrella and outputs a structured final recommendation.

---

## Technologies Used

- **Language**: Python 3.10+ (tested on Python 3.14.7)
- **API Client**: `openai>=1.40.0` (OpenAI Python SDK configured for Groq endpoint compatibility)
- **Environment Management**: `python-dotenv>=1.0.0`
- **LLM Provider / Host**: Groq Cloud API (`https://api.groq.com/openai/v1`)
- **Model Identified**: `openai/gpt-oss-20b`
- **Prompting Paradigms**: Direct Zero-Shot, Chain-of-Thought (CoT), Temperature-driven Self-Consistency sampling
- **Tooling & Integration**: Custom deterministic Python functions (`tools.py`)

---

## Installation

### Prerequisites
- Python 3.10 or higher installed
- A valid Groq Cloud API Key

### Step-by-Step Setup

1. **Clone or Navigate to the Workspace Directory**:
   ```bash
   cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_2\day2_assessment_task
   ```

2. **Create and Activate a Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Variables

Create a file named `.env` in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Security Note**: Never commit your actual API keys to version control. The `.gitignore` file is pre-configured to ignore `.env`.

---

## Running the Project

Run any of the individual experiments or evaluation scripts from the activated virtual environment:

1. **Run the Direct Prompting Baseline**:
   ```powershell
   python agent.py
   ```

2. **Run the Direct Prompting vs. Chain-of-Thought Comparison**:
   ```powershell
   python cot_compare.py
   ```

3. **Run the Self-Consistency Experiment**:
   ```powershell
   python self_consistency.py
   ```

4. **Run the ReAct Reasoning Trace Simulation**:
   ```powershell
   python react_trace.py
   ```

---

## Example Usage

### Example 1: `react_trace.py` Output
```
============================================================
REACT AGENT TRACE
============================================================

QUESTION:
I am planning a 2-day trip to Chennai.
My budget is ₹10,000.
Travel = ₹2,000
Hotel per night = ₹2,500
Food per day = ₹1,200
Local transport per day = ₹500
Calculate whether the trip fits my budget.
Also check the available weather information
and tell me whether I should consider carrying an umbrella.

THOUGHT:
I need to calculate the total trip cost first. Then I need weather information for Chennai.

ACTION:
calculate_trip_cost(2000, 2500, 2, 1200, 2, 500)

OBSERVATION:
{'travel': 2000, 'hotel': 5000, 'food': 2400, 'local_transport': 1000, 'total': 10400}

THOUGHT:
The total cost is ₹10400, which is ₹400 above the budget.
I still need weather information to answer the umbrella question.

ACTION:
get_weather('Chennai')

OBSERVATION:
{'temperature': '29°C', 'condition': 'Cloudy', 'rain_probability': '60%'}

THOUGHT:
The weather information shows Cloudy conditions and a 60% rain probability.
Therefore, carrying an umbrella would be a reasonable precaution.

FINAL ANSWER:
The estimated 2-day trip cost is ₹10400.
The trip exceeds the ₹10,000 budget by ₹400.
The weather tool reports Cloudy conditions at 29°C with a 60% rain probability.
Carrying an umbrella would be a reasonable precaution.
```

### Example 2: `cot_compare.py` Output Summary
- **Direct Prompting**: Produces a summary breakdown table and advises on budget adjustment options.
- **Chain-of-Thought**: Produces an explicit item-by-item calculation (`Travel: ₹2,000`, `Hotel: 2 nights * ₹2,500 = ₹5,000`, `Food: 2 days * ₹1,200 = ₹2,400`, `Transport: 2 days * ₹500 = ₹1,000`, `Total: ₹10,400`), explicitly followed by budget difference deduction and a concluding verdict.

---

## Project Workflow

```
               [ User Task / Question ]
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   [ agent.py ]   [ cot_compare.py ] [ self_consistency.py ]
         │                │                │
  Single zero-shot   Direct vs CoT    5 Runs @ T=0.7
    LLM API Call     API comparisons  5 Runs @ T=0.0
         │                │                │
         └────────────────┼────────────────┘
                          ▼
             [ Groq LLM API Server ]
                          │
                          ▼
            [ LLM Generative Response ]
                          
──────────────────────────────────────────────────────────
            [ Simulated ReAct Agentic Loop ]
                  ( react_trace.py )
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
         [ Thought 1 ]       [ Thought 2 ]
                │                   │
         [ Action 1 ]        [ Action 2 ]
                │                   │
       calculate_trip_cost()   get_weather()
         ( tools.py )         ( tools.py )
                │                   │
        [ Observation 1 ]   [ Observation 2 ]
                └─────────┬─────────┘
                          ▼
                   [ Final Answer ]
```

---

## Testing

- **Automated Test Suite**: Not implemented (no `pytest`, `unittest`, or test runner configuration files exist in the project).
- **Manual Verification Scripts**: The project relies on script-level runtime execution (`agent.py`, `cot_compare.py`, `react_trace.py`, `self_consistency.py`) which output execution traces directly to standard output.
- **Visual Validation Evidence**: Screen recordings and terminal execution captures are permanently logged in `output_screen/`:
  - `output_screen/cot_compare/`: Validates prompt execution and formatting.
  - `output_screen/react_trace/`: Validates accurate tool calculations and trace sequence.
  - `output_screen/self_consistency/`: Validates consistency across multiple temperature iterations.

---

## Limitations

1. **Simulated ReAct Loop**: `react_trace.py` is a hardcoded procedural simulation of a ReAct trace; it does not dynamically invoke LLM function-calling or an autonomous model loop.
2. **Missing Automated Consensus / Voting**: `self_consistency.py` generates 5 responses per temperature setting but lacks automated majority-vote aggregation or string/JSON extraction logic.
3. **Hardcoded Tool Data**: `tools.py` uses a static dictionary for weather data covering only three cities (Chennai, Bangalore, Coimbatore); queries for other cities return `"Unknown"`.
4. **No Dynamic Input Handling**: All trip budgets, durations, and itemized costs are hardcoded string constants within each script rather than accepting CLI arguments or interactive user prompts.
5. **No Model Fallbacks or Retry Logic**: API requests do not implement exponential backoff, rate-limit retries, or alternate model failover.

---

## Future Improvements

- **Autonomous Agent Implementation**: Integrate dynamic tool-calling using OpenAI function schemas (`tools=[...]`) so the LLM decides autonomously when and how to call `calculate_trip_cost` and `get_weather`.
- **Dynamic User Interface / CLI**: Support interactive CLI arguments (e.g., via `argparse` or `click`) or a lightweight UI (Streamlit/FastAPI) allowing arbitrary trip itineraries and budgets.
- **Live API Integration**: Replace static dictionary lookups in `tools.py` with real-time weather APIs (e.g., Open-Meteo or OpenWeatherMap).
- **Automated Self-Consistency Aggregation**: Implement regular expression or JSON-based response extraction coupled with majority-voting algorithms to compute statistical confidence.
- **Formal Unit Testing**: Add unit tests via `pytest` for `tools.py` functions and mocked API tests for network-dependent modules.

---

## Author / Project Information

- **Author**: GOKULAKRISHNA-S (`gokulakrishzna.s@gmail.com`)
- **Training Module**: AI Fluency Training — Day 2 Assessment
- **Repository**: `GOKULAKRISHNA-S/AI-FLUENCY-TRAINING-7376251CS187`
- **Commit Reference**: `b68c56d` ("AI FLUENCY TRAINING")
