# Day 5 - Placement Interview Coach (Groq Version)

## Scenario
Placement Interview Coach

This is an independent Day 5 scenario using Groq's OpenAI-compatible API.

Models:
- `openai/gpt-oss-20b`
- `openai/gpt-oss-120b`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Put your Groq key in `.env`:

```text
GROQ_API_KEY=your_key_here
```

## Run

```powershell
python main.py
```

Benchmark both models:

```powershell
python benchmark.py
```

## Day 5 concepts demonstrated

- Fixed scenario behaviour through a system prompt
- Non-streaming completion
- Streaming completion
- TTFT (time to first token)
- Total response time
- Output tokens and tokens/second
- Program-level system prompt override
- Comparison of GPT-OSS 20B and GPT-OSS 120B

## Important assignment note

The official Day 5 task asks for an Ollama Modelfile and Ollama REST API. This project is the Groq-compatible alternative because it uses the Groq API rather than a local Ollama server.
