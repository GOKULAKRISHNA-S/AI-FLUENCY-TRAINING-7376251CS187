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
    ("a good call", FakeCall("get_course_fee", '{"course_code": "AI202"}')),
    ("invalid JSON", FakeCall("get_course_fee", '{"course_code": "AI202"')),
    ("unknown tool", FakeCall("send_email", '{"to": "accounts@college.edu"}')),
    ("missing required", FakeCall("get_course_fee", '{}')),
    ("wrong type", FakeCall("get_course_fee", '{"course_code": 101}')),
    ("value outside the enum", FakeCall("get_course_fee", '{"course_code": "CS101", "semester": "summer"}')),
    ("invented extra argument", FakeCall("get_course_fee", '{"course_code": "CS101", "year": 2026}')),
    ("unknown course code", FakeCall("get_course_fee", '{"course_code": "ME404"}')),
    ("unsafe expression", FakeCall("calculator", json.dumps({"expression": "__import__(\'os\').system(\'ls\')"}))),
    ("empty arguments string", FakeCall("calculator", "")),
]

if __name__ == "__main__":
    print("=" * 78)
    for label, call in FAULTS:
        result = handle_tool_call(call, log=False)
        print(f"{label:<26} -> {result[:72]}")
    print("=" * 78)
    print("Every line above is a STRING. Nothing raised, nothing crashed:")
    print("each message goes back to the model, which can try again.")
