import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_20B = os.getenv("MODEL_20B")
MODEL_120B = os.getenv("MODEL_120B")

GROQ_URL = os.getenv(
    "GROQ_URL",
    "https://api.groq.com/openai/v1/chat/completions"
)

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing from .env")

if not MODEL_20B:
    raise RuntimeError("MODEL_20B is missing from .env")

if not MODEL_120B:
    raise RuntimeError("MODEL_120B is missing from .env")