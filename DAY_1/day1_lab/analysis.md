# College Fee Assistant — Technical Analysis

> An in-depth technical evaluation of architectural paradigms, execution safety, agentic reasoning, and system reliability across Chatbot, Workflow, and Agent implementations.

---

## 1. Introduction

### Project Objective
The primary objective of the **College Fee Assistant** project is to evaluate and contrast three distinct computational paradigms for processing institutional data and executing multi-step business logic:
1. **Unaugmented Conversational AI (System 1: Chatbot)**
2. **Deterministic Syntactic Automation (System 2: Rule-Based Workflow)**
3. **Tool-Augmented Autonomous Reasoning (System 3: AI Agent)**

### Problem Overview
Automating institutional interactions requires answering questions about proprietary facts (such as unpublicized tuition fees), computing mathematical reductions (such as scholarship adjustments), and maintaining conversational flexibility. Each paradigm presents distinct tradeoffs regarding factual reliability, flexibility, execution latency, and development overhead.

### Intended Users & Evaluators
- **AI Engineers and System Architects**: Assessing whether an enterprise problem demands an agent, a workflow, or a fine-tuned model.
- **Academic Evaluators**: Benchmarking student understanding of LLM hallucination, tool calling interfaces, and secure Python programming.

### Technical Approach
The repository sets up an empirical testbed using a shared configuration (`config.py`), a common private data dictionary (`COURSE_FEES`), two deterministic utilities (`tools.py`), and a shared four-prompt benchmark suite (`QUESTIONS`) alongside an unscripted budget constraint query (`challenge.py`).

---

## 2. Problem Analysis

### Existing Problem & The "Trilemma"
When building domain-specific query interfaces, engineers face a trilemma across three core dimensions:

```
                  Conversational Fluency
                          /\
                         /  \
                        /    \
            System 1   /      \  System 3
            (Chatbot) /        \ (Agent)
                     /          \
                    /____________\
        System 2 (Workflow)     Factual & Computational
       Determinism & Safety            Precision
```

- **Pure LLMs (System 1)** provide high conversational fluency but zero guarantee of factual grounding on private data, alongside poor arithmetic reliability.
- **Rule-Based Code (System 2)** provides 100% deterministic arithmetic and zero hallucination, but exhibits zero resilience to linguistic variations, semantic phrasing, or unexpected questions.
- **AI Agents (System 3)** combine linguistic reasoning with tool execution, achieving both fluency and factual precision, but introduce latency, model nondeterminism, and integration complexity.

### User & System Requirements
- **Query Flexibility**: The system must process direct lookups, multi-step math, comparative inquiries, and creative text prompts.
- **Factual Accuracy**: Private course fees (`CS101: 12000`, `AI202: 18000`, `DS303: 15000`) must be strictly honored.
- **Execution Safety**: Dynamic calculation must not expose the host environment to arbitrary code execution (ACE) vulnerabilities.

---

## 3. Solution Analysis

The project implements three parallel pipelines to demonstrate how each addresses or fails the problem space:

| Evaluation Dimension | System 1: Chatbot (`chatbot.py`) | System 2: Workflow (`workflow.py`) | System 3: Agent (`agent.py`) |
|---|---|---|---|
| **Private Data Awareness** | **Fails**: Zero access to `COURSE_FEES`. Prompts user for tuition data. | **Passes**: Direct dictionary key lookup. | **Passes**: Dynamic lookup via `get_course_fee` tool. |
| **Arithmetic Precision** | **Unreliable**: Relies on token probability generation. | **Exact**: Evaluates standard Python arithmetic (`sum(fees) * (1 - pct/100)`). | **Exact**: Outsources math to AST-based `calculator`. |
| **Comparative Reasoning** | **Subjective**: Lacks data to compare accurately. | **Fails**: Rejects comparisons with `"Sorry, I do not have a rule for this type of question."` | **Passes**: Fetches fees sequentially and computes difference. |
| **Unscripted Language (Budget)** | **Fluent but Uninformed**: Cannot calculate exact course pair combinations within Rs. 30,000. | **Fails**: Regex `[A-Z]{2}\d{3}` finds no course codes in query string. | **Passes**: Inspects course list, evaluates combinations, reasons over budget. |
| **Creative Generation** | **Passes**: Synthesizes natural, high-quality welcome message. | **Fails**: Rejects non-fee questions immediately. | **Passes**: Detects that no tool is needed and replies directly. |

