import json
import random
import tempfile
import unittest
from pathlib import Path
from multi_agent import _choose, _fresh_stats, _load_memory, run_world
from simulator import STRATEGIES


class MultiAgentTests(unittest.TestCase):
    def test_deterministic_with_same_seed(self):
        self.assertEqual(run_world(60, 9), run_world(60, 9))

    def test_three_agents_share_turns_and_keep_independent_stats(self):
        result = run_world(90, 42)
        self.assertEqual(result["money_features"], "DISABLED")
        self.assertEqual(result["agent_count"], 3)
        self.assertEqual(len(result["shared_event_board"]), 90)
        self.assertEqual(sum(row["attempts"] for row in result["agents_ranked_by_observed_points_per_attempt"]), 90)
        self.assertEqual({row["agent"] for row in result["agents_ranked_by_observed_points_per_attempt"]},
                         {"scout", "analyst", "specialist"})

    def test_agent_can_use_peer_results_for_untested_strategy(self):
        stats = _fresh_stats()
        social = {name: {"attempts": 0, "points": 0} for name in STRATEGIES}
        social["strategy_gamma"] = {"attempts": 4, "points": 4}
        self.assertEqual(_choose(stats, random.Random(1), 0, social, 0.5), "strategy_gamma")

    def test_memory_persists_and_resumes_learning(self):
        first = run_world(30, 42)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "memory.json"
            path.write_text(json.dumps(first["memory"]), encoding="utf-8")
            loaded = _load_memory(path)
            second = run_world(15, 43, memory=loaded)
        self.assertEqual(len(second["shared_event_board"]), 15)
        for name in ("scout", "analyst", "specialist"):
            before = sum(r["attempts"] for r in first["memory"]["agents"][name]["stats"].values())
            after = sum(r["attempts"] for r in second["memory"]["agents"][name]["stats"].values())
            self.assertGreaterEqual(after, before)
        self.assertEqual(sum(r["attempts"] for r in second["memory"]["agents"]["scout"]["stats"].values()), 15)

    def test_invalid_memory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"version":999}', encoding="utf-8")
            with self.assertRaises(ValueError):
                _load_memory(path)

    def test_invalid_rounds_and_social_weight_rejected(self):
        with self.assertRaises(ValueError):
            run_world(0)
        with self.assertRaises(ValueError):
            run_world(10, social_weight=1.1)


if __name__ == "__main__":
    unittest.main()
