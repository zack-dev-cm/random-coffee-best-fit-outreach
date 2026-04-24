# Contributing

Contributions are welcome when they keep the project public-safe and inspectable.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
python3 -m pytest -q
```

## Standards

- Keep the matcher deterministic and dependency-light.
- Add tests for scoring changes.
- Do not add scraping, stealth login, captcha bypass, selfbot behavior, or auto-send behavior.
- Use placeholders in examples. Do not commit real LinkedIn profiles, Discord handles, private messages, screenshots, cookies, tokens, or local operator paths.
- Keep the skill focused on reviewed, consent-first random coffee workflows.
