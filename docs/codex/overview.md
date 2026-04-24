# Overview

Random Coffee Best Fit Outreach is a public-safe matcher for opt-in 1:1 introductions.

## Product

- Python CLI: parse participant CSV files, rank best-fit pairs, and render reports or intro packets.
- Codex skill: guide reviewed LinkedIn or Discord outreach with OpenClaw or Computer Use while keeping sends manual and approved.

## Non-Goals

- No scraping.
- No LinkedIn automation.
- No Discord selfbot behavior.
- No automatic DMs, joins, invites, or reactions.
- No storage of private messages or raw profile dumps.

## Standard Checks

- `python3 -m pytest -q`
- `PYTHONPATH=src python3 -m random_coffee_matcher rank examples/participants.csv --format text`
- `python3.10 -m codex_harness audit . --strict --min-score 90`