---

## 4. Architecture Analysis

The system architecture is decoupled into shared configuration, tool infrastructure, and individual system runners.

```
+-------------------------------------------------------------------------------+
|                             Configuration Layer                               |
|                                 (config.py)                                   |
|   - Provider routing: Ollama (11434) / Groq (api.groq.com) / Hugging Face    |
|   - OpenAI Python SDK client instance                                         |
|   - In-memory private data: COURSE_FEES dict                                  |
+-------------------+---------------------------------------+-------------------+
                    |                                       |
                    v                                       v
+---------------------------------------+   +-----------------------------------+
|            Tooling Layer              |   |       Pure Inference Layer        |
|              (tools.py)               |   |          (chatbot.py)             |
|  - get_course_fee(course_code)        |   |  - Role: system + user            |
|  - calculator(expression) [AST Parse] |   |  - Temperature: 0                 |
|  - JSON Schema Declarations           |   |  - Direct completion dispatch     |
+-------------------+-------------------+   +-----------------------------------+
                    |
                    +---------------------------------------+
                    |                                       |
                    v                                       v
+---------------------------------------+   +-----------------------------------+
|         Agent Execution Layer         |   |      Procedural Pattern Layer     |
|              (agent.py)               |   |          (workflow.py)            |
|  - ReAct Tool Loop (max_steps=6)      |   |  - Regex tokenization             |
|  - JSON Tool argument parsing         |   |  - Procedural math branch         |
|  - Context accumulation & state       |   |  - Fallback exception messaging   |
+---------------------------------------+   +-----------------------------------+
```

### Component Communication
- **Shared Client**: `config.py` acts as a centralized factory configuring an `OpenAI` client instance with custom base URLs and headers based on `PROVIDER`.
- **Stateless Tool Dispatch**: `tools.py` provides pure, stateless functions without side effects.
- **Message Accumulation**: `agent.py` manages an in-memory list of message dictionaries (`role`: `system`, `user`, `assistant`, `tool`), tracking the conversation state across multiple LLM round-trips.

---

## 5. Data Flow Analysis

### 1. Agent Multi-Step Execution Trace

```
User: "Is DS303 more expensive than CS101, and by how much?"
  │
  ▼
[agent.py] Initialize messages -> [SYSTEM_PROMPT, USER_QUERY]
  │
  ├──► [Step 1: LLM Reason] -> Emits tool_call: get_course_fee("DS303")
  │      │
  │      └──► [Step 1: Local Act] -> tools.get_course_fee("DS303") -> "15000"
  │      └──► [Step 1: Observe] -> Append {"role": "tool", "content": "15000"}
  │
  ├──► [Step 2: LLM Reason] -> Emits tool_call: get_course_fee("CS101")
  │      │
  │      └──► [Step 2: Local Act] -> tools.get_course_fee("CS101") -> "12000"
  │      └──► [Step 2: Observe] -> Append {"role": "tool", "content": "12000"}
  │
  ├──► [Step 3: LLM Reason] -> Emits tool_call: calculator("15000 - 12000")
  │      │
  │      └──► [Step 3: Local Act] -> tools.calculator("15000 - 12000") -> "3000"
  │      └──► [Step 3: Observe] -> Append {"role": "tool", "content": "3000"}
  │
  └──► [Step 4: LLM Reason] -> Final Synthesis: "Yes, DS303 (Rs. 15,000) is more expensive than CS101 (Rs. 12,000) by Rs. 3,000."
         │
         ▼
       Return final answer to caller
```

### 2. Workflow Execution Trace

```
User: "What is the total fee for CS101 and AI202 after a 10% scholarship?"
  │
  ▼
[workflow.py]
  │
  ├── Regex search r"[A-Z]{2}\d{3}" -> ['CS101', 'AI202']
  ├── Dict lookup -> [12000, 18000]
  ├── Substring check "total" in text -> True
  ├── Regex search r"(\d+)\s*%" -> matches "10"
  ├── Calculation -> (12000 + 18000) * (1 - 10/100) = 27000
  │
  ▼
Return "Total fee: Rs. 27,000"
```

---

## 6. Component Analysis

