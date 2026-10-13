#!/usr/bin/env python3
"""Zero-cost paper business simulator. No real transactions or external calls."""
from __future__ import annotations
import argparse, json, random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path('data')
LEDGER_PATH = DATA_DIR / 'paper_ledger.json'

@dataclass
class Experiment:
    name: str
    attempts: int
    assumed_conversion_rate: float
    assumed_revenue_per_sale: float
    estimated_cost_per_attempt: float
    note: str

    def run(self, rng: random.Random) -> dict:
        wins = sum(rng.random() < self.assumed_conversion_rate for _ in range(self.attempts))
        revenue = round(wins * self.assumed_revenue_per_sale, 2)
        costs = round(self.attempts * self.estimated_cost_per_attempt, 2)
        return {'name': self.name, 'attempts': self.attempts, 'simulated_sales': wins,
                'assumed_conversion_rate': self.assumed_conversion_rate,
                'assumed_revenue_per_sale': self.assumed_revenue_per_sale,
                'simulated_revenue': revenue, 'estimated_costs': costs,
                'simulated_net_profit': round(revenue - costs, 2),
                'evidence_status': 'SYNTHETIC_ASSUMPTIONS_NOT_REAL_MARKET_DATA', 'note': self.note}

def load_ledger() -> dict:
    if LEDGER_PATH.exists(): return json.loads(LEDGER_PATH.read_text(encoding='utf-8'))
    return {'mode':'paper_only','real_money_spent':0.0,'verified_real_revenue':0.0,
            'experiments':[],'created_at':datetime.now(timezone.utc).isoformat()}

def main() -> None:
    parser = argparse.ArgumentParser(description='Run business ideas in paper mode.')
    parser.add_argument('--seed', type=int, default=42, help='Repeatable random seed')
    parser.add_argument('--attempts', type=int, default=100, help='Synthetic attempts per experiment')
    args = parser.parse_args()
    if args.attempts < 1 or args.attempts > 10000: parser.error('--attempts must be between 1 and 10000')
    # Illustrative assumptions only; these are not market statistics.
    experiments = [
      Experiment('digital_template', args.attempts, 0.02, 5.00, 0.00, 'Hypothetical low-price digital product; demand is unvalidated.'),
      Experiment('research_deliverable', args.attempts, 0.04, 15.00, 0.00, 'Hypothetical paid research task; requires a real buyer.'),
      Experiment('microtask', args.attempts, 0.10, 1.00, 0.00, 'Hypothetical task acceptance; availability and pay are unverified.')]
    rng = random.Random(args.seed)
    results = [e.run(rng) for e in experiments]
    ledger = load_ledger()
    run = {'run_at':datetime.now(timezone.utc).isoformat(),'seed':args.seed,
           'attempts_per_experiment':args.attempts,'results':results,
           'warning':'All revenue and conversion values are simulated from invented assumptions. They are not earnings, forecasts, or evidence of demand.'}
    ledger['experiments'].append(run)
    DATA_DIR.mkdir(exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, indent=2) + '\n', encoding='utf-8')
    print('AUTONOMOUS BUSINESS — PAPER MODE')
    print('Real transactions: DISABLED')
    print('Real money spent: $0.00')
    print('Verified real revenue: $0.00')
    print('Synthetic attempts per strategy: ' + str(args.attempts))
    print('-' * 76)
    for r in sorted(results, key=lambda item: item['simulated_net_profit'], reverse=True):
        print('{:<22} sales={:3}  revenue=${:7.2f}  est. costs=${:6.2f}  paper net=${:7.2f}'.format(r['name'],r['simulated_sales'],r['simulated_revenue'],r['estimated_costs'],r['simulated_net_profit']))
    print('-' * 76)
    print('IMPORTANT: paper net is not real income. Assumptions need real-world validation.')
    print('Ledger saved to ' + str(LEDGER_PATH))

if __name__ == '__main__': main()
