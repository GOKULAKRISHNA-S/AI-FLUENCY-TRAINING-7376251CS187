# Project Analysis: Reasoning, Prompting Paradigms, and Agentic Tracing

## 1. Problem Statement

### 1.1 The Practical Problem
Multi-step travel planning presents a classic compound decision-making problem. A traveler must evaluate a financial constraint (determining whether itemized travel, lodging, daily meals, and local commuting fit within a ₹10,000 ceiling) alongside environmental variables (checking regional meteorological conditions to determine whether to pack weather-protection gear such as an umbrella). 

### 1.2 Why the Problem Matters in LLM Engineering
When standard Large Language Models (LLMs) are tasked with such compound problems via direct prompting, they are susceptible to several established failure modes:
1. **Arithmetic Hallucination**: Autoregressive transformers predict token sequences based on statistical distributions rather than executing formal arithmetic. Without chain-of-thought scratchpads or external calculators, intermediate calculation errors frequently accumulate.
2. **Knowledge Cutoff and Grounding Gaps**: LLMs cannot reliably know real-time or localized external data (such as city-specific weather forecasts) without tool augmentation or retrieval mechanisms.
3. **Stochastic Inconsistency**: Variations in sampling hyperparameters (e.g., temperature) cause models to produce differing response formats, intermediate steps, and reasoning chains across repeated invocations.
4. **Lack of Auditability**: Monolithic zero-shot responses obscure the decision-making process, making it impossible for evaluators or downstream software agents to verify the intermediate steps leading to a conclusion.

### 1.3 What the Project Demonstrates
This project implements an empirical laboratory in Python to systematically examine how different prompting methodologies and agentic reasoning abstractions address these failure modes using the Groq API (`openai/gpt-oss-20b`). Specifically, it compares:
- Direct Zero-Shot Prompting (`agent.py`)
- Chain-of-Thought (CoT) Step-by-Step Prompting (`cot_compare.py`)
- Stochastic Self-Consistency Sampling across Temperatures (`self_consistency.py`)
- Explicit ReAct (Reasoning + Acting) Decomposition with Deterministic Tools (`react_trace.py` and `tools.py`)

---

## 2. Objective

The primary technical objective is to benchmark, demonstrate, and document the mechanics of reasoning and agentic problem decomposition. Specifically:
- **Zero-Shot Prompting**: Observe baseline model behavior when given raw arithmetic and constraint verification questions without guidance.
- **Chain-of-Thought Conditioning**: Test whether appending meta-prompting constraints ("Break the calculation into clear steps. Provide a concise reasoning summary followed by the final answer.") forces the model to externalize intermediate mathematical deductions before outputting a verdict.
- **Temperature & Consistency Analysis**: Quantify how sampling temperature ($T = 0.7$ vs. $T = 0.0$) impacts response syntax, tabular formatting, and semantic correctness across multiple identical queries.
- **Agentic Workflow Modeling**: Model an end-to-end ReAct loop combining internal reasoning states (`THOUGHT`), deterministic external actions (`ACTION`), and environmental feedback (`OBSERVATION`) to solve a composite task requiring both arithmetic computation and tool-grounded fact retrieval.

---

## 3. Project Architecture

The codebase is organized into modular Python scripts separating configuration, tool definitions, experimental evaluations, and captured artifacts.

```
day2_assessment_task/
├── config.py             # Centralized environment and client configuration
├── tools.py              # External deterministic computation & data tools
├── agent.py              # Zero-shot baseline prompting script
├── cot_compare.py        # Direct vs. Chain-of-Thought comparative experiment
├── self_consistency.py   # Multi-run temperature stability benchmark
├── react_trace.py        # Simulated ReAct reasoning and acting workflow
├── requirements.txt      # Dependency specification
├── .env                  # Environment variable configuration (git-ignored)
├── .gitignore            # Git exclusion definitions
├── README.md             # Project overview and runbook
├── analysis.md           # In-depth technical evaluation document
└── output_screen/        # Verified execution screenshots
    ├── cot_compare/      # Terminal output captures for cot_compare.py
    ├── react_trace/      # Terminal output captures for react_trace.py
    └── self_consistency/ # Terminal output captures for self_consistency.py
```

### Component Breakdown

