#!/usr/bin/env python3
"""Pure strategy sandbox. No money, currency, payments, purchases, or network calls."""
import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path("data")
LEDGER_PATH = DATA_DIR / "simulation_ledger.json"

# These probabilities are toy game parameters, not real-world evidence.
STRATEGIES = {
    "strategy_alpha": {"success_probability": 0.02, "score_per_success": 5},
    "strategy_beta": {"success_probability": 0.04, "score_per_success": 2},
    "strategy_gamma": {"success_probability": 0.10, "score_per_success": 1},
}

def simulate(name, config, attempts, rng):
    successes = sum(rng.random() < config["success_probability"] for _ in range(attempts))
    return {
        "strategy": name,
        "attempts": attempts,
        "successes": successes,
        "success_rate": round(successes / attempts, 4),
        "abstract_score": successes * config["score_per_success"],
        "score_per_success": config["score_per_success"],
        "configured_probability": config["success_probability"],
        "evidence": "SYNTHETIC_GAME_RULES_ONLY",
    }

def main():
    parser = argparse.ArgumentParser(description="Run a money-free strategy simulation.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--attempts", type=int, default=100)
    args = parser.parse_args()
    if not 1 <= args.attempts <= 10000:
        parser.error("--attempts must be between 1 and 10000")

    rng = random.Random(args.seed)
    results = [simulate(n, c, args.attempts, rng) for n, c in STRATEGIES.items()]
    ledger = {"mode": "simulation_only", "money_features": "DISABLED", "runs": []}
    if LEDGER_PATH.exists():
        ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    ledger["runs"].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "attempts_per_strategy": args.attempts,
        "results": results,
        "note": "Scores are abstract game points, not money, earnings, revenue, or financial forecasts."
    })
    DATA_DIR.mkdir(exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")

    print("AUTONOMOUS STRATEGY SANDBOX")
    print("MONEY: NOT USED OR REPRESENTED")
    print("Payments, purchases, financial accounts, APIs, and network calls: NONE")
    print("Metric: abstract points")
    print("-" * 64)
    for r in sorted(results, key=lambda x: x["abstract_score"], reverse=True):
        print("{:<18} successes={:3}  success_rate={:.1%}  points={:4}".format(
            r["strategy"], r["successes"], r["success_rate"], r["abstract_score"]))
    print("-" * 64)
    print("Toy simulation only; the probabilities are not real-world evidence.")
    print("Local log: " + str(LEDGER_PATH))

if __name__ == "__main__":
    main()
