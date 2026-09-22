# College Fee Assistant — Comparative AI Architecture Lab

> A comparative study and implementation of three AI engineering paradigms—Pure LLM Chatbot, Rule-Based Deterministic Workflow, and Tool-Calling Autonomous AI Agent—applied to private institutional course advising.

---

## 1. Project Overview

The **College Fee Assistant** project is a targeted benchmarking and architectural lab designed to analyze how different software and artificial intelligence paradigms solve domain-specific data retrieval, arithmetic calculation, and student advising challenges.

### Problem It Solves
Modern organizations frequently require automated systems to handle structured queries involving proprietary or private business data (such as confidential tuition fees) along with mathematical computations (such as scholarship deductions and cost comparisons). Standard off-the-shelf Large Language Models (LLMs) do not possess internal knowledge of proprietary, unindexed institutional data and frequently hallucinate numeric facts or perform inaccurate mental arithmetic. Conversely, hardcoded programmatic workflows are completely brittle and fail when user inquiries depart from strict syntactic patterns.

### Target Users
- **AI and Software Engineers**: Evaluating architectural tradeoffs between prompt-only chatbots, rigid deterministic code, and autonomous tool-augmented agents.
- **Academic Advisors & Students**: The end-user persona interacting with the system to inquire about course tuition, compute scholarship discounts, and evaluate multi-course budgets.

### What the System Does
The system implements and contrasts three distinct architectural approaches to answer queries about a set of private college courses (`CS101`, `AI202`, `DS303`):
1. **System 1 (Chatbot - Pure LLM)**: Relies exclusively on pre-trained parametric knowledge through system and user prompting.
2. **System 2 (Workflow - Rule-Based Engine)**: Uses regex pattern matching and procedural logic without any machine learning model.
3. **System 3 (AI Agent - Tool-Augmented ReAct Loop)**: Implements an autonomous multi-step reasoning loop where the LLM evaluates the query, decides whether to invoke deterministic local tools (`get_course_fee` and an AST-based `calculator`), observes tool outputs, and synthesizes a grounded response.

---

## 2. Problem Statement

### The Real-World Problem
Enterprise and institutional software requires systems that can understand natural human language while maintaining 100% factual accuracy regarding private data and mathematical calculations.

### Existing Difficulties
1. **Private Data Isolation**: Proprietary course fees (`CS101: 12,000`, `AI202: 18,000`, `DS303: 15,000`) do not exist in public LLM pre-training corpuses. An unaugmented LLM either hallucinates arbitrary figures or admits ignorance.
2. **Arithmetic Inaccuracy in LLMs**: Autoregressive next-token prediction struggles with complex multi-step math (e.g., sum calculation followed by percentage deductions) without external calculation aids.
3. **Rigidity of Rule-Based Systems**: Traditional regex/conditional pipelines can calculate values deterministically if the exact syntax matches, but they cannot process natural language variations, comparative semantics ("is X more expensive than Y?"), or creative text generation.

---

## 3. Proposed Solution

This project presents a side-by-side comparative architecture evaluating three levels of system capability against a standardized test set (`QUESTIONS`):

```
                        User Question
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
┌──────────────┐      ┌──────────────┐      ┌─────────────────┐
│   System 1   │      │   System 2   │      │    System 3     │
│ Pure Chatbot │      │ Rule Workflow│      │    AI Agent     │
└──────┬───────┘      └──────┬───────┘      └────────┬────────┘
       │                      │                      │
 Prompt Only            Regex Parsing         Reason + Tool Call
 (No Data/Tools)        & Hardcoded Logic     (AST Calc + Data)
       │                      │                      │
       ▼                      ▼                      ▼
Hallucination /         Exact for Regex;      Factual, Grounded,
Polite Ignorance        Fails on Unscripted    Flexible Reasoning
```

### Complete End-to-End Flow
1. **System 1 (Chatbot)**: User query -> LLM completion with system prompt -> Natural language answer (unaware of private data).
2. **System 2 (Workflow)**: User query -> Regex course code extraction -> Dict lookup -> Hardcoded total/scholarship logic -> Formatted text response.
3. **System 3 (Agent)**: User query -> LLM tool selection -> JSON tool call emission -> Local Python tool execution (`get_course_fee`, `calculator`) -> Observation fed back -> Iterative loop (max 6 steps) -> Final grounded response.

---

## 4. Key Features