### `config.py`
- **Purpose**: Centralizes API credential loading, runtime validation, and client initialization.
- **Main Components**:
  - `load_dotenv()`: Ingests environment variables from `.env`.
  - `API_KEY = os.getenv("GROQ_API_KEY")`: Retrieves Groq authentication key.
  - Runtime guard: Raises `ValueError("GROQ_API_KEY is missing. Add it to the .env file.")` if unassigned.
  - `client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")`: Instantiates an OpenAI SDK client pointed at Groq's low-latency inference endpoint.
  - `MODEL = "openai/gpt-oss-20b"`: Constant declaring the target model identifier.
- **Inputs**: `.env` file containing `GROQ_API_KEY`.
- **Outputs**: Exported `client` object and `MODEL` string.
- **Dependencies**: `os`, `dotenv` (`python-dotenv`), `openai.OpenAI`.
- **Interaction**: Imported by `agent.py`, `cot_compare.py`, and `self_consistency.py`.

### `tools.py`
- **Purpose**: Defines deterministic helper functions that offload arithmetic calculation and external state retrieval away from the LLM.
- **Main Functions**:
  1. `calculate_trip_cost(travel_cost, hotel_per_night, nights, food_per_day, days, local_transport_per_day)`:
     - Calculates:
       $$\text{hotel\_cost} = \text{hotel\_per\_night} \times \text{nights}$$
       $$\text{food\_cost} = \text{food\_per\_day} \times \text{days}$$
       $$\text{transport\_cost} = \text{local\_transport\_per\_day} \times \text{days}$$
       $$\text{total\_cost} = \text{travel\_cost} + \text{hotel\_cost} + \text{food\_cost} + \text{transport\_cost}$$
     - Returns dictionary: `{"travel": ..., "hotel": ..., "food": ..., "local_transport": ..., "total": ...}`.
  2. `get_weather(city)`:
     - Queries an internal static dictionary containing meteorological profiles for `"Chennai"`, `"Bangalore"`, and `"Coimbatore"`.
     - Returns: `{"temperature": ..., "condition": ..., "rain_probability": ...}`. Defaults to `"Unknown"` fields if the city is not found.
- **Inputs**: Numerical cost values, integers representing trip duration, and string city names.
- **Outputs**: Structured Python dictionaries.
- **Dependencies**: Pure standard Python (no external dependencies).
- **Interaction**: Imported and called by `react_trace.py`.

### `agent.py`
- **Purpose**: Implements the baseline direct zero-shot prompting strategy.
- **Main Components**:
  - `QUESTION`: String constant detailing a 2-day Chennai trip budget query.
  - `client.chat.completions.create(...)`: Direct single-turn inference call.
- **Inputs**: Hardcoded prompt string.
- **Outputs**: Prints LLM response directly to standard output.
- **Dependencies**: `config.client`, `config.MODEL`.
- **Interaction**: Acts as the unassisted benchmark against which CoT and ReAct are evaluated.

### `cot_compare.py`
- **Purpose**: Runs a controlled comparative test between direct prompting and zero-shot Chain-of-Thought prompting on identical input.
- **Main Functions**:
  - `direct_prompt()`: Submits raw `QUESTION` to `MODEL`.
  - `reasoning_prompt()`: Appends step-by-step reasoning instructions to `QUESTION` before submission.
- **Inputs**: Shared `QUESTION` string.
- **Outputs**: Terminal output displaying both generated responses side-by-side.
- **Dependencies**: `config.client`, `config.MODEL`.
- **Interaction**: Tests prompting efficacy without modifying backend model parameters.

### `self_consistency.py`
- **Purpose**: Evaluates stochastic output stability by generating multiple reasoning paths across differing temperature regimes.
- **Main Functions**:
  - `run_experiment(temperature)`: Executes a 5-iteration loop querying `MODEL` with `temperature` set to the specified argument, collecting and printing responses.
- **Inputs**: Prompt string, temperature float (`0.7` and `0.0`).
- **Outputs**: 10 formatted terminal logs (5 per temperature setting) returning generated answers.
- **Dependencies**: `config.client`, `config.MODEL`.
- **Interaction**: Isolates the effect of sampling temperature on reasoning divergence.

### `react_trace.py`
- **Purpose**: Simulates an end-to-end ReAct (Reasoning + Acting) execution trajectory.
- **Main Components**:
  - Programmatic interleaving of reasoning strings (`THOUGHT`), tool execution invocations (`ACTION`), and return payload captures (`OBSERVATION`).
- **Inputs**: Complex multi-objective user question (cost calculation + umbrella necessity).
- **Outputs**: Step-by-step execution trace printed to console concluding with a synthesized final answer.
- **Dependencies**: `tools.calculate_trip_cost`, `tools.get_weather`.
- **Interaction**: Bridges deterministic tool execution with cognitive reasoning steps.

