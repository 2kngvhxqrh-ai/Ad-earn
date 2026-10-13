import random
import unittest
from multi_agent import _choose, _fresh_stats, run_world
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

    def test_invalid_rounds_and_social_weight_rejected(self):
        with self.assertRaises(ValueError):
            run_world(0)
        with self.assertRaises(ValueError):
            run_world(10, social_weight=1.1)


if __name__ == "__main__":
    unittest.main()
