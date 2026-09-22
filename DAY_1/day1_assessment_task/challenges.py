"""
CareerLens — Agent Challenge Runner

This file provides evaluation challenges for the CareerLens AI Agent.

Purpose:
    - Give the CareerLens agent a realistic placement-readiness challenge.
    - Allow the agent to use its existing tools.
    - Check whether the agent produces a correct and useful final answer.
    - Demonstrate that the agent can reason over multiple pieces of information.

This file does NOT replace agent.py.
It acts as an evaluation/testing layer for the agent.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# ============================================================
# ENVIRONMENT SETUP
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not configured. "
        "Please add it to your .env file."
    )


# ============================================================
# GROQ / OPENAI-COMPATIBLE CLIENT
# ============================================================

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"


# ============================================================
# IMPORT CAREERLENS TOOLS
# ============================================================

from tools import (
    get_academic_performance,
    get_skill_profile,
    get_dsa_progress,
    get_project_profile,
    get_target_job_requirements,
    calculate_skill_gaps,
)


# ============================================================
# TOOL REGISTRY
# ============================================================

TOOLS = {
    "get_academic_performance": get_academic_performance,
    "get_skill_profile": get_skill_profile,
    "get_dsa_progress": get_dsa_progress,
    "get_project_profile": get_project_profile,
    "get_target_job_requirements": get_target_job_requirements,
    "calculate_skill_gaps": calculate_skill_gaps,
}


# ============================================================
# TOOL DEFINITIONS FOR THE LLM
# ============================================================

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_academic_performance",
            "description": (
                "Retrieve the student's academic performance, "
                "including CGPA and academic information."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_skill_profile",
            "description": (
                "Retrieve the student's current technical skill profile."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_dsa_progress",
            "description": (
                "Retrieve the student's Data Structures and Algorithms "
                "learning/progress information."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_project_profile",
            "description": (
                "Retrieve information about the student's projects, "
                "project experience, and practical development experience."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "get_target_job_requirements",
            "description": (
                "Retrieve the skills and requirements expected for "
                "the student's target job role."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },

    {
        "type": "function",
        "function": {
            "name": "calculate_skill_gaps",
            "description": (
                "Calculate the gap between the student's current skills "
                "and the target job requirements."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


# ============================================================
# CHALLENGE
# ============================================================

CHALLENGE = {
    "title": "Placement Readiness Challenge",

    "description": """
You are CareerLens, an AI-powered Personal Placement Readiness Agent.

Your task is to determine whether the student is currently
prepared for their target job role.

You must investigate the student's:

1. Academic performance
2. Technical skills
3. DSA progress
4. Project experience
5. Target job requirements
6. Skill gaps

Use the available tools instead of guessing.

After collecting the required information, provide a final
placement-readiness report.
""",

    "requirements": [
        "Use tools to retrieve the student's academic performance.",
        "Use tools to retrieve the student's technical skill profile.",
        "Use tools to retrieve DSA progress.",
        "Use tools to retrieve project experience.",
        "Use tools to retrieve target job requirements.",
        "Calculate the student's skill gaps.",
        "Identify the most important missing skills.",
        "Provide a practical preparation plan.",
        "Do not invent information that was not provided by the tools.",
    ],
}


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):
    """
    Execute a CareerLens tool.

    Some tools do not require arguments.
    """

    if tool_name not in TOOLS:
        return {
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        tool = TOOLS[tool_name]

        # ----------------------------------------------------
        # Tools without arguments
        # ----------------------------------------------------

        if tool_name == "calculate_skill_gaps":
            result = tool()
        else:
            result = tool()

        # ----------------------------------------------------
        # Convert result to JSON-compatible output
        # ----------------------------------------------------

        if isinstance(result, str):
            return result

        return json.dumps(
            result,
            indent=2,
            default=str
        )

    except Exception as error:
        return {
            "error": str(error)
        }


# ============================================================
# AGENT LOOP
# ============================================================

def run_challenge():
    """
    Run the placement-readiness challenge against CareerLens.
    """

    print("=" * 70)
    print("CAREERLENS — AGENT CHALLENGE")
    print("=" * 70)

    print("\nCHALLENGE:")
    print(CHALLENGE["title"])

    print("\n" + CHALLENGE["description"].strip())

    print("\nREQUIREMENTS:")

    for index, requirement in enumerate(
        CHALLENGE["requirements"],
        start=1
    ):
        print(f"{index}. {requirement}")

    print("\n" + "=" * 70)
    print("AGENT STARTING")
    print("=" * 70)

    messages = [
        {
            "role": "system",
            "content": """
