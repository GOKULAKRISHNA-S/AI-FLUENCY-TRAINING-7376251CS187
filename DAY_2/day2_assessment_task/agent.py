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


print("=" * 60)
print("DIRECT PROMPTING")
print("=" * 60)


print("\nQUESTION:")
print(QUESTION)


response = client.chat.completions.create(

    model=MODEL,

    messages=[
        {
            "role": "user",
            "content": QUESTION
        }
    ]
)


print("\nFINAL ANSWER:")

print(
    response.choices[0].message.content
)