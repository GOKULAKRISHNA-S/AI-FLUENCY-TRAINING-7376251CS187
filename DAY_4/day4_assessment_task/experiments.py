from vram_estimate import (
    estimate,
    verdict
)


MEMORY_GB = 8.0

PARAMS_B = 8.0


def context_experiment():

    print("# Context Length Experiment")
    print()

    print(
        "| Context | Weights (GB) | "
        "KV Cache (GB) | Total (GB) | Fits? |"
    )

    print(
        "|---:|---:|---:|---:|---|"
    )

    contexts = [
        4,
        8,
        16,
        32,
        64,
        128
    ]

    for context in contexts:

        weights, kv, total = estimate(
            PARAMS_B,
            "Q4_K_M",
            context
        )

        result = verdict(
            total,
            MEMORY_GB
        )

        print(
            f"| {context}K | "
            f"{weights:.2f} | "
            f"{kv:.2f} | "
            f"{total:.2f} | "
            f"{result} |"
        )


def quantization_experiment():

    print("\n# Quantization Experiment")
    print()

    print(
        "| Quantization | Weights (GB) | "
        "KV Cache (GB) | Total (GB) | Fits? |"
    )

    print(
        "|---|---:|---:|---:|---|"
    )

    precisions = [
        "Q3_K_M",
        "Q4_K_M",
        "Q5_K_M",
        "Q6_K",
        "Q8_0",
        "FP16"
    ]

    for precision in precisions:

        weights, kv, total = estimate(
            PARAMS_B,
            precision,
            8
        )

        result = verdict(
            total,
            MEMORY_GB
        )

        print(
            f"| {precision} | "
            f"{weights:.2f} | "
            f"{kv:.2f} | "
            f"{total:.2f} | "
            f"{result} |"
        )


def main():

    context_experiment()

    quantization_experiment()


if __name__ == "__main__":
    main()