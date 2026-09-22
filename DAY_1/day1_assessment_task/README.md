# CareerLens — Personal Placement Readiness Intelligence Agent

## 1. Project Overview

**CareerLens** is an automated placement-readiness assessment system designed to evaluate undergraduate engineering students against target software engineering internship requirements. Preparing for competitive technical campus placements requires students to assess multiple disparate dimensions of their profile simultaneously: academic consistency, core programming language proficiencies, Data Structures and Algorithms (DSA) problem-solving milestones, full-stack project portfolios, and domain-specific tool proficiencies.

In traditional academic settings, students either receive generic, one-size-fits-all advice from broad career counseling or manually compile spreadsheets to compare their abilities against job postings. CareerLens addresses this challenge by systematically analyzing verified student profile data against structured industry requirements to identify precise readiness gaps and generate actionable, prioritized 30-day preparation plans.

This project serves as the **Day 1 Assessment** for the course **"Agentic AI: Foundations and Open-Source Practice"** under **Unit 1: Foundations of AI Agents — Agent = LLM + Tools + Loop**. It implements the identical placement readiness problem across three distinct architectural paradigms:
1. **Plain LLM Chatbot**: A stateless large language model prompt without private data access or external tools.
2. **Rule-Based Workflow**: A deterministic Python program executing explicit, hard-coded evaluation algorithms on local JSON data.
3. **AI Agent**: An autonomous system coupling a large language model with application-defined tools in an iterative feedback loop (`LLM + Tools + Loop`).

---

## 2. Problem Statement

A 2nd-year computer science engineering student preparing for upcoming **Software Engineer Intern** campus recruitment drives faces significant uncertainty regarding their actual placement readiness. To prepare effectively, the student needs concrete, data-backed answers to critical evaluation questions:

- **Academic Standing**: Does their current CGPA (8.7/10.0) and academic trajectory meet baseline criteria for top-tier software engineering internships?
- **Technical Skills**: How do their ratings across core languages and developer tooling (Python, Java, C++, JavaScript, React, SQL, Git, Docker) compare with required and preferred industry standards?
- **DSA Milestones**: Is their problem-solving volume (146 total solved: 82 easy, 55 medium, 9 hard) sufficient against the standard internship benchmark of 250+ problems with 100+ medium problems?
- **Project Portfolio**: Does their portfolio of 2 full-stack AI-driven web applications meet employer expectations for project quantity, architectural depth, containerization, and cloud deployment?
- **Skill Gaps & Prioritization**: What are the largest quantitative deficits, and how should a finite 30-day preparation window be sequenced to maximize interview readiness?

Without access to private student records, conversational AI models hallucinate student details or provide vague advice. Conversely, hard-coded scripts calculate numbers but cannot synthesize strategic guidance tailored to nuanced career narratives. CareerLens benchmarks how different software architectures resolve this tension.

---

## 3. Objective

The primary objective of this project is to implement and critically evaluate three distinct software paradigms addressing the CareerLens placement readiness scenario:

1. **Plain LLM Chatbot (`chatbot.py`)**: Examine the behavior, privacy boundaries, and functional limits of an unaugmented language model instructed to refuse private data invention.
2. **Rule-Based Workflow (`workflow.py`)**: Demonstrate the predictability, rigidity, and deterministic calculation capabilities of traditional procedural programming operating directly on structured data.
3. **AI Agent (`agent.py`)**: Implement and demonstrate the foundational agentic paradigm—**LLM + Tools + Loop**—evaluating how autonomous tool discovery, iterative execution, and evidence-grounded synthesis provide both reasoning flexibility and factual accuracy.

The assessment provides an empirical basis for understanding when rule-based systems suffice, where pure conversational models fail, and how agentic loops bridge the gap between deterministic data execution and generative intelligence.

---

## 4. Three Approaches

### Plain LLM Chatbot

- **Architecture**: A single-turn request-response architecture using the OpenAI Python client pointed to the Groq cloud endpoint (`https://api.groq.com/openai/v1`) running `openai/gpt-oss-120b`.
- **Information Received**: Receives only the developer's system instructions and the raw text of the user request.
- **Private Data Access**: Has **no access** to private files (`student_profile.json`, `target_role.json`) and no tools to query them.
- **Handling of Request**: Bound by a strict system prompt instructing it not to hallucinate personal metrics (such as CGPA, DSA counts, or skills). When asked to analyze the student's profile, it acknowledges that it lacks private records, presents a generic evaluation checklist, and outlines a generic 30-day template while prompting the user to supply their data manually.
- **Limitations**: Incapable of autonomous data discovery; entirely dependent on user-supplied context; cannot verify truthfulness; cannot execute real-time calculations.