---

## 4. Complete Execution Flow

### Flow 1: Direct Prompting (`agent.py`)
1. Program execution starts.
2. `config.py` loads environment variables and constructs the Groq `OpenAI` client.
3. `agent.py` defines the literal string `QUESTION`.
4. The client dispatches an HTTP POST request to `https://api.groq.com/openai/v1/chat/completions` containing a single user message.
5. The Groq inference engine processes the prompt with `openai/gpt-oss-20b`.
6. The client receives the response payload.
7. The extracted message string is printed to the terminal.
8. Process exits (Code 0).

### Flow 2: CoT vs. Direct Comparison (`cot_compare.py`)
1. Program initializes and loads `config.py`.
2. Prints test header and original question.
3. Invokes `direct_prompt()`:
   - Issues zero-shot chat completion request.
   - Captures and prints direct response.
4. Invokes `reasoning_prompt()`:
   - Appends explicit reasoning directives to `QUESTION`.
   - Issues augmented chat completion request.
   - Captures and prints Chain-of-Thought response.
5. Both outputs are juxtaposed in standard out for manual qualitative evaluation.
6. Process exits (Code 0).

### Flow 3: Temperature Sensitivity & Self-Consistency (`self_consistency.py`)
1. Program initializes client and model constants from `config.py`.
2. Calls `run_experiment(0.7)`:
   - Enters loop `for run in range(5)`.
   - In each iteration, dispatches chat completion with `temperature=0.7`.
   - Collects output into `answers` list and prints `RUN 1` through `RUN 5`.
3. Calls `run_experiment(0.0)`:
   - Enters loop `for run in range(5)`.
   - In each iteration, dispatches chat completion with `temperature=0.0` (greedy decoding).
   - Collects output and prints `RUN 1` through `RUN 5`.
4. Process terminates (Code 0).

### Flow 4: ReAct Reasoning-Action Trace (`react_trace.py`)

The execution strictly mirrors the classic ReAct trajectory:

```
[ User Input / Task Query ]
            │
            ▼
     [ Step 1: THOUGHT ]
  "I need to calculate total trip cost first.
   Then I need weather information for Chennai."
            │
            ▼
     [ Step 2: ACTION ]
  calculate_trip_cost(2000, 2500, 2, 1200, 2, 500)
            │
            ▼
   [ Step 3: OBSERVATION ]
  {'travel': 2000, 'hotel': 5000, 'food': 2400, 'local_transport': 1000, 'total': 10400}
            │
            ▼
     [ Step 4: THOUGHT ]
  "The total cost is ₹10400, which is ₹400 above the budget.
   I still need weather information to answer the umbrella question."
            │
            ▼
     [ Step 5: ACTION ]
  get_weather('Chennai')
            │
            ▼
   [ Step 6: OBSERVATION ]
  {'temperature': '29°C', 'condition': 'Cloudy', 'rain_probability': '60%'}
            │
            ▼
     [ Step 7: THOUGHT ]
  "The weather information shows Cloudy conditions and a 60% rain probability.
   Therefore, carrying an umbrella would be a reasonable precaution."
            │
            ▼
   [ Step 8: FINAL ANSWER ]
  Synthesized report: ₹10,400 total cost (₹400 over budget) +
  Cloudy, 29°C, 60% rain probability -> carry an umbrella.
```

---

## 5. Data Flow

```
+---------------------------------------------------------------------------------------------------+
| SCRIPT               INPUT DATA            PROCESSING / DECISION             TOOL / API           |
+---------------------------------------------------------------------------------------------------+
| agent.py             Literal string        Zero-shot language modeling       Groq Cloud API       |
|                      (travel question)                                       (gpt-oss-20b)        |
|                                                                                                   |
| cot_compare.py       Literal string        Prompt transformation             Groq Cloud API       |
|                      + CoT directive       (Direct vs Step-by-step)          (gpt-oss-20b)        |
|                                                                                                   |
| self_consistency.py  Literal string        Temperature parameterization      Groq Cloud API       |
|                      + summary directive   (T=0.7 vs T=0.0 across 5 runs)    (gpt-oss-20b)        |
|                                                                                                   |
| react_trace.py       Literal string        Procedural state transitions:     tools.py:            |
|                      (budget + weather)    1. Cost calculation               - calculate_trip_cost|
|                                            2. Budget comparison (>10000)     - get_weather        |
|                                            3. Weather condition retrieval                         |
+---------------------------------------------------------------------------------------------------+
                                                │
                                                ▼
+---------------------------------------------------------------------------------------------------+
| RESULTS & FINAL OUTPUT                                                                            |
+---------------------------------------------------------------------------------------------------+
| - agent.py: Natural language response with calculated total and budget verdict.                   |
| - cot_compare.py: Side-by-side comparison tables showing structured reasoning improvements.       |
| - self_consistency.py: 10 logged completions demonstrating syntactic variance vs semantic parity. |
| - react_trace.py: Full audit trail of thoughts, tool arguments, raw returns, and final verdict.   |
+---------------------------------------------------------------------------------------------------+
```

