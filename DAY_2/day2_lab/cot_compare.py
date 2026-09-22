import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Day_1')))

from config import client, MODEL, banner

QUESTIONS = [
    # 1. Multi-step arithmetic
    "A student takes three courses costing Rs. 12,000, Rs. 18,000 and Rs. 15,000. "
    "She gets a 15% scholarship on the total and pays the rest in 4 equal instalments. "
    "How much is each instalment?",
    # 2. Counting in two parts
    "A lab has 18 computers. In the morning each computer is shared by 2 students, "
    "and in the afternoon by 3 students. How many student sittings happen in one day?",
    # 3. Ordering / logic
    "Ravi is taller than Kumar. Kumar is taller than Arun. Priya is shorter than Arun. "
    "Who is the tallest and who is the shortest?",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."

COT_PROMPT = ("You are a helpful assistant. Solve the problem step by step. "
              "Number each step and show the calculation in that step. "
              "After the steps, write the last line exactly as: Final Answer: <answer>")

def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt},
                  {"role": "user", "content": question}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")