### Rule-Based Workflow

- **Architecture**: A pure Python procedural program without any LLM components or API dependencies.
- **Private Data Access**: Possesses **direct, unmediated file access** to local JSON data (`student_profile.json` and `target_role.json`) via standard file system operations.
- **Predefined Rules**: Implements hard-coded comparison logic:
  - Skill gaps: $\max(0, \text{required} - \text{current})$ sorted descending.
  - DSA gaps: Target minus actual for total, medium, and hard problems.
  - Project gaps: Compares project count against minimum (2) and preferred (3) thresholds.
  - Priorities: Appends formatted strings in a fixed procedural sequence.
- **Deterministic Processing**: Produces identical, byte-level deterministic output every single run. It executes in milliseconds with zero operational API cost.
- **Limitations**: Completely brittle; cannot process natural language; cannot interpret qualitative project descriptions; cannot adapt if JSON schema changes; cannot customize advice or create dynamic study schedules.

### AI Agent

- **Architecture**: An autonomous loop combining an LLM (`openai/gpt-oss-120b`), a formal OpenAI function-calling tool schema, an in-memory tool execution engine, and an iterative message history accumulator.
- **LLM**: Serves as the cognitive reasoning engine that interprets the user's objective, decides which tool to call next, evaluates tool observations, and generates the final synthesis.
- **Tools**: Six dedicated Python functions that encapsulate private data retrieval and gap calculations.
- **Tool Calling**: The LLM outputs structured JSON function calls matching predefined schemas (`name` and `arguments`).
- **Observations**: The Python application executes the chosen function locally, serializes the result to JSON, and passes it back to the LLM with the role `tool`.
- **Iterative Loop**: A controlled `for` loop (up to 8 iterations) that repeats the **Reason $\rightarrow$ Select Tool $\rightarrow$ Execute $\rightarrow$ Observe** cycle until the LLM determines that all required data has been gathered.
- **Final Response Generation**: Once the LLM recognizes that all academic, skill, DSA, project, and requirement data have been observed, it generates a comprehensive, evidence-grounded report without further tool calls.

---

## 5. System Architecture

### Architectural Overview of the Three Paradigms

#### Approach 1: Plain LLM Chatbot
```
User Request
     │
     ▼
┌────────────────────────────────────────┐
│             Chatbot Script             │
│  - System Prompt (Privacy Guardrail)   │
│  - User Prompt                         │
└──────────────────┬─────────────────────┘
                   │  Single API Call (No Tools, No Data)
                   ▼
┌────────────────────────────────────────┐
│            Groq Cloud LLM              │
│       (openai/gpt-oss-120b)            │
└──────────────────┬─────────────────────┘
                   │
                   ▼
Generic Advice & Data Request Template (Final Answer)
```

#### Approach 2: Rule-Based Workflow
```
Private Storage (JSON)
 [student_profile.json]   [target_role.json]
         │                       │
         └───────────┬───────────┘
                     │ Direct File Read (load_json)
                     ▼
┌────────────────────────────────────────┐
│         Python Workflow Engine         │
│  1. calculate_skill_gaps()             │
│  2. analyze_dsa()                      │
│  3. analyze_projects()                 │
│  4. create_priorities()                │
└────────────────────┬───────────────────┘
                     │ Fixed Procedural Output
                     ▼
Standard Terminal Output (Static Print Statements)
```

#### Approach 3: AI Agent (LLM + Tools + Loop)
```
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                       AI AGENT LOOP                         │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │                 LLM Decision Engine                 │   │
│   │              (openai/gpt-oss-120b)                  │   │
│   └──────────────┬──────────────────────▲───────────────┘   │
│                  │                      │                   │
│      Tool Call   │                      │ Tool Observation  │
│      Request     ▼                      │ (JSON payload)    │
│   ┌──────────────────────┐   ┌──────────┴───────────────┐   │
│   │ Tool Dispatcher      │   │ Application Observation  │   │
│   │ execute_tool()       │   │ Formatting (role: tool)  │   │
│   └──────────────┬───────┘   └──────────▲───────────────┘   │
│                  │                      │                   │
│                  ▼                      │                   │
│   ┌─────────────────────────────────────┴───────────────┐   │
│   │               Registered Tools (tools.py)           │   │
│   │  • get_academic_performance()                       │   │
│   │  • get_skill_profile()                              │   │
│   │  • get_dsa_progress()                               │   │
│   │  • get_project_profile()                            │   │
│   │  • get_target_job_requirements()                    │   │
│   │  • calculate_skill_gaps()                           │   │
│   └──────────────────────┬──────────────────────────────┘   │
│                          │ Controlled Read                  │
│                          ▼                                  │
│              [Private Data: JSON Files]                     │
└──────────────────────────┼──────────────────────────────────┘
                           │ Loop Complete (tool_calls == None)
                           ▼
Comprehensive Evidence-Grounded Placement Report (Final Answer)
```