| Feature | Implementation | Purpose & Fit | Status |
|---|---|---|---|
| **Multi-Provider LLM Configuration** | `config.py` | Allows switching between local (`ollama`) and cloud-hosted (`groq`, `huggingface`) inference providers via standard OpenAI-compatible client API. | Implemented |
| **System 1: Pure LLM Chatbot** | `chatbot.py` | Demonstrates zero-tool baseline conversational LLM behavior against private institutional questions. | Implemented |
| **System 2: Rule-Based Workflow** | `workflow.py` | Demonstrates deterministic regex-based string extraction and mathematical calculation without an LLM. | Implemented |
| **System 3: Tool-Calling AI Agent** | `agent.py` | Multi-step agent loop coordinating LLM reasoning with external tool dispatch. | Implemented (Note: SDK parameter limitation documented below) |
| **Safe AST Expression Evaluator** | `tools.py` (`calculator`) | Evaluates arithmetic (`+`, `-`, `*`, `/`, unary `-`) safely using Python's `ast` module, avoiding dangerous `eval()`. | Implemented |
| **Private Fee Lookup Tool** | `tools.py` (`get_course_fee`) | Case-insensitive lookup against private in-memory course repository. | Implemented |
| **Setup Diagnostic** | `check_setup.py` | Validates Python runtime, active provider, model name, and API connectivity. | Implemented |
| **Comparative Challenge Runner** | `challenge.py` | Evaluates Workflow vs. Agent against an unscripted budget constraint inquiry. | Implemented |

---

## 5. System Architecture

```
                                +---------------------------+
                                |        Environment        |
                                |       (.env file)         |
                                +-------------+-------------+
                                              |
                                              v
                                +---------------------------+
                                |         config.py         |
                                |  - Provider & Model config|
                                |  - OpenAI Client instance |
                                |  - COURSE_FEES data       |
                                |  - Benchmark QUESTIONS    |
                                +-------------+-------------+
                                              |
       +--------------------------------------+------------------------------------+
       |                                      |                                    |
       v                                      v                                    v
+---------------+                     +---------------+                  +-------------------+
|  chatbot.py   |                     |  workflow.py  |                  |     agent.py      |
|  (System 1)   |                     |  (System 2)   |                  |    (System 3)     |
+-------+-------+                     +-------+-------+                  +---------+---------+
        |                                     |                                    |
        | [User Prompt]                       | [Regex Extraction]                 | [Multi-Turn Loop]
        v                                     v                                    v
+---------------+                     +---------------+                  +-------------------+
| LLM Provider  |                     |  COURSE_FEES  |                  | LLM Provider      |
| (Groq/Ollama) |                     |  Dictionary   |                  | (Tool Calling API)|
+-------+-------+                     +-------+-------+                  +---------+---------+
        |                                     |                                    | ^
        | [Text Generation]                   | [Hardcoded Math]     [Tool Calls]  | | [Observations]
        v                                     v                                    v |
+---------------+                     +---------------+                  +-------------------+
| Output String |                     | Output String |                  |     tools.py      |
+---------------+                     +---------------+                  | - get_course_fee  |
                                                                         | - calculator (AST)|
                                                                         +---------+---------+
                                                                                   |
                                                                                   v
                                                                         +-------------------+
                                                                         | Grounded Response |
                                                                         +-------------------+
```

---

## 6. Application Workflow

### Step-by-Step Execution Pathways

#### System 1 (Chatbot Flow):
1. User supplies natural language question (e.g., `"What is the fee for AI202?"`).
2. Script prepares payload with system prompt `"You are a helpful college assistant."`.
3. Client dispatches HTTP request to OpenAI-compatible endpoint.
4. Model generates text based purely on pre-training data; cannot retrieve private fees.
5. Response is returned to standard output.

#### System 2 (Workflow Flow):
1. Script receives question string.
2. Regex `[A-Z]{2}\d{3}` scans query to extract uppercase alphanumeric course tokens.
3. System checks `COURSE_FEES` hash map:
   - If no valid courses found, returns fallback: `"Sorry, I can only answer questions about course fees."`
   - If `"total"` is in query, sums discovered fees, checks for scholarship percentage regex, applies deduction, and returns formatted string.
   - If exactly one course is matched, returns individual fee.
   - For all other linguistic structures (comparisons, greetings, budget planning), aborts with fallback error.