---

## 6. AI / LLM Architecture

### 6.1 Provider and Runtime Initialization
The project utilizes the Groq Cloud inference platform, accessed through the official `openai` Python library by re-pointing the client's `base_url` to `https://api.groq.com/openai/v1`. This leverages Groq's specialized Language Processing Unit (LPU) architecture for near-instantaneous token generation.

```python
# config.py
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)
MODEL = "openai/gpt-oss-20b"
```

### 6.2 Prompt Structuring and Context Handling
- **System Prompts**: None of the scripts define a `system` role message. All requests are formatted strictly with `{"role": "user", "content": ...}`.
- **Context Accumulation**: Invocations are single-turn stateless interactions. There is no multi-turn conversation memory, chat session history, or rolling context window.
- **Temperature Configuration**:
  - `agent.py` & `cot_compare.py`: Temperature is left unspecified, defaulting to the model/provider default (typically 1.0).
  - `self_consistency.py`: Explicitly parameterized to `temperature=0.7` (sampling for variety) and `temperature=0` (greedy decoding for strict determinism).
- **Structured Output**: No structured JSON schemas (`response_format={"type": "json_object"}`) or Pydantic validation models are employed. Outputs are parsed purely as raw strings (`response.choices[0].message.content`).

### 6.3 Separation of Responsibilities: LLM vs. Deterministic Code

| Functional Responsibility | Component Responsible | Technical Implementation |
|---|---|---|
| Natural language generation | LLM (`openai/gpt-oss-20b`) | `client.chat.completions.create` |
| Direct prompt reasoning | LLM (`openai/gpt-oss-20b`) | Inherent attention mechanisms over token context |
| Precise arithmetic calculation | Deterministic Code | `tools.py -> calculate_trip_cost()` |
| Ground-truth weather lookup | Deterministic Code | `tools.py -> get_weather()` |
| Budget conditional evaluation | Deterministic Code | `react_trace.py -> if cost_result["total"] > 10000:` |
| Sampling variance control | Deterministic Code | `self_consistency.py -> run_experiment(temperature)` |

---

## 7. Agentic AI Analysis

To evaluate this codebase rigorously according to academic and industry standards, we dissect its agentic attributes:

### 7.1 Perception
- **Implemented**: In `agent.py`, `cot_compare.py`, and `self_consistency.py`, perception is limited to static user text provided in the prompt string.
- **In `react_trace.py`**: The system receives structured perceptual inputs via tool return payloads (e.g., dictionary containing `'total': 10400` and dictionary containing `'condition': 'Cloudy', 'rain_probability': '60%'`).

### 7.2 Reasoning / Decision Making
- In `cot_compare.py`, reasoning is delegated to the internal autoregressive generation of the model prompted with CoT constraints.
- In `react_trace.py`, reasoning is explicitly modeled in code:
  - Evaluating if total cost exceeds the budget ceiling:
    ```python
    if cost_result["total"] > 10000:
        difference = cost_result["total"] - 10000
    ```
  - Evaluating weather observations to conclude that a 60% rain probability warrants carrying an umbrella.

### 7.3 Tool Usage
- Two deterministic Python tools are defined in `tools.py`.
- **Critical Finding**: Tools are **not** exposed to the LLM via the OpenAI `tools` / function-calling schema (`tools=[{"type": "function", ...}]`). In `react_trace.py`, tools are invoked deterministically by Python code rather than selected dynamically by the model.

### 7.4 Action & Feedback Loop
- **Action**: In `react_trace.py`, actions consist of function executions (`calculate_trip_cost(...)` and `get_weather(...)`).
- **Feedback**: The output of Action 1 (`cost_result`) feeds into Thought 2, which recognizes that budget analysis is complete but weather analysis remains unresolved, prompting Action 2 (`get_weather(...)`).

### 7.5 Autonomy Classification

