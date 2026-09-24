from pathlib import Path
from bs4 import BeautifulSoup


# Tool 1: Read the webpage
def read_webpage():
    try:
        file_path = Path(__file__).parent / "travel_data.html"

        html = file_path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(" ", strip=True)

        return text

    except Exception as e:
        return f"Error reading webpage: {e}"


# Tool 2: Find information on the webpage
def find_on_page(keyword):
    try:
        page_text = read_webpage()

        words = keyword.lower().split()

        sentences = page_text.split(".")

        matches = []

        for sentence in sentences:
            sentence_lower = sentence.lower()

            if all(word in sentence_lower for word in words):
                matches.append(sentence.strip())

        if matches:
            return " ".join(matches)

        # Try individual important words
        matches = []

        for sentence in sentences:
            sentence_lower = sentence.lower()

            if any(word in sentence_lower for word in words):
                matches.append(sentence.strip())

        if matches:
            return " ".join(matches[:5])

        return f"No information found for '{keyword}'."

    except Exception as e:
        return f"Error searching webpage: {e}"


# Tool 3: Calculate trip cost
def calculate_trip_cost(
    hotel_price,
    nights,
    food_per_day,
    travel_cost
):
    try:
        hotel_total = hotel_price * nights
        food_total = food_per_day * nights
        total = hotel_total + food_total + travel_cost

        return (
            f"Hotel cost: ₹{hotel_total}\n"
            f"Food cost: ₹{food_total}\n"
            f"Travel cost: ₹{travel_cost}\n"
            f"Total trip cost: ₹{total}"
        )

    except Exception as e:
        return f"Calculation error: {e}"