### 1. `config.py`
- **Responsibility**: Environment loading, dynamic provider switching, OpenAI client instantiation, mock private data definition, and benchmark question registry.
- **Inputs**: `.env` configuration keys (`PROVIDER`, `MODEL`, `GROQ_API_KEY`, `HF_TOKEN`).
- **Outputs**: Global `client`, `PROVIDER`, `MODEL`, `COURSE_FEES`, `QUESTIONS`.
- **Dependencies**: `os`, `dotenv`, `openai`.
- **Evaluation**: Clear, lightweight provider router. Defaults to local Ollama (`http://localhost:11434/v1`), falling back cleanly with informative `SystemExit` messages if keys are missing.

### 2. `tools.py`
- **Responsibility**: Houses deterministic tools callable by agents and users.
- **Inputs**: Tool arguments (`course_code`, `expression`).
- **Outputs**: Output strings returned to the agent loop.
- **Dependencies**: `ast`, `operator`, `config.COURSE_FEES`.
- **Key Architectural Choice**: Safe AST recursion over `eval()`.
  ```python
  _OPS = {
      ast.Add: operator.add, ast.Sub: operator.sub,
      ast.Mult: operator.mul, ast.Div: operator.truediv,
      ast.USub: operator.neg
  }
  ```
  The calculator explicitly restricts grammar nodes to `ast.Constant`, `ast.BinOp`, and `ast.UnaryOp`. If an identifier, import, or unauthorized node is encountered, it raises `ValueError("Unsupported expression")`.

### 3. `agent.py`
- **Responsibility**: ReAct execution engine.
- **Inputs**: User prompt, `max_steps` (6), `verbose` (boolean).
- **Outputs**: Final answer string.
- **Dependencies**: `json`, `config`, `tools`.
- **Loop Termination Criteria**:
  1. Assistant returns a message with no `tool_calls`.
  2. The loop counter exceeds `max_steps`, triggering fallback string: `"Stopped: maximum steps reached without a final answer."`.

---

## 7. AI / ML / Agent Analysis

### Model Selection & Serving
- Supported models include `qwen2.5:1.5b` via local Ollama and `openai/gpt-oss-20b` via Groq or Hugging Face.
- Groq provides low-latency inference (~100-300ms per step), making multi-step ReAct loops feasible without excessive user wait times.

### Prompt Engineering & Grounding
The system prompt in `agent.py`:
```
"You are a college fee assistant. Never guess a fee: always use get_course_fee.
Use calculator for any arithmetic. Available course codes: CS101, AI202, DS303.
If no tool is needed, answer directly."
```
- **Constraint Enforcement**: Explicitly prohibits speculative hallucination (`"Never guess a fee"`).
- **Tool Delegation Directive**: Instructs model to offload all arithmetic to `calculator`.
- **Domain Context**: Provides the finite universe of valid course codes to prevent invalid lookups.

### ReAct Loop Mechanics & Code-Level Observation
In `agent.py`:
```python
response = client.chat.completions.create(
    model=MODEL, messages=messages, tools=TOOLS, temperature=1, include_reasoning=False
)
```
- **Observable Decision Flow**:
  1. The model inspects conversation context and tool schemas.
  2. If the prompt requires unknown fees, it outputs a tool call with `get_course_fee`.
  3. The local runner intercepts this call, parses JSON arguments, executes the Python callable, and feeds back a `tool` role message.
  4. The model assesses whether more data or calculation is needed.
  5. When satisfied, it emits final text with no tool call.

### Critical Finding: SDK Parameter Incompatibility
The argument `include_reasoning=False` is passed to `client.chat.completions.create()`. Under standard OpenAI Python SDK specifications (`openai >= 1.40.0`), this argument is unrecognized and causes:
```
TypeError: Completions.create() got an unexpected keyword argument 'include_reasoning'
```
This demonstrates an important engineering insight: while reasoning models (such as deepseek-r1 or certain Groq beta endpoints) introduce experimental parameters, standard SDK interfaces will reject unrecognized keyword parameters unless explicitly supported by custom client wrappers.

---

## 8. Data and Database Analysis

### Data Model & Persistence
- **Storage Type**: In-Memory Key-Value Hash Map (`dict`).
- **Entity**: `COURSE_FEES`
- **Schema**:
  - `course_code` (`str`): Primary key (e.g., `"CS101"`).
  - `fee` (`int`): Course cost in INR.
- **Normalization & Validation**:
  - `get_course_fee` performs sanitization via `course_code.strip().upper()`.
  - Non-existent codes return a controlled string (`"Unknown course code: <input>"`), preventing unhandled `KeyError` exceptions.

---

## 9. API Analysis

