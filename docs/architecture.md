# Architecture

The project has two surfaces:

- `random_coffee_matcher`: a small Python CLI for deterministic candidate ranking and intro packet generation.
- `random-coffee-best-fit-outreach`: a Codex skill that wraps the CLI in reviewed LinkedIn or Discord outreach loops.

## Data Flow

1. The operator creates a CSV from opt-in or intentionally public participant data.
2. The CLI parses people into normalized records.
3. The matcher evaluates every permitted pair.
4. Reports and packets expose score reasons and risks.
5. Codex uses the skill to review drafts, ask for approval, and log any OpenClaw browser work.

## Matching Model

The matcher is intentionally simple:

- complementarity: one side's offers match the other side's needs
- context: shared domains and skills
- logistics: language and timezone feasibility
- safety: explicit do-not-match constraints and weak consent warnings

The score is a prioritization aid, not an automated decision. A human should review the top matches before outreach.

## Outreach Boundary

LinkedIn and Discord are outreach surfaces, not hidden data sources. Browser or desktop review is operator-controlled and summarized conservatively. Live messages are manual and require explicit user approval.
