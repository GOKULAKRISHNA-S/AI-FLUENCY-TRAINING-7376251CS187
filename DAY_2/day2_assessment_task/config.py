import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


API_KEY = os.getenv("GROQ_API_KEY")


if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to the .env file."
    )


client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


MODEL = "openai/gpt-oss-20b"