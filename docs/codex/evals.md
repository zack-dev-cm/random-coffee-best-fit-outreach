# Evals

## Checks

- Unit tests cover CSV alias parsing, do-not-match blocking, consent warnings, CLI JSON output, and packet rendering.
- CLI smoke checks the example cohort ranking.
- ClawHub skill surface check blocks platform-control and message-delivery wording from the published skill bundle.
- Public-surface audit checks AGENTS, docs, CI, PR template, security policy, and leak risks.

## Match Quality Metrics

- Top pair should have a concrete need-offer reason.
- A pair with explicit do-not-match must never appear.
- Missing consent should create a risk note.
- Outreach packets must include a live-send gate and double opt-in language.
