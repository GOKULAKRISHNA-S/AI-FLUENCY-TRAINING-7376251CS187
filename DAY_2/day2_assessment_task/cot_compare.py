from config import client, MODEL


QUESTION = """
I want to plan a 2-day trip to Chennai.

My budget is ₹10,000.

The estimated costs are:

Travel = ₹2,000
Hotel per night = ₹2,500
Food per day = ₹1,200
Local transport per day = ₹500

Can I complete the trip within my budget?
How much money will I be over or under budget?
"""


def direct_prompt():

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": QUESTION
            }
        ]
    )

    return response.choices[0].message.content


def reasoning_prompt():

    prompt = QUESTION + """

Solve this problem carefully.

Break the calculation into clear steps.

Provide a concise reasoning summary followed by
the final answer.
"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


print("=" * 60)
print("DIRECT PROMPTING VS CHAIN-OF-THOUGHT-STYLE REASONING")
print("=" * 60)


print("\nQUESTION:")
print(QUESTION)


print("\n" + "=" * 60)
print("DIRECT PROMPTING")
print("=" * 60)

print(
    direct_prompt()
)


print("\n" + "=" * 60)
print("CHAIN-OF-THOUGHT-STYLE REASONING")
print("=" * 60)

print(
    reasoning_prompt()
)