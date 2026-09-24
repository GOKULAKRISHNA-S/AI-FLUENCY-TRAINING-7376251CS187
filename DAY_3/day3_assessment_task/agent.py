import json

from config import client, MODEL
from tools import (
    read_webpage,
    find_on_page,
    calculate_trip_cost
)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": (
                "Read the local travel_data.html webpage. "
                "Use this when the user asks for information "
                "contained in the travel guide."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "find_on_page",
            "description": (
                "Search the local travel webpage for information "
                "about a destination, attraction, fee, opening hours, "
                "hotel, package, or other travel information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "The topic or keyword to search for."
                    }
                },
                "required": ["keyword"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_trip_cost",
            "description": (
                "Calculate the total cost of a trip using hotel cost, "
                "number of nights, food cost per day and travel cost."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_price": {
                        "type": "number"
                    },
                    "nights": {
                        "type": "integer"
                    },
                    "food_per_day": {
                        "type": "number"
                    },
                    "travel_cost": {
                        "type": "number"
                    }
                },
                "required": [
                    "hotel_price",
                    "nights",
                    "food_per_day",
                    "travel_cost"
                ]
            }
        }
    }
]


def run_tool(name, arguments):

    if name == "read_webpage":
        return read_webpage()

    elif name == "find_on_page":
        return find_on_page(arguments["keyword"])

    elif name == "calculate_trip_cost":
        return calculate_trip_cost(
            arguments["hotel_price"],
            arguments["nights"],
            arguments["food_per_day"],
            arguments["travel_cost"]
        )

    return "Unknown tool."


def agent(question):

    messages = [
        {
            "role": "system",
            "content": """
You are a Smart Travel Research Agent.

You have access ONLY to these three tools:

1. read_webpage
2. find_on_page
3. calculate_trip_cost

NEVER use or invent any other tool such as web_search.

Use find_on_page when the user asks about specific information
from the travel guide.

Use read_webpage when the user needs broader information
from the travel guide.

Use calculate_trip_cost when arithmetic is required.

If no tool is needed, answer normally.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )

    message = response.choices[0].message

    # No tool required
    if not message.tool_calls:
        return message.content

    messages.append(message)

    # Execute requested tools
    for tool_call in message.tool_calls:

        name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print(f"\n[Tool Call] {name}")
        print(f"[Arguments] {arguments}")

        result = run_tool(name, arguments)

        print(f"[Tool Result]\n{result}")

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
        )

    # Ask LLM to generate final answer
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content