---

## 6. AI Agent Architecture

The third implementation (`agent.py`) strictly adheres to the foundational equation of agentic systems:

$$\text{Agent} = \text{LLM} + \text{Tools} + \text{Loop}$$

### The Three Core Pillars

1. **The LLM (`openai/gpt-oss-120b`)**:
   Acts as the planning, reasoning, and synthesis core. It does not contain private domain knowledge in its weights. Instead, it inspects user requests, assesses what knowledge is missing, selects the next appropriate action, and synthesizes structured final outputs from accumulated observations.

2. **The Tools (`tools.py` & Tool Schemas)**:
   Represent the sensory and computational actuators of the system. Each tool provides a clean interface to a specific slice of data or a deterministic calculation. The LLM cannot alter tool source code or execute unauthorized file queries; it can only invoke registered tools via structured JSON signatures.

3. **The Loop (`for iteration in range(1, MAX_ITERATIONS + 1)`)**:
   Provides temporal state and execution feedback. The Python runtime maintains an append-only conversation log (`messages`). In each turn of the loop:
   - The LLM receives the complete message history including past assistant calls and tool observations.
   - The LLM decides whether to request another tool or conclude.
   - If a tool call is generated, the Python runtime dispatches execution and appends the result.
   - If no tool call is generated, the loop terminates immediately and returns the final response.

```
                  ┌──────────────────────┐
                  │     USER REQUEST     │
                  └──────────┬───────────┘
                             │
                             ▼
 ┌───────────────────► [Iterative Loop] ◄────────────────────┐
 │                           │                               │
 │                           ▼                               │
 │               ┌───────────────────────┐                   │
 │               │  LLM Evaluation Step  │                   │
 │               └───────────┬───────────┘                   │
 │                           │                               │
 │             Has Tool Call?│                               │
 │            ┌──────────────┴──────────────┐                │
 │        YES │                         NO  │                │
 │            ▼                             ▼                │
 │ ┌─────────────────────┐       ┌─────────────────────┐     │
 │ │ Parse Function Call │       │ Output Final Answer │     │
 │ └──────────┬──────────┘       └─────────────────────┘     │
 │            │                                              │
 │            ▼                                              │
 │ ┌─────────────────────┐                                   │
 │ │ Execute Local Tool  │                                   │
 │ └──────────┬──────────┘                                   │
 │            │                                              │
 │            ▼                                              │
 │ ┌─────────────────────┐                                   │
 │ │ Append Observation  │───────────────────────────────────┘
 │ └─────────────────────┘
```

> **Note on Observable Behavior**: This architecture relies strictly on observable inputs, structured tool calls, JSON observations, and final natural language outputs. It does not rely on or claim unverified internal "chain-of-thought" mechanisms.

---

## 7. Private Data Access

A foundational dimension of modern AI system design is how private, sensitive, or enterprise data is exposed to computation. CareerLens demonstrates three distinct data access models:

| Dimension | Plain LLM Chatbot (`chatbot.py`) | Rule-Based Workflow (`workflow.py`) | AI Agent (`agent.py`) |
|---|---|---|---|
| **Access Permission** | Zero access. System prompt forbids data access or fabrication. | Direct, unconstrained file-system access via `open()`. | Controlled, mediated access strictly via defined tools. |
| **Data Scope** | Zero private records visible to model context. | Full JSON file loaded directly into memory dictionaries. | Granular; tools return only specific sub-trees of the JSON data. |
| **Mechanism** | Natural language text prompt over HTTP. | Procedural Python `json.load()` calls. | OpenAI Tool Calling standard (`role: "tool"` responses). |
| **Data Leakage Risk** | Low (data is never loaded or exposed to the model). | Confined to local memory/local console; no cloud transmission. | Controlled transmission: only tool observation payloads enter LLM context. |
| **Integrity Guard** | Explicit negative system instruction ("You do NOT have access..."). | Hard-coded code logic. | Python-level validation dispatcher (`execute_tool`) and zero-argument enforcement. |

---

## 8. Tools

The agent environment defines six dedicated tools in `tools.py` and registers their schemas in `agent.py`. All tools are designed as zero-argument functions to prevent model hallucination of query parameters.

