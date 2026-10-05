import json

from config import client, MODEL, banner

SCHEMA = {
    "type": "object",
    "properties": {
        "venue_type": {
            "type": "string"
        },
        "needs_budget": {
            "type": "boolean"
        },
        "needs_tool": {
            "type": "boolean"
        }
    },
    "required": [
        "venue_type",
        "needs_budget",
        "needs_tool"
    ],
    "additionalProperties": False
}

QUESTION = (
    "I want to conduct a coding event in an auditorium "
    "and calculate the budget."
)

def ask(response_format, label):
    print(f"\n--- {label} ---")

    try:
        request = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Extract the request as JSON with the keys "
                        "venue_type, needs_budget and needs_tool. "
                        "Reply with JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": QUESTION
                }
            ],
            "temperature": 0
        }

        if response_format is not None:
            request["response_format"] = response_format

        reply = client.chat.completions.create(**request)

        text = reply.choices[0].message.content.strip()

        print("raw:", text)
        print("parsed:", json.loads(text))

    except Exception as error:
        print(
            "ERROR:",
            type(error).__name__,
            error
        )

if __name__ == "__main__":
    banner("STRUCTURED OUTPUT DEMO")

    ask(
        None,
        "1. No constraint"
    )

    ask(
        {"type": "json_object"},
        "2. JSON mode"
    )

    ask(
        {
            "type": "json_schema",
            "json_schema": {
                "name": "event_request",
                "strict": True,
                "schema": SCHEMA
            }
        },
        "3. Strict schema mode"
    )
