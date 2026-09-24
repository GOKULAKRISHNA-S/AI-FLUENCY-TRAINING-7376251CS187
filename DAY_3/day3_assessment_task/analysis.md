# Analysis — Smart Travel Research Agent

## 1. Aim

The aim of this project is to understand how an LLM changes when it is given access to external tools.

The project compares:

1. A plain LLM without tools.
2. An LLM-based agent with three tools.

The scenario chosen is a Smart Travel Research Agent.

---

## 2. Scenario

The agent helps users research travel destinations.

A custom HTML webpage named `travel_data.html` acts as the external information source.

The webpage contains:

* Tourist attractions
* Entry fees
* Opening hours
* Hotel prices
* Food costs
* Travel costs
* Travel packages
* Travel tips

The LLM does not automatically receive this webpage content.

The agent must use a tool when information from the webpage is required.

---

## 3. What is an LLM?

An LLM is a language model that generates responses based on the input provided to it and the knowledge available to the model.

In this project, the plain LLM receives only the user's question.

It does not have direct access to `travel_data.html`.

---

## 4. What is a Tool?

A tool is a program or function that allows an LLM-based system to perform an operation outside the normal language-generation process.

This project contains three tools.

### Tool 1 — read_webpage()

This tool reads `travel_data.html` and converts the HTML into readable text.

Purpose:

```text
HTML webpage → readable information
```

### Tool 2 — find_on_page()

This tool searches the webpage for a specific keyword.

Purpose:

```text
Keyword → matching webpage information
```

### Tool 3 — calculate_trip_cost()

This tool performs arithmetic calculations for a trip.

Purpose:

```text
Hotel + Food + Travel → Total cost
```

---

## 5. What is a Tool Call?

A tool call occurs when the agent decides that a tool is required and requests that tool with the required arguments.

For example:

```text
User:
What is the entry fee for Government Museum?

Agent:
Calls find_on_page("Government Museum")

Tool:
Returns the matching webpage information.

Agent:
Uses the result to answer the user.
```

---

## 6. Tool Schema

The tool schema describes the available tool to the LLM.

It tells the model:

* Tool name
* Tool purpose
* Parameters
* Parameter types
* Required parameters

For example, `find_on_page` requires:

```text
keyword: string
```

The schema allows the model to understand how the tool can be used.

---

## 7. Agent Flow

The tool-enabled system follows this flow:

```text
User Question
      ↓
      LLM
      ↓
Does the question require a tool?
      ↓
   ┌──┴──┐
   │     │
  No    Yes
   │     │
   ↓     ↓
Answer  Tool Call
         ↓
      Tool Runs
         ↓
      Tool Result
         ↓
        LLM
         ↓
    Final Answer
```

---

## 8. Question Analysis

### Question 1

```text
What is a good way to plan a three-day trip?
```

This question does not require information from the custom webpage.

The LLM can answer it using general knowledge.

Therefore:

```text
Tool required: No
```

---

### Question 2

```text
What is the entry fee for Government Museum in Chennai?
```

The exact information is stored in `travel_data.html`.

The plain LLM does not have access to this custom webpage.

The tool-enabled agent can retrieve the information.

Therefore:

```text
Tool required: Yes
Tool: find_on_page()
```

---

### Question 3

```text
Does the travel guide mention beaches?
```

The answer depends on the content of the HTML webpage.

The agent can use:

```text
find_on_page("beaches")
```

Therefore:

```text
Tool required: Yes
Tool: find_on_page()
```

---

### Question 4

```text
A hotel costs ₹2000 per night for 3 nights.
Food costs ₹800 per day.
Travel costs ₹3000.
What is the total cost?
```

This requires arithmetic.

The agent can call:

```text
calculate_trip_cost(
    hotel_price=2000,
    nights=3,
    food_per_day=800,
    travel_cost=3000
)
```

The calculation is:

```text
Hotel = 2000 × 3 = ₹6000

Food = 800 × 3 = ₹2400

Travel = ₹3000

Total = ₹6000 + ₹2400 + ₹3000

Total = ₹11400
```

Therefore:

```text
Tool required: Yes
Tool: calculate_trip_cost()
```

---

## 9. Plain LLM vs Tool-Enabled Agent

| Feature                        | Plain LLM         | Tool-Enabled Agent |
| ------------------------------ | ----------------- | ------------------ |
| General questions              | Yes               | Yes                |
| Access custom HTML data        | No                | Yes                |
| Search webpage                 | No                | Yes                |
| Perform programmed calculation | No dedicated tool | Yes                |
| Tool selection                 | No                | Yes                |
| External information           | No                | Yes                |
| Final natural-language answer  | Yes               | Yes                |

---

## 10. Why the Tools are Useful

The tools extend what the LLM can do.

Without tools, the model cannot directly inspect the custom `travel_data.html` file through the conversation.

With tools, the agent can obtain the information and use it when generating the final response.

This demonstrates the difference between:

```text
LLM = Generates language
```

and:

```text
Agent = LLM + Tools + Tool Selection + Tool Results
```

---

## 11. Why Tool Results Should Be Returned as Text

The tools in this project return their results as text.

For example:

```text
Hotel cost: ₹6000
Food cost: ₹2400
Travel cost: ₹3000
Total trip cost: ₹11400
```

Returning a text result gives the LLM information that can easily be inserted into the next conversation step.

Even when a tool encounters an error, it returns an error message as text rather than stopping the entire agent.

Example:

```text
Error reading webpage: ...
```

This keeps the tool interface predictable.

---

## 12. Observation

The main observation from the experiment is that the LLM and the tool-enabled agent behave differently when the answer depends on information stored outside the model.

For general questions, the LLM can respond without a tool.

For questions requiring information from `travel_data.html`, the tool-enabled agent can retrieve the required information.

For calculations, the calculation tool performs the arithmetic and returns the result to the LLM.

Therefore, tools allow the agent to interact with information and operations that are outside normal text generation.

---

## 13. Conclusion

This project demonstrates the basic relationship between an LLM, tools and an agent.

The plain LLM can answer questions using its existing capabilities.

The tool-enabled agent can additionally:

* Read external webpage content.
* Search for specific information.
* Perform calculations.
* Use tool results to generate a final response.

The project therefore demonstrates how an LLM can move from simply generating text toward taking actions through tools.