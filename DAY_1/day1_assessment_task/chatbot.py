import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )


client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"


SYSTEM_PROMPT = """
You are CareerLens, a career-readiness assistant.

You do NOT have access to the student's private files.

You must not invent personal information such as:

- CGPA
- technical skills
- DSA progress
- projects
- certifications

If personalized analysis is requested but the required
private data has not been provided, explain that the data
is unavailable.

You may still provide general career guidance.
"""


USER_REQUEST = """
I am preparing for a Software Engineer internship.

Analyze my academic performance, DSA progress,
technical skills, and projects against the target job
requirements.

Identify my most important gaps and create a
prioritized 30-day improvement plan.
"""


def main():

    print("=" * 70)
    print("CAREERLENS — PLAIN CHATBOT")
    print("=" * 70)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_REQUEST
            }
        ],
        temperature=0.2
    )

    print("\nFINAL RESPONSE\n")

    print(
        response.choices[0].message.content
    )


if __name__ == "__main__":
    main()