You are CareerLens, a Personal Placement Readiness Intelligence Agent.

Your job is to investigate the student's profile using the
available tools and then produce a fact-based placement
readiness report.

IMPORTANT RULES:

1. Do not guess student information.
2. Use tools to retrieve information.
3. Use multiple tools when necessary.
4. Calculate skill gaps before making recommendations.
5. Base your conclusions on tool results.
6. Clearly separate facts from recommendations.
7. Provide a practical action plan.
8. Continue the tool-use loop until you have enough information
   to answer the challenge.
""",
        },

        {
            "role": "user",
            "content": CHALLENGE["description"],
        },
    ]

    max_iterations = 10

    for iteration in range(1, max_iterations + 1):

        print("\n" + "=" * 70)
        print(f"ITERATION {iteration}")
        print("=" * 70)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message

        # ----------------------------------------------------
        # Add assistant message to conversation
        # ----------------------------------------------------

        messages.append(assistant_message)

        # ----------------------------------------------------
        # Check whether the model requested tools
        # ----------------------------------------------------

        if not assistant_message.tool_calls:

            final_answer = assistant_message.content

            print("\n" + "=" * 70)
            print("FINAL AGENT OUTPUT")
            print("=" * 70)

            print(final_answer)

            return final_answer

        # ----------------------------------------------------
        # Execute requested tools
        # ----------------------------------------------------

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                    or "{}"
                )
            except json.JSONDecodeError:
                arguments = {}

            print(f"\nTOOL CALL: {tool_name}")
            print(f"ARGUMENTS: {arguments}")

            result = execute_tool(
                tool_name,
                arguments
            )

            print("TOOL RESULT:")
            print(result)

            # ------------------------------------------------
            # Return tool result to the model
            # ------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": (
                        result
                        if isinstance(result, str)
                        else json.dumps(
                            result,
                            indent=2,
                            default=str
                        )
                    ),
                }
            )

    # --------------------------------------------------------
    # Maximum iteration safety
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("MAXIMUM ITERATIONS REACHED")
    print("=" * 70)

    return None


# ============================================================
# CHALLENGE VALIDATION
# ============================================================

def validate_output(output):
    """
    Validate whether the agent produced a meaningful
    placement-readiness response.

    This is not a perfect semantic evaluator.
    It provides a simple automated quality gate.
    """

    if not output:
        return False, [
            "Agent did not produce a final answer."
        ]

    output_lower = output.lower()

    required_concepts = {
        "academic": [
            "academic",
            "cgpa",
            "grade",
            "performance",
        ],

        "skills": [
            "skill",
            "technical",
        ],

        "dsa": [
            "dsa",
            "data structure",
            "algorithm",
        ],

        "projects": [
            "project",
        ],

        "gap": [
            "gap",
            "missing",
            "improve",
        ],

        "recommendation": [
            "recommend",
            "plan",
            "action",
            "should",
            "focus",
        ],
    }

    failures = []

    for category, keywords in required_concepts.items():

        found = any(
            keyword in output_lower
            for keyword in keywords
        )

        if not found:
            failures.append(
                f"Missing or unclear section: {category}"
            )

    # --------------------------------------------------------
    # Final validation result
    # --------------------------------------------------------

    if failures:
        return False, failures

    return True, []


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        result = run_challenge()

        print("\n" + "=" * 70)
        print("CHALLENGE VALIDATION")
        print("=" * 70)

        passed, issues = validate_output(result)

        if passed:

            print("\nSTATUS: PASSED")

            print(
                "\nCareerLens successfully produced "
                "a placement-readiness response."
            )

        else:

            print("\nSTATUS: NEEDS IMPROVEMENT")

            print("\nIssues found:")

            for issue in issues:
                print(f"- {issue}")

        print("\n" + "=" * 70)
        print("CHALLENGE COMPLETE")
        print("=" * 70)

    except Exception as error:

        print("\n" + "=" * 70)
        print("CHALLENGE FAILED")
        print("=" * 70)

        print(f"\nError: {error}")