import time
import requests

from config import (
    GROQ_API_KEY,
    MODEL_20B,
    MODEL_120B,
    GROQ_URL
)

from scenario import (
    SYSTEM_PROMPT,
    PROMPTS
)


def run(model, prompt):

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "stream": False
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    start = time.perf_counter()

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    elapsed = time.perf_counter() - start

    response.raise_for_status()

    data = response.json()

    answer = data["choices"][0]["message"]["content"]

    tokens = data.get(
        "usage",
        {}
    ).get(
        "completion_tokens",
        0
    )

    tps = (
        tokens / elapsed
        if elapsed > 0
        else 0
    )

    return elapsed, tokens, tps, answer


print("=" * 70)
print("SCHOLARSHIP ADVISOR BENCHMARK")
print("=" * 70)

for prompt in PROMPTS:

    print("\nPROMPT:")
    print(prompt)

    for model in [
        MODEL_20B,
        MODEL_120B
    ]:

        elapsed, tokens, tps, answer = run(
            model,
            prompt
        )

        print("\nMODEL:", model)
        print(f"Time: {elapsed:.3f} seconds")
        print(f"Tokens: {tokens}")
        print(f"Tokens/sec: {tps:.2f}")
        print("Answer:", answer[:250])