```
[ Categorization Spectrum ]
1. Plain LLM Chatbot  <--- agent.py, cot_compare.py, self_consistency.py
2. Rule-Based Workflow <--- react_trace.py (Hardcoded ReAct simulation)
3. Autonomous Agent    <--- NOT IMPLEMENTED (Requires dynamic model tool-calling loop)
```

- **Verdict**: The project is **not** a fully autonomous agentic system. `agent.py`, `cot_compare.py`, and `self_consistency.py` are plain LLM queries exploring prompting strategies. `react_trace.py` is a **rule-based simulation** of the ReAct paradigm demonstrating the thought-action-observation structure without dynamic model-driven autonomy.

---

## 8. Prompt Engineering Analysis

### 8.1 Base User Prompt Analysis
Used across `agent.py` and `cot_compare.py`:
```text
I want to plan a 2-day trip to Chennai.
My budget is ₹10,000.
The estimated costs are:
Travel = ₹2,000
Hotel per night = ₹2,500
Food per day = ₹1,200
Local transport per day = ₹500
Can I complete the trip within my budget?
How much money will I be over or under budget?
```
- **Strengths**: Explicit numerical values; clear unit boundaries (per night, per day); concise dual questions.
- **Weaknesses**: Leaves duration interpretation slightly ambiguous (e.g., does a 2-day trip imply 1 night or 2 nights? The scripts and model assume 2 nights).

### 8.2 Chain-of-Thought Meta-Prompt Analysis
Used in `cot_compare.py`:
```text
Solve this problem carefully.
Break the calculation into clear steps.
Provide a concise reasoning summary followed by the final answer.
```
- **Mechanism**: This is an implementation of **Zero-Shot Chain-of-Thought (Zero-Shot CoT)**, related to Kojima et al.'s *"Let's think step by step"*.
- **Impact**: Forces the model to allocate output tokens to intermediate multiplication and summation steps before generating the concluding verdict. As verified in `output_screen/cot_compare/Screenshot 2026-09-22 211012.png`, this caused the model to produce an itemized markdown calculation table before issuing its budget determination.

### 8.3 Self-Consistency Prompt Analysis
Used in `self_consistency.py`:
```text
A student has a budget of ₹10,000 for a 2-day Chennai trip.
Travel costs ₹2,000.
Hotel costs ₹2,500 per night.
Food costs ₹1,200 per day.
Local transport costs ₹500 per day.
Calculate the total cost and determine whether the student is within the budget.
Give a concise reasoning summary and final answer.
```
- **Structure**: Rephrases the scenario in the third person ("A student has..."). 
- **Effect**: Standardizes the output structure to facilitate comparison across repeated sampling runs.

---

## 9. Tools Analysis

### Tool 1: `calculate_trip_cost`
- **File & Function**: `tools.py → calculate_trip_cost`
- **Purpose**: Computes itemized sub-totals and grand total for a multi-day trip.
- **Parameters**:
  - `travel_cost` (numeric): Flat transit expense.
  - `hotel_per_night` (numeric): Nightly lodging rate.
  - `nights` (int): Number of hotel nights.
  - `food_per_day` (numeric): Daily meal allowance.
  - `days` (int): Total trip duration in days.
  - `local_transport_per_day` (numeric): Daily intracity commute expense.
- **Return Type**: Python `dict` containing `"travel"`, `"hotel"`, `"food"`, `"local_transport"`, and `"total"`.
- **Invocation**: Procedurally called in `react_trace.py` (Line 50).
- **Necessity**: Replaces error-prone LLM arithmetic with exact CPU integer/float addition and multiplication ($2000 + 5000 + 2400 + 1000 = 10400$).

### Tool 2: `get_weather`
- **File & Function**: `tools.py → get_weather`
- **Purpose**: Retrieves meteorological conditions for a given destination city.
- **Parameters**: `city` (string).
- **Return Type**: Python `dict` with keys `"temperature"`, `"condition"`, `"rain_probability"`.
- **Invocation**: Procedurally called in `react_trace.py` (Line 116).
- **Necessity**: Provides dynamic ground-truth data that cannot be deduced purely through mathematical reasoning or frozen LLM weights.

---

## 10. Decision-Making Analysis

A core evaluation criterion for agentic systems is discerning where decisions are made:

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 DECISION ARCHITECTURE                  │
                  └────────────────────────────────────────────────────────┘
                                 │                           │
                                 ▼                           ▼
                     [ Deterministic Logic ]       [ LLM Generative Logic ]
                     - Budget threshold check      - Synthesizing advice & tips
                       (total > 10000)             - Choosing response formats
                     - Exact cost arithmetic         (Markdown table vs list)
                       (sum of line items)         - Tone and phrasing of verdict
                     - Weather data lookup         - Strategy for budget cuts
                       (dictionary matching)         (bus vs rail, dhabas, passes)
