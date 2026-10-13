"""Multi-agent toy world with independent and shared learning; abstract points only."""
import argparse
import json
import random
from pathlib import Path
from simulator import STRATEGIES, simulate

REPORT_PATH = Path("data/multi_agent_report.json")
DEFAULT_AGENTS = {"scout": {"epsilon": 0.35}, "analyst": {"epsilon": 0.15}, "specialist": {"epsilon": 0.05}}


def _fresh_stats():
    return {name: {"attempts": 0, "successes": 0, "points": 0} for name in STRATEGIES}


def _social_stats(board, observer):
    result = {name: {"attempts": 0, "points": 0} for name in STRATEGIES}
    for event in board:
        if event["agent"] != observer:
            row = result[event["strategy"]]
            row["attempts"] += 1
            row["points"] += event["abstract_points"]
    return result


def _choose(stats, rng, epsilon, social=None, social_weight=0.35):
    names = list(STRATEGIES)
    if rng.random() < epsilon:
        return rng.choice(names)
    social = social or {name: {"attempts": 0, "points": 0} for name in names}
    untried = [name for name in names if stats[name]["attempts"] == 0]
    if untried:
        observed = [name for name in untried if social[name]["attempts"]]
        if observed:
            return max(observed, key=lambda name: social[name]["points"] / social[name]["attempts"])
        return untried[0]

    def blended_value(name):
        own = stats[name]["points"] / stats[name]["attempts"]
        peer = social[name]["points"] / social[name]["attempts"] if social[name]["attempts"] else own
        return (1 - social_weight) * own + social_weight * peer

    return max(names, key=blended_value)


def run_world(rounds=300, seed=42, social_weight=0.35):
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")
    if not 0 <= social_weight <= 1:
        raise ValueError("social_weight must be between 0 and 1")
    rng = random.Random(seed)
    agents = {name: {"epsilon": cfg["epsilon"], "stats": _fresh_stats(), "history": []}
              for name, cfg in DEFAULT_AGENTS.items()}
    shared_board = []
    agent_names = list(agents)
    for turn in range(1, rounds + 1):
        agent_name = agent_names[(turn - 1) % len(agent_names)]
        agent = agents[agent_name]
        peers = _social_stats(shared_board, agent_name)
        strategy = _choose(agent["stats"], rng, agent["epsilon"], peers, social_weight)
        outcome = simulate(strategy, STRATEGIES[strategy], 1, rng)
        points = outcome["abstract_score"]
        row = agent["stats"][strategy]
        row["attempts"] += 1
        row["successes"] += outcome["successes"]
        row["points"] += points
        event = {"turn": turn, "agent": agent_name, "strategy": strategy,
                 "success": bool(outcome["successes"]), "abstract_points": points}
        agent["history"].append(event)
        shared_board.append(event)

    summaries = []
    for name, agent in agents.items():
        stats = agent["stats"]
        attempts = sum(row["attempts"] for row in stats.values())
        successes = sum(row["successes"] for row in stats.values())
        points = sum(row["points"] for row in stats.values())
        summaries.append({"agent": name, "epsilon": agent["epsilon"], "attempts": attempts,
                          "successes": successes, "abstract_points": points,
                          "points_per_attempt": round(points / attempts, 4) if attempts else 0,
                          "strategy_stats": stats})
    summaries.sort(key=lambda row: row["points_per_attempt"], reverse=True)
    return {"mode": "synthetic_multi_agent_simulation", "money_features": "DISABLED",
            "rounds": rounds, "seed": seed, "social_learning_weight": social_weight,
            "agent_count": len(agents),
            "agents_ranked_by_observed_points_per_attempt": summaries,
            "shared_event_board": shared_board,
            "note": "Invented game rules only. Abstract points are not money or evidence of real-world performance."}


def main():
    parser = argparse.ArgumentParser(description="Run a money-free multi-agent toy world.")
    parser.add_argument("--rounds", type=int, default=300, help="Total turns shared by all agents")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--social-weight", type=float, default=0.35,
                        help="Influence of peers' observed outcomes, from 0 to 1")
    args = parser.parse_args()
    report = run_world(args.rounds, args.seed, args.social_weight)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("MULTI-AGENT TOY WORLD")
    print("MONEY: NOT USED OR REPRESENTED")
    print("Agents: {} | total turns: {} | social learning weight: {:.2f}".format(
        report["agent_count"], report["rounds"], report["social_learning_weight"]))
    print("-" * 64)
    for row in report["agents_ranked_by_observed_points_per_attempt"]:
        print("{:<14} turns={:3} successes={:3} points={:4} avg_points/turn={:.3f}".format(
            row["agent"], row["attempts"], row["successes"], row["abstract_points"], row["points_per_attempt"]))
    print("-" * 64)
    print("Toy simulation only. Local report: {}".format(REPORT_PATH))


if __name__ == "__main__":
    main()
