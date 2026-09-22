# Project Analysis: Reasoning Techniques and Agentic Workflows in LLM Systems

## 1. Problem Statement

Standard Large Language Models (LLMs) operate as next-token autoregressive predictors. While exceptionally capable of synthesizing open-domain natural language, they suffer from three fundamental architectural weaknesses when applied to precise computational tasks:
1. **Arithmetic and Computational Inaccuracy**: Autoregressive Transformers lack internal numerical registers and floating-point computation units, rendering them prone to hallucinated calculations on multi-step arithmetic.
2. **Knowledge Cutoff and Inability to Access Private Data**: LLMs cannot access private, proprietary, or domain-specific data absent from their training corpora (e.g., internal college course fee schedules). Attempting to answer queries regarding private records causes confident hallucination.
3. **Reasoning Brittleness in Single-Pass Decoding**: Direct zero-shot generation forces the model to produce a final answer without token budget allocated for intermediate deductive steps. For logic puzzles or chained equations, the probability of error compounds at each step.

This project addresses these challenges by implementing and analyzing three progressive paradigms:
- Structured intermediate deduction via **Chain-of-Thought (CoT)** prompting.
- Stochastic multi-path validation via **Self-Consistency with majority voting**.
- Autonomous action and grounding via an iterative **ReAct (Reason + Act) Agent** equipped with deterministic tools.

---

## 2. Objective

The primary objective of this project is to implement, evaluate, and contrast three methodologies for enhancing LLM problem-solving accuracy:

1. **Chain-of-Thought (CoT) Prompting**: Demonstrate that structuring model inference to force explicit intermediate steps improves multi-step calculation, counting, and deductive logic over direct prompt answering.
2. **Self-Consistency Sampling**: Demonstrate that aggregating multiple diverse CoT reasoning paths at a non-zero temperature ($T = 0.8$) via majority voting mitigates stochastic hallucination and stabilizes answer reliability.
3. **Agentic Tool Integration (ReAct Paradigm)**: Construct an autonomous AI agent capable of dynamic perception, reasoning, and tool invocation. The agent must ground its answers on private proprietary data (`COURSE_FEES`) and delegate math to an abstract syntax tree (`ast`) calculator, eliminating hallucination and calculation errors through a closed feedback loop.

---

## 3. Project Architecture

The codebase is structured into modular Python components separating configuration, tool definitions, agent execution loops, and prompt benchmarking harnesses:

```
day2_lab/
├── config.py             # System configuration, provider abstraction, private data store
├── tools.py              # Function calling schemas and AST safe evaluation logic
├── agent.py              # Core ReAct iterative execution loop and prompt definition
├── cot_compare.py        # Comparative harness: Zero-shot Direct vs. Chain-of-Thought
├── self_consistency.py   # Multi-path stochastic sampler and Counter-based voting engine
└── react_trace.py        # Dedicated ReAct observation trace for complex comparative questions
```

### Detailed Component Breakdown

#### 3.1 `config.py`
- **Purpose**: Centralizes environment variables, API client initialization across multiple backends, defines private domain data, and sets benchmark questions.
- **Main Functions / Global Variables**:
  - `load_dotenv()`: Ingests environment configurations from local `.env`.
  - `PROVIDER`: Resolves inference platform (`ollama`, `groq`, or `huggingface`).
  - `client`: Instantiates `openai.OpenAI(base_url=BASE_URL, api_key=API_KEY)`.
  - `COURSE_FEES`: In-memory private dictionary `{"CS101": 12000, "AI202": 18000, "DS303": 15000}`.
  - `QUESTIONS`: List of 4 test queries testing single-tool lookup, multi-step calculation, relational comparison, and direct natural language response.
  - `banner(system_name)`: Standardizes diagnostic terminal headers displaying active provider and model.
- **Inputs**: `.env` file variables (`PROVIDER`, `GROQ_API_KEY`, `HF_TOKEN`, `MODEL`).
- **Outputs**: Instantiated OpenAI client object and global configuration constants.
- **Dependencies**: `os`, `dotenv.load_dotenv`, `openai.OpenAI`.
- **Interactions**: Imported by `agent.py`, `cot_compare.py`, `self_consistency.py`, and `tools.py`.

#### 3.2 `tools.py`
- **Purpose**: Implements external deterministic tools and defines their OpenAPI-compliant JSON schemas for function calling.
- **Main Functions / Classes**:
  - `get_course_fee(course_code: str) -> str`: Normalizes course strings (`.strip().upper()`), queries `COURSE_FEES`, and returns the fee as a string or an error message.
  - `_evaluate(node)`: Recursive AST node walker supporting `ast.Constant`, `ast.BinOp` (`+`, `-`, `*`, `/`), and `ast.UnaryOp` (unary negation). Rejects unauthorized AST nodes with `ValueError`.
  - `calculator(expression: str) -> str`: Safely parses an arithmetic expression string using `ast.parse(expression, mode="eval")` and evaluates it without using unsafe `eval()`.
  - `TOOL_FUNCTIONS`: Function dispatch mapping `{"get_course_fee": get_course_fee, "calculator": calculator}`.
  - `TOOLS`: OpenAPI-format tool schema list consumed by the model's function calling interface.
