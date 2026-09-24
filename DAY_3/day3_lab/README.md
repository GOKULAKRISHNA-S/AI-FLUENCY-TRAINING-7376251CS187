# Autonomous ReAct Agent with Tool Use and Production Guardrails

## Overview

This project implements an autonomous conversational agent based on the **ReAct (Reason + Act)** pattern using Python and the OpenAI-compatible API standard. The system is designed to solve a core problem of Large Language Models (LLMs): **hallucination of private institutional data and arithmetic errors in multi-step reasoning**.

By integrating deterministic external tools with an LLM decision-making loop, the agent autonomously retrieves factual data from local files or web pages and performs precise arithmetic. Furthermore, the repository demonstrates the critical transition from an unconstrained agent (`my_agent.py`) to an enterprise-hardened agent (`my_agent_fixed.py`) equipped with three runtime guardrails: **loop detection**, **per-observation truncation**, and a **global character budget**.

## Key Features

- **Safe AST-Based Calculator**: Evaluates arithmetic expressions (`+`, `-`, `*`, `/`, `**`, unary `-`) using Python's `ast` (Abstract Syntax Tree) module without unsafe `eval()` execution.
- **Web & Local Document Reader**: Fetches remote web pages via HTTP/HTTPS or reads local filesystem documents (`.html`, `.txt`), sanitizing content by stripping HTML tags and embedded scripts.
- **Dynamic ReAct Loop**: Implements multi-turn reasoning and tool invocation using OpenAI function calling schemas (`tools` parameter) with `temperature=0`.
- **Multi-Provider LLM Support**: Modular configuration supporting **Ollama** (local offline models such as `qwen2.5:1.5b`), **Groq** (cloud inference such as `openai/gpt-oss-20b`), and **HuggingFace** router endpoints.
- **Guardrail 1 — Loop & Stall Detection**: Halts execution when an identical tool call (identical tool name and arguments) is executed 3 times without progression.
- **Guardrail 2 — Observation Truncation**: Caps individual tool outputs at 1,500 characters to prevent context window saturation from oversized documents.
- **Guardrail 3 — Cumulative Character Budget**: Limits total accumulated message characters to 30,000 per session to protect against unbounded token consumption and API billing overruns.
- **Synthetic Stress Testing Utility**: Includes a page generator (`make_big_page.py`) creating a 3,000-row document (360KB) to systematically trigger and validate context overflow defenses.

## Project Architecture

```
day3_lab/
├── .env                  # Environment configuration (API keys & provider selection)
├── .gitignore            # Git ignore rules for venv, cache, and secrets
├── requirements.txt      # Python package dependencies
├── config.py             # Provider configuration, client setup, and reference data
├── my_tools.py           # Deterministic tools (safe calculator & webpage/file reader)
├── my_agent.py           # Baseline ReAct agent loop (without runtime guardrails)
├── my_agent_fixed.py     # Hardened ReAct agent loop with 3 active guardrails
├── make_big_page.py      # Script generating stress-testing HTML page
├── notice.html           # Real-world sample document (course fees & scholarship rules)
├── big.html              # Generated large HTML file (3,000 student attendance records)
├── README.md             # Project documentation and operational guide
└── analysis.md           # Comprehensive technical and academic evaluation
```

## How It Works

The execution flow follows the classical Reason-Act-Observe cycle:

```
                  +--------------------------------+
                  |           User Prompt          |
                  +--------------------------------+
                                  |
                                  v
+-------------------> [Step 1: Reason (LLM)] <------------------+
|                                 |                             |
|                    Does LLM request tools?                    |
|                                 |                             |
|                 +---------------+---------------+             |
|                 | NO                            | YES         |
|                 v                               v             |
|        [Return Final Answer]           [Step 2: Act (Tool)]   |
|                                                 |             |
|                                         Execute Function      |
|                                                 |             |
|                                                 v             |
|                                    [Step 3: Guardrail Check]  |
|                                      - Loop detection (>=3)   |
|                                      - Truncation (1500 chars)|
|                                      - Budget cap (30k chars) |
|                                                 |             |
|                                                 v             |
|                                    [Step 4: Append to State]  |
|                                    {"role": "tool", ...}      |
+-------------------------------------------------+             |
```

