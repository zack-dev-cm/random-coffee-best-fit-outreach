from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Person:
    person_id: str
    display_name: str
    role: str = ""
    organization: str = ""
    location: str = ""
    timezone: str = ""
    languages: tuple[str, ...] = ()
    domains: tuple[str, ...] = ()
    skills: tuple[str, ...] = ()
    offers: str = ""
    needs: str = ""
    linkedin_url: str = ""
    discord_ref: str = ""
    preferred_channel: str = "preferred"
    availability: str = ""
    consent_notes: str = ""
    do_not_match: tuple[str, ...] = ()
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "person_id": self.person_id,
            "display_name": self.display_name,
            "role": self.role,
            "organization": self.organization,
            "location": self.location,
            "timezone": self.timezone,
            "languages": list(self.languages),
            "domains": list(self.domains),
            "skills": list(self.skills),
            "offers": self.offers,
            "needs": self.needs,
            "linkedin_url": self.linkedin_url,
            "discord_ref": self.discord_ref,
            "preferred_channel": self.preferred_channel,
            "availability": self.availability,
            "consent_notes": self.consent_notes,
            "do_not_match": list(self.do_not_match),
            "notes": self.notes,
        }


@dataclass(frozen=True)
class MatchCandidate:
    person_a: Person
    person_b: Person
    score: float
    reasons: tuple[str, ...]
    risk_notes: tuple[str, ...]
    agenda: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "person_a": self.person_a.to_dict(),
            "person_b": self.person_b.to_dict(),
            "score": round(self.score, 2),
            "reasons": list(self.reasons),
            "risk_notes": list(self.risk_notes),
            "agenda": list(self.agenda),
        }