#### System 3 (AI Agent Flow):
1. Agent initializes conversation history with `SYSTEM_PROMPT` instructing the model to never guess fees and to invoke `get_course_fee` and `calculator`.
2. Iterative loop begins (up to `max_steps = 6`):
   - **Reason**: Calls LLM completion passing tool definitions (`TOOLS`).
   - **Evaluate**: If the LLM response contains no tool calls, loop terminates and content is returned.
   - **Act**: For each `tool_call` returned in message:
     - Parses arguments from JSON string.
     - Dispatches call to matching function in `TOOL_FUNCTIONS`.
     - Executes either `get_course_fee(course_code)` or `calculator(expression)`.
   - **Observe**: Appends tool output to message history (`role: "tool"`).
3. Loop repeats with updated context until LLM generates its final synthesis or hits step limit.

---

## 7. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Runtime Environment** | Python 3.10+ (Tested on Python 3.14) | Base programming language |
| **LLM Interface SDK** | `openai` (`>= 1.40.0`) | Client interface conforming to OpenAI Chat Completions standard |
| **Environment Management** | `python-dotenv` (`>= 1.0.0`) | Parses local `.env` configuration |
| **Inference Providers** | Groq (`api.groq.com`), Ollama (`localhost:11434`), Hugging Face (`router.huggingface.co`) | Multi-backend LLM inference options |
| **Parsing & Parsing Safety** | Python Standard Library `ast`, `operator` | Safe AST arithmetic evaluation without code execution vulnerabilities |
| **Text Processing** | Python Standard Library `re` | Regular expression matching for deterministic workflow |
| **Data Serialization** | Python Standard Library `json` | Encoding and decoding tool calling payloads |
| **Data Storage** | In-Memory Dictionary (`COURSE_FEES`) | Mock private institutional database |

---

## 8. Project Structure

```
day1_lab/
│
├── .env                # Local environment configuration (Provider, API keys, Model)
├── .gitignore           # Git ignore declarations
├── requirements.txt    # Application dependencies (openai, python-dotenv)
│
├── config.py           # Centralized configuration, client factory, private data & benchmark suite
├── check_setup.py      # Diagnostic script to test connectivity with the chosen LLM provider
├── tools.py            # Tool implementations (get_course_fee, safe AST calculator) and schemas
├── chatbot.py          # System 1: Pure LLM implementation
├── workflow.py         # System 2: Deterministic, regex-based workflow implementation
├── agent.py            # System 3: Autonomous ReAct tool-calling agent implementation
├── challenge.py        # Benchmark challenge script comparing Workflow vs. Agent
│
├── README.md           # High-level architecture and operational documentation
└── analysis.md         # In-depth technical analysis and comparative evaluation
```

---

## 9. Core Components

### 1. `config.py`
- **Responsibility**: Environment loading, dynamic provider switching, OpenAI client instantiation, mock private data definition, and benchmark question registry.
- **Inputs**: Environment variables (`PROVIDER`, `MODEL`, `GROQ_API_KEY`, `HF_TOKEN`).
- **Outputs**: Configured `client` instance, strings `PROVIDER`, `MODEL`, dict `COURSE_FEES`, list `QUESTIONS`.
- **Relationship**: Imported by all execution scripts (`check_setup.py`, `chatbot.py`, `workflow.py`, `agent.py`, `tools.py`).

### 2. `tools.py`
- **Responsibility**: Houses deterministic tools callable by agents and users.
- **Components**:
  - `get_course_fee(course_code)`: Case-insensitive dictionary lookup returning course fee in INR or error string.
  - `calculator(expression)`: Parses input with `ast.parse(mode="eval")` and evaluates strictly binary/unary arithmetic operators (`+`, `-`, `*`, `/`).
  - `TOOLS`: OpenAI-compliant JSON schemas specifying tool names, descriptions, and JSON Schema parameters.
  - `TOOL_FUNCTIONS`: Function dispatch mapping strings to python callables.
- **Inputs**: Function arguments generated by LLM tool calls.
- **Outputs**: Stringified scalar values or descriptive error strings.

### 3. `chatbot.py`
- **Responsibility**: Executes System 1 baseline. Sends questions directly to LLM with standard system prompt.
- **Inputs**: Natural language strings from `QUESTIONS`.
- **Outputs**: Generated string from model choices.

