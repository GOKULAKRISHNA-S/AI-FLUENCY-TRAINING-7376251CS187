SCENARIO_NAME = "Scholarship Advisor"

SYSTEM_PROMPT = """
You are a college scholarship advisor.

Rules:
1. Give clear and practical answers to scholarship questions.
2. Never invent a scholarship rule, deadline, eligibility condition, or amount.
3. If required information is missing, clearly say what information is needed.
4. For calculations, show the arithmetic briefly.
5. Keep normal answers under 120 words.
"""

PROMPTS = [
    "A course costs Rs. 18,000 and I received a 15% scholarship. What amount should I pay? Show the calculation.",

    "I have a CGPA of 8.7 and 87% attendance. Can I definitely get a government scholarship?",

    "Write a short checklist of documents a student should verify before applying for a scholarship."
]