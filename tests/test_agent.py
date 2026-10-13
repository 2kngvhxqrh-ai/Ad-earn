import unittest
from agent import run_agent

class AgentTests(unittest.TestCase):
    def test_deterministic_with_same_seed(self):
        self.assertEqual(run_agent(50, 12), run_agent(50, 12))
    def test_money_free_and_three_strategies(self):
        result = run_agent(100, 42)
        self.assertEqual(result["money_features"], "DISABLED")
        self.assertEqual(len(result["strategy_stats"]), 3)
        self.assertEqual(sum(s["attempts"] for s in result["strategy_stats"].values()), 100)
        self.assertNotIn("revenue", result)
        self.assertNotIn("currency", result)
    def test_invalid_rounds_rejected(self):
        with self.assertRaises(ValueError):
            run_agent(0)

if __name__ == "__main__":
    unittest.main()
