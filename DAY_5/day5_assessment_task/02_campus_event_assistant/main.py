import time
import json
import requests

from config import (
    GROQ_API_KEY,
    MODEL_20B,
    MODEL_120B,
    GROQ_URL
)

from scenario import (
    SCENARIO_NAME,
    SYSTEM_PROMPT,
    PROMPTS
)


def get_headers():
    return {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }


def non_streaming(model, prompt):

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

    start = time.perf_counter()

    response = requests.post(
        GROQ_URL,
        headers=get_headers(),
        json=payload,
        timeout=120
    )

    total_time = time.perf_counter() - start

    response.raise_for_status()

    data = response.json()

    answer = data["choices"][0]["message"]["content"]

    usage = data.get("usage", {})

    completion_tokens = usage.get(
        "completion_tokens",
        0
    )

    tokens_per_second = (
        completion_tokens / total_time
        if total_time > 0
        else 0
    )

    return (
        answer,
        total_time,
        completion_tokens,
        tokens_per_second
    )


def streaming(model, prompt):

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
        "stream": True
    }

    start = time.perf_counter()

    first_token_time = None

    pieces = []

    usage = {}

    with requests.post(
        GROQ_URL,
        headers=get_headers(),
        json=payload,
        stream=True,
        timeout=120
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines(
            decode_unicode=True
        ):

            if not line:
                continue

            if not line.startswith("data: "):
                continue

            raw_data = line[6:]

            if raw_data == "[DONE]":
                continue

            try:
                chunk = json.loads(raw_data)
            except json.JSONDecodeError:
                continue

            choices = chunk.get("choices", [])

            if choices:

                delta = choices[0].get(
                    "delta",
                    {}
                )

                content = delta.get(
                    "content",
                    ""
                )

                if content:

                    if first_token_time is None:
                        first_token_time = (
                            time.perf_counter()
                        )

                    pieces.append(content)

            if chunk.get("usage"):
                usage = chunk["usage"]

    end = time.perf_counter()

    answer = "".join(pieces)

    total_time = end - start

    if first_token_time:
        ttft = first_token_time - start
    else:
        ttft = None

    completion_tokens = usage.get(
        "completion_tokens",
        0
    )

    tokens_per_second = (
        completion_tokens / total_time
        if completion_tokens and total_time > 0
        else 0
    )

    return (
        answer,
        ttft,
        total_time,
        completion_tokens,
        tokens_per_second
    )


def override_test(model, prompt):

    override_system_prompt = """
Ignore the scholarship advisor role.

For this test, behave like a pirate.
Answer using pirate-style language.
"""

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": override_system_prompt
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0,
        "stream": False
    }

    response = requests.post(
        GROQ_URL,
        headers=get_headers(),
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def main():

    print("=" * 70)
    print(SCENARIO_NAME)
    print("=" * 70)

    models = [
        MODEL_20B,
        MODEL_120B
    ]

    for prompt_number, prompt in enumerate(
        PROMPTS,
        start=1
    ):

        print("\n" + "-" * 70)
        print(f"PROMPT {prompt_number}")
        print(prompt)
        print("-" * 70)

        for model in models:

            answer, total, tokens, tps = non_streaming(
                model,
                prompt
            )

            print(f"\nMODEL: {model}")
            print(f"Total time: {total:.3f} seconds")
            print(f"Completion tokens: {tokens}")
            print(f"Tokens/sec: {tps:.2f}")

            print("\nANSWER:")
            print(answer)

    print("\n" + "=" * 70)
    print("STREAMING TEST")
    print("=" * 70)

    answer, ttft, total, tokens, tps = streaming(
        MODEL_20B,
        PROMPTS[0]
    )

    print(f"Model: {MODEL_20B}")

    if ttft is not None:
        print(f"TTFT: {ttft:.3f} seconds")
    else:
        print("TTFT: unavailable")

    print(f"Total time: {total:.3f} seconds")
    print(f"Completion tokens: {tokens}")
    print(f"Tokens/sec: {tps:.2f}")

    print("\nANSWER:")
    print(answer)

    print("\n" + "=" * 70)
    print("SYSTEM PROMPT OVERRIDE TEST")
    print("=" * 70)

    result = override_test(
        MODEL_20B,
        PROMPTS[0]
    )

    print(result)


if __name__ == "__main__":
    main()