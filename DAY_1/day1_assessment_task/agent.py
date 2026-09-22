import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import (
    get_academic_performance,
    get_skill_profile,
    get_dsa_progress,
    get_project_profile,
    get_target_job_requirements,
    calculate_skill_gaps
)


load_dotenv()


API_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not API_KEY:

    raise ValueError(
        "GROQ_API_KEY is missing from .env"
    )


client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


MODEL = "openai/gpt-oss-120b"

MAX_ITERATIONS = 8


TOOLS = [

    {
        "type": "function",

        "function": {

            "name":
                "get_academic_performance",

            "description":
                "Retrieve the student's "
                "private academic performance.",

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

            "name":
                "get_skill_profile",

            "description":
                "Retrieve the student's "
                "private technical skills.",

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

            "name":
                "get_dsa_progress",

            "description":
                "Retrieve the student's "
                "private DSA progress.",

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

            "name":
                "get_project_profile",

            "description":
                "Retrieve the student's "
                "private project information.",

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

            "name":
                "get_target_job_requirements",

            "description":
                "Retrieve the target "
                "job requirements.",

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

            "name":
                "calculate_skill_gaps",

            "description":
                "Calculate skill gaps "
                "against the target job.",

            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


AVAILABLE_TOOLS = {

    "get_academic_performance":
        get_academic_performance,

    "get_skill_profile":
        get_skill_profile,

    "get_dsa_progress":
        get_dsa_progress,

    "get_project_profile":
        get_project_profile,

    "get_target_job_requirements":
        get_target_job_requirements,

    "calculate_skill_gaps":
        calculate_skill_gaps
}


SYSTEM_PROMPT = """
You are CareerLens, an AI career-readiness agent.

The student's private information is NOT directly available
to you.

You can access private information ONLY through the tools.

Never invent student information.

When personalized analysis is requested:

1. Understand what information is required.
2. Select appropriate tools.
3. Execute the tools.
4. Examine the returned information.
5. Decide whether more information is required.
6. Call additional tools when necessary.
7. Continue until enough information is available.
8. Produce the final answer.

IMPORTANT TOOL RULES:

All available tools are zero-argument tools.

Never invent or construct arguments for these tools.

Call the tools exactly as defined in their schemas.

For calculate_skill_gaps, do not provide:
- gaps
- required_skills
- student_skills
- or any other arguments.

The tool itself reads the private student and job data.

The final answer should include:

- Current profile summary
- Academic observations
- Technical skill gaps
- DSA gaps
- Project observations
- Priority areas
- 30-day improvement plan

Base the answer on evidence returned by tools.

Do not guarantee that the student will get a job.

Do not reveal hidden chain-of-thought.
"""


USER_REQUEST = """
I am preparing for a Software Engineer internship.

Analyze my academic performance, DSA progress,
technical skills, and projects against the target
job requirements.

Identify my most important gaps and create a
prioritized 30-day improvement plan.
"""


def execute_tool(function_name, arguments):

    if function_name not in AVAILABLE_TOOLS:
        raise ValueError(
            f"Unknown tool: {function_name}"
        )

    tool_function = AVAILABLE_TOOLS[function_name]

    # These tools do not require arguments.
    no_argument_tools = {
        "get_academic_performance",
        "get_skill_profile",
        "get_dsa_progress",
        "get_project_profile",
        "get_target_job_requirements",
        "calculate_skill_gaps"
    }

    if function_name in no_argument_tools:
        return tool_function()

    return tool_function(**arguments)

def main():

    print("=" * 70)
    print("CAREERLENS — AI AGENT")
    print("=" * 70)

    messages = [

        {
            "role":
                "system",

            "content":
                SYSTEM_PROMPT
        },

        {
            "role":
                "user",

            "content":
                USER_REQUEST
        }
    ]


    for iteration in range(
        1,
        MAX_ITERATIONS + 1
    ):

        print(
            f"\n{'=' * 20} "
            f"ITERATION {iteration} "
            f"{'=' * 20}"
        )


        response = (
            client.chat.completions.create(

                model=MODEL,

                messages=messages,

                tools=TOOLS,

                tool_choice="auto",

                temperature=0.1
            )
        )


        assistant_message = (
            response.choices[0].message
        )


        # ------------------------------------------------
        # FINAL RESPONSE
        # ------------------------------------------------

        if not assistant_message.tool_calls:

            print(
                "\nFINAL ANSWER\n"
            )

            print(
                assistant_message.content
            )

            return


        # ------------------------------------------------
        # ADD ASSISTANT TOOL CALL TO HISTORY
        # ------------------------------------------------

        messages.append(
            assistant_message.model_dump(
                exclude_none=True
            )
        )


        # ------------------------------------------------
        # EXECUTE EACH TOOL
        # ------------------------------------------------

        for tool_call in (
            assistant_message.tool_calls
        ):

            function_name = (
                tool_call.function.name
            )


            raw_arguments = (
                tool_call.function.arguments
            )


            arguments = json.loads(
                raw_arguments
            )


            print(
                f"\nTOOL CALL: "
                f"{function_name}"
            )


            print(
                f"ARGUMENTS: "
                f"{arguments}"
            )


            result = execute_tool(
                function_name,
                arguments
            )


            print(
                "\nOBSERVATION:"
            )


            print(
                json.dumps(
                    result,
                    indent=2
                )
            )


            messages.append(
                {
                    "role":
                        "tool",

                    "tool_call_id":
                        tool_call.id,

                    "name":
                        function_name,

                    "content":
                        json.dumps(result)
                }
            )


    print(
        "\nMaximum agent iterations reached."
    )


if __name__ == "__main__":
    main()