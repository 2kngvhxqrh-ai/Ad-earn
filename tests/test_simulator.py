import random
import unittest
from simulator import simulate

class SimulationTests(unittest.TestCase):
    def test_seed_is_repeatable(self):
        config = {"success_probability": 0.2, "score_per_success": 3}
        self.assertEqual(simulate("test", config, 100, random.Random(7)),
                         simulate("test", config, 100, random.Random(7)))

    def test_score_is_abstract_points(self):
        config = {"success_probability": 1.0, "score_per_success": 2}
        result = simulate("test", config, 10, random.Random(1))
        self.assertEqual(result["successes"], 10)
        self.assertEqual(result["abstract_score"], 20)
        self.assertEqual(result["evidence"], "SYNTHETIC_GAME_RULES_ONLY")
        self.assertNotIn("revenue", result)
        self.assertNotIn("currency", result)

if __name__ == "__main__":
    unittest.main()
