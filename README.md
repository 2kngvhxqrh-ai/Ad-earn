# Autonomous Business Simulator (Paper Mode)

A zero-cost sandbox for testing online-revenue hypotheses without making purchases, sending messages, or moving real money.

## Safety and honesty

- **Paper mode only:** no payment integrations, purchases, outreach, or external API calls.
- **No real earnings:** conversion rates and sale values are invented example assumptions, not market research or forecasts.
- **Real money spent:** $0 for this prototype; verified real revenue remains $0.
- **No third-party dependencies:** Python standard library only.
- The $5/day target is an objective to evaluate, not a promised result.

## Run

```bash
python simulator.py
python -m unittest discover -s tests -v
```

Optional parameters:

```bash
python simulator.py --attempts 250 --seed 7
```

The program runs three synthetic strategies, prints results, and appends a local ledger at `data/paper_ledger.json`. The ledger is ignored by Git so local run data is not accidentally committed.

## Current limitations

This first version tests the mechanics of a simulation only. It does not discover real opportunities, access websites, create products, find customers, or earn money. Its conversion rates and prices are deliberately synthetic.

## Next stages

1. Add explicit assumptions and sensitivity analysis.
2. Add evidence collection from permitted public sources, with no automated outreach or purchases.
3. Compare simulated estimates with manually verified market evidence.
4. Only consider real operation after explicit approval.
