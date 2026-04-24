from __future__ import annotations

import json

from .models import MatchCandidate


def render_json(candidates: list[MatchCandidate]) -> str:
    return json.dumps([candidate.to_dict() for candidate in candidates], indent=2, ensure_ascii=False) + "\n"


def render_text(candidates: list[MatchCandidate]) -> str:
    if not candidates:
        return "No matches above the requested threshold.\n"
    lines: list[str] = []
    for index, candidate in enumerate(candidates, start=1):
        lines.append(
            f"{index}. {candidate.person_a.person_id} <> {candidate.person_b.person_id} "
            f"score={candidate.score:.1f}"
        )
        for reason in candidate.reasons[:3]:
            lines.append(f"   - {reason}")
        for risk in candidate.risk_notes[:2]:
            lines.append(f"   risk: {risk}")
    return "\n".join(lines) + "\n"


def render_markdown(candidates: list[MatchCandidate]) -> str:
    lines = ["# Random Coffee Match Report", ""]
    if not candidates:
        lines.append("No matches above the requested threshold.")
        return "\n".join(lines) + "\n"

    lines.extend(
        [
            "| Rank | Pair | Score | Main reason | Risks |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for index, candidate in enumerate(candidates, start=1):
        pair = f"{candidate.person_a.display_name} <> {candidate.person_b.display_name}"
        reason = candidate.reasons[0] if candidate.reasons else "Manual review needed"
        risks = "; ".join(candidate.risk_notes) if candidate.risk_notes else "None"
        lines.append(f"| {index} | {pair} | {candidate.score:.1f} | {reason} | {risks} |")
    lines.append("")
    for index, candidate in enumerate(candidates, start=1):
        lines.append(f"## {index}. {candidate.person_a.display_name} <> {candidate.person_b.display_name}")
        lines.append("")
        lines.append(f"Score: **{candidate.score:.1f}/100**")
        lines.append("")
        lines.append("Agenda:")
        for item in candidate.agenda:
            lines.append(f"- {item}")
        lines.append("")
    return "\n".join(lines) + "\n"

