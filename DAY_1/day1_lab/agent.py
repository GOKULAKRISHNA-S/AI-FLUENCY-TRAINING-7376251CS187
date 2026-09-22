import json
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee. Always use get_course_fee for course fees. "
    "Use calculator only for arithmetic calculations. "
    "Available course codes are CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        # Ask the model what to do
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        message = response.choices[0].message

        # No tool required -> final answer
        if not message.tool_calls:
            return (message.content or "").strip()

        # Add the assistant message exactly as returned
        messages.append(message)

        # Execute requested tools
        for call in message.tool_calls:

            name = call.function.name

            try:
                arguments = json.loads(
                    call.function.arguments or "{}"
                )
            except json.JSONDecodeError:
                result = "Invalid tool arguments."
                arguments = {}

            else:

                function = TOOL_FUNCTIONS.get(name)

                if function is None:
                    result = f"Unknown tool: {name}"
                else:
                    try:
                        result = function(**arguments)
                    except Exception as error:
                        result = f"Tool error: {error}"

            if verbose:
                print(
                    f"   step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        try:
            answer = agent(question)
            print("A:", answer)

        except Exception as error:
            print("ERROR:", error)

        print("-" * 70)