1. **Initialization**: The user prompt and `SYSTEM_PROMPT` are placed into the message history array.
2. **Model Invocation (Reason)**: The agent calls `client.chat.completions.create` with `tools=TOOLS` and `temperature=0`.
3. **Termination Check**: If the model emits no `tool_calls`, its textual response is returned as the final answer.
4. **Tool Execution (Act)**: If tool calls are present, the agent parses the JSON arguments, looks up the corresponding Python function in `TOOL_FUNCTIONS`, and executes it.
5. **Observation & Guardrail Evaluation**:
   - In `my_agent.py`: Tool output is converted to string and appended to the message array.
   - In `my_agent_fixed.py`: The call signature is counted (halts if count $\ge 3$), the result string is truncated to 1,500 characters, and the cumulative character budget is tracked before appending.
6. **Iterative Feedback**: The conversation history with the tool observation is sent back to the LLM for the next reasoning step. The process repeats up to `max_steps=6`.

## Technologies Used

- **Language**: Python 3.10+ (Verified on Python 3.14.7)
- **LLM Client / SDK**: `openai>=1.40.0` (standardized OpenAI Python client)
- **Inference Providers**:
  - **Groq Cloud API** (`https://api.groq.com/openai/v1`) using model `openai/gpt-oss-20b`
  - **Ollama** (`http://localhost:11434/v1`) using model `qwen2.5:1.5b`
  - **HuggingFace Router** (`https://router.huggingface.co/v1`)
- **HTTP Client**: `requests` (with custom User-Agent `AgenticAI-Lab/1.0`)
- **Configuration Management**: `python-dotenv>=1.0.0`
- **Parsing & Security**: Python standard library `ast` (Abstract Syntax Tree) and `re` (regular expressions)

## Installation

### 1. Clone or Navigate to the Repository

```bash
cd c:\Users\gokul\Documents\AI_FLUENCY_TRAINING\DAY_3\day3_lab
```

### 2. Set Up Virtual Environment

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create or update the `.env` file in the root of `day3_lab/`:

```env
# Provider Selection: ollama | groq | huggingface
PROVIDER=groq

# Model Identifier
MODEL=openai/gpt-oss-20b

# API Keys (Required for cloud providers; leave blank or dummy for Ollama)
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

> **Security Note**: Never commit actual API keys to version control. The repository `.gitignore` explicitly excludes `.env`.

## Running the Project

### 1. Generate Stress-Testing Data (Optional)

Generate `big.html` (3,000 attendance records, ~360 KB):
```powershell
python make_big_page.py
```

### 2. Verify Tool Implementations Independently

Execute unit demonstrations for the calculator and webpage reader:
```powershell
python my_tools.py
```

### 3. Run the Baseline Agent (Unprotected)

```powershell
$env:PYTHONIOENCODING="utf-8"
python my_agent.py
```

### 4. Run the Hardened Agent (With Guardrails)

```powershell
$env:PYTHONIOENCODING="utf-8"
python my_agent_fixed.py
```

*(Setting `PYTHONIOENCODING="utf-8"` prevents Windows terminal encoding errors when models output unicode characters like non-breaking spaces `\u202f` or currency symbols).*

## Example Usage

### Successful Multi-Step Reasoning (`notice.html`)

**User Query**:
```
"Read day3_lab/notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship."
```

**Execution Trace (`my_agent_fixed.py`)**:
```
=== MY AGENT (guards on) | provider: groq | model: openai/gpt-oss-20b ===

Q: Read day3_lab/notice.html and tell me the total fee for CS101 and AI202 after the merit scholarship.
   step 1: read_webpage({'url': 'day3_lab/notice.html'}) -> Read error: 'day3_lab/notice.html' is not a URL and no such file exists.
   step 2: read_webpage({'url': './day3_lab/notice.html'}) -> Read error: './day3_lab/notice.html' is not a URL and no such file exists.
   step 3: read_webpage({'url': 'notice.html'}) -> Fee Notice Department of AI and Data Science - Fee Notice 2026 The following course fees are applicable for the current
A: The combined fee for CS101 and AI202 before any discount is:
- CS101: Rs. 12,000
- AI202: Rs. 18,000
Total before scholarship = Rs. 30,000

A merit scholarship gives a 10% reduction on the total fee:
- 10% of 30,000 = 3,000

