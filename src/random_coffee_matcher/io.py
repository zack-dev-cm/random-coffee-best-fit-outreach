from __future__ import annotations

import csv
import re
from pathlib import Path

from .models import Person


ALIASES = {
    "person_id": {"person_id", "id", "contact_id", "participant_id"},
    "display_name": {"display_name", "name", "full_name"},
    "role": {"role", "title"},
    "organization": {"organization", "org", "company"},
    "location": {"location", "city"},
    "timezone": {"timezone", "tz"},
    "languages": {"languages", "language"},
    "domains": {"domains", "domain", "industries", "industry"},
    "skills": {"skills", "expertise", "tags"},
    "offers": {"offers", "offer", "i_can_offer", "can_offer"},
    "needs": {"needs", "need", "i_need", "looking_for"},
    "linkedin_url": {"linkedin_url", "linkedin", "linkedin_profile_ref", "linkedin_profile"},
    "discord_ref": {"discord_ref", "discord", "discord_handle", "discord_user"},
    "preferred_channel": {"preferred_channel", "preferred_channels", "channel", "outreach_channel"},
    "availability": {"availability", "meeting_constraints"},
    "consent_notes": {"consent_notes", "consent", "sharing_consent"},
    "do_not_match": {"do_not_match", "blocked_ids", "exclude"},
    "notes": {"notes", "context"},
}

CANONICAL_COLUMNS = (
    "person_id",
    "display_name",
    "role",
    "organization",
    "location",
    "timezone",
    "languages",
    "domains",
    "skills",
    "offers",
    "needs",
    "linkedin_url",
    "discord_ref",
    "preferred_channel",
    "availability",
    "consent_notes",
    "do_not_match",
    "notes",
)

SPLIT_RE = re.compile(r"\s*[;,|]\s*")
KEY_RE = re.compile(r"[^a-z0-9]+")


def normalize_key(value: str) -> str:
    return KEY_RE.sub("_", (value or "").strip().lower()).strip("_")


def alias_map(fieldnames: list[str] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in fieldnames or []:
        key = normalize_key(raw)
        for canonical, aliases in ALIASES.items():
            if key == canonical or key in aliases:
                out[canonical] = raw
                break
    return out


def split_list(value: str) -> tuple[str, ...]:
    parts = [part.strip() for part in SPLIT_RE.split(value or "") if part.strip()]
    return tuple(dict.fromkeys(parts))


def get(row: dict[str, str], mapped: dict[str, str], key: str, default: str = "") -> str:
    raw_key = mapped.get(key)
    if not raw_key:
        return default
    return (row.get(raw_key) or "").strip()


def read_people_csv(path: str | Path) -> list[Person]:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        mapped = alias_map(reader.fieldnames)
        people: list[Person] = []
        for index, row in enumerate(reader, start=1):
            display_name = get(row, mapped, "display_name")
            person_id = get(row, mapped, "person_id") or normalize_key(display_name) or f"person_{index}"
            people.append(
                Person(
                    person_id=person_id,
                    display_name=display_name or person_id,
                    role=get(row, mapped, "role"),
                    organization=get(row, mapped, "organization"),
                    location=get(row, mapped, "location"),
                    timezone=get(row, mapped, "timezone"),
                    languages=split_list(get(row, mapped, "languages")),
                    domains=split_list(get(row, mapped, "domains")),
                    skills=split_list(get(row, mapped, "skills")),
                    offers=get(row, mapped, "offers"),
                    needs=get(row, mapped, "needs"),
                    linkedin_url=get(row, mapped, "linkedin_url"),
                    discord_ref=get(row, mapped, "discord_ref"),
                    preferred_channel=get(row, mapped, "preferred_channel", "preferred") or "preferred",
                    availability=get(row, mapped, "availability"),
                    consent_notes=get(row, mapped, "consent_notes"),
                    do_not_match=split_list(get(row, mapped, "do_not_match")),
                    notes=get(row, mapped, "notes"),
                )
            )
    return people


def write_template(path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CANONICAL_COLUMNS)
