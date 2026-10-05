import json
from config import client, MODEL, banner

SCHEMA = {
    "type": "object",
    "properties": {
        "course_code": {"type": "string"},
        "wants_scholarship": {"type": "boolean"},
        "needs_tool": {"type": "boolean"},
    },
    "required": ["course_code", "wants_scholarship", "needs_tool"],
    "additionalProperties": False,
}

QUESTION = "What do I pay for AI202 if I have the merit scholarship?"

def ask(response_format, label, system_message="Extract the request details as JSON. Reply with JSON only."):
    print(f"\n--- {label} ---")
    try:
        reply = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": QUESTION},
            ],
            temperature=0,
            response_format=response_format,
        )
        text = reply.choices[0].message.content.strip()
        print("raw :", text)
        print("parsed:", json.loads(text))
    except Exception as error:
        print(f"not supported here ({type(error).__name__}: {error})")

if __name__ == "__main__":
    banner("STRUCTURED OUTPUTS - GROQ")
    ask(None, "1. no constraint (free text)")
    ask({"type": "json_object"}, "2. JSON mode: valid JSON, any shape")
    ask(
        {
            "type": "json_schema",
            "json_schema": {
                "name": "fee_query",
                "strict": True,
                "schema": SCHEMA,
            },
        },
        "3. schema mode: valid JSON in YOUR shape",
    )