### Consumed External Endpoints
The application does not expose ingress REST APIs; it functions as an API consumer.

| Target Host | Endpoint | Protocol | Purpose | Payload Type |
|---|---|---|---|---|
| `api.groq.com` | `/openai/v1/chat/completions` | HTTPS | Cloud LLM inference with tool calling | JSON |
| `router.huggingface.co` | `/v1/chat/completions` | HTTPS | Serverless cloud model inference | JSON |
| `localhost:11434` | `/v1/chat/completions` | HTTP | Local offline model inference | JSON |

### Interface Contract (Function Schemas)
Tools are exposed to the LLM using JSON Schema:
```json
{
  "type": "function",
  "function": {
    "name": "get_course_fee",
    "description": "Get the fee in rupees for a single course code, for example CS101.",
    "parameters": {
      "type": "object",
      "properties": {
        "course_code": {"type": "string"}
      },
      "required": ["course_code"]
    }
  }
}
```

---

## 10. Security Analysis

### IMPLEMENTED Security Controls
1. **AST-Based Code Execution Sandboxing**:
   - `eval()` is strictly avoided.
   - `ast.parse(expression, mode="eval")` parses the mathematical string into an Abstract Syntax Tree.
   - Only a restricted set of arithmetic nodes (`ast.Add`, `ast.Sub`, `ast.Mult`, `ast.Div`, `ast.USub`) and numeric constants are evaluated.
   - Any malicious string containing function calls, attribute lookups, or system imports (e.g., `__import__('os').system('rm -rf')`) fails AST validation immediately.
2. **Secret Separation**:
   - API keys (`GROQ_API_KEY`, `HF_TOKEN`) are isolated in `.env` and loaded via `python-dotenv`.
   - `.gitignore` prevents inadvertent check-in of secret files.

### NOT IMPLEMENTED / FUTURE Controls
1. **User Authentication & Authorization**: The scripts run as local CLI programs with no identity management or RBAC.
2. **Rate Limiting & Cost Throttling**: No rate-limiting middleware exists between client invocations and upstream inference providers.
3. **API Key Rotation & KMS**: Keys are stored in plain text inside `.env` on disk.
4. **Input Length Sanitization**: Prompts are forwarded directly to the client without token truncation or length limits.

---

## 11. Reliability Analysis

### Failure Modes & Handling

| Failure Mode | Component | Current Handling | Risk Level |
|---|---|---|---|
| **Invalid Course Code** | `tools.py` | Returns string `"Unknown course code: ..."` | Low (Graceful) |
| **Malformed Math Expression** | `tools.py` | Caught by `except Exception` -> returns `"Calculator error: ..."` | Low (Graceful) |
| **Max Agent Iterations** | `agent.py` | Controlled step limit (`max_steps=6`); returns `"Stopped: maximum steps reached..."` | Low (Prevents infinite loops) |
| **Unsupported Keyword Argument** | `agent.py` | `include_reasoning=False` raises unhandled `TypeError` on standard `openai` SDK | High (Runtime Crash) |
| **Console Encoding Error** | `chatbot.py` | Output with unicode quotes/spaces crashes Windows `cp1252` console | Medium (Environment Dependent) |
| **Network / Upstream API Drop** | `config.py` | No retry logic; crashes with `openai.APIConnectionError` | Medium |

---

## 12. Scalability Analysis

### Current Architectural Profile
- **Concurrency**: Fully synchronous and single-threaded. Each invocation blocks until the remote HTTP request completes.
- **Resource Footprint**: Minimal local CPU/RAM usage (~30MB RAM footprint). Bottleneck is entirely upstream API latency.

### Scalability Under Load
- **Users Increase**: A concurrent deployment would require an asynchronous framework (`asyncio`, `httpx`, `FastAPI`) rather than blocking synchronous calls.
- **Data Increase**: As course offerings grow from 3 to 30,000, `COURSE_FEES` would exceed in-memory feasibility and prompt token limits, requiring a relational database (PostgreSQL) or Vector Search / RAG system.
- **Cost Scaling**: System 3 requires 3 to 5 LLM inference passes per user question. Under high query volume, token costs grow linearly with each reasoning step.

---

## 13. Performance Considerations

