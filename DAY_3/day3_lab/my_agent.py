import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Day_1')))
from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a college assistant. Use read_webpage to read any page or file the user "
    "mentions, and use calculator for every arithmetic step. Never guess a number that "
    "should come from a page. If no tool is needed, answer directly."
)

def agent(question, max_steps=6, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]

    for step in range(1, max_steps + 1):
        # 1. REASON
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        message = response.choices[0].message

        # 2. STOP: no tool requested means the model has finished
        if not message.tool_calls:
            return message.content.strip()

        # 3. RECORD the model's request
        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function",
                            "function": {"name": call.function.name,
                                         "arguments": call.function.arguments}}
                           for call in message.tool_calls]})

        # 4. ACT and 5. OBSERVE
        for call in message.tool_calls:
            name = call.function.name
            arguments = {}
            try:
                arguments = json.loads(call.function.arguments or "{}")
                function = TOOL_FUNCTIONS.get(name)
                if function is None:
                    result = f"Unknown tool: {name}. Available: {list(TOOL_FUNCTIONS)}"
                else:
                    result = function(**arguments)
            except json.JSONDecodeError as error:
                result = f"Argument error: {error}. Send valid JSON."
            except TypeError as error:
                result = f"Argument error: {error}"
            if verbose:
                print(f"   step {step}: {name}({arguments}) -> {str(result)[:120]}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": str(result)})

    # 6. SAFETY EXIT
    return "Stopped: maximum steps reached without a final answer."

if __name__ == "__main__":
    banner("MY AGENT (no guards)")
    question = ("Read notice.html and tell me the total fee for CS101 and AI202 "
                "after the merit scholarship.")
    print("Q:", question)
    print("A:", agent(question))