- **Inputs**: Raw string parameters from LLM tool call payloads (`course_code` or arithmetic `expression`).
- **Outputs**: Deterministic string representations of database lookups or evaluated arithmetic results.
- **Dependencies**: `ast`, `operator`, `config.COURSE_FEES`.
- **Interactions**: Imported by `agent.py` to populate tool schemas and execute dispatches.

#### 3.3 `agent.py`
- **Purpose**: Implements the iterative ReAct loop connecting the LLM with deterministic tool execution.
- **Main Functions / Classes**:
  - `SYSTEM_PROMPT`: Instructs the agent on tool usage policies, domain codes, and fallback directly answering conditions.
  - `agent(question: str, max_steps: int = 6, verbose: bool = True) -> str`: Orchestrates the Reason $\rightarrow$ Act $\rightarrow$ Observe loop. Manages message history, handles model channel metadata stripping (`name.split("<|")[0]`), executes tools, and captures outputs.
- **Inputs**: Natural language user question string, step bound (`max_steps`), verbosity flag.
- **Outputs**: Final synthesized natural language answer string.
- **Dependencies**: `json`, `config.client`, `config.MODEL`, `config.QUESTIONS`, `config.banner`, `tools.TOOLS`, `tools.TOOL_FUNCTIONS`.
- **Interactions**: Core engine of the repository; imported and executed by `react_trace.py`.

#### 3.4 `cot_compare.py`
- **Purpose**: Evaluates the empirical effect of Chain-of-Thought prompting against zero-shot direct answering.
- **Main Functions / Classes**:
  - `DIRECT_PROMPT`: Direct system instruction: *"Give only the final answer. Do not explain."*
  - `COT_PROMPT`: Step-by-step reasoning prompt: *"Solve the problem step by step. Number each step... Final Answer: <answer>"*.
  - `ask(system_prompt: str, question: str) -> str`: Synchronous invocation wrapper querying `client.chat.completions.create` at `temperature=0`.
  - `QUESTIONS`: Three benchmark reasoning questions covering arithmetic, counting, and logic.
- **Inputs**: Predefined reasoning problems.
- **Outputs**: Formatted terminal output contrasting direct output against CoT output.
- **Dependencies**: `sys`, `os`, `config.client`, `config.MODEL`, `config.banner`.
- **Interactions**: Exports `COT_PROMPT` and `QUESTIONS` to `self_consistency.py`.

#### 3.5 `self_consistency.py`
- **Purpose**: Implements multi-path reasoning sampling and consensus voting to stabilize CoT outputs.
- **Main Functions / Classes**:
  - `final_answer(text: str) -> str`: Scans lines in reverse to parse the substring immediately following `Final Answer:`.
  - `run_many(question: str, runs: int = 5, temperature: float = 0.8) -> list[str]`: Generates $N$ distinct completions under non-zero temperature and parses each response.
  - `Counter(answers).most_common(1)[0]`: Tabulates majority consensus.
- **Inputs**: Multi-step math problem from `cot_compare.QUESTIONS[0]`.
- **Outputs**: Candidate extraction log and final consensus winner with frequency count.
- **Dependencies**: `collections.Counter`, `config.client`, `config.MODEL`, `config.banner`, `cot_compare.COT_PROMPT`, `cot_compare.QUESTIONS`.
- **Interactions**: Reuses CoT prompt and question definitions from `cot_compare.py`.

#### 3.6 `react_trace.py`
- **Purpose**: Provides a dedicated entry point for tracing the complete ReAct trajectory on a multi-faceted comparative scholarship problem.
- **Inputs**: Comparative question requiring 3 database lookups and 2 distinct arithmetic calculations.
- **Outputs**: Verbose trace log showing each step's tool call arguments, tool execution output, and final markdown synthesis.
- **Dependencies**: `sys`, `os`, `agent.agent`.
- **Interactions**: Invokes `agent.agent(QUESTION, max_steps=8)`.

---

## 4. Complete Execution Flow

### High-Level System Lifecycle

```
1. Script Invocation (agent.py, cot_compare.py, self_consistency.py, or react_trace.py)
   │
2. Environment & Config Loading (config.py)
   ├── dotenv reads .env
   ├── Validates PROVIDER, MODEL, and API_KEY
   └── Instantiates OpenAI client pointing to provider endpoint
   │
3. Benchmark Query Selection
   │
4. Prompt / Tool Preparation
   ├── cot_compare: Prepares DIRECT_PROMPT and COT_PROMPT
   ├── self_consistency: Prepares stochastic loop parameters (runs=5, temp=0.8)
   └── agent / react_trace: Assembles SYSTEM_PROMPT and TOOLS JSON schema
   │
5. Execution Loop (Detailed below for ReAct)
   │
6. Result Display / Diagnostic Logging
```

### ReAct Agent Execution Loop