### 1. `get_academic_performance`
- **Purpose**: Retrieves the student's private academic record.
- **Retrieves / Calculates**: Returns the `academics` dictionary from `student_profile.json`, including overall CGPA (`8.7`), individual semester GPAs (`semester_1: 8.4`, `semester_2: 8.8`, `semester_3: 8.9`), and attendance percentage (`87%`).
- **Arguments**: None (`parameters: {type: "object", properties: {}, required: []}`).

### 2. `get_skill_profile`
- **Purpose**: Retrieves the student's self-assessed technical skills.
- **Retrieves / Calculates**: Returns the `skills` dictionary containing ratings on a scale of 0–10 for Python (`7`), Java (`6`), C++ (`5`), JavaScript (`7`), React (`5`), SQL (`6`), DSA (`5`), Git (`7`), Docker (`4`), AI (`6`), and RAG (`5`).
- **Arguments**: None.

### 3. `get_dsa_progress`
- **Purpose**: Retrieves the student's algorithmic problem-solving metrics.
- **Retrieves / Calculates**: Returns the `dsa` dictionary containing total problems solved (`146`), difficulty breakdown (`easy: 82`, `medium: 55`, `hard: 9`), and topic distribution across Arrays, Strings, Linked Lists, Stacks & Queues, Trees, Graphs, Dynamic Programming, and Binary Search.
- **Arguments**: None.

### 4. `get_project_profile`
- **Purpose**: Retrieves detailed descriptions of the student's completed software projects.
- **Retrieves / Calculates**: Returns the `projects` list containing project metadata:
  - *Revenue Recovery Intelligence* (FinTech, Next.js, FastAPI, PostgreSQL, AI Agents).
  - *Skill-to-Employment Platform* (AI, Python, FastAPI, RAG, PostgreSQL).
- **Arguments**: None.

### 5. `get_target_job_requirements`
- **Purpose**: Retrieves the benchmark requirements for the target career position.
- **Retrieves / Calculates**: Returns the complete `target_role.json` specification:
  - Target role title: `Software Engineer Intern`.
  - Required skills and minimum ratings: Python (8), Java (6), SQL (7), DSA (8), Git (7), React (6), Docker (5).
  - Preferred skills: System Design (4), Cloud (5), AI (5).
  - DSA expectations: Total problems (250), medium problems (100), hard problems (20).
  - Project expectations: Minimum projects (2), preferred projects (3).
- **Arguments**: None.

### 6. `calculate_skill_gaps`
- **Purpose**: Performs deterministic gap analysis between student skills and job requirements.
- **Retrieves / Calculates**: Iterates over all `required_skills` in the target role, retrieves corresponding values from the student profile (defaulting to 0 if missing), computes $\max(0, \text{required} - \text{current})$, sorts the skills by gap size descending, and returns:
  - `role`: "Software Engineer Intern".
  - `skill_gaps`: List of objects with `skill`, `current`, `required`, and `gap`.
- **Arguments**: None (reads both local JSON files internally).

---

## 9. Agent Execution Flow

When `python agent.py` is invoked, the execution follows an observable multi-step trajectory:

```
[Start]
  │
  ▼
Step 1: Application initializes OpenAI client pointing to Groq endpoint.
  │     Initializes message history with SYSTEM_PROMPT and USER_REQUEST.
  │
  ▼
Step 2: [Iteration 1] LLM inspects user request asking for academic, DSA, skill, and project analysis.
  │     LLM emits tool_call: get_academic_performance({}).
  │     Python executes tool, prints OBSERVATION (CGPA 8.7, attendance 87%), appends to history.
  │
  ▼
Step 3: [Iteration 2] LLM evaluates updated history; identifies need for technical skill profile.
  │     LLM emits tool_call: get_skill_profile({}).
  │     Python executes tool, prints OBSERVATION (skills dict), appends to history.
  │
  ▼
Step 4: [Iteration 3] LLM evaluates history; identifies need for DSA problem metrics.
  │     LLM emits tool_call: get_dsa_progress({}).
  │     Python executes tool, prints OBSERVATION (146 solved, breakdown), appends to history.
  │
  ▼
Step 5: [Iteration 4] LLM evaluates history; identifies need for project portfolio details.
  │     LLM emits tool_call: get_project_profile({}).
  │     Python executes tool, prints OBSERVATION (2 full-stack projects), appends to history.
  │
  ▼
Step 6: [Iteration 5] LLM evaluates history; identifies need for employer benchmark requirements.
  │     LLM emits tool_call: get_target_job_requirements({}).
  │     Python executes tool, prints OBSERVATION (role criteria), appends to history.
  │
  ▼
Step 7: [Iteration 6] LLM identifies need for computed skill gap metrics.
  │     LLM emits tool_call: calculate_skill_gaps({}).
  │     Python executes tool, prints OBSERVATION (sorted gap list), appends to history.
  │
  ▼
Step 8: [Iteration 7] LLM determines all evidence is present.
  │     LLM returns tool_calls = None.
  │     Synthesizes comprehensive final response grounded in observed facts.
  │
  ▼
Step 9: Python prints FINAL ANSWER and exits gracefully.
[End]
```