Total fee after the merit scholarship = 30,000 - 3,000 = Rs. 27,000
```

### Infinite Loop Interception (`big.html`)

**User Query**:
```
"Read day3_lab/big.html and tell me how many students are listed."
```

**Execution Trace**:
```
Q: Read day3_lab/big.html and tell me how many students are listed.
   step 1: read_webpage({'url': 'day3_lab/big.html'}) -> Read error: 'day3_lab/big.html' is not a URL and no such file exists.
   step 2: read_webpage({'url': 'big.html'}) -> Attendance Register Student 0001 Roll BA0001 Attendance 61% Remarks: regular attendance recorded Student 0002...
   step 3: read_webpage({'url': 'big.html'}) -> Attendance Register Student 0001 Roll BA0001 Attendance 61% Remarks: regular attendance recorded Student 0002...
A: Stopped: the tool read_webpage was called 3 times with the same arguments and no progress was made. Last result: Attendance Register Student 0001 Roll BA0001...
```

## Project Workflow

```
[Start Script]
      |
[config.py] -------> Load .env, validate PROVIDER, instantiate OpenAI client
      |
[my_tools.py] -----> Define safe AST evaluator & requests/regex file scraper
      |
[my_agent*.py] ----> Build system instructions & initialize conversation history
      |
   [Loop] ---------> client.chat.completions.create(model, messages, tools, temperature=0)
      |
   [Branch] -------> No tool calls? ----> Terminate and display final response
      |                                              ^
      |                                              |
      +------------> Tool calls requested?           |
                           |                         |
                           v                         |
                     Execute Tool                    |
                           |                         |
                     [Guardrails]                    |
                     - Loop check                    |
                     - Truncation                    |
                     - Budget cap                    |
                           |                         |
                     Append result to messages ------+
```

## Testing

- **Automated Test Suite**: Not implemented (No dedicated `pytest` or `unittest` suite exists in the project).
- **Embedded Script Testing**:
  - `my_tools.py`: Tests valid arithmetic, exponentiation, syntax injection rejection (`import os`), local file loading, and missing file error handling.
  - `my_agent.py`: Tests baseline end-to-end question answering against `notice.html`.
  - `my_agent_fixed.py`: Tests three distinct scenarios:
    1. Multi-step reasoning with path recovery (`notice.html`).
    2. Missing file failure recovery (`fees.html`).
    3. Truncated large document loop prevention (`big.html`).

To run all embedded verification checks:
```powershell
python my_tools.py
python my_agent.py
python my_agent_fixed.py
```

## Limitations

1. **No Session State Persistence**: Message history exists only in volatile memory during the Python process execution; no database or disk caching is implemented.
2. **Fixed Maximum Iteration Window**: Both agents hardcode `max_steps=6`. Complex questions requiring >6 tool calls terminate prematurely.
3. **Naïve Loop Detection**: Loop guard checks only exact syntactic match of `(name, json.dumps(arguments, sort_keys=True))`. If an LLM alternates between subtly different argument formats (e.g. `'big.html'` vs `'./big.html'`), loop detection is delayed.
4. **Basic HTML Scraping**: `read_webpage` utilizes regular expressions rather than an HTML DOM parser (such as BeautifulSoup), making it vulnerable to malformed HTML markup.
5. **No Parallel Tool Execution**: Although the OpenAI API returns multiple tool calls in a single turn, the loop evaluates them sequentially without asynchronous concurrency.
6. **Hardcoded Path Sensitivity**: Running the script from directories other than `day3_lab/` requires model path adaptation as demonstrated in the execution logs.

## Future Improvements

- [ ] Implement an asynchronous execution engine (`asyncio` / `httpx`) for concurrent tool execution.
- [ ] Replace regex HTML stripping with a robust DOM parser (`BeautifulSoup` or `selectolax`).
- [ ] Add semantic chunking and vector search (RAG) for large files instead of brute-force truncation.
- [ ] Implement fuzzy/semantic loop detection to capture paraphrased repeating tool arguments.
- [ ] Develop formal `pytest` unit and integration test suites covering edge cases and mock API responses.

## Author / Project Information

- **Course / Context**: AI Fluency Training — Day 3 Laboratory
- **Repository**: `GOKULAKRISHNA-S/AI-FLUENCY-TRAINING-7376251CS187`
- **Environment**: Python 3.14 on Windows 11