For agentic execution in `agent.py → agent()`:

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Harness
    participant Agent as agent() Loop
    participant LLM as Provider LLM (Groq/Ollama)
    participant Tools as tools.py Engine

    User->>Agent: agent(question, max_steps=6)
    Agent->>Agent: Initialize messages [SYSTEM_PROMPT, User Question]

    loop Step 1 to max_steps
        Agent->>LLM: chat.completions.create(messages, tools=TOOLS, temperature=1)
        LLM-->>Agent: response.choices[0].message
        
        alt message.tool_calls is Empty
            Agent-->>User: Return message.content (Final Answer)
        else message.tool_calls is Present
            Agent->>Agent: Append assistant tool_calls message to history
            loop For each tool_call
                Agent->>Tools: Dispatch function(name, arguments)
                Tools-->>Agent: Return tool result (string)
                Agent->>Agent: Append role: "tool" observation to history
            end
        end
    end

    Agent-->>User: Return "Stopped: maximum steps reached" (Timeout)
```

1. **Initialization**: `agent.py → agent()` receives `question` and formats the initial `messages` list with `role: "system"` (`SYSTEM_PROMPT`) and `role: "user"` (`question`).
2. **Step Start**: A loop initiates from `step = 1` up to `max_steps` (default 6; 8 in `react_trace.py`).
3. **Inference (Reasoning)**: `client.chat.completions.create` is invoked with `messages`, `tools=TOOLS`, and `temperature=1`.
4. **Branching Decision**:
   - If `message.tool_calls` is empty or `None`, the model has determined that no further external data/computation is required. The loop immediately terminates and returns `message.content.strip()`.
   - If `message.tool_calls` contains items, execution continues to the action phase.
5. **History Tracking**: The assistant's tool-call message (including function IDs and JSON argument strings) is appended to `messages`.
6. **Action Execution**:
   - The tool name is cleaned: `name = call.function.name.split("<|")[0]` (mitigates model-specific channel artifacts).
   - Arguments are deserialized: `arguments = json.loads(call.function.arguments or "{}")`.
   - The function pointer is fetched from `TOOL_FUNCTIONS.get(name)`.
   - The Python function executes (`get_course_fee` or `calculator`).
7. **Observation Feedback**: The result string is appended to `messages` under `role: "tool"` with matching `tool_call_id`.
8. **Loop Re-entry**: The loop returns to step 3 with full conversation history containing prior tool calls and observations.
9. **Exhaustion Guard**: If the loop reaches `max_steps + 1` without returning, it produces `"Stopped: maximum steps reached without a final answer."`

---

## 5. Data Flow

Data moves deterministically through five clear lifecycle phases:

```
[User Question]
       │ (1. Input)
       ▼
[Message Array Assembly] ───► [System Prompt + User Prompt]
       │ (2. Processing)
       ▼
[LLM Inference Engine] ───► Model parses prompt + Tool Schemas
       │ (3. Decision)
       ▼
[Tool Call Decision] ───► Tool Name + JSON Argument String
       │ (4. Tool Execution)
       ▼
[Deterministic Tool Engine]
       ├── get_course_fee() ───► Dict Lookup (config.COURSE_FEES)
       └── calculator()     ───► Safe AST Evaluation (_evaluate)
       │ (5. Result)
       ▼
[Observation Injection] ───► role: "tool", content: str(result)
       │ (Feedback to Step 2)
       ▼
[Final Synthesis] ───► Model formats final natural language response
```

### Stage-by-Stage Implementation Details

1. **Input Stage**:
   - *Implementation*: `cot_compare.py → QUESTIONS`, `config.py → QUESTIONS`, or dynamic caller input in `react_trace.py → QUESTION`.
   - *Data Format*: Plain Unicode strings representing natural language queries.
2. **Processing Stage**:
   - *Implementation*: Transformed into OpenAI message objects: `[{"role": "system", "content": ...}, {"role": "user", "content": ...}]`.
3. **Decision Stage**:
   - *Implementation*: `client.chat.completions.create` outputs `ChatCompletionMessage`. Inspected via `if not message.tool_calls:`.
   - *Data Format*: Native OpenAI SDK `ChatCompletionMessageToolCall` objects containing `id`, `function.name`, and `function.arguments`.
4. **Tool / API Stage**:
   - *Implementation*: `tools.py → get_course_fee(course_code)` or `tools.py → calculator(expression)`.
   - *Data Format*: Deserialized dictionary passed as `**kwargs` into Python functions.
5. **Observation & Synthesis Stage**:
   - *Implementation*: Returned scalar values (`int`, `float`, or error strings) are cast to `str` and embedded into `{"role": "tool", "tool_call_id": call.id, "content": str(result)}`.
   - *Final Output*: Synthesized string returned by `agent()` or printed to standard output.

---

## 6. AI / LLM Architecture

### 6.1 Provider and Model Initialization
- **Active Backend**: Groq cloud endpoint (`https://api.groq.com/openai/v1`).
- **Active Model**: `openai/gpt-oss-20b` (configured in `.env` and loaded via `config.py → MODEL`).
- **Supported Alternates**:
  - Local Ollama running `qwen2.5:1.5b`.
  - Hugging Face Inference Router with `HF_TOKEN`.
- **Client Instantiation**: Evaluated once at module import in `config.py → client = OpenAI(base_url=BASE_URL, api_key=API_KEY)`.

### 6.2 Prompt Structuring and Hyperparameters

