from config import client, MODEL


QUESTION = """
A student has a budget of ₹10,000 for a 2-day Chennai trip.

Travel costs ₹2,000.

Hotel costs ₹2,500 per night.

Food costs ₹1,200 per day.

Local transport costs ₹500 per day.

Calculate the total cost and determine whether
the student is within the budget.

Give a concise reasoning summary and final answer.
"""


def run_experiment(temperature):

    print("\n" + "=" * 60)

    print(
        f"TEMPERATURE = {temperature}"
    )

    print("=" * 60)


    answers = []


    for run in range(5):

        response = client.chat.completions.create(

            model=MODEL,

            temperature=temperature,

            messages=[
                {
                    "role": "user",
                    "content": QUESTION
                }
            ]
        )


        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        answers.append(answer)


        print(
            f"\nRUN {run + 1}"
        )

        print("-" * 40)

        print(answer)


    return answers


print("=" * 60)
print("SELF-CONSISTENCY EXPERIMENT")
print("=" * 60)


run_experiment(0.7)


run_experiment(0)