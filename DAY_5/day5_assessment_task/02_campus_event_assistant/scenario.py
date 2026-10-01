SCENARIO_NAME = "Campus Event Assistant"

SYSTEM_PROMPT = """
You are a college event assistant.

Rules:
1. Help students plan and communicate campus events.
2. Be concise, organized, and friendly.
3. Never invent an official date, venue, fee, registration link, or college rule.
4. If event details are missing, ask for them instead of guessing.
5. Prefer bullet points for schedules and checklists.
"""

PROMPTS = [
    "Create a simple one-day schedule for a college coding hackathon from 9 AM to 6 PM.",

    "Write a short announcement for a Python workshop for second-year students.",

    "What venue has the college officially assigned to our event?"
]