```

### Deterministic Decisions (Code-driven)
1. **Cost Calculation**: `tools.py → calculate_trip_cost` computes exact subtotals deterministically.
2. **Budget Boundary Check**: `react_trace.py` executes `if cost_result["total"] > 10000:` to choose between printing "above the budget" vs "leaving ₹... in the budget".
3. **Execution Sequencing**: The transition from cost calculation to weather lookup in `react_trace.py` is hardcoded in procedural code.

### LLM Decisions (Model-driven)
1. **Formatting & Structure**: In `cot_compare.py` and `self_consistency.py`, the model dynamically decides whether to render calculations as Markdown bullet points or Markdown tables.
2. **Value-Added Recommendations**: In `output_screen/cot_compare/Screenshot 2026-09-22 211012.png`, the LLM unprompted generated a "Tips to stay within ₹10,000" section suggesting cheaper bus/rail options, 3-star hotels/guest houses, eating at local dhabas, and using single-day city transit passes.

---

## 11. Error Handling

| Vulnerability / Failure Mode | Current Status | Code-Level Evidence | Impact / Risk |
|---|---|---|---|
| **Missing API Key** | **Handled** | `config.py:13-17` | Raises explicit `ValueError` if `GROQ_API_KEY` is not found in `.env`. |
| **Invalid / Nonexistent City** | **Handled** | `tools.py:56-63` | Returns dictionary with `"Unknown"` values via `.get(city, default)`. |
| **Network / API Outage** | **Not Handled** | `agent.py`, `cot_compare.py`, `self_consistency.py` | Raw `OpenAI` client calls lack `try...except` blocks, crashing with unhandled API connection exceptions. |
| **Rate Limiting (HTTP 429)** | **Not Handled** | Entire project | No exponential backoff or retry logic implemented. |
| **Invalid Tool Input Types** | **Not Handled** | `tools.py:1` | Non-numeric arguments to `calculate_trip_cost` will raise unhandled `TypeError`. |
| **Model Output Invalidation** | **Not Handled** | `self_consistency.py` | No schema parsing; assumes `choices[0].message.content` is always a non-empty string. |

---

## 12. Testing and Validation

### 12.1 Automated Testing
- **Status**: **Not implemented**.
- **Evidence**: No test framework (`pytest`, `unittest`), test directories (`tests/`), or test files exist in the repository.

### 12.2 Manual Script Verification
The developer validated functionality by running standalone execution scripts and verifying standard output in terminal sessions.

### 12.3 Execution Evidence from Logged Artifacts (`output_screen/`)

#### 1. `output_screen/react_trace/`
- **`Screenshot 2026-09-22 210850.png`**:
  - Terminal executing: `python react_trace.py`
  - Validates `THOUGHT 1`, `ACTION 1: calculate_trip_cost(2000, 2500, 2, 1200, 2, 500)`
  - Validates `OBSERVATION 1`: `{'travel': 2000, 'hotel': 5000, 'food': 2400, 'local_transport': 1000, 'total': 10400}`
  - Validates `THOUGHT 2`: "The total cost is ₹10400, which is ₹400 above the budget..."
- **`Screenshot 2026-09-22 210857.png`**:
  - Validates `ACTION 2: get_weather('Chennai')`
  - Validates `OBSERVATION 2`: `{'temperature': '29°C', 'condition': 'Cloudy', 'rain_probability': '60%'}`
  - Validates `FINAL ANSWER`: Correctly combines ₹10,400 cost (₹400 over budget) with recommendation to carry an umbrella due to 60% rain probability.

#### 2. `output_screen/cot_compare/`
- **`Screenshot 2026-09-22 211006.png` & `...1012.png` & `...1018.png`**:
  - Terminal executing: `python cot_compare.py`
  - Demonstrates `direct_prompt()` producing a table totaling ₹10,400 with actionable budget-reduction strategies.
  - Demonstrates `reasoning_prompt()` structuring calculations with an explicit step-by-step breakdown followed by a definitive budget check conclusion.

#### 3. `output_screen/self_consistency/`
- **`Screenshot 2026-09-22 210905.png` through `...0929.png`**:
  - Terminal executing: `python self_consistency.py`
  - Across all 5 runs at $T=0.7$ and all 5 runs at $T=0.0$, the final arithmetic answer remains 100% consistent: **Total cost: ₹10,400 (₹400 over budget)**.
  - Variations observed at $T=0.7$ were purely structural (Run 1 used bullet lists; Run 2 used a formatted Markdown table; Runs 4 and 5 used concise bolded formulas).

---

## 13. Scenario / Experiment Analysis

### Comparative Evaluation Matrix

| Dimension | Direct Prompting (`agent.py`) | Chain-of-Thought (`cot_compare.py`) | Self-Consistency (`self_consistency.py`) | ReAct Trace (`react_trace.py`) |
|---|---|---|---|---|
| **LLM Model Used** | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` | None (Simulated pure Python) |
| **Inference Calls** | 1 | 2 | 10 (5 @ T=0.7, 5 @ T=0.0) | 0 |
| **External Tools** | None | None | None | 2 (`calculate_trip_cost`, `get_weather`) |
| **Reasoning Method** | Implicit / Internal | Prompt-constrained CoT | Stochastic sampling comparison | Step-by-step trace simulation |
| **Arithmetic Precision** | Dependent on model | Dependent on model | Dependent on model | 100% exact (Python integer math) |
| **External Fact Retrieval** | None | None | None | Dictionary-grounded weather lookup |
| **Output Variance** | Single instance | Comparative instance | High syntactic variance @ 0.7, deterministic @ 0.0 | Completely deterministic |

