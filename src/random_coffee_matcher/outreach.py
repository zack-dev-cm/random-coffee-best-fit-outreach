from __future__ import annotations

from .models import MatchCandidate, Person


def first_name(person: Person) -> str:
    return (person.display_name or person.person_id).split()[0]


def safe_goal(person: Person) -> str:
    if person.needs:
        return person.needs.split(";")[0].split(",")[0].strip()
    if person.domains:
        return "work in " + person.domains[0]
    return "a focused peer intro"


def safe_offer(person: Person) -> str:
    if person.offers:
        return person.offers.split(";")[0].split(",")[0].strip()
    if person.skills:
        return person.skills[0]
    return "relevant experience"


def anonymized_opt_in(recipient: Person, other: Person, program_name: str) -> str:
    return (
        f"Hi {first_name(recipient)}, I am running a small opt-in {program_name} round. "
        f"I see a possible 15-minute intro: you are looking for {safe_goal(recipient)}, "
        f"and the other person can bring {safe_offer(other)}. "
        "Would you like me to ask them too? No pressure if not."
    )


def manual_first_touch(person: Person, program_name: str, channel: str) -> str:
    label = channel_label(channel)
    surface = "here" if channel == "preferred" else f"on {label}"
    return (
        f"Hi {first_name(person)}, I am curating a small opt-in {program_name} round for "
        f"{person.domains[0] if person.domains else 'operator'} peers. "
        f"Open to being considered for one useful 15-minute intro {surface}?"
    )


def mutual_utility(candidate: MatchCandidate) -> str:
    if candidate.reasons:
        return candidate.reasons[0].rstrip(".") + "."
    return "Potential fit needs manual review."


def render_intro_packet(
    candidate: MatchCandidate,
    *,
    program_name: str = "random coffee",
    operator_name: str = "operator",
    channel: str = "preferred",
) -> str:
    a = candidate.person_a
    b = candidate.person_b
    resolved_channel = resolve_channel(a, b, channel)
    resolved_label = channel_label(resolved_channel)
    lines = [
        "# Random Coffee Intro Packet",
        "",
        f"- Operator: {operator_name}",
        f"- Program: {program_name}",
        f"- Score: {candidate.score:.1f}/100",
        f"- Pair: {a.display_name} <> {b.display_name}",
        f"- Primary channel: reviewed {resolved_label} outreach",
        "",
        "## Mutual Utility",
        "",
        mutual_utility(candidate),
        "",
        "## Agenda",
        "",
    ]
    for item in candidate.agenda:
        lines.append(f"- {item}")
    lines.extend(["", "## Reasons", ""])
    for item in candidate.reasons:
        lines.append(f"- {item}")
    if candidate.risk_notes:
        lines.extend(["", "## Review Risks", ""])
        for item in candidate.risk_notes:
            lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## First Touch Drafts",
            "",
            f"### {a.display_name}",
            "",
            manual_first_touch(a, program_name, resolved_channel),
            "",
            f"### {b.display_name}",
            "",
            manual_first_touch(b, program_name, resolved_channel),
            "",
            "## Double Opt-In Drafts",
            "",
            f"### Ask {a.display_name}",
            "",
            anonymized_opt_in(a, b, program_name),
            "",
            f"### Ask {b.display_name}",
            "",
            anonymized_opt_in(b, a, program_name),
            "",
            "## Live Send Gate",
            "",
            "- A human operator must review this packet before any LinkedIn or Discord message is sent.",
            "- Do not reveal names, handles, profile URLs, or private context until both sides opt in.",
            "- Log the final action and outcome after manual send or after deciding not to send.",
            "",
        ]
    )
    return "\n".join(lines)


def resolve_channel(a: Person, b: Person, requested: str) -> str:
    requested = (requested or "preferred").strip().lower()
    if requested in {"linkedin", "discord"}:
        return requested
    a_pref = (a.preferred_channel or "").strip().lower()
    b_pref = (b.preferred_channel or "").strip().lower()
    if a_pref == b_pref and a_pref in {"linkedin", "discord"}:
        return a_pref
    if a.discord_ref and b.discord_ref:
        return "discord"
    if a.linkedin_url and b.linkedin_url:
        return "linkedin"
    return "preferred"


def channel_label(channel: str) -> str:
    normalized = (channel or "preferred").strip().lower()
    if normalized == "linkedin":
        return "LinkedIn"
    if normalized == "discord":
        return "Discord"
    return "preferred channel"
