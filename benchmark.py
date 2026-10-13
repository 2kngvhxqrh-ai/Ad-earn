"""Repeatable, money-free benchmark and epsilon experiment for toy strategies."""
import argparse
import json
import random
from pathlib import Path
from statistics import mean, pstdev
from agent import run_agent
from simulator import STRATEGIES, simulate

REPORT_PATH = Path("data/benchmark_report.json")
EPSILON_CANDIDATES = (0.0, 0.05, 0.15, 0.30, 0.60, 1.0)


def _validate(seeds, rounds):
    if not 1 <= seeds <= 1000:
        raise ValueError("seeds must be between 1 and 1000")
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")


def _adaptive_score(seed, rounds, epsilon):
    result = run_agent(rounds=rounds, seed=seed, epsilon=epsilon)
    return sum(row["points"] for row in result["strategy_stats"].values()) / rounds


def _fixed_score(seed, rounds, name, config):
    # Distinct deterministic stream per strategy avoids accidentally giving
    # every baseline the exact same sequence of random draws.
    rng = random.Random(seed * 1009 + list(STRATEGIES).index(name) * 9176)
    return simulate(name, config, rounds, rng)["abstract_score"] / rounds


def run_benchmark(seeds=30, rounds=300, epsilon=0.15):
    _validate(seeds, rounds)
    if not 0 <= epsilon <= 1:
        raise ValueError("epsilon must be between 0 and 1")
    results = {"adaptive_agent": [_adaptive_score(seed, rounds, epsilon) for seed in range(seeds)]}
    for name, config in STRATEGIES.items():
        results[name] = [_fixed_score(seed, rounds, name, config) for seed in range(seeds)]
    summaries = [{
        "candidate": name,
        "mean_abstract_points_per_turn": round(mean(scores), 5),
        "population_stddev": round(pstdev(scores), 5),
        "seeds_tested": seeds,
    } for name, scores in results.items()]
    summaries.sort(key=lambda row: row["mean_abstract_points_per_turn"], reverse=True)
    return {
        "mode": "synthetic_benchmark", "money_features": "DISABLED",
        "seeds": seeds, "rounds_per_seed": rounds, "epsilon": epsilon,
        "ranking": summaries,
        "warning": "Synthetic game only. Scores are abstract points and do not predict income or real-world outcomes.",
    }


def run_epsilon_experiment(seeds=30, rounds=300):
    """Select epsilon on one seed range and report a separate held-out range."""
    _validate(seeds, rounds)
    training = []
    for epsilon in EPSILON_CANDIDATES:
        scores = [_adaptive_score(seed, rounds, epsilon) for seed in range(seeds)]
        training.append({"epsilon": epsilon, "mean_points_per_turn": mean(scores),
                         "stddev": pstdev(scores)})
    winner = max(training, key=lambda row: row["mean_points_per_turn"])["epsilon"]
    # Offset seeds to keep the validation set distinct from tuning seeds.
    validation_scores = {}
    validation = []
    for epsilon in EPSILON_CANDIDATES:
        scores = [_adaptive_score(seeds + seed + 10000, rounds, epsilon) for seed in range(seeds)]
        validation_scores[epsilon] = scores
        validation.append({"epsilon": epsilon, "mean_points_per_turn": round(mean(scores), 5),
                           "stddev": round(pstdev(scores), 5)})
    selected_validation = next(row for row in validation if row["epsilon"] == winner)
    default_validation = next(row for row in validation if row["epsilon"] == 0.15)
    # Paired seed-by-seed comparisons expose whether a tuning choice is robust,
    # instead of relying only on the difference between two averages.
    default_scores = validation_scores[0.15]
    comparisons = []
    for epsilon in EPSILON_CANDIDATES:
        deltas = [candidate - baseline for candidate, baseline in zip(validation_scores[epsilon], default_scores)]
        delta_mean = mean(deltas)
        standard_error = pstdev(deltas) / (len(deltas) ** 0.5) if len(deltas) > 1 else 0.0
        comparisons.append({
            "epsilon": epsilon,
            "mean_delta_vs_default": round(delta_mean, 5),
            "approx_95pct_interval": [
                round(delta_mean - 1.96 * standard_error, 5),
                round(delta_mean + 1.96 * standard_error, 5),
            ],
            "validation_seeds_beaten": sum(delta > 0 for delta in deltas),
            "validation_seeds_tied": sum(delta == 0 for delta in deltas),
            "validation_seed_count": len(deltas),
        })
    selected_comparison = next(row for row in comparisons if row["epsilon"] == winner)
    return {
        "mode": "epsilon_tuning_with_holdout", "money_features": "DISABLED",
        "training_seeds": seeds, "validation_seeds": seeds, "rounds_per_seed": rounds,
        "epsilon_candidates": list(EPSILON_CANDIDATES),
        "training_results": [{**row, "mean_points_per_turn": round(row["mean_points_per_turn"], 5)}
                              for row in training],
        "selected_epsilon": winner,
        "validation_results": validation,
        "paired_validation_comparisons": comparisons,
        "selected_paired_comparison": selected_comparison,
        "validation_comparison": {
            "selected_epsilon_mean": selected_validation["mean_points_per_turn"],
            "default_epsilon_0_15_mean": default_validation["mean_points_per_turn"],
            "selected_minus_default": round(selected_validation["mean_points_per_turn"] -
                                             default_validation["mean_points_per_turn"], 5),
        },
        "warning": "Synthetic benchmark only. A held-out comparison reduces tuning bias but does not prove real-world performance.",
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark and tune toy strategies using abstract points.")
    parser.add_argument("--seeds", type=int, default=30)
    parser.add_argument("--rounds", type=int, default=300)
    parser.add_argument("--epsilon", type=float, default=0.15)
    parser.add_argument("--tune-epsilon", action="store_true",
                        help="Compare exploration settings on separate training and validation seed sets")
    args = parser.parse_args()
    report = (run_epsilon_experiment(args.seeds, args.rounds) if args.tune_epsilon
              else run_benchmark(args.seeds, args.rounds, args.epsilon))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("MONEY-FREE STRATEGY EXPERIMENT")
    print("Money/currency/payment features: DISABLED")
    print("Report mode: {}".format(report["mode"]))
    if report["mode"] == "synthetic_benchmark":
        print("Seeds: {} | rounds per seed: {}".format(report["seeds"], report["rounds_per_seed"]))
        for row in report["ranking"]:
            print("{:<18} mean points/turn={:.5f} stddev={:.5f}".format(
                row["candidate"], row["mean_abstract_points_per_turn"], row["population_stddev"]))
    else:
        print("Training seeds: {} | held-out validation seeds: {}".format(
            report["training_seeds"], report["validation_seeds"]))
        print("Selected epsilon: {}".format(report["selected_epsilon"]))
        print("Held-out difference vs default epsilon 0.15: {}".format(
            report["validation_comparison"]["selected_minus_default"]))
        for row in report["validation_results"]:
            print("epsilon={:.2f} mean points/turn={:.5f} stddev={:.5f}".format(
                row["epsilon"], row["mean_points_per_turn"], row["stddev"]))
    print(report["warning"])
    print("Local report: {}".format(REPORT_PATH))


if __name__ == "__main__":
    main()