### 4. `workflow.py`
- **Responsibility**: Executes System 2 baseline. Implements strict procedural extraction and calculation rules.
- **Inputs**: Natural language questions.
- **Outputs**: Formatted answer strings or fallback rejection messages.

### 5. `agent.py`
- **Responsibility**: Executes System 3. Orchestrates the iterative loop between LLM reasoning and local tool execution.
- **Inputs**: Natural language question, optional `max_steps` (default 6), `verbose` flag.
- **Outputs**: Synthesized response string combining data from multiple tool invocations.

### 6. `challenge.py`
- **Responsibility**: Evaluates Workflow vs. Agent on an unscripted budget constraint query: `"I can pay Rs. 30,000. Which two courses can I take together within this budget?"`.

---

## 10. AI / ML / Agent Architecture

The project implements an **autonomous Tool-Calling Agent (ReAct Pattern)** in `agent.py`.

```
                      +-----------------------------+
                      |     User Input / Prompt     |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
               +----->|       LLM Reason Step       |<----+
               |      |  (client.chat.completions)  |     |
               |      +--------------+--------------+     |
               |                     |                    |
               |           Does message contain           |
               |               tool calls?                |
               |              /           \               |
               |          [Yes]           [No]            |
               |            /               \             |
               |           v                 v            |
               |    +--------------+   +---------------+  |
               |    | Act: Parse   |   | Final Answer: |  |
               |    | Tool Call ID |   | Return text   |  |
               |    | & Arguments  |   | to caller     |  |
               |    +-------+------+   +---------------+  |
               |            |                             |
               |            v                             |
               |    +--------------+                      |
               |    | Local Tool   |                      |
               |    | Execution    |                      |
               |    | (tools.py)   |                      |
               |    +-------+------+                      |
               |            |                             |
               |            v                             |
               |    +--------------+                      |
               |    | Observe:     |                      |
               +----+ Append tool  |----------------------+
                    | result msg   |
                    +--------------+
```

### Agent Observable Mechanics
- **Model**: Default `qwen2.5:1.5b` (Ollama) or `openai/gpt-oss-20b` (Groq/HF).
- **System Prompt**: Enforces strict grounding rules:
  > `"You are a college fee assistant. Never guess a fee: always use get_course_fee. Use calculator for any arithmetic. Available course codes: CS101, AI202, DS303. If no tool is needed, answer directly."`
- **Tool Selection**: The model receives OpenAI-format schemas describing `get_course_fee` and `calculator`.
- **Observation Feeding**: Each tool execution creates a message with `role: "tool"` matching the `tool_call_id`. The model processes this feedback in the next reasoning iteration.

### Code Accuracy Notice regarding `agent.py`
In `agent.py`, line 18 includes the parameter `include_reasoning=False` inside `client.chat.completions.create(...)`. In official versions of the `openai` Python SDK (including standard releases `>= 1.40.0`), `Completions.create()` does not accept `include_reasoning` as a keyword argument and raises a `TypeError: Completions.create() got an unexpected keyword argument 'include_reasoning'`. This parameter is specific to certain third-party proxies or custom fork signatures.

---

## 11. Database / Data Model

The application does not use an external relational or document database. Data storage is implemented in-memory in `config.py`.

### Course Fee Data Structure

| Entity / Key | Type | Value (INR) | Description |
|---|---|---|---|
| `CS101` | `int` | 12,000 | Computer Science Introductory Course Fee |
| `AI202` | `int` | 18,000 | Artificial Intelligence Core Course Fee |
| `DS303` | `int` | 15,000 | Data Science Core Course Fee |

### Benchmark Evaluation Suite

| Query ID | Prompt String | Target Capability Tested |
|---|---|---|
| Q1 | `"What is the fee for AI202?"` | Single fact retrieval from private database |
| Q2 | `"What is the total fee for CS101 and AI202 after a 10% scholarship?"` | Multi-item retrieval + percentage deduction math |
| Q3 | `"Is DS303 more expensive than CS101, and by how much?"` | Multi-item retrieval + comparative numeric reasoning |
| Q4 | `"Write a two-line welcome message for new AI students."` | Creative generation with no database lookup |

---

## 12. API Documentation

The project does not expose an HTTP/REST server. Instead, it consumes external LLM APIs via the OpenAI Python Client specification.

### Consumed External API Specification

