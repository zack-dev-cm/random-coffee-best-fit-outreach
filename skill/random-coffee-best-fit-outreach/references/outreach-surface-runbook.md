# Outreach Surface Runbook

Use this runbook only after a match report or intro packet exists.

## Preflight

1. Confirm the user approved review or live manual outreach.
2. Confirm the operator owns the LinkedIn or Discord account being used.
3. Confirm the target people came from opt-in, consented, or intentionally public data.
4. Prepare a log file with timestamp, operator, target person id, target surface, intended action, and outcome.

## OpenClaw Browser Steps

Use OpenClaw for browser-controlled LinkedIn or Discord Web when available:

```bash
openclaw browser --browser-profile <profile> start --json
openclaw browser --browser-profile <profile> open "<target-url>" --json
openclaw browser --browser-profile <profile> snapshot --format ai --limit 260
openclaw browser --browser-profile <profile> screenshot --json
```

If you are developing against a local OpenClaw checkout, compare `openclaw --version` with the local checkout version before browser work. Prefer the current installed CLI when the config was written by a newer OpenClaw than the checkout.

Use `https://www.linkedin.com/` for LinkedIn review or `https://discord.com/channels/@me` for Discord Web only when the operator is already authenticated and the user approved the surface.

## Computer Use GUI Steps

Use Computer Use when the user explicitly asks for Discord desktop or when a GUI session cannot be represented cleanly through OpenClaw browser controls.

Rules:

- Observe first and summarize the current state.
- Ask for approval before navigating to a person, server, DM, or compose box.
- Keep the operator in control of login, 2FA, captcha, account warnings, and final send.
- Never claim that Codex sent a message automatically.

## Review Mode

- Summarize only high-level signals: role, current project themes, relevant skills, server/community context, and likely fit.
- Do not copy long profile text, posts, comments, server messages, or private DMs into generated artifacts.
- Update the CSV with tags and notes only when the information is allowed for this workflow.

## Manual Send Mode

Only after approval:

1. Open the approved packet.
2. Re-read the exact draft.
3. Let the operator paste or type it in LinkedIn or Discord.
4. Log whether it was sent, skipped, blocked, or changed.
5. Capture evidence only if it does not expose private messages or personal data.

The skill should never claim that Codex, OpenClaw, or Computer Use sent a LinkedIn or Discord message automatically.
