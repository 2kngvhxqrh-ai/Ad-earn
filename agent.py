"""Adaptive strategy agent for a strictly money-free sandbox."""
import argparse
import json
import random
from pathlib import Path
from simulator import STRATEGIES, simulate

STATE_PATH = Path("data/agent_state.json")

def choose_strategy(stats, rng, epsilon=0.15):
    names = list(STRATEGIES)
    if rng.random() < epsilon:
        return rng.choice(names)
    untried = [n for n in names if stats[n]["attempts"] == 0]
    if untried:
        return untried[0]
    return max(names, key=lambda n: stats[n]["points"] / stats[n]["attempts"])

def run_agent(rounds=300, seed=42, epsilon=0.15):
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")
    if not 0 <= epsilon <= 1:
        raise ValueError("epsilon must be between 0 and 1")
    rng = random.Random(seed)
    stats = {n: {"attempts": 0, "successes": 0, "points": 0} for n in STRATEGIES}
    history = []
    for turn in range(1, rounds + 1):
        name = choose_strategy(stats, rng, epsilon)
        outcome = simulate(name, STRATEGIES[name], 1, rng)
        points = outcome["abstract_score"]
        stats[name]["attempts"] += 1
        stats[name]["successes"] += outcome["successes"]
        stats[name]["points"] += points
        history.append({"turn": turn, "strategy": name, "points": points})
    ranked = sorted(stats.items(), key=lambda item: item[1]["points"] / item[1]["attempts"] if item[1]["attempts"] else 0, reverse=True)
    return {
        "mode": "simulation_only",
        "money_features": "DISABLED",
        "rounds": rounds,
        "seed": seed,
        "epsilon": epsilon,
        "strategy_stats": stats,
        "ranking_by_observed_points_per_attempt": [
            {"strategy": name, **row, "points_per_attempt": round(row["points"] / row["attempts"], 4) if row["attempts"] else 0}
            for name, row in ranked
        ],
        "history": history,
        "warning": "Toy game only. Points are not money. Success probabilities are invented, not real-world evidence."
    }

def main():
    parser = argparse.ArgumentParser(description="Learn a strategy using abstract points only.")
    parser.add_argument("--rounds", type=int, default=300)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epsilon", type=float, default=0.15)
    args = parser.parse_args()
    result = run_agent(args.rounds, args.seed, args.epsilon)
    STATE_PATH.parent.mkdir(exist_ok=True)
    STATE_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("ADAPTIVE STRATEGY AGENT — SIMULATION ONLY")
    print("MONEY: NOT USED OR REPRESENTED")
    print("Rounds: {}".format(result["rounds"]))
    print("-" * 58)
    for row in result["ranking_by_observed_points_per_attempt"]:
        print("{:<18} attempts={:3} successes={:3} points={:4} avg_points/attempt={:.3f}".format(row["strategy"], row["attempts"], row["successes"], row["points"], row["points_per_attempt"]))
    print("-" * 58)
    print("Saved local learning report: {}".format(STATE_PATH))
    print(result["warning"])

if __name__ == "__main__":
    main()