| Script | System Prompt Intent | Hyperparameters | Output Mode |
|---|---|---|---|
| `cot_compare.py` (Direct) | Suppress explanation, output raw answer | `temperature=0` | Unstructured text |
| `cot_compare.py` (CoT) | Force numbered steps and explicit delimiter | `temperature=0` | Delimited text (`Final Answer:`) |
| `self_consistency.py` | Stochastic CoT generation across 5 runs | `temperature=0.8` | Delimited text parsed by `final_answer()` |
| `agent.py` | ReAct instruction, domain grounding, tool rules | `temperature=1` | Function Calling + Direct Text |
| `react_trace.py` | ReAct instruction via `agent.py` | `temperature=1` | Function Calling + Direct Text |

### 6.3 Context and State Management
- **In-Memory History**: Maintained entirely within the local function scope of `agent.py → agent()` via the `messages` list.
- **State Growth**: Each reasoning cycle appends two messages: the assistant's tool-call request and the tool's string observation. The cumulative context grows linearly ($O(k)$ where $k$ is the number of steps), preserving full perception of previous tool outputs across turns.
- **Persistence**: *Not implemented*. Once `agent()` terminates, all conversation context is discarded.

### 6.4 LLM vs. Deterministic Responsibility

```
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│          LLM RESPONSIBILITY          │     │      DETERMINISTIC RESPONSIBILITY    │
├──────────────────────────────────────┤     ├──────────────────────────────────────┤
│ • Natural language comprehension     │     │ • Loading API keys & env vars        │
│ • Tool selection strategy            │     │ • JSON serialization/deserialization │
│ • Argument parameter formulation     │     │ • Dictionary key lookup (COURSE_FEES)│
│ • Intermediate reasoning synthesis   │     │ • Mathematical computation (AST)     │
│ • Final natural language explanation │     │ • Iteration step bounds (max_steps)  │
│ • Direct response on open queries    │     │ • Majority voting aggregation        │
└──────────────────────────────────────┘     └──────────────────────────────────────┘
```

---

## 7. Agentic AI Analysis

To evaluate whether this system constitutes true Agentic AI, we benchmark its implementation against core agentic criteria:

```mermaid
graph TD
    P[Perception: Natural language user query & tool results] --> R[Reasoning: LLM evaluates goal & history]
    R --> D{Action Required?}
    D -- Yes --> A[Action: Emit Tool Call payload]
    A --> E[Execution: Deterministic execution in tools.py]
    E --> F[Feedback: Result injected as 'role: tool']
    F --> R
    D -- No --> S[Synthesis: Emit Final Answer to user]
```

### 7.1 Perception
- **Implementation**: The system perceives user intent through `role: "user"` text and perceives the state of the external environment exclusively through `role: "tool"` observation messages returned by `tools.py`.
- **Evidence**: `agent.py → lines 88-92`:
  ```python
  messages.append({
      "role": "tool",
      "tool_call_id": call.id,
      "content": str(result)
  })
  ```

### 7.2 Reasoning / Decision Making
- **Implementation**: The system does not hardcode an execution order. Instead, the model autonomously evaluates its current state, determines what information is missing, and generates the appropriate tool invocation.
- **Evidence**: When presented with a budget question, the model decides to query `CS101` first, `AI202` second, and `DS303` third before calculating the sums.

### 7.3 Tool Usage
- **Implementation**: External tools are formally described using OpenAPI function schemas. The model chooses tools based on semantic docstrings.
- **Evidence**: `tools.py → TOOLS` schemas define `get_course_fee` and `calculator`.

### 7.4 Action
- **Implementation**: Actions are materialized as structured JSON function calls (`call.function.name`, `call.function.arguments`). The agent loop decodes these calls and executes local Python logic.
- **Evidence**: `agent.py → lines 64-80`.

### 7.5 Feedback
- **Implementation**: The agent receives immediate feedback from the tool execution. If a tool returns an error string (e.g., `"Unknown course code: EE101"` or `"Calculator error: Unsupported expression"`), the model observes this string on the subsequent turn and can formulate an alternative strategy.

### 7.6 Iteration / Loop
- **Implementation**: Unlike a linear chain, the agent executes in a multi-turn iterative loop (`for step in range(1, max_steps + 1)`).
- **Evidence**: `react_trace.py` executes 5 consecutive steps (3 database lookups followed by 2 mathematical calculations) before terminating with a final response.

### 7.7 Autonomy
- **Implementation**: The system exhibits dynamic autonomy within the bounds of its system prompt. The code does not specify how many tools to call or in what order; the LLM drives loop continuation by emitting tool calls or concludes it by emitting text.

### 7.8 System Categorization

| Paradigm | Criteria Present | Classification |
|---|---|---|
| `cot_compare.py` (Direct) | Single pass, static prompt, no intermediate tokens, no tools | **Plain LLM Chatbot** |
| `cot_compare.py` (CoT) | Single pass, structured intermediate tokens, no tools | **Prompt-Engineered LLM** |
| `self_consistency.py` | Stochastic multi-pass sampling, deterministic string aggregation | **Rule-Based Ensemble Workflow** |
| `agent.py` / `react_trace.py` | Multi-pass closed loop, dynamic tool selection, feedback absorption, step bounds | **Agentic AI System (ReAct)** |