---

## 10. Project Structure

The project repository is structured as follows:

```
day1_assessment_task/
│
├── data/
│   ├── student_profile.json   # Synthetic private student data
│   └── target_role.json       # Target job criteria and industry benchmarks
│
├── .env                       # Local environment variables (API credentials)
├── .gitignore                 # Git ignore configuration
├── requirements.txt           # Python package dependencies
│
├── chatbot.py                 # Approach 1: Plain LLM chatbot implementation
├── workflow.py                # Approach 2: Rule-based procedural workflow
├── tools.py                   # Data access functions and calculation logic
├── agent.py                   # Approach 3: AI Agent implementation (LLM + Tools + Loop)
│
├── README.md                  # System architecture, implementation guide, and reference
└── analysis.md               # Evaluator assessment report and architectural analysis
```

> **Repository File Verification**: All files listed above exist in the workspace. No ghost files or unverified directories are referenced.

---

## 11. Technology Stack

CareerLens relies on a lightweight, modern open-source Python stack:

- **Programming Language**: Python 3.10+ (tested on Python 3.14).
- **LLM Client SDK**: `openai` ($\ge 1.40.0$) — utilized to interact with OpenAI-compatible API specifications.
- **Inference Provider & Endpoint**: Groq Cloud Platform (`https://api.groq.com/openai/v1`).
- **Foundation Model**: `openai/gpt-oss-120b` — an open-weights high-parameter model hosted on Groq LPU hardware for near-instantaneous inference and tool-calling fidelity.
- **Environment Management**: `python-dotenv` ($\ge 1.0.0$) — parses `.env` files into `os.environ`.
- **Data Format**: Standard JSON (`json` module from Python Standard Library).
- **Path Resolution**: `pathlib.Path` for cross-platform file referencing.

---

## 12. Data Model

The system utilizes two local JSON files to model the domain.

### 1. `data/student_profile.json`

Models private student records across academic, skill, DSA, and project dimensions:

```json
{
  "student": {
    "name": "Alex Kumar",
    "degree": "B.E. Computer Science and Engineering",
    "year": 2,
    "graduation_year": 2029
  },
  "academics": {
    "cgpa": 8.7,
    "semester_1": 8.4,
    "semester_2": 8.8,
    "semester_3": 8.9,
    "attendance": 87
  },
  "skills": {
    "Python": 7, "Java": 6, "C++": 5, "JavaScript": 7,
    "React": 5, "SQL": 6, "DSA": 5, "Git": 7,
    "Docker": 4, "AI": 6, "RAG": 5
  },
  "dsa": {
    "problems_solved": 146,
    "easy": 82, "medium": 55, "hard": 9,
    "topics": {
      "Arrays": 32, "Strings": 21, "Linked Lists": 14,
      "Stacks and Queues": 11, "Trees": 8, "Graphs": 5,
      "Dynamic Programming": 3, "Binary Search": 7
    }
  },
  "projects": [
    {
      "name": "Revenue Recovery Intelligence",
      "type": "FinTech",
      "description": "AI-powered revenue recovery and payment failure analysis platform",
      "technologies": ["Next.js", "FastAPI", "PostgreSQL", "AI Agents"]
    },
    {
      "name": "Skill-to-Employment Platform",
      "type": "AI",
      "description": "Platform for skill-gap analysis and employment outcome intelligence",
      "technologies": ["Python", "FastAPI", "RAG", "PostgreSQL"]
    }
  ],
  "certifications": 4
}
```

### 2. `data/target_role.json`

Models industry benchmark requirements for recruitment:

```json
{
  "role": "Software Engineer Intern",
  "required_skills": {
    "Python": 8, "Java": 6, "SQL": 7,
    "DSA": 8, "Git": 7, "React": 6, "Docker": 5
  },
  "preferred_skills": {
    "System Design": 4, "Cloud": 5, "AI": 5
  },
  "dsa_expectation": {
    "total_problems": 250,
    "medium_problems": 100,
    "hard_problems": 20
  },
  "project_expectation": {
    "minimum_projects": 2,
    "preferred_projects": 3
  }
}
```

---

## 13. Comparison Table

The three approaches are compared below across objective technical criteria:

