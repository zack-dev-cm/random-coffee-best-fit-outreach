# Intake Schema

Use this schema when converting notes, a spreadsheet, or an old Telegram contact map into the public matcher format.

## Required Fields

- `person_id`: stable slug, no spaces
- `display_name`: name or pseudonym approved for operator use
- `languages`: one or more language codes or names
- `offers`: what this person can help with
- `needs`: what this person wants help with
- `consent_notes`: what can be shared before and after opt-in

## Strongly Recommended Fields

- `timezone`: use `UTC`, `UTC+1`, `UTC-5`, or similar offset text
- `domains`: industries or communities
- `skills`: practical capabilities
- `linkedin_url`: profile URL if participant provided it or it is intentionally public
- `discord_ref`: Discord username, handle, server-local display name, or approved contact hint
- `availability`: broad windows, not private calendar details
- `do_not_match`: person ids to block

## Conversion Rules

- Telegram usernames are not required in this LinkedIn or Discord workflow.
- Convert handles and profile URLs into private working data unless the final packet needs them after approval.
- Store profile signals as short summaries or tags.
- Use fictional examples in public docs and tests.
