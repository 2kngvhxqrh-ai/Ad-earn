import random
import unittest
from simulator import Experiment

class ExperimentTests(unittest.TestCase):
    def test_same_seed_repeats_same_result(self):
        e = Experiment('test', 100, 0.2, 5.0, 0.0, 'synthetic')
        self.assertEqual(e.run(random.Random(7)), e.run(random.Random(7)))

    def test_costs_are_subtracted(self):
        e = Experiment('test', 10, 1.0, 2.0, 0.5, 'synthetic')
        result = e.run(random.Random(1))
        self.assertEqual(result['simulated_sales'], 10)
        self.assertEqual(result['simulated_revenue'], 20.0)
        self.assertEqual(result['estimated_costs'], 5.0)
        self.assertEqual(result['simulated_net_profit'], 15.0)

    def test_results_are_marked_synthetic(self):
        result = Experiment('test', 1, 0.0, 1.0, 0.0, 'synthetic').run(random.Random(1))
        self.assertEqual(result['evidence_status'], 'SYNTHETIC_ASSUMPTIONS_NOT_REAL_MARKET_DATA')
        self.assertEqual(result['simulated_sales'], 0)

if __name__ == '__main__':
    unittest.main()
