import unittest
from benchmark import run_benchmark


class BenchmarkTests(unittest.TestCase):
    def test_repeatable_and_money_free(self):
        first = run_benchmark(seeds=4, rounds=40)
        second = run_benchmark(seeds=4, rounds=40)
        self.assertEqual(first, second)
        self.assertEqual(first["money_features"], "DISABLED")
        self.assertEqual(len(first["ranking"]), 4)
        self.assertTrue(all(row["seeds_tested"] == 4 for row in first["ranking"]))

    def test_invalid_arguments_rejected(self):
        with self.assertRaises(ValueError):
            run_benchmark(seeds=0)
        with self.assertRaises(ValueError):
            run_benchmark(rounds=0)
        with self.assertRaises(ValueError):
            run_benchmark(epsilon=1.5)


if __name__ == "__main__":
    unittest.main()
