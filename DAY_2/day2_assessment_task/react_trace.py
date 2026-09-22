from tools import calculate_trip_cost, get_weather


QUESTION = """
I am planning a 2-day trip to Chennai.

My budget is ₹10,000.

Travel = ₹2,000
Hotel per night = ₹2,500
Food per day = ₹1,200
Local transport per day = ₹500

Calculate whether the trip fits my budget.

Also check the available weather information
and tell me whether I should consider carrying an umbrella.
"""


print("=" * 60)
print("REACT AGENT TRACE")
print("=" * 60)


print("\nQUESTION:")
print(QUESTION)


# STEP 1

print("\nTHOUGHT:")

print(
    "I need to calculate the total trip cost first. "
    "Then I need weather information for Chennai."
)


# STEP 2

print("\nACTION:")

print(
    "calculate_trip_cost("
    "2000, 2500, 2, 1200, 2, 500)"
)


cost_result = calculate_trip_cost(

    travel_cost=2000,

    hotel_per_night=2500,

    nights=2,

    food_per_day=1200,

    days=2,

    local_transport_per_day=500
)


# STEP 3

print("\nOBSERVATION:")

print(cost_result)


# STEP 4

print("\nTHOUGHT:")


if cost_result["total"] > 10000:

    difference = (
        cost_result["total"] - 10000
    )

    print(
        f"The total cost is ₹{cost_result['total']}, "
        f"which is ₹{difference} above the budget."
    )

else:

    difference = (
        10000 - cost_result["total"]
    )

    print(
        f"The total cost is ₹{cost_result['total']}, "
        f"leaving ₹{difference} in the budget."
    )


print(
    "I still need weather information to answer "
    "the umbrella question."
)


# STEP 5

print("\nACTION:")

print(
    "get_weather('Chennai')"
)


weather_result = get_weather("Chennai")


# STEP 6

print("\nOBSERVATION:")

print(weather_result)


# STEP 7

print("\nTHOUGHT:")

print(
    "The weather information shows "
    f"{weather_result['condition']} conditions "
    f"and a "
    f"{weather_result['rain_probability']} "
    "rain probability."
)


print(
    "Therefore, carrying an umbrella would be "
    "a reasonable precaution."
)


# FINAL ANSWER

print("\nFINAL ANSWER:")


print(
    f"The estimated 2-day trip cost is "
    f"₹{cost_result['total']}."
)


if cost_result["total"] > 10000:

    print(
        f"The trip exceeds the ₹10,000 budget by "
        f"₹{cost_result['total'] - 10000}."
    )

else:

    print(
        f"The trip remains ₹{10000 - cost_result['total']} "
        "within the budget."
    )


print(
    f"The weather tool reports "
    f"{weather_result['condition']} conditions "
    f"at {weather_result['temperature']} "
    f"with a "
    f"{weather_result['rain_probability']} "
    "rain probability."
)


print(
    "Carrying an umbrella would be "
    "a reasonable precaution."
)