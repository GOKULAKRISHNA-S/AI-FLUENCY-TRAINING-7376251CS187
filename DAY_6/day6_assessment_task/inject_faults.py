import json

from robust_agent import handle_tool_call

class FakeFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class FakeCall:
    def __init__(self, name, arguments, call_id="call_test"):
        self.id = call_id
        self.type = "function"
        self.function = FakeFunction(name, arguments)

FAULTS = [
    (
        "good call",
        FakeCall(
            "get_item_price",
            '{"item": "projector"}'
        )
    ),
    (
        "invalid JSON",
        FakeCall(
            "get_item_price",
            '{"item": "projector"'
        )
    ),
    (
        "unknown tool",
        FakeCall(
            "send_email",
            '{"to": "admin@college.edu"}'
        )
    ),
    (
        "missing required",
        FakeCall(
            "get_venue_charge",
            '{}'
        )
    ),
    (
        "wrong type",
        FakeCall(
            "get_venue_charge",
            '{"venue_type": 101}'
        )
    ),
    (
        "invalid enum",
        FakeCall(
            "get_venue_charge",
            '{"venue_type": "playground"}'
        )
    ),
    (
        "invented argument",
        FakeCall(
            "get_venue_charge",
            '{"venue_type": "auditorium", "year": 2026}'
        )
    ),
    (
        "unknown item",
        FakeCall(
            "get_item_price",
            '{"item": "laser"}'
        )
    ),
    (
        "unsafe expression",
        FakeCall(
            "calculate_event_cost",
            json.dumps({
                "expression": "__import__('os').system('dir')"
            })
        )
    ),
    (
        "arguments array",
        FakeCall(
            "get_item_price",
            '["projector"]'
        )
    )
]

if __name__ == "__main__":
    print("=" * 78)

    for label, call in FAULTS:
        result = handle_tool_call(
            call,
            log=False
        )

        print(
            f"{label:<25} -> {result[:100]}"
        )

    print("=" * 78)
    print("All injected faults were handled without crashing.")
