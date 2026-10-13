import unittest
from multi_agent import run_world


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

    def test_invalid_rounds_rejected(self):
        with self.assertRaises(ValueError):
            run_world(0)


if __name__ == "__main__":
    unittest.main()
