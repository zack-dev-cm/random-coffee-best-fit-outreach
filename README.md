# Random Coffee Best Fit Outreach

**Rank opt-in random coffee matches and prepare reviewed LinkedIn or Discord outreach packets.**

This repo turns a chat-first random coffee prototype into a public, inspectable workflow for best-fit 1:1 introductions. It keeps the useful part, matching people by mutual utility, and uses a Codex + OpenClaw or Computer Use operating loop for reviewed manual outreach on LinkedIn or Discord.

It is not a LinkedIn scraper, Discord selfbot, stealth messenger, or auto-DM bot. The CLI works from participant data you are allowed to use. The skill helps Codex create drafts, review profile context in an operator-controlled browser or GUI session, and log what a human approved.

## Quick Start

Rank matches from the example cohort:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
random-coffee-matcher rank examples/participants.csv --format markdown
```

Create a double opt-in intro packet:

```bash
random-coffee-matcher packet examples/participants.csv founder-ai growth-host --channel preferred --out /tmp/random-coffee-packet.md
```

Generate a blank intake CSV template:

```bash
random-coffee-matcher template --out /tmp/random-coffee-people.csv
```

## What It Does

- reads a small CSV of opt-in participants
- scores pair fit from offers, needs, skills, domains, language, timezone, and explicit do-not-match constraints
- renders ranked match reports with transparent reasons and risks
- drafts double opt-in messages that do not reveal the other person's identity before consent
- includes a Codex skill for reviewed LinkedIn or Discord outreach using OpenClaw or Computer Use

## CSV Columns

The matcher accepts these canonical columns:

```csv
person_id,display_name,role,organization,location,timezone,languages,domains,skills,offers,needs,linkedin_url,discord_ref,preferred_channel,availability,consent_notes,do_not_match,notes
```

Comma-like fields can use `;`, `,`, or `|` separators. `do_not_match` contains person ids that must never be paired with that participant.

## Public Boundary

- Use participant-provided, consented, or intentionally public profile data.
- Keep LinkedIn and Discord review read-only unless the user explicitly approves a live manual send.
- Do not automate unsolicited LinkedIn messaging, Discord DMs, joins, invites, or server actions.
- Do not bypass login, captcha, rate limits, platform protections, or user privacy settings.
- Store summaries and tags for matching; avoid copying private messages or long post excerpts into public artifacts.
- Run double opt-in before revealing identities, handles, links, or detailed context.

## Included

- `src/random_coffee_matcher/`: dependency-free matcher CLI
- `examples/participants.csv`: placeholder sample cohort
- `skill/random-coffee-best-fit-outreach/SKILL.md`: Codex outreach workflow
- `skill/random-coffee-best-fit-outreach/references/`: outreach and intake runbooks
- `tests/`: regression tests for scoring, rendering, and CLI behavior

## Development

```bash
python3 -m pytest -q
python3 -m random_coffee_matcher rank examples/participants.csv --format text
```

## Security

See [SECURITY.md](SECURITY.md) for responsible disclosure and public-surface boundaries.

## License

MIT
