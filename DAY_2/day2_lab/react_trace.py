import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Day_1')))

from agent import agent

QUESTION = ("Which is cheaper: CS101 and AI202 with a 10% scholarship, "
            "or all three courses with a 25% scholarship? By how much?")

print("QUESTION:", QUESTION, "\n")
print("--- the agent's actions and observations ---")
answer = agent(QUESTION, max_steps=8)
print("\nFINAL ANSWER:", answer)