---

## 14. Results and Observations

1. **Arithmetic Reliability on Simple Tasks**: On this specific budget problem, the `openai/gpt-oss-20b` model successfully computed the arithmetic total ($2000 + 5000 + 2400 + 1000 = 10400$) across all direct and CoT runs. However, relying on the model for arithmetic remains fundamentally probabilistic compared to tool offloading.
2. **Formatting Sensitivity to Sampling Temperature**:
   - At $T = 0.7$, the model exhibited noticeable formatting creativity: some runs rendered full Markdown calculation tables, while others produced concise bullet lists.
   - At $T = 0.0$, output token generation converged toward identical or near-identical phrasing and formatting.
3. **ReAct Auditability Advantage**: The trace in `react_trace.py` provides complete transparency into intermediate calculations and external API fetches. An auditor can immediately see why the system decided an umbrella was needed (because `get_weather` returned a 60% rain probability).

---

## 15. Strengths

- **Clean Modular Structure**: Code is cleanly partitioned into configuration (`config.py`), tools (`tools.py`), and focused experiment scripts.
- **Strict Environment Separation**: Sensitive credentials (`GROQ_API_KEY`) are kept out of source code and safely isolated in `.env` with `.gitignore` enforcement.
- **Fast Inference via Groq**: Utilizing Groq's endpoint enables sub-second responses for multi-run evaluations (such as the 10 sequential calls in `self_consistency.py`).
- **Comprehensive Visual Logging**: Terminal outputs are documented with timestamped screenshots in `output_screen/`.
- **Accurate ReAct Abstraction**: The execution trace in `react_trace.py` faithfully models the interleaving of Thought, Action, and Observation from the seminal ReAct literature (Yao et al., 2022).

---

## 16. Limitations

1. **Non-Autonomous ReAct Execution**: `react_trace.py` simulates the ReAct pattern procedurally; it does not implement dynamic LLM tool calling or an autonomous loop where the model decides which tool to call based on input.
2. **Missing Automated Consensus Mechanism**: While `self_consistency.py` samples multiple reasoning paths, it does not implement automated answer extraction (e.g., regex/parsing) or majority-voting algorithms to compute consensus programmatically.
3. **Static Mock Data**: The weather tool in `tools.py` uses a hardcoded dictionary covering only 3 Indian cities. Any other destination yields `"Unknown"`.
4. **Hardcoded Problem Parameters**: Budgets, city names, and line-item costs are hardcoded string constants rather than configurable CLI arguments or runtime user inputs.
5. **Absence of Automated Test Suites**: No automated unit or integration tests exist to verify tool correctness or API interface contracts.
6. **No API Resilience**: Scripts lack try/catch error handling, backoff retries, or failover mechanisms against network interruption or rate limiting.

---

## 17. Security Considerations

- **Credential Isolation**: Verified. `GROQ_API_KEY` is loaded strictly through `os.getenv` via `python-dotenv`. No secrets are hardcoded in source files.
- **Git Hygiene**: `.env` is explicitly listed in `.gitignore`, preventing accidental key exposure.
- **Prompt Injection Surface**: Low in the current state because inputs are hardcoded constants. However, if user-facing inputs are introduced without sanitization, direct concatenation patterns in `cot_compare.py` (`prompt = QUESTION + ...`) would be vulnerable to prompt injection.
- **Tool Execution Sandboxing**: The tools in `tools.py` perform benign arithmetic and in-memory lookups. They execute with standard local Python permissions and do not access filesystems or execute shell commands.

