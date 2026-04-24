# AGENTS.md

This repository ships one small public-safe surface: a deterministic random coffee matcher plus a Codex skill for offline intro packet review.

## Operating Rules

- Restate the cohort goal, consent boundary, offline packet boundary, and verification step before editing.
- Keep diffs narrow. Do not add platform-control, account-action, or message-delivery behavior.
- Treat public-surface review as part of the default loop.
- Put durable knowledge in `docs/codex/`.

## Repo Map

- [Overview](docs/codex/overview.md)
- [Architecture](docs/codex/architecture.md)
- [Workflow](docs/codex/workflow.md)
- [Evals](docs/codex/evals.md)
- [Cleanup](docs/codex/cleanup.md)

## Main Code Paths

- `src/random_coffee_matcher/`: matcher models, CSV parsing, scoring, rendering, and CLI.
- `skill/random-coffee-best-fit-outreach/`: offline Codex skill wrapper.
- `examples/`: fictional public examples only.
- `tests/`: regression tests.
- `.codex/agents/`: project-scoped custom agents.

## Default Verification

1. Run `python3 -m pytest -q`.
2. Run `PYTHONPATH=src python3 -m random_coffee_matcher rank examples/participants.csv --format text`.
3. Run `python3 scripts/check_clawhub_skill_surface.py`.
4. Run `python3.10 -m codex_harness audit . --strict --min-score 90` from a checkout that has `codex_harness` available.