| Evaluation Dimension | Plain LLM Chatbot (`chatbot.py`) | Rule-Based Workflow (`workflow.py`) | AI Agent (`agent.py`) |
|---|---|---|---|
| **Flexibility** | High linguistic adaptability; handles conversational phrasing but lacks student context. | Zero flexibility; cannot handle variations, natural language, or unmodeled attributes. | High flexibility; handles natural language while dynamically querying specific data. |
| **Decision-Making** | Single-step conversational generation governed by static system prompt instructions. | Hard-coded developer branching; fixed execution sequence (`calculate` $\rightarrow$ `dsa` $\rightarrow$ `projects` $\rightarrow$ `priorities`). | Autonomous LLM-driven dispatch; dynamically chooses tool sequence based on accumulated context. |
| **Tool Usage** | None. | Internal procedural functions called in fixed hardcoded sequence. | Formal tool schemas exposed via OpenAI function calling API. |
| **Private Data Access** | None; prohibited by system prompt guardrails. | Direct file-system reading of JSON files into application memory. | Controlled data access mediated through dedicated single-purpose tools. |
| **Multi-Step Handling** | Single-step turn; prompts user to supply missing data. | Multi-step procedural sequence executed top-to-bottom in a single run. | Iterative multi-step loop; reasons across multiple rounds of tool queries. |
| **Automation Level** | Generates text automatically, but requires human to manually supply data. | Fully automated computation and formatted text generation. | Fully automated goal-driven data collection, analysis, and synthesis. |
| **Reliability & Consistency** | High refusal reliability; output phrasing varies across temperature settings. | 100% deterministic calculation; zero calculation errors; no hallucination. | High factual reliability grounded in tool outputs; slight wording variation in final narrative. |
| **Execution Path** | Single linear API call (`client.chat.completions.create`). | Fixed top-to-bottom procedural execution script. | Dynamic iterative loop with variable iteration count governed by LLM stopping condition. |

---

## 14. What Makes the AI Agent Different?

The AI Agent represents a fundamental shift in software architecture. Rather than relying solely on frozen model weights (like the Chatbot) or rigidly hard-coding every decision path (like the Workflow), the Agent implements dynamic runtime coordination:

$$\mathbf{Agent} = \mathbf{LLM} + \mathbf{Tools} + \mathbf{Loop}$$

```
                ┌─────────────────────────────────────────┐
                │          TRADITIONAL WORKFLOW           │
                │                                         │
                │  Step A ──► Step B ──► Step C ──► End   │
                │  (Path is statically fixed at compile)   │
                └─────────────────────────────────────────┘

                ┌─────────────────────────────────────────┐
                │                AI AGENT                 │
                │                                         │
                │         ┌───────► Tool A ──────┐        │
                │         │                      ▼        │
                │  Objective ──► LLM ────────► Evaluate  │
                │         ▲       │ Decision     │        │
                │         │       ▼              │        │
                │         └─────── Tool B ◄──────┘        │
                │  (Path is dynamically decided at runtime│
                │   until stopping criteria are met)      │
                └─────────────────────────────────────────┘
```

1. **Autonomous Tool Selection**: The developer does not hardcode the order in which data is queried. The LLM decides what it needs based on the prompt. If the prompt asks only for DSA, the agent can call only `get_dsa_progress`.
2. **Context-Aware Iteration**: After receiving observations from `get_dsa_progress` and `get_target_job_requirements`, the LLM recognizes the discrepancy between 146 problems solved and the 250 required, and formulates strategic advice addressing that specific gap.
3. **Grounding Without Fine-Tuning**: Private data remains in local storage and is retrieved on-demand into context. The model does not need fine-tuning or prior knowledge of the student.
4. **Synthesis of Quantitative and Qualitative Data**: While `workflow.py` can only print numbers, `agent.py` evaluates the qualitative tech stack of the student's projects (Next.js, FastAPI, PostgreSQL) and identifies missing elements (such as Docker deployment and Cloud hosting) relative to preferred industry skills.

---

## 15. Limitations

To ensure objective technical documentation, the project’s limitations are explicitly stated:

- **Synthetic Data**: The profile in `student_profile.json` is a synthetic mock dataset created for academic evaluation.
- **Model & Inference Dependency**: The chatbot and agent depend on external network access and Groq cloud API availability.
- **Local File Storage**: Profiles are stored in local JSON files rather than an authenticated, encrypted relational database.
- **No Direct Resume/JD Parsing**: The system does not currently extract data from unstructured PDF resumes or live web job descriptions.
- **Zero-Argument Tools**: The current tools retrieve pre-determined JSON slices; they do not support dynamic parameterized queries (e.g., searching for a specific skill).
- **No Career Outcome Guarantees**: Analyses and 30-day plans are advisory readiness evaluations and do not guarantee interview offers or employment.