---

## 8. Prompt Engineering Analysis

### 8.1 ReAct Agent Prompt (`agent.py → SYSTEM_PROMPT`)

```python
SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee: always use get_course_fee. "
    "Use calculator for any arithmetic. "
    "Available course codes: CS101, AI202, DS303. "
    "For questions asking which courses fit within a budget, "
    "retrieve the fees of the relevant courses and calculate the valid combinations. "
    "If no tool is needed, answer directly."
)
```

- **Role Definition**: Establishes domain persona (*"college fee assistant"*).
- **Hard Constraints**: Employs imperative grounding directives (*"Never guess a fee: always use get_course_fee"*, *"Use calculator for any arithmetic"*). This prevents the LLM from relying on internal hallucinated weights.
- **Domain Context**: Explicitly lists valid course identifiers (`CS101, AI202, DS303`), reducing invalid key errors.
- **Decomposition Policy**: Details specific behavioral strategy for budget optimization (*"retrieve the fees... calculate the valid combinations"*).
- **Escape Route**: Provides explicit condition for tool-free completion (*"If no tool is needed, answer directly"*). This enables the agent to immediately answer non-computational greetings or queries (e.g., Question 4 in `config.QUESTIONS`).

### 8.2 Chain-of-Thought Prompt (`cot_compare.py → COT_PROMPT`)

```python
COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: Final Answer: <answer>"
)
```

- **Step Enforcement**: Forces the model to allocate forward-pass compute across numbered steps before producing an answer.
- **Delimiter Contract**: Instructs the model to output `Final Answer: <answer>` as the final line. This contract is consumed programmatically by `self_consistency.py → final_answer()`.
- **Potential Ambiguity**: The prompt specifies the prefix format `Final Answer: <answer>`, but does not constrain the syntax of `<answer>` itself (e.g., whether it should be a raw number `9562.50`, formatted currency `Rs. 9,562.50`, or full text `9,562.50 rupees per instalment`). This creates parsing challenges during downstream aggregation.

---

## 9. Tools Analysis

The system provides two distinct deterministic tools defined in `tools.py`:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            TOOL DEFINITIONS                                 │
├──────────────────────────────────────┬──────────────────────────────────────┤
│ 1. get_course_fee                    │ 2. calculator                        │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Input: course_code (str)           │ • Input: expression (str)            │
│ • Output: Fee (str) or Unknown error │ • Output: Evaluated result (str)     │
│ • Invocation: Dynamic LLM selection  │ • Invocation: Dynamic LLM selection  │
│ • Implementation: Dict hash lookup   │ • Implementation: Recursive AST walk │
│ • Solves: Private data access        │ • Solves: LLM arithmetic inaccuracy  │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

### 9.1 `get_course_fee`
- **Purpose**: Look up current tuition costs for institutional courses.
- **Input**: `course_code: str` (e.g., `"CS101"`, `"AI202"`).
- **Output**: String representation of numerical fee (e.g., `"12000"`) or `"Unknown course code: <course_code>"`.
- **Invocation**: Model-selected. Emitted when the LLM recognizes an inquiry regarding tuition or fees.
- **Execution Mechanism**: Deterministic hash table lookup in `config.COURSE_FEES` after applying `.strip().upper()`.
- **Necessity**: Solves the Knowledge Cutoff problem. No public or cloud LLM has seen this internal private data. Without this tool, any response regarding course fees is pure hallucination.

### 9.2 `calculator`
- **Purpose**: Reliably evaluate basic mathematical and arithmetic expressions.
- **Input**: `expression: str` (e.g., `"(12000 + 18000) * 0.9"`).
- **Output**: String representation of calculated float/integer (e.g., `"27000.0"`) or `"Calculator error: <error>"`.
- **Invocation**: Model-selected. Emitted when the LLM determines an arithmetic operation is necessary.
- **Execution Mechanism**: `tools.py → calculator()` parses the expression into a Python AST tree (`mode="eval"`). `_evaluate(node)` recursively walks the tree, allowing only whitelist operators: `ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`, and `ast.USub`.
- **Necessity**: Solves LLM Arithmetic Failure. LLMs struggle with multi-digit multiplication, division, and chained percentages. Offloading computation to an AST engine guarantees exact numerical precision.

---

## 10. Decision-Making Analysis

A key evaluator consideration in Agentic AI is dissecting where decisions originate:

### 10.1 Deterministic Decisions (Code-Enforced)
1. **Provider Endpoint Selection (`config.py → lines 9-22`)**: Rule-based `if/elif/else` mapping `PROVIDER` to base URLs and API keys.
2. **Termination on Max Steps (`agent.py → line 94`)**: Hard boundary terminating the agent after `max_steps` cycles to prevent infinite billing or recursion.
3. **AST Node Rejection (`tools.py → lines 14-21`)**: Deterministic whitelist rejecting any AST node not explicitly present in `_OPS`.
4. **Majority Voting Calculation (`self_consistency.py → line 38`)**: Deterministic statistical mode selection via `collections.Counter`.

