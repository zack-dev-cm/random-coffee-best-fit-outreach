---
name: random-coffee-best-fit-outreach
description: Consent-first random coffee skill for ranking best-fit people, drafting double opt-in LinkedIn or Discord outreach, and logging reviewed OpenClaw or Computer Use work without Telegram bot execution, selfbots, scraping, or automated sending.
metadata: {"openclaw":{"skillKey":"random-coffee-best-fit-outreach","requires":{"anyBins":["python3","python"]}}}
---

# Random Coffee Best Fit Outreach

## Goal

Run a consent-first random coffee workflow:

- normalize opt-in people into a small participant CSV
- rank best-fit 1:1 intro candidates by mutual utility
- draft first-touch and double opt-in LinkedIn or Discord messages
- use OpenClaw or Computer Use only for reviewed browser or GUI context and evidence logging
- keep any live send manual and explicitly approved

## Use This Skill When

- the user asks for random coffee, best-fit introductions, warm networking, or founder/operator matching
- LinkedIn or Discord should be used to reach people, but without hidden scraping, selfbots, auto-joins, or auto-DM behavior
- an older chat-first matching project exists and should be adapted into a public-safe outreach workflow
- Codex should produce a repeatable outreach packet, not ad hoc social messages

## Inputs

Use a CSV with these canonical columns:

```csv
person_id,display_name,role,organization,location,timezone,languages,domains,skills,offers,needs,linkedin_url,discord_ref,preferred_channel,availability,consent_notes,do_not_match,notes
```

Read `references/intake-schema.md` when the user gives messy notes, an old Telegram contact map, copied LinkedIn summaries, or Discord community notes.

## Workflow

1. Restate the cohort goal, target audience, consent boundary, and verification command.
2. Normalize participant data into the CSV schema. Use placeholder or consented data only.
3. Rank matches:
   - In a cloned repo: `python3 -m random_coffee_matcher rank <people.csv> --format markdown --out <report.md>`.
   - From this skill wrapper in the repo: `python3 {baseDir}/scripts/random_coffee_matcher.py rank <people.csv> --format markdown --out <report.md>`.
4. Review the top matches. Prefer pairs with clear mutual utility, language overlap, manageable timezone gaps, and complete consent notes.
5. Generate a reviewed packet for any selected pair:
   - `python3 -m random_coffee_matcher packet <people.csv> <person-a-id> <person-b-id> --out <packet.md>`.
6. Ask the user before any live send. If approved, use OpenClaw for browser surfaces or Computer Use for Discord desktop/web GUI work around an operator-owned session.
7. Log the result: sent, skipped, blocked, replied, opted in, declined, or scheduled.

## Outreach Surface Boundary

Read `references/outreach-surface-runbook.md` before browser or GUI work.

Rules:

- Use an operator-owned LinkedIn or Discord account.
- Prefer OpenClaw for browser-controlled LinkedIn or Discord Web. Use Computer Use when the user explicitly wants Discord desktop or a GUI session that OpenClaw cannot control cleanly.
- Browser and GUI review are read-only until the user explicitly approves a manual send.
- Do not automate unsolicited LinkedIn messages, Discord DMs, server joins, invites, or reactions.
- Do not bypass login, captcha, rate limits, platform protections, or privacy settings.
- Summarize profile signals as tags and short notes. Do not copy private messages or long profile/post text into public artifacts.
- Stop and report if login, verification, captcha, account warning, or platform friction appears.

## Outreach Rules

- First touch asks whether the person wants to be considered. It should not reveal another person's identity.
- Double opt-in asks each side before sharing names, handles, links, or detailed context.
- Keep drafts short, concrete, and easy to decline.
- Avoid fake urgency, pressure, claims of personal familiarity, or unverifiable praise.
- If either person declines or does not reply after the agreed follow-up limit, close the case.

## Verification

For the open-source repo, run:

```bash
python3 -m pytest -q
python3 -m random_coffee_matcher rank examples/participants.csv --format text
```

Before publishing, run the local public-surface audit available in the surrounding Codex workspace when present.
