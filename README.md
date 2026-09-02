# Authorized Phishing Simulation Platform

![CI](https://github.com/BabaDee-code/phishing-attack-simulation-platform/actions/workflows/ci.yml/badge.svg)

A safe, employer-facing phishing awareness simulation project for authorized security training. This repository focuses on campaign governance, user education, risk scoring, metrics, and defensible reporting. It does **not** collect credentials, bypass controls, evade detection, or send real phishing emails.

## What this project shows

- Security awareness campaign design
- Safe landing page and training redirect workflow
- Risk scoring for simulated user interactions
- Campaign reporting and executive metrics
- Governance guardrails for ethical simulation
- Unit-tested Python logic and CI validation

## Safety boundaries

This project is for authorized internal training only. It intentionally excludes credential harvesting, stealth, persistence, evasion, exploit delivery, mailbox compromise, or real email-sending automation.

## Repository structure

```text
src/phish_sim/              Campaign and risk-scoring logic
data/sample_events.json     Simulated awareness event data
tests/                      Unit tests
.github/workflows/ci.yml    Automated test workflow
docs/rules-of-engagement.md Authorized-use guardrails
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements-dev.txt
pytest -q
PYTHONPATH=src python -m phish_sim.report data/sample_events.json
```

On Windows PowerShell, use `$env:PYTHONPATH = "src"` before the final command.

## Example metrics

```json
{
  "total_events": 5,
  "clicked": 2,
  "reported": 2,
  "training_completed": 3,
  "campaign_risk_score": 35
}
```

## Portfolio talking points

This project demonstrates how I would run phishing simulations responsibly: define rules of engagement, protect users, avoid credential capture, measure behavior, and convert outcomes into actionable training and security metrics.
