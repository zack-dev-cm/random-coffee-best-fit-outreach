## Summary

- what changed
- why it changed

## Validation

- [ ] `python3 -m pytest -q`
- [ ] `PYTHONPATH=src python3 -m random_coffee_matcher rank examples/participants.csv --format text`
- [ ] `python3.10 -m codex_harness audit . --strict --min-score 90`

## Security And Public Surface

- [ ] No secrets, cookies, browser profiles, private messages, private paths, or local URLs were introduced
- [ ] No scraping, selfbot, stealth, or automated-send behavior was introduced
- [ ] README, `SKILL.md`, examples, and docs were reviewed for leak risk

