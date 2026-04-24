from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .io import read_people_csv, write_template
from .matching import rank_matches, score_pair
from .outreach import render_intro_packet
from .render import render_json, render_markdown, render_text


def write_output(text: str, out: str | None) -> None:
    if out:
        Path(out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)


def find_person(people, ref: str):
    needle = ref.strip().lower()
    for person in people:
        if person.person_id.lower() == needle or person.display_name.lower() == needle:
            return person
    raise SystemExit(f"person not found: {ref}")


def cmd_rank(args: argparse.Namespace) -> int:
    people = read_people_csv(args.people_csv)
    candidates = rank_matches(people, top_k=args.top_k, min_score=args.min_score)
    if args.format == "json":
        text = render_json(candidates)
    elif args.format == "markdown":
        text = render_markdown(candidates)
    else:
        text = render_text(candidates)
    write_output(text, args.out)
    return 0


def cmd_packet(args: argparse.Namespace) -> int:
    people = read_people_csv(args.people_csv)
    person_a = find_person(people, args.person_a)
    person_b = find_person(people, args.person_b)
    candidate = score_pair(person_a, person_b)
    if candidate is None:
        raise SystemExit("pair is blocked or has no score")
    text = render_intro_packet(
        candidate,
        program_name=args.program_name,
        operator_name=args.operator_name,
        channel=args.channel,
    )
    write_output(text, args.out)
    return 0


def cmd_template(args: argparse.Namespace) -> int:
    write_template(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank opt-in random coffee matches and render outreach packets.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rank = subparsers.add_parser("rank", help="rank match candidates from a participant CSV")
    rank.add_argument("people_csv")
    rank.add_argument("--top-k", type=int, default=20)
    rank.add_argument("--min-score", type=float, default=1.0)
    rank.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    rank.add_argument("--out")
    rank.set_defaults(func=cmd_rank)

    packet = subparsers.add_parser("packet", help="render a reviewed intro packet for one pair")
    packet.add_argument("people_csv")
    packet.add_argument("person_a")
    packet.add_argument("person_b")
    packet.add_argument("--program-name", default="random coffee")
    packet.add_argument("--operator-name", default="operator")
    packet.add_argument("--channel", choices=["preferred", "linkedin", "discord"], default="preferred")
    packet.add_argument("--out")
    packet.set_defaults(func=cmd_packet)

    template = subparsers.add_parser("template", help="write a blank participant CSV template")
    template.add_argument("--out", required=True)
    template.set_defaults(func=cmd_template)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