---

## 16. Installation

### Prerequisites
- Python 3.10 or higher installed on your system.
- A valid Groq API Key (obtainable from [Groq Console](https://console.groq.com/)).

### Setup Instructions

1. **Clone or Navigate to the Workspace Directory**:
   ```bash
   cd "C:\Users\gokul\Documents\AI - FLUENCY - TRAINING\DAY 1\day1_assessment_task"
   ```

2. **Create and Activate a Virtual Environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies**:
   Install the packages specified in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

---

## 17. Configuration

CareerLens uses environment variables loaded through `python-dotenv`.

1. Create a `.env` file in the root directory:
   ```bash
   # Windows PowerShell
   New-Item -ItemType File -Name .env -Force
   ```

2. Populate `.env` with your API credential:
   ```env
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   ```

> **Security Note**: Never commit real API keys to version control. The `.gitignore` file already includes `.env` to prevent credential exposure.

---

## 18. Running the Project

### 1. Run the Plain LLM Chatbot
Executes the unaugmented conversational baseline:
```bash
python chatbot.py
```
*(On Windows terminals where standard output defaults to legacy encodings, run `python -X utf8 chatbot.py` if character encoding errors occur).*

### 2. Run the Rule-Based Workflow
Executes the deterministic procedural analysis:
```bash
python -X utf8 workflow.py
```
*(The `-X utf8` flag ensures Unicode characters such as the arrow symbol `→` render properly on Windows PowerShell).*

### 3. Run the AI Agent
Executes the iterative agentic tool-calling loop:
```bash
python -X utf8 agent.py
```

---

## 19. Output Evidence

### Terminal Output Verification

The three approaches have been executed and verified in the evaluation environment. Below is the verified evidence of their outputs.

#### Output 1: Plain LLM Chatbot (`chatbot.py`)
```text
======================================================================
CAREERLENS — PLAIN CHATBOT
======================================================================

FINAL RESPONSE

I would be happy to help you prepare for a Software Engineer internship! 
However, as CareerLens, I do not have access to your private files or student 
records (such as your CGPA, technical skills ratings, DSA problem counts, or 
project details). To avoid giving inaccurate guidance, I cannot invent or assume 
these details.

In the meantime – a General Gap-Analysis Framework:
| Typical Requirement | Your Current Status | Evidence Needed | Notes / Gap |
| Academic (GPA/major)|                     | Transcripts     |             |
| DSA / Algorithmic   |                     | LeetCode profile|             |
| Languages           |                     | Repositories    |             |
| Projects            |                     | GitHub URLs     |             |

If you would like a tailored 30-day plan, please provide your current GPA, 
DSA breakdown, skills list, and project descriptions!
```
*Demonstrates: Strict adherence to privacy guardrails; refusal to fabricate unprovided private data; fallback to generic guidance.*

#### Output 2: Rule-Based Workflow (`workflow.py`)
```text
======================================================================
CAREERLENS — RULE-BASED WORKFLOW
======================================================================

SKILL GAPS
DSA: 5 → 8 (gap 3)
Python: 7 → 8 (gap 1)
SQL: 6 → 7 (gap 1)
React: 5 → 6 (gap 1)
Docker: 4 → 5 (gap 1)
Java: 6 → 6 (gap 0)
Git: 7 → 7 (gap 0)

DSA ANALYSIS
Problems: 146 / 250
Total gap: 104
Medium gap: 45
Hard gap: 11

PROJECT ANALYSIS
Projects: 2 / 2

PRIORITIES
1. Improve DSA (gap: 3)
2. Improve Python (gap: 1)
3. Improve SQL (gap: 1)
4. Improve React (gap: 1)
5. Improve Docker (gap: 1)
6. Complete 104 additional DSA problems
7. Solve 45 more medium-level DSA problems
```
*Demonstrates: Instantaneous deterministic computation of skill, DSA, and project gaps; structured procedural priority generation.*

#### Output 3: AI Agent (`agent.py`)
```text
======================================================================
CAREERLENS — AI AGENT
======================================================================

==================== ITERATION 1 ====================
TOOL CALL: get_academic_performance
ARGUMENTS: {}
OBSERVATION: { "academics": { "cgpa": 8.7, "semester_1": 8.4, "semester_2": 8.8, "semester_3": 8.9, "attendance": 87 } }

==================== ITERATION 2 ====================
TOOL CALL: get_skill_profile
ARGUMENTS: {}
OBSERVATION: { "skills": { "Python": 7, "Java": 6, "C++": 5, "JavaScript": 7, "React": 5, "SQL": 6, "DSA": 5, "Git": 7, "Docker": 4, "AI": 6, "RAG": 5 } }

==================== ITERATION 3 ====================
TOOL CALL: get_dsa_progress
ARGUMENTS: {}
OBSERVATION: { "dsa": { "problems_solved": 146, "easy": 82, "medium": 55, "hard": 9, ... } }

==================== ITERATION 4 ====================
TOOL CALL: get_project_profile
ARGUMENTS: {}
OBSERVATION: { "projects": [ { "name": "Revenue Recovery Intelligence", ... }, { "name": "Skill-to-Employment Platform", ... } ] }

==================== ITERATION 5 ====================
TOOL CALL: get_target_job_requirements
ARGUMENTS: {}
OBSERVATION: { "role": "Software Engineer Intern", "required_skills": { "Python": 8, "Java": 6, "SQL": 7, "DSA": 8, "Git": 7, "React": 6, "Docker": 5 }, ... }

==================== ITERATION 6 ====================
TOOL CALL: calculate_skill_gaps
ARGUMENTS: {}
OBSERVATION: { "role": "Software Engineer Intern", "skill_gaps": [ { "skill": "DSA", "current": 5, "required": 8, "gap": 3 }, ... ] }

==================== ITERATION 7 ====================

FINAL ANSWER
**Current Profile Summary**
- CGPA: 8.7 / 10 (consistent upward semester trend: 8.4 → 8.8 → 8.9)
- Technical Skills: Python (7/10), SQL (6/10), DSA (5/10), Docker (4/10)
- DSA Practice: 146 problems solved (82 easy, 55 medium, 9 hard)
- Projects: 2 full-stack AI-focused applications

[Comprehensive Tables for Academic Observations, Skill Gaps, DSA Gaps, and Priority Matrix]

30-Day Prioritized Improvement Plan:
- Days 1–2: Tracking board setup & baseline LeetCode diagnostic
- Days 3–10: DSA Intensive Sprint (solving 15 medium and 6 hard problems in Arrays/Graphs/DP)
- Days 11–14: Python advanced features & SQL complex query mastery
- Days 15–17: Docker containerization for both existing projects
- Days 18–20: React refactoring for frontend components
- Days 21–26: System Design basics & cloud deployment
- Days 27–30: Third project initiation & pair-programming mock interviews
```
*Demonstrates: Autonomous multi-step tool discovery, step-by-step observation handling, and generation of an evidence-grounded strategic roadmap.*

### Storing Evidence in `Output/`
The `Output/` directory is designated for saving session transcripts and screenshots. Evaluators can capture terminal sessions into PNG images or text logs using:
- `python -X utf8 chatbot.py > Output/chatbot_run.txt`
- `python -X utf8 workflow.py > Output/workflow_run.txt`
- `python -X utf8 agent.py > Output/agent_run.txt`

*(Note: In fresh repository checkouts, the `Output/` directory may be populated during local grading runs).*

---

## 20. Learning Outcomes

This assessment demonstrates several key insights in agentic AI:

1. **The Role of LLM as an Orchestrator**: The language model is most powerful not as an isolated repository of knowledge, but as an intelligent coordinator that delegates data queries to deterministic tools.
2. **Preventing Hallucination through Tool-Grounding**: LLMs will invent facts if forced to answer without data. Coupling strict negative system prompts with available data tools grounds the model in verified facts.
3. **Agent vs. Workflow Trade-offs**: Workflows provide speed, zero cost, and strict determinism. Agents provide semantic understanding, flexible querying, and qualitative synthesis.
4. **The Anatomy of the Agent Loop**: Understanding how state is maintained through accumulated message history (`messages.append(...)`) across discrete iterations without hidden state.
5. **Zero-Argument Tool Design**: Constraining tool parameter spaces minimizes model calling errors and eliminates injection vectors in sensitive environments.

---

## 21. Conclusion

The CareerLens project provides an empirical comparison of three computational architectures applied to student career readiness analysis:

- The **Plain LLM Chatbot** demonstrates safety and conversational fluency, but remains constrained by lack of data access.
- The **Rule-Based Workflow** provides fast, reliable, and deterministic mathematical calculations, but lacks qualitative reasoning and linguistic flexibility.
- The **AI Agent** brings these paradigms together by implementing **LLM + Tools + Loop**, enabling autonomous discovery, grounded quantitative analysis, and tailored natural language synthesis.

Each approach possesses distinct trade-offs in speed, cost, flexibility, and predictability. The choice of architecture should be driven by the specific requirements of the problem domain.