---

## 18. Reproducibility

The project is fully reproducible under the following specifications:
1. **Operating System**: Windows, macOS, or Linux.
2. **Python Version**: Python 3.10 to 3.14.
3. **Dependencies**: `openai>=1.40.0`, `python-dotenv>=1.0.0` (installed via `pip install -r requirements.txt`).
4. **Environment**: Active Groq API key configured in `.env` as `GROQ_API_KEY=...`.
5. **Execution**:
   ```bash
   python agent.py
   python cot_compare.py
   python self_consistency.py
   python react_trace.py
   ```
6. **Determinism Note**: While `react_trace.py` and runs at `temperature=0.0` produce deterministic outputs, runs at `temperature=0.7` will naturally exhibit minor syntactic variations across runs while preserving semantic arithmetic conclusions.

---

## 19. Technical Learnings

1. **Prompt Engineering vs. Tool Offloading**: Prompting techniques like Chain-of-Thought improve the model's intermediate scratchpad reasoning, but offloading computation to deterministic tools (`tools.py`) eliminates mathematical hallucinations entirely.
2. **The Anatomy of ReAct**: Decomposing complex tasks into explicit `Thought → Action → Observation` cycles enables verifiable auditing and structured integration of external real-time data.
3. **Sampling Dynamics in LLMs**: Controlling temperature is critical when designing production workflows—greedy decoding ($T=0$) ensures consistent formatting for parsers, whereas moderate temperature ($T=0.7$) allows for creative variance.

---

## 20. Possible Improvements

### CURRENT IMPLEMENTATION vs. FUTURE IMPROVEMENT

| Feature Area | CURRENT IMPLEMENTATION | FUTURE IMPROVEMENT |
|---|---|---|
| **Agent Autonomy** | Procedural script simulating ReAct trace in Python (`react_trace.py`). | Implement autonomous agent loop using OpenAI function calling (`tools=[...]`) where the LLM dynamically selects tools and handles responses. |
| **Weather Data** | Static Python dictionary supporting 3 hardcoded cities (`tools.py`). | Integrate live REST API (e.g., OpenWeatherMap or Open-Meteo) for real-time global weather forecasts. |
| **Self-Consistency** | Sequential printout of 5 runs per temperature setting (`self_consistency.py`). | Implement programmatic regex extraction of final cost and budget verdict with automated majority-voting consensus. |
| **User Interaction** | Hardcoded problem constants inside `.py` scripts. | Add command-line argument parsing (`argparse`) or an interactive web UI (Streamlit / FastAPI). |
| **Testing** | Manual inspection of terminal stdout saved as screenshot PNGs. | Add automated test suite (`pytest`) testing tool calculations, edge cases, and mocked API responses. |
| **Resilience** | Unhandled API calls. | Wrap client calls in robust retry mechanisms with exponential backoff (`tenacity` library). |

---

## 21. Final Technical Assessment

### Evidence-Based Summary
- **WHAT**: The project implements an experimental evaluation suite in Python exploring Direct Prompting, Chain-of-Thought reasoning, temperature-driven Self-Consistency sampling, and a simulated ReAct agentic workflow using the Groq API (`openai/gpt-oss-20b`).
- **HOW**:
  - `config.py` establishes an OpenAI-compatible client connection to Groq's infrastructure.
  - `agent.py` and `cot_compare.py` query the model with and without step-by-step reasoning constraints.
  - `self_consistency.py` systematically benchmarks output variance across $T=0.7$ and $T=0.0$.
  - `tools.py` provides deterministic mathematical computation and mock data retrieval.
  - `react_trace.py` demonstrates the state transitions of a ReAct agent.
- **EVIDENCE**:
  - `config.py` validates `GROQ_API_KEY` via `os.getenv`.
  - `tools.py → calculate_trip_cost()` executes exact arithmetic: $2000 + 5000 + 2400 + 1000 = 10400$.
  - `output_screen/` contains verified terminal captures confirming execution traces for all scripts.
- **LIMITATIONS PROVEN BY CODE**: The ReAct execution in `react_trace.py` is a scripted simulation rather than an autonomous dynamic model tool-calling loop; `self_consistency.py` lacks automated voting aggregation; and `tools.py` relies on a static 3-city dictionary.