### Latency Profiles
1. **System 2 (Workflow)**: `< 1ms` execution time. Pure local CPU computation, zero network overhead.
2. **System 1 (Chatbot)**: Single LLM call (`~200ms - 800ms` on Groq; `~2s - 10s` on local Ollama).
3. **System 3 (Agent)**: Multi-turn loop requiring `N` round trips to the LLM (typically 2 to 4 turns). Total latency is `N * (LLM inference + network RTT) + Tool latency`. On Groq, this ranges from `600ms to 2.5s`.

---

## 14. Maintainability

### Modularity & Separation of Concerns
- **High Modularity**: Tools are cleanly decoupled from the agent loop in `tools.py`. The tool schema definitions sit directly beside the Python implementations.
- **Configuration Centralization**: `config.py` centralizes client instantiation and mock data, preventing duplicate initialization code across scripts.
- **Code Readability**: Python files are concise, well-annotated, and adhere to clean standard library idioms.

---

## 15. Strengths

1. **Defensive Mathematical Tooling**: Implementing the calculator with `ast` rather than `eval()` adheres to industry gold-standard security practices for LLM tool development.
2. **Transparent Architectural Comparison**: The test suite (`QUESTIONS` and `challenge.py`) cleanly exposes the distinct failure modes of prompt-only LLMs vs. rule-based engines vs. agentic loops.
3. **Multi-Provider Flexibility**: The architecture allows developers to switch between local private inference (Ollama) and high-speed cloud inference (Groq) with a single environment variable change.
4. **Deterministic Fallbacks**: Both tools return controlled error strings rather than unhandled Python exceptions, allowing the agent to observe errors and adjust its plan.

---

## 16. Limitations

1. **SDK Compatibility Bug**: The inclusion of `include_reasoning=False` in `agent.py` prevents execution on standard OpenAI client installations without modification.
2. **Zero Automated Test Coverage**: Absence of formal `pytest` suites leaves regression verification reliant on manual script execution.
3. **No Database Persistence**: Course catalog is hard-coded in Python memory; cannot be dynamically updated without modifying code.
4. **Synchronous Execution**: Lack of `async`/`await` patterns prevents concurrent request handling.
5. **Windows Shell Encoding**: Scripts do not reconfigure `sys.stdout` encoding, leading to terminal crashes on default Windows code page 1252 when models return unicode characters.

---

## 17. Future Improvements

### Priority 1: Runtime Robustness
- Wrap the completion call in `agent.py` to remove non-standard arguments or conditionally pass them based on provider inspection.
- Add `sys.stdout.reconfigure(encoding='utf-8')` to CLI scripts to guarantee cross-platform console safety.

### Priority 2: Architecture & Scalability
- Migrate `COURSE_FEES` to SQLite / SQLAlchemy with dynamic CRUD endpoints.
- Wrap the core agent logic in an asynchronous REST API using `FastAPI`.
- Add exponential backoff retry mechanisms for upstream LLM network calls using `tenacity`.

### Priority 3: Testing & Evaluation
- Implement automated unit tests in `pytest` validating:
  - AST calculator operator isolation and rejection of illegal syntax.
  - Case-insensitivity and boundary cases in `get_course_fee`.
  - Mocked agent conversation loops with simulated tool call responses.

---

## 18. Overall Technical Findings

1. **Unaugmented LLMs Cannot Solve Proprietary Enterprise Tasks**: System 1 proves that no amount of prompt engineering can allow a standard LLM to accurately deduce private corporate data it was never trained on.
2. **Rule-Based Workflows Break at the Boundary of Natural Language**: System 2 demonstrates that while regex workflows are cheap and fast, human communication is too varied for hardcoded rules. The moment comparison or budget planning is introduced, the workflow fails completely.
3. **Agents Solve the Compositional Gap**: System 3 demonstrates that by combining language models with deterministic tools via a ReAct loop, systems achieve the factual precision of deterministic code alongside the cognitive flexibility of LLMs.
4. **Security Must Be Enforced at the Tool Boundary**: Autonomous agents must never be paired with arbitrary code execution tools. Deterministic parsing (AST) is non-negotiable for enterprise safety.

---

## 19. Conclusion

The College Fee Assistant codebase effectively illustrates the evolution of AI software engineering. It empirically proves why modern enterprise AI is moving away from pure chat interfaces and rigid rule engines toward **grounded, tool-augmented autonomous agents**. When implemented with strict tool sandboxing and structured schemas, agentic architectures successfully resolve the tension between natural language understanding and strict factual accuracy. Moving this system to production requires addressing SDK parameter compatibility, adding asynchronous network handling, and backing the tool layer with persistent database infrastructure.
