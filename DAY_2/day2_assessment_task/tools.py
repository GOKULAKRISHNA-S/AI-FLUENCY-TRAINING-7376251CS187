def calculate_trip_cost(
    travel_cost,
    hotel_per_night,
    nights,
    food_per_day,
    days,
    local_transport_per_day
):

    hotel_cost = hotel_per_night * nights

    food_cost = food_per_day * days

    transport_cost = local_transport_per_day * days

    total_cost = (
        travel_cost
        + hotel_cost
        + food_cost
        + transport_cost
    )

    return {
        "travel": travel_cost,
        "hotel": hotel_cost,
        "food": food_cost,
        "local_transport": transport_cost,
        "total": total_cost
    }


def get_weather(city):

    weather_data = {

        "Chennai": {
            "temperature": "29°C",
            "condition": "Cloudy",
            "rain_probability": "60%"
        },

        "Bangalore": {
            "temperature": "24°C",
            "condition": "Partly Cloudy",
            "rain_probability": "40%"
        },

        "Coimbatore": {
            "temperature": "26°C",
            "condition": "Cloudy",
            "rain_probability": "50%"
        }

    }

    return weather_data.get(
        city,
        {
            "temperature": "Unknown",
            "condition": "Unknown",
            "rain_probability": "Unknown"
        }
    )