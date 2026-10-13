import unittest
from benchmark import run_benchmark, run_epsilon_experiment


class BenchmarkTests(unittest.TestCase):
    def test_repeatable_and_money_free(self):
        first = run_benchmark(seeds=4, rounds=40)
        second = run_benchmark(seeds=4, rounds=40)
        self.assertEqual(first, second)
        self.assertEqual(first["money_features"], "DISABLED")
        self.assertEqual(len(first["ranking"]), 4)
        self.assertTrue(all(row["seeds_tested"] == 4 for row in first["ranking"]))

    def test_epsilon_tuning_reports_separate_holdout(self):
        result = run_epsilon_experiment(seeds=3, rounds=30)
        self.assertEqual(result["mode"], "epsilon_tuning_with_holdout")
        self.assertEqual(result["money_features"], "DISABLED")
        self.assertEqual(result["training_seeds"], 3)
        self.assertEqual(result["validation_seeds"], 3)
        self.assertIn(result["selected_epsilon"], result["epsilon_candidates"])
        self.assertEqual(len(result["validation_results"]), len(result["epsilon_candidates"]))
        self.assertEqual(result["validation_comparison"]["default_epsilon_0_15_mean"],
                         next(row["mean_points_per_turn"] for row in result["validation_results"]
                              if row["epsilon"] == 0.15))

    def test_invalid_arguments_rejected(self):
        with self.assertRaises(ValueError):
            run_benchmark(seeds=0)
        with self.assertRaises(ValueError):
            run_benchmark(rounds=0)
        with self.assertRaises(ValueError):
            run_benchmark(epsilon=1.5)
        with self.assertRaises(ValueError):
            run_epsilon_experiment(seeds=0)


if __name__ == "__main__":
    unittest.main()