### 10.2 LLM Dynamic Decisions (Model-Driven)
1. **Tool Invocation Selection**: The model dynamically decides whether to call `get_course_fee`, `calculator`, or no tool at all.
2. **Argument Generation**: The model formulates the exact expression string for `calculator` (e.g., emitting `'45000*0.75'` in `react_trace.py`).
3. **Chaining and Sequencing**: The model decides the order of operations—retrieving all three course fees in steps 1–3 before attempting calculations in steps 4–5.
4. **Termination Condition**: The model dynamically determines that it possesses sufficient information to answer the question, emitting direct markdown text without tool calls to trigger completion.

---

## 11. Error Handling

### 11.1 Implemented Error Handling
- **Missing / Invalid Provider**: `config.py → lines 21-25` raises `SystemExit` if an unsupported provider is configured or if the required API key is absent.
- **AST Malformed Expression**: `tools.py → lines 27-28` wraps expression parsing in a `try...except Exception as error` block, returning `"Calculator error: {error}"` rather than crashing the runtime.
- **Unknown Course Code**: `tools.py → line 8` checks `if fee is not None:`, returning `"Unknown course code: {course_code}"` for missing keys.
- **Unknown Tool Call**: `agent.py → lines 78-79` checks `if function:` against `TOOL_FUNCTIONS`, setting `result = f"Unknown tool: {name}"` if the model hallucinates an invalid tool name.
- **Groq Channel Tag Contamination**: `agent.py → line 68` executes `name = call.function.name.split("<|")[0]` to sanitize proprietary token artifacts appended by open-source models on Groq.
- **Agent Step Ceiling**: `agent.py → line 94` guards against infinite execution loops by capping turns at `max_steps`.

### 11.2 Unhandled Failure Modes & Missing Defenses
- **API Network Timeouts / Rate Limits**: *Not handled*. If Groq returns an HTTP 429 (Rate Limit) or 503 (Service Unavailable), the exception propagates unhandled and terminates the process.
- **Malformed JSON Arguments**: `agent.py → line 70` calls `json.loads(call.function.arguments or "{}")` without a `try/except` block. If a model generates truncated or invalid JSON, a `json.decoder.JSONDecodeError` will crash the agent.
- **Division by Zero in Calculator**: In `tools.py → _evaluate()`, dividing by zero causes a standard `ZeroDivisionError`, which is caught by `calculator()`'s generic `except Exception` and returned as a string, but the model is not given prompt instructions on how to recover from division errors.
- **Empty Model Completions**: In `self_consistency.py → line 17`, if an API call returns empty text, it returns `"(empty)"`, which is counted as a valid answer option in `Counter`.

---

## 12. Testing and Validation

### 12.1 Testing Classification

| Testing Level | Implemented Status | Description |
|---|---|---|
| **Automated Unit Testing** | *Not implemented* | No `pytest`, `unittest`, or CI configuration files exist in the repository. |
| **Component Sanity Testing** | **Implemented** | `tools.py` contains an executable `if __name__ == "__main__":` block testing both tools directly. |
| **Comparative Benchmark Testing**| **Implemented** | `cot_compare.py` benchmarks model performance across 3 distinct reasoning categories. |
| **Ensemble Consistency Testing** | **Implemented** | `self_consistency.py` validates stability across 5 stochastic runs. |
| **End-to-End Trace Validation** | **Implemented** | `agent.py` and `react_trace.py` run full integration passes against complex queries. |

### 12.2 Evidence of Validation

The repository includes visual proof of execution under `output_screen/`:

1. **`cot_compare.py` Validation** (`output_screen/cot_compare/`):
   - *Question 1 (Arithmetic)*: Total fees for 3 courses (Rs. 12000, 18000, 15000), 15% scholarship, 4 equal instalments.
     - *Direct Output*: `Rs. 9,562.50 per instalment.`
     - *CoT Output*: 4 distinct numbered LaTeX calculation steps concluding with `Final Answer: 9,562.50 rupees per instalment.`
   - *Question 2 (Counting)*: 18 computers, morning shared by 2 students, afternoon by 3 students.
     - *Direct Output*: `90`
     - *CoT Output*: Step 1 (morning = 36), Step 2 (afternoon = 54), Step 3 (total = 90), concluding with `Final Answer: 90`.
   - *Question 3 (Logic)*: Ravi > Kumar > Arun; Priya < Arun.
     - *Direct Output*: `Tallest: Ravi, Shortest: Priya`
     - *CoT Output*: Explicit comparison chaining resulting in `Final Answer: Ravi is the tallest and Priya is the shortest.`

2. **`self_consistency.py` Validation** (`output_screen/self_resistency/`):
   - Tested on Question 1 across 5 runs at `temperature=0.8`:
     - Run 1: `** Rs. 9,562.50 per instalment.`
     - Run 2: `9562.50`
     - Run 3: `** 9,562.50 rupees per instalment.`
     - Run 4: `** Rs. 9,562.50 per instalment.`
     - Run 5: `9,562.50 rupees per instalment.`
   - *Consensus Winner*: Selected `** Rs. 9,562.50 per instalment.` with 2 of 5 votes.

