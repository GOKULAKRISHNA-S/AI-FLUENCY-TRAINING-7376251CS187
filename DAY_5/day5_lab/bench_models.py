"""Day 5, Part D: compare two models on the same prompts.
Contains both Local Ollama (commented out) and Groq API (active)."""
import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

PROMPTS = [
    "Reply with exactly: OK",
    "In two sentences, what is an AI agent?",
    "A course costs Rs. 18,000. A 15% scholarship is applied. Calculate the scholarship amount and the final payable amount. Show the calculation step by step. Give the final payable amount clearly.",
]

# ==========================================
# 1. LOCAL OLLAMA CONFIGURATION (Commented)
# ==========================================
# BASE_OLLAMA = "http://localhost:11434"
# MODELS_OLLAMA = ["qwen2.5:1.5b", "qwen2.5:7b"]      # put YOUR two models here
#
# def run_ollama(model, prompt):
#     start = time.time()
#     data = requests.post(f"{BASE_OLLAMA}/api/generate",
#                          json={"model": model, "prompt": prompt, "stream": False},
#                          timeout=600).json()
#     elapsed = time.time() - start
#     tokens = data.get("eval_count", 0)
#     load_ms = data.get("load_duration", 0) / 1e6
#     return elapsed, tokens, tokens / elapsed if elapsed else 0, load_ms, data.get("response", "").strip()
#
# if __name__ == "__main__":
#     for model in MODELS_OLLAMA:
#         print("=" * 72)
#         print("MODEL:", model)
#         for prompt in PROMPTS:
#             elapsed, tokens, rate, load_ms, text = run_ollama(model, prompt)
#             print(f"\n  prompt: {prompt[:50]}")
#             print(f"  {elapsed:5.1f} s | {tokens:4d} tokens | {rate:5.1f} tok/s | load {load_ms:7.1f} ms")
#             print(f"  answer: {text[:160]}")
#         print()


# ==========================================
# 2. GROQ API CONFIGURATION (Active)
# ==========================================
BASE = "https://api.groq.com/openai/v1"
API_KEY = os.getenv("GROQ_API_KEY")
# Using the model from .env, and a standard fast model for comparison
MODELS = [
    os.getenv("MODEL", "openai/gpt-oss-120b"),
    os.getenv("MODEL2", "openai/gpt-oss-20b")
]

if not API_KEY:
    print("Error: GROQ_API_KEY not found in .env file.")
    exit(1)

def run_groq(model, prompt):
    start = time.time()

    try:
        response = requests.post(
            f"{BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0
            },
            timeout=60
        )

        elapsed = time.time() - start

        if response.status_code != 200:
            return elapsed, 0, 0, 0, (
                f"API Error {response.status_code}: {response.text[:300]}"
            )

        data = response.json()

        text = data["choices"][0]["message"]["content"].strip()

        usage = data.get("usage", {})
        tokens = usage.get("completion_tokens", 0)

        rate = tokens / elapsed if elapsed else 0

        return elapsed, tokens, rate, 0.0, text

    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        return elapsed, 0, 0, 0, f"Connection Error: {e}"

if __name__ == "__main__":
    for model in MODELS:
        print("=" * 72)
        print("MODEL:", model)
        for prompt in PROMPTS:
            elapsed, tokens, rate, load_ms, text = run_groq(model, prompt)
            print(f"\n  prompt: {prompt[:50]}")
            print(f"  {elapsed:5.1f} s | {tokens:4d} tokens | {rate:5.1f} tok/s | load {load_ms:7.1f} ms")
            print(f"  answer: {text}")
        print()