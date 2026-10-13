"""Repeatable benchmark of adaptive choices against fixed toy strategies.

This is an invented game benchmark. It contains no currency, payments, or network calls.
"""
import argparse
import json
import random
from pathlib import Path
from statistics import mean, pstdev
from agent import run_agent
from simulator import STRATEGIES, simulate

REPORT_PATH = Path("data/benchmark_report.json")


def run_benchmark(seeds=30, rounds=300, epsilon=0.15):
    if not 1 <= seeds <= 1000:
        raise ValueError("seeds must be between 1 and 1000")
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")
    if not 0 <= epsilon <= 1:
        raise ValueError("epsilon must be between 0 and 1")

    results = {"adaptive_agent": [], **{name: [] for name in STRATEGIES}}
    for seed in range(seeds):
        adaptive = run_agent(rounds=rounds, seed=seed, epsilon=epsilon)
        total = sum(row["points"] for row in adaptive["strategy_stats"].values())
        results["adaptive_agent"].append(total / rounds)
        for name, config in STRATEGIES.items():
            rng = random.Random(seed)
            outcome = simulate(name, config, rounds, rng)
            results[name].append(outcome["abstract_score"] / rounds)

    summaries = []
    for name, scores in results.items():
        summaries.append({
            "candidate": name,
            "mean_abstract_points_per_turn": round(mean(scores), 5),
            "population_stddev": round(pstdev(scores), 5),
            "seeds_tested": seeds,
        })
    summaries.sort(key=lambda row: row["mean_abstract_points_per_turn"], reverse=True)
    return {
        "mode": "synthetic_benchmark",
        "money_features": "DISABLED",
        "seeds": seeds,
        "rounds_per_seed": rounds,
        "epsilon": epsilon,
        "ranking": summaries,
        "warning": "Synthetic game only. Scores are abstract points and do not predict income or real-world outcomes.",
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark adaptive and fixed toy strategies.")
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--rounds", type=int, default=300)
    parser.add_argument("--epsilon", type=float, default=0.15)
    args = parser.parse_args()
    report = run_benchmark(args.seeds, args.rounds, args.epsilon)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("MONEY-FREE STRATEGY BENCHMARK")
    print("Money/currency/payment features: DISABLED")
    print("Seeds: {} | rounds per seed: {}".format(report["seeds"], report["rounds_per_seed"]))
    print("-" * 66)
    for row in report["ranking"]:
        print("{:<18} mean points/turn={:.5f} stddev={:.5f}".format(
            row["candidate"], row["mean_abstract_points_per_turn"], row["population_stddev"]))
    print("-" * 66)
    print(report["warning"])
    print("Local report: {}".format(REPORT_PATH))


if __name__ == "__main__":
    main()
