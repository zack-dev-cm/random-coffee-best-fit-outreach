from __future__ import annotations

import itertools
import re

from .models import MatchCandidate, Person


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "can",
    "for",
    "from",
    "help",
    "i",
    "in",
    "is",
    "need",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+-]*")
TZ_RE = re.compile(r"(?:utc|gmt)?\s*([+-])\s*(\d{1,2})(?::?(\d{2}))?", re.IGNORECASE)


def normalize_id(value: str) -> str:
    return (value or "").strip().lower().lstrip("@")


def stem_token(token: str) -> str:
    if len(token) > 4 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 4 and token.endswith("s"):
        return token[:-1]
    return token


def tokenize(*values: str) -> set[str]:
    text = " ".join(value or "" for value in values).lower()
    tokens = [stem_token(token) for token in TOKEN_RE.findall(text)]
    return {token for token in tokens if token not in STOPWORDS and len(token) >= 2}


def list_tokens(values: tuple[str, ...]) -> set[str]:
    return tokenize(" ".join(values))


def parse_utc_offset(value: str) -> float | None:
    raw = (value or "").strip()
    if not raw:
        return None
    if raw.upper() == "UTC":
        return 0.0
    match = TZ_RE.search(raw)
    if not match:
        return None
    sign = -1 if match.group(1) == "-" else 1
    hours = int(match.group(2))
    minutes = int(match.group(3) or "0")
    if hours > 14 or minutes >= 60:
        return None
    return sign * (hours + minutes / 60)


def timezone_points(a: Person, b: Person) -> tuple[float, str | None]:
    a_offset = parse_utc_offset(a.timezone)
    b_offset = parse_utc_offset(b.timezone)
    if a_offset is None or b_offset is None:
        return 0.0, None
    delta = abs(a_offset - b_offset)
    delta = min(delta, 24 - delta)
    if delta <= 3:
        return 8.0, f"timezones are close ({a.timezone} and {b.timezone})"
    if delta <= 6:
        return 4.0, f"timezones are workable ({a.timezone} and {b.timezone})"
    return -4.0, f"timezone gap needs manual scheduling ({a.timezone} and {b.timezone})"


def language_points(a: Person, b: Person) -> tuple[float, str | None, str | None]:
    a_lang = {lang.strip().lower() for lang in a.languages if lang.strip()}
    b_lang = {lang.strip().lower() for lang in b.languages if lang.strip()}
    if not a_lang or not b_lang:
        return 0.0, None, None
    overlap = sorted(a_lang & b_lang)
    if overlap:
        return 8.0, "shared language: " + ", ".join(overlap), None
    return -6.0, None, "no declared language overlap"


def blocked(a: Person, b: Person) -> bool:
    a_id = normalize_id(a.person_id)
    b_id = normalize_id(b.person_id)
    return b_id in {normalize_id(item) for item in a.do_not_match} or a_id in {
        normalize_id(item) for item in b.do_not_match
    }


def score_pair(a: Person, b: Person) -> MatchCandidate | None:
    if normalize_id(a.person_id) == normalize_id(b.person_id) or blocked(a, b):
        return None

    score = 0.0
    reasons: list[str] = []
    risks: list[str] = []

    a_offer = tokenize(a.offers, " ".join(a.skills), " ".join(a.domains), a.role)
    b_offer = tokenize(b.offers, " ".join(b.skills), " ".join(b.domains), b.role)
    a_need = tokenize(a.needs)
    b_need = tokenize(b.needs)

    a_to_b = sorted(a_offer & b_need)
    b_to_a = sorted(b_offer & a_need)
    shared_domains = sorted(list_tokens(a.domains) & list_tokens(b.domains))
    shared_skills = sorted(list_tokens(a.skills) & list_tokens(b.skills))

    if a_to_b:
        points = min(24.0, 8.0 * len(a_to_b))
        score += points
        reasons.append(f"{a.display_name} can help {b.display_name} with {', '.join(a_to_b[:4])}")
    if b_to_a:
        points = min(24.0, 8.0 * len(b_to_a))
        score += points
        reasons.append(f"{b.display_name} can help {a.display_name} with {', '.join(b_to_a[:4])}")
    if a_to_b and b_to_a:
        score += 10.0
        reasons.append("mutual need-offer fit")
    if shared_domains:
        score += min(12.0, 4.0 * len(shared_domains))
        reasons.append("shared domain: " + ", ".join(shared_domains[:4]))
    if shared_skills:
        score += min(10.0, 3.0 * len(shared_skills))
        reasons.append("shared skills: " + ", ".join(shared_skills[:4]))

    language_score, language_reason, language_risk = language_points(a, b)
    score += language_score
    if language_reason:
        reasons.append(language_reason)
    if language_risk:
        risks.append(language_risk)

    tz_score, tz_reason = timezone_points(a, b)
    score += tz_score
    if tz_reason and tz_score >= 0:
        reasons.append(tz_reason)
    elif tz_reason:
        risks.append(tz_reason)

    availability_overlap = tokenize(a.availability) & tokenize(b.availability)
    if availability_overlap:
        score += 4.0
        reasons.append("availability overlap: " + ", ".join(sorted(availability_overlap)[:3]))

    if not a.consent_notes or not b.consent_notes:
        risks.append("consent notes are incomplete")
    if not has_any_contact_ref(a) or not has_any_contact_ref(b):
        risks.append("outreach reference missing for at least one participant")
    if not a_to_b and not b_to_a:
        risks.append("no direct need-offer overlap found")

    clamped = max(0.0, min(100.0, score))
    if clamped <= 0:
        return None

    agenda = build_agenda(a, b, a_to_b, b_to_a, shared_domains)
    return MatchCandidate(
        person_a=a,
        person_b=b,
        score=clamped,
        reasons=tuple(reasons[:8]),
        risk_notes=tuple(risks[:6]),
        agenda=tuple(agenda),
    )


def build_agenda(
    a: Person,
    b: Person,
    a_to_b: list[str],
    b_to_a: list[str],
    shared_domains: list[str],
) -> list[str]:
    agenda: list[str] = []
    if a_to_b:
        agenda.append(f"{b.display_name} asks about {', '.join(a_to_b[:3])}.")
    if b_to_a:
        agenda.append(f"{a.display_name} asks about {', '.join(b_to_a[:3])}.")
    if shared_domains:
        agenda.append(f"Compare current work in {', '.join(shared_domains[:3])}.")
    if not agenda:
        agenda.append("Validate whether goals and current work make a useful intro.")
    agenda.append("Agree on one concrete next step or close the loop as no fit.")
    return agenda[:4]


def rank_matches(people: list[Person], *, top_k: int = 20, min_score: float = 1.0) -> list[MatchCandidate]:
    candidates = []
    for a, b in itertools.combinations(people, 2):
        candidate = score_pair(a, b)
        if candidate and candidate.score >= min_score:
            candidates.append(candidate)
    candidates.sort(key=lambda item: (-item.score, item.person_a.person_id, item.person_b.person_id))
    return candidates[: max(1, top_k)]


def has_any_contact_ref(person: Person) -> bool:
    return bool(person.linkedin_url.strip() or person.discord_ref.strip())