#### Endpoint
`POST {BASE_URL}/chat/completions`
- Local: `http://localhost:11434/v1/chat/completions`
- Groq: `https://api.groq.com/openai/v1/chat/completions`
- Hugging Face: `https://router.huggingface.co/v1/chat/completions`

#### Request Payload Structure (Tool Calling)
```json
{
  "model": "openai/gpt-oss-20b",
  "temperature": 1.0,
  "messages": [
    {
      "role": "system",
      "content": "You are a college fee assistant..."
    },
    {
      "role": "user",
      "content": "What is the fee for AI202?"
    }
  ],
  "tools": [
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
    },
    {
      "type": "function",
      "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {
          "type": "object",
          "properties": {
            "expression": {"type": "string"}
          },
          "required": ["expression"]
        }
      }
    }
  ]
}
```

#### Expected Model Response Structure (Tool Call Request)
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": null,
        "tool_calls": [
          {
            "id": "call_123456",
            "type": "function",
            "function": {
              "name": "get_course_fee",
              "arguments": "{\"course_code\": \"AI202\"}"
            }
          }
        ]
      }
    }
  ]
}
```

---

## 13. Authentication and Security

### Authentication Implementation
- **API Key Handling**: Authentication is managed using standard bearer tokens passed to the `OpenAI` client.
- **Provider Switching**:
  - `ollama`: Uses `"ollama"` as a dummy key.
  - `groq`: Uses `GROQ_API_KEY` loaded from `.env`.
  - `huggingface`: Uses `HF_TOKEN` loaded from `.env`.
- Secrets are stored in `.env` and excluded from source control via `.gitignore`.

### Security Mechanisms & Limitations
- **AST Safe Calculator vs `eval()`**: The `calculator` function in `tools.py` parses arithmetic using Python's `ast` (Abstract Syntax Tree) module. It explicitly validates operator types (`Add`, `Sub`, `Mult`, `Div`, `USub`) and node types (`Constant`, `BinOp`, `UnaryOp`). Arbitrary code execution or system command injections are completely blocked.
- **Absence of User Authentication**: There is no end-user authentication, session management, or role-based access control (RBAC).
- **Console Encoding Vulnerability (Windows)**: On Windows terminals using default code page `cp1252`, non-ASCII output from LLMs (such as unicode spaces `\u202f` or quotes) can cause a `UnicodeEncodeError` unless `PYTHONIOENCODING=utf-8` is configured.

---

## 14. Installation

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14.
- Git (optional, if cloning).
- Active internet connection (for Groq/HuggingFace) OR a locally running Ollama instance (`ollama run qwen2.5:1.5b`).

### Setup Commands

1. **Clone or Navigate to Project Directory**:
   ```bash
   cd day1_lab
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 15. Environment Configuration

Create or edit the `.env` file in the root directory.

```ini
# Choose one of: ollama | groq | huggingface
PROVIDER=groq

# Optional: override default model
# For groq / huggingface: openai/gpt-oss-20b
# For ollama: qwen2.5:1.5b
MODEL=openai/gpt-oss-20b

# Required if PROVIDER=groq
GROQ_API_KEY=YOUR_GROQ_API_KEY

# Required if PROVIDER=huggingface
HF_TOKEN=YOUR_HF_TOKEN
```

---

## 16. Running the Project

### 1. Verify Configuration and Setup
```bash
python check_setup.py
```
*Expected Output*: Displays Python version, active provider, model name, and model reply `SETUP OK`.

### 2. Run Individual Tools Standalone
```bash
python tools.py
```
*Expected Output*: Validates standalone execution of `get_course_fee` and `calculator`.

### 3. Run System 1 (Chatbot)
```bash
# Set UTF-8 encoding on Windows to prevent console charmap errors:
# PowerShell:
$env:PYTHONIOENCODING="utf-8"; python chatbot.py
# Bash:
PYTHONIOENCODING=utf-8 python chatbot.py
```

### 4. Run System 2 (Rule-Based Workflow)
```bash
python workflow.py
```

### 5. Run System 3 (AI Agent)
```bash
$env:PYTHONIOENCODING="utf-8"; python agent.py
```
*(Note: See Section 10 for runtime note regarding `include_reasoning` argument).*

### 6. Run Comparative Challenge Benchmark
```bash
$env:PYTHONIOENCODING="utf-8"; python challenge.py
```

---

## 17. Testing

