"""Multi-agent toy world with independent and shared learning; abstract points only."""
import argparse
import json
import random
from pathlib import Path
from simulator import STRATEGIES, simulate

REPORT_PATH = Path("data/multi_agent_report.json")
MEMORY_PATH = Path("data/multi_agent_memory.json")
MEMORY_EVENT_LIMIT = 1000
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


def _validated_stats(raw):
    """Accept saved learning statistics only when their shape and values are safe."""
    if not isinstance(raw, dict) or set(raw) != set(STRATEGIES):
        raise ValueError("saved memory has an invalid strategy set")
    result = {}
    for name in STRATEGIES:
        row = raw[name]
        if not isinstance(row, dict):
            raise ValueError("saved memory has an invalid strategy row")
        clean = {}
        for key in ("attempts", "successes", "points"):
            value = row.get(key)
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ValueError("saved memory values must be non-negative integers")
            clean[key] = value
        if clean["successes"] > clean["attempts"]:
            raise ValueError("saved successes cannot exceed attempts")
        result[name] = clean
    return result


def _load_memory(path):
    """Load local agent stats and peer examples; no network or external services."""
    if not path.exists():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("could not read saved agent memory: {}".format(exc)) from exc
    if not isinstance(raw, dict) or raw.get("version") != 1:
        raise ValueError("saved agent memory has an unsupported format")
    saved_agents = raw.get("agents")
    if not isinstance(saved_agents, dict) or set(saved_agents) != set(DEFAULT_AGENTS):
        raise ValueError("saved agent memory has an invalid agent set")
    agents = {}
    for name, config in DEFAULT_AGENTS.items():
        entry = saved_agents[name]
        if not isinstance(entry, dict):
            raise ValueError("saved agent memory has an invalid entry")
        agents[name] = _validated_stats(entry.get("stats"))
    history = raw.get("peer_history", [])
    if not isinstance(history, list):
        raise ValueError("saved peer history must be a list")
    clean_history = []
    for event in history[-MEMORY_EVENT_LIMIT:]:
        if not isinstance(event, dict) or event.get("agent") not in DEFAULT_AGENTS:
            raise ValueError("saved peer history contains an invalid event")
        if event.get("strategy") not in STRATEGIES:
            raise ValueError("saved peer history contains an invalid strategy")
        points = event.get("abstract_points")
        if isinstance(points, bool) or not isinstance(points, int) or points < 0:
            raise ValueError("saved peer history contains invalid points")
        clean_history.append({"agent": event["agent"], "strategy": event["strategy"],
                              "abstract_points": points})
    return {"agents": agents, "peer_history": clean_history}


def run_world(rounds=300, seed=42, social_weight=0.35, memory=None):
    if not 1 <= rounds <= 10000:
        raise ValueError("rounds must be between 1 and 10000")
    if not 0 <= social_weight <= 1:
        raise ValueError("social_weight must be between 0 and 1")
    rng = random.Random(seed)
    agents = {}
    for name, cfg in DEFAULT_AGENTS.items():
        stats = _validated_stats(memory["agents"][name]) if memory else _fresh_stats()
        agents[name] = {"epsilon": cfg["epsilon"], "stats": stats, "history": []}
    peer_history = list(memory["peer_history"]) if memory else []
    shared_board = []
    agent_names = list(agents)
    for turn in range(1, rounds + 1):
        agent_name = agent_names[(turn - 1) % len(agent_names)]
        agent = agents[agent_name]
        peers = _social_stats(peer_history + shared_board, agent_name)
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
    new_history = (peer_history + [{"agent": e["agent"], "strategy": e["strategy"],
                                   "abstract_points": e["abstract_points"]} for e in shared_board])[-MEMORY_EVENT_LIMIT:]
    new_memory = {"version": 1, "agents": {name: {"stats": agent["stats"]}
                                          for name, agent in agents.items()},
                  "peer_history": new_history}
    return {"mode": "synthetic_multi_agent_simulation", "money_features": "DISABLED",
            "rounds": rounds, "seed": seed, "social_learning_weight": social_weight,
            "agent_count": len(agents),
            "agents_ranked_by_observed_points_per_attempt": summaries,
            "shared_event_board": shared_board, "memory": new_memory,
            "note": "Invented game rules only. Abstract points are not money or evidence of real-world performance."}


def main():
    parser = argparse.ArgumentParser(description="Run a money-free multi-agent toy world.")
    parser.add_argument("--rounds", type=int, default=300, help="Total turns shared by all agents")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--social-weight", type=float, default=0.35,
                        help="Influence of peers' observed outcomes, from 0 to 1")
    parser.add_argument("--resume", action="store_true",
                        help="Continue from local abstract-point learning memory saved by an earlier run")
    parser.add_argument("--memory-path", type=Path, default=MEMORY_PATH,
                        help="Local JSON file for learning memory")
    args = parser.parse_args()
    memory = _load_memory(args.memory_path) if args.resume else None
    report = run_world(args.rounds, args.seed, args.social_weight, memory=memory)
    REPORT_PATH.parent.mkdir(exist_ok=True)
    args.memory_path.parent.mkdir(parents=True, exist_ok=True)
    args.memory_path.write_text(json.dumps(report["memory"], indent=2) + "\n", encoding="utf-8")
    report.pop("memory")
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("MULTI-AGENT TOY WORLD")
    print("MONEY: NOT USED OR REPRESENTED")
    print("Agents: {} | new turns: {} | social learning weight: {:.2f}".format(
        report["agent_count"], report["rounds"], report["social_learning_weight"]))
    print("Learning memory: {}".format("resumed and updated" if args.resume else "fresh and saved"))
    print("-" * 64)
    for row in report["agents_ranked_by_observed_points_per_attempt"]:
        print("{:<14} lifetime turns={:3} successes={:3} points={:4} avg_points/turn={:.3f}".format(
            row["agent"], row["attempts"], row["successes"], row["abstract_points"], row["points_per_attempt"]))
    print("-" * 64)
    print("Toy simulation only. Local report: {}".format(REPORT_PATH))


if __name__ == "__main__":
    main()
