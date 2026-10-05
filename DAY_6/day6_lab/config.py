import os
from openai import OpenAI

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set. Set your Groq API key before running the agent.")

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if MODEL not in {"openai/gpt-oss-20b", "openai/gpt-oss-120b"}:
    raise ValueError("GROQ_MODEL must be openai/gpt-oss-20b or openai/gpt-oss-120b")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)

def banner(title):
    print("=" * 78)
    print(title)
    print("Provider: Groq")
    print(f"Model: {MODEL}")
    print("=" * 78)
