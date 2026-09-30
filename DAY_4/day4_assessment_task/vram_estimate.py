import argparse


BYTES_PER_PARAM = {
    "FP16": 2.00,
    "BF16": 2.00,
    "Q8_0": 1.00,
    "Q6_K": 0.81,
    "Q5_K_M": 0.68,
    "Q4_K_M": 0.57,
    "Q3_K_M": 0.43,
}


KV_GB_PER_B_PER_1K = 0.02

OVERHEAD = 1.10


def estimate(params_b, precision="Q4_K_M", context_k=8):

    if precision not in BYTES_PER_PARAM:
        raise ValueError(
            f"Unknown precision: {precision}\n"
            f"Available: {list(BYTES_PER_PARAM.keys())}"
        )

    weights_gb = params_b * BYTES_PER_PARAM[precision]

    kv_gb = params_b * context_k * KV_GB_PER_B_PER_1K

    total_gb = (weights_gb + kv_gb) * OVERHEAD

    return weights_gb, kv_gb, total_gb


def verdict(total_gb, available_gb):

    if total_gb <= available_gb * 0.7:
        return "fits comfortably"

    if total_gb <= available_gb:
        return "fits, but tight"

    return "does NOT fit"


def report(
    name,
    params_b,
    precision,
    context_k,
    available_gb
):

    weights, kv, total = estimate(
        params_b,
        precision,
        context_k
    )

    result = verdict(
        total,
        available_gb
    )

    print(
        f"{name:<24}"
        f"{precision:<9}"
        f"{params_b:>6.1f}B "
        f"ctx {context_k:>4}K "
        f"weights {weights:>7.2f} GB "
        f"KV {kv:>7.2f} GB "
        f"total {total:>7.2f} GB "
        f"-> {result}"
    )


def reference_models(available_gb):

    print("\nREFERENCE MODEL ESTIMATES")
    print("=" * 110)

    report(
        "Qwen small",
        1.5,
        "Q4_K_M",
        8,
        available_gb
    )

    report(
        "8B mid model",
        8.0,
        "Q4_K_M",
        8,
        available_gb
    )

    report(
        "8B FP16",
        8.0,
        "FP16",
        8,
        available_gb
    )

    report(
        "30B model",
        30.0,
        "Q4_K_M",
        8,
        available_gb
    )

    report(
        "70B model",
        70.0,
        "Q4_K_M",
        8,
        available_gb
    )


def context_experiment(available_gb):

    print("\nCONTEXT LENGTH EXPERIMENT")
    print("=" * 110)

    contexts = [
        4,
        8,
        32,
        128
    ]

    for context in contexts:

        report(
            "8B Q4_K_M",
            8.0,
            "Q4_K_M",
            context,
            available_gb
        )


def quantization_experiment(available_gb):

    print("\nQUANTIZATION EXPERIMENT")
    print("=" * 110)

    precisions = [
        "Q3_K_M",
        "Q4_K_M",
        "Q5_K_M",
        "Q8_0",
        "FP16"
    ]

    for precision in precisions:

        report(
            "8B model",
            8.0,
            precision,
            8,
            available_gb
        )


def custom_model(
    params,
    precision,
    context,
    available_gb
):

    print("\nCUSTOM MODEL")
    print("=" * 110)

    report(
        "Custom model",
        params,
        precision,
        context,
        available_gb
    )


def main():

    parser = argparse.ArgumentParser(
        description="Day 4 LLM memory estimator"
    )

    parser.add_argument(
        "--memory",
        type=float,
        default=8.0,
        help="Available memory in GB"
    )

    parser.add_argument(
        "--params",
        type=float,
        help="Model parameters in billions"
    )

    parser.add_argument(
        "--precision",
        choices=BYTES_PER_PARAM.keys(),
        help="Model quantization / precision"
    )

    parser.add_argument(
        "--context",
        type=int,
        help="Context length in K tokens"
    )

    args = parser.parse_args()

    print("=" * 110)
    print("DAY 4 — LOCAL LLM MEMORY ESTIMATOR")
    print("=" * 110)

    print(
        f"\nAvailable memory: "
        f"{args.memory:.2f} GB"
    )

    if args.params is not None:

        if (
            args.precision is None
            or args.context is None
        ):
            parser.error(
                "--params requires "
                "--precision and --context"
            )

        custom_model(
            args.params,
            args.precision,
            args.context,
            args.memory
        )

    else:

        reference_models(args.memory)

        context_experiment(args.memory)

        quantization_experiment(args.memory)


if __name__ == "__main__":
    main()