# Autonomous Strategy Sandbox

A zero-cost, money-free simulation for experimenting with autonomous strategies.

## Absolute scope

- No money or currency represented in the program.
- No revenue, profit, sales, payment, purchase, deposit, or financial-account features.
- No paid services, third-party libraries, API calls, or network calls.
- No real-world actions. It runs toy simulations using synthetic probabilities.
- The score is abstract game points only; it is not an estimate of earnings.

## Run

```bash
python simulator.py
python -m unittest discover -s tests -v
```

Optional repeatable run:

```bash
python simulator.py --attempts 250 --seed 7
```

The program compares three toy strategies and appends results to a local file at `data/simulation_ledger.json`. It does not contact websites or discover real opportunities. The probabilities are invented game parameters and should not be treated as evidence about real-world outcomes.
