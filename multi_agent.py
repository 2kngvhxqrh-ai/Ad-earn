"""Multi-agent toy world: independent agents learn using abstract points only."""
import argparse
import json
import random
from pathlib import Path

from simulator import STRATEGIES, simulate

REPORT_PATH = Path("data/multi_agent_report.json")
DEFAULT_AGENTS = {
    "scout": {"epsilon": 0.35},
    "analyst": {"epsilon": 0.15},
    "specialist": {"epsilon": 0.05},
}


def _fresh_stats():
    return {name: {"attempts": 0, "successes": 0, "points": 0} for name in STRATEGIES}


def _choose(stats, rng, epsilon):
    names = list(STRATEGIES)
    if rng.random() < epsilon:
        return rng.choice(names)
    untried = [name for name in names if stats[name]["attempts"] == 0]
    if untried:
        return untried[0]
    return max(names, key=lambda name: stats[name]["points"] / stats[name]["attempts"])


def run_world(rounds=300, seed=42):
    """Run a deterministic, round-robin world of independent learning agents."""
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")

    rng = random.Random(seed)
    agents = {
        name: {"epsilon": config["epsilon"], "stats": _fresh_stats(), "history": []}
        for name, config in DEFAULT_AGENTS.items()
    }
    shared_board = []

    for turn in range(1, rounds + 1):
        # Agents take turns in a shared world but maintain separate learning records.
        agent_name = list(agents)[(turn - 1) % len(agents)]
        agent = agents[agent_name]
        strategy = _choose(agent["stats"], rng, agent["epsilon"])
        outcome = simulate(strategy, STRATEGIES[strategy], 1, rng)
        points = outcome["abstract_score"]
        stats = agent["stats"][strategy]
        stats["attempts"] += 1
        stats["successes"] += outcome["successes"]
        stats["points"] += points

        event = {
            "turn": turn,
            "agent": agent_name,
            "strategy": strategy,
            "success": bool(outcome["successes"]),
            "abstract_points": points,
        }
        agent["history"].append(event)
        shared_board.append(event)

    summaries = []
    for name, agent in agents.items():
        attempts = sum(row["attempts"] for row in agent["stats"].values())
        successes = sum(row["successes"] for row in agent["stats"].values())
        points = sum(row["points"] for row in agent["stats"].values())
        summaries.append({
            "agent": name,
            "epsilon": agent["epsilon"],
            "attempts": attempts,
            "successes": successes,
            "abstract_points": points,
            "points_per_attempt": round(points / attempts, 4) if attempts else 0,
            "strategy_stats": agent["stats"],
        })

    summaries.sort(key=lambda row: row["points_per_attempt"], reverse=True)
    return {
        "mode": "synthetic_multi_agent_simulation",
        "money_features": "DISABLED",
        "rounds": rounds,
        "seed": seed,
        "agent_count": len(agents),
        "agents_ranked_by_observed_points_per_attempt": summaries,
        "shared_event_board": shared_board,
        "note": "Invented game rules only. Abstract points are not money or evidence of real-world performance.",
    }


def main():
    parser = argparse.ArgumentParser(description="Run a money-free multi-agent toy world.")
    parser.add_argument("--rounds", type=int, default=300, help="Total turns shared by all agents")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    report = run_world(args.rounds, args.seed)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("MULTI-AGENT TOY WORLD")
    print("MONEY: NOT USED OR REPRESENTED")
    print("Agents: {} | total turns: {}".format(report["agent_count"], report["rounds"]))
    print("-" * 64)
    for row in report["agents_ranked_by_observed_points_per_attempt"]:
        print("{:<14} turns={:3} successes={:3} points={:4} avg_points/turn={:.3f}".format(
            row["agent"], row["attempts"], row["successes"],
            row["abstract_points"], row["points_per_attempt"]))
    print("-" * 64)
    print("Toy simulation only. Local report: {}".format(REPORT_PATH))


if __name__ == "__main__":
    main()