### Test Setup
- Automated unit test suites (e.g., `pytest`, `unittest`) are **not present** in the repository.
- Testing is implemented via script-level benchmark execution suites in the `if __name__ == "__main__":` blocks of `check_setup.py`, `tools.py`, `chatbot.py`, `workflow.py`, `agent.py`, and `challenge.py`.

### Verified Test Executions
1. `check_setup.py`: Executed successfully against provider `groq` with model `openai/gpt-oss-20b`. Model returned `SETUP OK`.
2. `tools.py`: Standalone execution verified:
   - `get_course_fee('ai202')` -> `18000`
   - `calculator('(12000 + 18000) * 0.9')` -> `27000.0`
   - `calculator('15000 - 12000')` -> `3000`
3. `workflow.py`: Standalone execution verified:
   - Q1: `Fee for AI202: Rs. 18,000` (Passed)
   - Q2: `Total fee: Rs. 27,000` (Passed)
   - Q3: `Sorry, I do not have a rule for this type of question.` (Expected limitation)
   - Q4: `Sorry, I can only answer questions about course fees.` (Expected limitation)

---

## 18. Output / Screenshots

The repository does not contain binary image assets or screenshot files. All outputs are produced directly in standard output. Below is the verified console transcript across systems:

```
=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===

Q: What is the fee for AI202?
A: Fee for AI202: Rs. 18,000
----------------------------------------------------------------------
Q: What is the total fee for CS101 and AI202 after a 10% scholarship?
A: Total fee: Rs. 27,000
----------------------------------------------------------------------
Q: Is DS303 more expensive than CS101, and by how much?
A: Sorry, I do not have a rule for this type of question.
----------------------------------------------------------------------
Q: Write a two-line welcome message for new AI students.
A: Sorry, I can only answer questions about course fees.
----------------------------------------------------------------------
```

---

## 19. Limitations

1. **In-Memory Mock Database**: Course data is stored in a static Python dictionary (`COURSE_FEES`) without persistence, indexing, or concurrency control.
2. **SDK Parameter Incompatibility in `agent.py`**: The `include_reasoning=False` parameter passed in `agent.py` causes standard OpenAI SDK versions to throw a `TypeError`.
3. **Rigid Pattern Matching in `workflow.py`**: Only matches exact course code formats and simple `"total"` + scholarship queries. Any phrasing variance causes a failure.
4. **Console Encoding Sensitivity**: Scripts lack explicit UTF-8 stdout wrapping, leading to `UnicodeEncodeError` on Windows systems unless `PYTHONIOENCODING=utf-8` is passed in shell environment.
5. **Lack of Automated Testing Framework**: Testing relies on manual execution of CLI scripts rather than CI/CD test runners.

---

## 20. Future Improvements

- **Resolve SDK Parameter Mismatch**: Remove or wrap `include_reasoning` in a compatibility check for standard OpenAI SDK installations.
- **Persistent Database Integration**: Replace `COURSE_FEES` with SQLite or PostgreSQL via an ORM.
- **REST / Web Interface**: Wrap the systems with FastAPI or Flask to expose endpoints for modern web and mobile frontends.
- **Automated Test Suite**: Introduce `pytest` suites covering unit tests for `tools.py` and mock integration tests for `agent.py`.
- **Expanded Agent Tooling**: Provide tools for checking seat availability, prerequisite verification, and semester scheduling.

---

## 21. Learning Outcomes

1. **Tradeoff Analysis Across AI Paradigms**: Understanding where pure LLMs excel (creative synthesis), where deterministic rules excel (speed and cost), and where agents are essential (grounded multi-step reasoning).
2. **Safe Code Execution Patterns**: Utilizing Python's `ast` module to construct a zero-risk expression evaluator, eliminating the severe vulnerabilities of `eval()`.
3. **Tool Calling & Agentic Loops**: Structuring tool schemas, managing conversation history across turns, and handling assistant tool invocations.
4. **Provider-Agnostic LLM Architecture**: Building an abstraction layer supporting multiple model providers (Ollama, Groq, HuggingFace) via standard protocol interfaces.

---

## 22. Conclusion

The College Fee Assistant project demonstrates the strengths and weaknesses of three core software engineering paradigms for automated reasoning. While pure LLMs hallucinate on private institutional data and rule-based workflows break on unscripted language, an autonomous tool-calling agent bridges the gap by combining deterministic data retrieval and safe arithmetic with natural language comprehension.
