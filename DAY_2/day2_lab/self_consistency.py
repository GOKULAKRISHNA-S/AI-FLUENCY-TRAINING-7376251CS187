import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Day_1')))

from collections import Counter
from config import client, MODEL, banner
from cot_compare import COT_PROMPT, QUESTIONS

RUNS = 5
TEMPERATURE = 0.8          # deliberately NOT 0, so each run can differ

def final_answer(text):
    """Pull out the text after 'Final Answer:' (the last line of a CoT reply)."""
    for line in reversed(text.splitlines()):
        if "final answer" in line.lower():
            return line.split(":", 1)[-1].strip()
    return text.splitlines()[-1].strip() if text.strip() else "(empty)"

def run_many(question, runs=RUNS, temperature=TEMPERATURE):
    answers = []
    for attempt in range(1, runs + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": COT_PROMPT},
                      {"role": "user", "content": question}],
            temperature=temperature,
        )
        answer = final_answer(response.choices[0].message.content)
        print(f"   run {attempt}: {answer}")
        answers.append(answer)
    return answers

if __name__ == "__main__":
    banner("SELF-CONSISTENCY")
    question = QUESTIONS[0]
    print("QUESTION:", question, "\n")
    answers = run_many(question)
    winner, count = Counter(answers).most_common(1)[0]
    print(f"\nMajority answer ({count} of {len(answers)} runs): {winner}")