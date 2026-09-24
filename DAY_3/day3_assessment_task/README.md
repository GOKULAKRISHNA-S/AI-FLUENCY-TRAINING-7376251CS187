# Smart Travel Research Agent

## Overview

Smart Travel Research Agent is a small Agentic AI project that demonstrates how an LLM can use external tools to obtain information and perform calculations.

The project compares a normal LLM with a tool-enabled agent.

The agent can:

1. Read a locally created HTML travel webpage.
2. Search for specific information inside the webpage.
3. Calculate total trip expenses.

## Scenario

The scenario is a travel research assistant.

The project uses a custom `travel_data.html` webpage containing information about:

* Destinations
* Tourist attractions
* Entry fees
* Opening hours
* Hotel prices
* Food costs
* Travel costs
* Travel packages
* Travel tips

## Project Structure

```text
smart_travel_agent/
│
├── .env
├── .gitignore
├── requirements.txt
├── travel_data.html
├── config.py
├── tools.py
├── agent.py
├── no_tool.py
├── tool_enabled.py
├── README.md
├── analysis.md
└── screenshots/
```

## Three Tools

### 1. read_webpage()

Reads the HTML travel webpage and converts it into readable text.

### 2. find_on_page()

Searches the webpage for information related to a keyword.

### 3. calculate_trip_cost()

Calculates hotel, food and travel expenses.

## LLM vs Tool-Enabled Agent

### Plain LLM

`no_tool.py` sends the question directly to the LLM.

The model does not have access to `travel_data.html`.

### Tool-Enabled Agent

`tool_enabled.py` uses `agent.py`.

The agent can decide whether it needs one of the available tools.

The tool result is then returned to the LLM so that it can generate the final answer.

## Example Questions

### Question 1

```text
What is a good way to plan a three-day trip?
```

This can be answered using general knowledge.

### Question 2

```text
What is the entry fee for Government Museum in Chennai?
```

This requires information from the travel webpage.

### Question 3

```text
Does the travel guide mention beaches?
```

This requires the `find_on_page()` tool.

### Question 4

```text
A hotel costs ₹2000 per night for 3 nights.
Food costs ₹800 per day.
Travel costs ₹3000.
What is the total cost?
```

This requires the calculation tool.

## Technologies

* Python
* Groq API
* OpenAI Python SDK
* GPT-OSS-20B
* BeautifulSoup
* HTML
* python-dotenv

## Learning Outcome

This project demonstrates:

* LLM
* Tool
* Tool schema
* Tool call
* Tool result
* Agent decision-making
* External information retrieval
* Programmatic calculation
* LLM-only vs tool-enabled behavior
