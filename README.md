# Autonomous Strategy Sandbox

A zero-cost, money-free sandbox for testing adaptive strategies and multiple autonomous toy agents.

## Absolute scope

- No money or currency represented in the program.
- No revenue, profit, sales, payment, purchase, deposit, or financial-account features.
- No paid services, third-party libraries, API calls, or network calls at runtime.
- No real-world actions. It runs toy simulations using synthetic probabilities.
- Scores are abstract game points only; they are not estimates of earnings or real-world performance.

## Run

```bash
python simulator.py --attempts 100 --seed 42
python -m unittest discover -s tests -v
python agent.py --rounds 300 --seed 42
python multi_agent.py --rounds 300 --seed 42
python benchmark.py --seeds 30 --rounds 300
```

## Multi-agent toy world

`multi_agent.py` runs three independent agents in a shared, turn-based environment:

- **Scout** explores more often.
- **Analyst** balances exploration and exploiting observed results.
- **Specialist** explores less and relies more on its own observed results.

Each agent keeps separate strategy statistics. All turns are recorded on a shared event board, and the final report ranks agents by observed abstract points per turn. The agents do not control external systems and do not communicate with network services.

Reports and learning memory are written locally under `data/`, which is ignored by Git. A fixed seed makes a fresh run reproducible. By default each run starts fresh and saves memory; use `python multi_agent.py --rounds 300 --resume` to continue from saved per-agent statistics and a bounded history of peer outcomes. Use `--memory-path path/to/file.json` to choose a different local memory file. The memory file is local-only and is not committed.

## Benchmarking

`benchmark.py` compares the adaptive agent with each fixed toy strategy over multiple deterministic seeds. It reports mean abstract points per turn and variability, rather than relying on one lucky run. Try `python benchmark.py --seeds 30 --rounds 300`. The benchmark tests only invented game rules and cannot estimate real-world earnings.

## Important limitation

The world is a small, synthetic game, not a general intelligence test. Its probabilities and point rewards are invented parameters. Results show only how these agents behave under those rules; they do not establish real-world ability.
