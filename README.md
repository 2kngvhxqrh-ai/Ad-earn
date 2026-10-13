# Autonomous Strategy Sandbox

A zero-cost, money-free simulation for experimenting with autonomous strategies.

## Absolute scope

- No money or currency represented in the program.
- No revenue, profit, sales, payment, purchase, deposit, or financial-account features.
- No paid services, third-party libraries, API calls, or network calls at runtime.
- No real-world actions. It runs toy simulations using synthetic probabilities.
- The score is abstract game points only; it is not an estimate of earnings.

## Run

```bash
python simulator.py
python -m unittest discover -s tests -v
python agent.py --rounds 300 --seed 42
```

The adaptive agent uses an epsilon-greedy policy to choose among three toy strategies, observe abstract point outcomes, and rank strategies by observed points per attempt. It writes a local report to `data/agent_state.json`.

The probabilities and point rewards are invented game parameters, not evidence about real-world outcomes. A fixed seed makes runs reproducible. No internet connection or external service is required at runtime.
