# Architecture

The repo has two layers:

- `src/random_coffee_matcher/`: deterministic, dependency-free CLI core.
- `skill/random-coffee-best-fit-outreach/`: procedural Codex skill for reviewed outreach.

## Data Model

`Person` stores participant goals, offers, logistics, consent notes, and approved contact references. `MatchCandidate` stores score, reasons, risks, and agenda bullets.

## Scoring

Scoring favors:

- mutual need-offer overlap
- shared domains or skills
- language overlap
- workable timezone distance
- complete consent and outreach references

Explicit `do_not_match` constraints block a pair before scoring.

## Outreach

The CLI renders first-touch and double opt-in drafts. The skill handles channel-specific review and logging. Live sends stay manual.

