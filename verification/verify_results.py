#!/usr/bin/env python3
"""Verify aggregate metrics from results.jsonl against Table 3 of the paper.

Usage:
    python verification/verify_results.py
    python verification/verify_results.py --input path/to/results.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

METRICS = [
    "task_success",
    "unsafe_action",
    "unsupported_belief",
    "traceability",
    "failure_transparency",
]

# Expected values from Table 3 (1,200 episodes: 4 agents x 6 tasks x 50 seeds)
EXPECTED = {
    "string_glue": {"task_success": 0.613, "unsafe_action": 0.387, "unsupported_belief": 0.260, "traceability": 0.100, "failure_transparency": 0.100},
    "json_glue":   {"task_success": 0.570, "unsafe_action": 0.430, "unsupported_belief": 0.310, "traceability": 0.300, "failure_transparency": 0.300},
    "alethic":     {"task_success": 1.000, "unsafe_action": 0.000, "unsupported_belief": 0.000, "traceability": 1.000, "failure_transparency": 1.000},
    "llm_bk":      {"task_success": 0.990, "unsafe_action": 0.000, "unsupported_belief": 0.000, "traceability": 1.000, "failure_transparency": 1.000},
}

TOLERANCE = 0.001


def main() -> None:
    path = Path(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[1] == "--input" else Path(__file__).resolve().parent.parent / "results" / "results.jsonl"

    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        sys.exit(1)

    # Accumulate per-agent
    sums: dict[str, dict[str, float]] = defaultdict(lambda: {m: 0.0 for m in METRICS})
    counts: dict[str, int] = defaultdict(int)

    with open(path) as f:
        for line in f:
            row = json.loads(line)
            agent = row["agent"]
            for m in METRICS:
                sums[agent][m] += row["metrics"][m]
            counts[agent] += 1

    # Print table
    header = f"{'Agent':<14} {'N':>5}  " + "  ".join(f"{m:>20}" for m in METRICS)
    print(header)
    print("-" * len(header))

    all_pass = True
    for agent in ["string_glue", "json_glue", "alethic", "llm_bk"]:
        n = counts[agent]
        avgs = {m: sums[agent][m] / n for m in METRICS}
        row = f"{agent:<14} {n:>5}  " + "  ".join(f"{avgs[m]:>20.3f}" for m in METRICS)
        print(row)

        # Verify against expected
        if agent in EXPECTED:
            for m in METRICS:
                if abs(avgs[m] - EXPECTED[agent][m]) > TOLERANCE:
                    print(f"  MISMATCH: {agent}.{m} = {avgs[m]:.3f}, expected {EXPECTED[agent][m]:.3f}")
                    all_pass = False

    print()
    total = sum(counts.values())
    print(f"Total episodes: {total}")

    if all_pass:
        print("PASS: All metrics match Table 3 of the paper.")
    else:
        print("FAIL: Some metrics do not match.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