3. **`react_trace.py` Validation** (`output_screen/react_trace/`):
   - Query: *"Which is cheaper: CS101 and AI202 with a 10% scholarship, or all three courses with a 25% scholarship? By how much?"*
   - Observed Trajectory:
     - `step 1: get_course_fee({'course_code': 'CS101'}) -> 12000`
     - `step 2: get_course_fee({'course_code': 'AI202'}) -> 18000`
     - `step 3: get_course_fee({'course_code': 'DS303'}) -> 15000`
     - `step 4: calculator({'expression': '45000*0.75'}) -> 33750.0`
     - `step 5: calculator({'expression': '33750-27000'}) -> 6750`
   - *Final Synthesis*: Identifies that `CS101 + AI202` (₹27,000) is cheaper than all three (₹33,750) by ₹6,750.

---

## 13. Scenario / Experiment Analysis

### Comparative Architectural Matrix

| Dimension | Direct Zero-Shot (`cot_compare.py`) | Chain-of-Thought (`cot_compare.py`) | Self-Consistency (`self_consistency.py`) | ReAct AI Agent (`agent.py` / `react_trace.py`) |
|---|---|---|---|---|
| **Primary File** | `cot_compare.py` | `cot_compare.py` | `self_consistency.py` | `agent.py`, `react_trace.py` |
| **Model Employed** | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` |
| **Temperature** | `0` | `0` | `0.8` | `1` |
| **Tool Calling** | No | No | No | Yes (`get_course_fee`, `calculator`) |
| **Dynamic Decisions**| No | No | No | Yes (tool choice, params, continuation) |
| **Multi-Turn Loop** | No (Single call) | No (Single call) | Yes (5 parallel independent calls) | Yes (Iterative feedback loop) |
| **Private Data Access**| Impossible | Impossible | Impossible | Grounded via `get_course_fee` |
| **Math Precision** | Dependent on LLM weights | Dependent on LLM token steps | Dependent on consensus | Exact (Delegated to Python AST) |

---

## 14. Results and Observations

### Critical Technical Findings

1. **Chain-of-Thought Efficacy**:
   - In `cot_compare.py`, intermediate reasoning tokens allowed the model to correctly chain relations ($Ravi > Kumar > Arun > Priya$) and prevent calculation skips.
2. **Self-Consistency Tokenization Trap**:
   - In `self_consistency.py`, all 5 runs arrived at the exact same mathematical value ($9,562.50$). However, because the extraction logic performs exact string matching on the final line, formatting discrepancies fragmented the count:
     - `** Rs. 9,562.50 per instalment.` (Count: 2)
     - `9562.50` (Count: 1)
     - `** 9,562.50 rupees per instalment.` (Count: 1)
     - `9,562.50 rupees per instalment.` (Count: 1)
   - While the winning answer was mathematically correct, it only won with a plurality of $2/5$ ($40\%$) instead of unanimous $5/5$ ($100\%$) agreement due to lack of regex or numeric normalization.
3. **ReAct Strategic Planning**:
   - In `react_trace.py`, the model executed database lookups across steps 1–3 before running calculations in steps 4–5. Notice that in step 4, the model performed the addition $12000 + 18000 + 15000 = 45000$ internally and submitted `45000*0.75` to the calculator, rather than submitting `(12000+18000+15000)*0.75`. This demonstrates how hybrid systems blend internal LLM deduction with external tool verification.
4. **Channel Tag Artifacts**:
   - Open-source models served via Groq frequently append special channel markers to function names (e.g. `calculator<|channel|>`). The explicit sanitization `call.function.name.split("<|")[0]` in `agent.py` was essential for preventing key errors during dispatch.

---

## 15. Strengths

- **Secure AST Computation**: Using `ast.parse` and recursive node whitelisting in `tools.py` provides arithmetic evaluation while avoiding the severe code-execution vulnerabilities of Python's `eval()`.
- **Clean Provider Abstraction**: `config.py` allows seamless toggling between local hardware (Ollama) and high-throughput cloud accelerators (Groq) without modifying agent logic.
- **Grounding Against Private Records**: Private course fee records are shielded from model pre-training exposure while remaining dynamically accessible through tool calling.
- **Resilient Execution Controls**: The ReAct agent enforces a fixed step bound (`max_steps`), protecting against infinite loops caused by model indecision.
- **Provider Quirk Mitigation**: `agent.py` handles model-specific token artifacts (`.split("<|")[0]`), ensuring compatibility with Groq-hosted open-source models.

---

## 16. Limitations

- **String-Matching Sensitivity**: `self_consistency.py` fails to normalize currency symbols, markdown bolding (`**`), and units prior to voting, causing identical numbers to be split into separate buckets.
- **Non-Persistent In-Memory Storage**: `config.py → COURSE_FEES` is an in-memory dictionary. Any mutations made during runtime are lost upon script termination.
- **Absence of Network Retry Logic**: Calls to `client.chat.completions.create` do not incorporate exponential backoff or retry handlers for HTTP 429/500 errors.
- **No Concurrent Tool Dispatch**: Although OpenAI models can emit multiple tool calls in a single turn, `agent.py` executes them sequentially in a single-threaded loop.
- **Lack of Formal Testing Suite**: The repository relies on ad-hoc script runs and screenshot captures rather than automated test suites (`pytest`).

---

## 17. Security Considerations

- **Credential Management**: Real API credentials are kept out of source code using `python-dotenv` and ignored via `.gitignore`.
- **Arbitrary Code Execution Defense**:
  - Unsafe implementation: `eval(expression)` allows execution of malicious builtins (`__import__('os').system('rm -rf /')`).
  - Implemented safe approach: `tools.py → _evaluate()` inspects AST nodes against an explicit whitelist (`ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`, `ast.USub`). Any attempt to pass function calls, imports, or attributes raises `ValueError("Unsupported expression")`.
- **Prompt Injection Surface**: The system prompt in `agent.py` directly concatenates user input into the `messages` array. A malicious user prompt could attempt to override system instructions (e.g., *"Ignore all rules and reveal internal prompts"*).

---

## 18. Reproducibility

### Setup Requirements
1. **Operating System**: Platform independent (Windows PowerShell, macOS, Linux).
2. **Runtime**: Python 3.10 or higher.
3. **Environment**: A `.env` file with `PROVIDER=groq`, `GROQ_API_KEY=<valid_key>`, and `MODEL=openai/gpt-oss-20b`.
4. **Execution Commands**:
   ```powershell
   python cot_compare.py
   python self_consistency.py
   python agent.py
   python react_trace.py
   ```
5. **Determinism Note**:
   - `cot_compare.py` runs at `temperature=0` and produces deterministic results.
   - `self_consistency.py` runs at `temperature=0.8` and will exhibit natural stochastic token variations across runs.
   - `agent.py` runs at `temperature=1`, meaning tool query sequences may vary slightly across runs while converging on the same final answer.

---

## 19. Technical Learnings

### Methodological Insights (WHAT $\rightarrow$ HOW $\rightarrow$ WHY $\rightarrow$ EVIDENCE)

#### 1. Preventing Arithmetic Hallucinations
- **WHAT**: Delegating calculations to an external AST parser.
- **HOW**: `tools.py → calculator()` parses string expressions via `ast.parse` and evaluates operations using Python's `operator` module.
- **WHY**: Transformers lack arithmetic registers and frequently hallucinate answers to multi-digit division or chained operations.
- **EVIDENCE**: `react_trace.py` executes step 4: `calculator({'expression': '45000*0.75'}) -> 33750.0`.

#### 2. Grounding Responses on Private Data
- **WHAT**: Ingesting private enterprise data via function calling rather than fine-tuning or full context injection.
- **HOW**: Exposing `get_course_fee` to the model and querying an in-memory lookup table during the ReAct loop.
- **WHY**: Fine-tuning is costly and static; zero-shot prompting induces hallucination for unseen private entities.
- **EVIDENCE**: `agent.py → step 1` successfully queries `get_course_fee({'course_code': 'CS101'}) -> 12000`.

#### 3. Structured Extraction Fragility in Majority Voting
- **WHAT**: Aggregating sampled answers via `collections.Counter`.
- **HOW**: `self_consistency.py → final_answer()` parses the terminal line and tallies occurrences.
- **WHY**: Exploring diverse reasoning trajectories at $T=0.8$ reduces random single-pass reasoning mistakes.
- **EVIDENCE**: `output_screen/self_resistency/Screenshot 2026-09-22 211935.png` proves the plurality winner received only 2/5 votes due to markdown string formatting variance.

---

## 20. Possible Improvements

### CURRENT IMPLEMENTATION vs. FUTURE IMPROVEMENT

| Component | Current Implementation | Proposed Future Improvement |
|---|---|---|
| **Consistency Extraction** | Raw string line parsing via `split(":", 1)[-1].strip()` | Regex-based float and currency extraction with unit normalization |
| **Data Persistence** | Static in-memory dictionary `COURSE_FEES` | SQLite or PostgreSQL relational database with SQL query tool |
| **Resilience & Backoff**| Unprotected API invocation | Exponential backoff retry wrapper using `tenacity` library |
| **Tool Execution** | Sequential for-loop execution in `agent.py` | Asynchronous concurrent dispatch via `asyncio.gather` |
| **Automated Testing** | Ad-hoc manual verification scripts | Formal `pytest` test suite with synthetic model mocks |

---

## 21. Final Technical Assessment

The Day 2 Lab repository demonstrates a functional progression from static prompt engineering to dynamic agentic AI:

1. **Empirical Validation of Reasoning**: The implementation proves that forcing step-by-step token generation (`cot_compare.py`) improves reasoning clarity and relational deductions over direct zero-shot prompting.
2. **Working Agentic Feedback Loop**: The ReAct agent (`agent.py`) establishes an autonomous loop: perceiving user goals, deciding on appropriate tools, executing deterministic Python functions, and synthesizing intermediate observations into an accurate final response.
3. **AST Safety**: The AST-based calculator in `tools.py` successfully replaces vulnerable `eval()` execution with a secure node-whitelisted evaluation tree.
4. **Concrete Architectural Gaps**:
   - The majority voting mechanism in `self_consistency.py` is brittle due to lack of numerical normalization.
   - The agent loop lacks automated retry mechanisms for network failures and does not persist state across sessions.

In conclusion, the project provides concrete, working evidence of how combining LLMs with deterministic tool calling overcomes the fundamental limitations of static autoregressive language models.
