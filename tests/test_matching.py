from random_coffee_matcher.io import read_people_csv
from random_coffee_matcher.matching import rank_matches, score_pair
from random_coffee_matcher.models import Person


def test_rank_matches_prioritizes_mutual_need_offer_fit():
    people = [
        Person(
            person_id="founder",
            display_name="Founder",
            timezone="UTC+1",
            languages=("EN",),
            domains=("AI agents",),
            skills=("infra",),
            offers="technical architecture and infrastructure",
            needs="distribution partners",
            consent_notes="share summary",
        ),
        Person(
            person_id="community",
            display_name="Community",
            timezone="UTC+0",
            languages=("EN",),
            domains=("startups",),
            skills=("growth",),
            offers="distribution and partnerships",
            needs="technical speakers and infrastructure help",
            consent_notes="share summary",
        ),
        Person(
            person_id="blocked",
            display_name="Blocked",
            offers="distribution",
            needs="architecture",
            do_not_match=("founder",),
            consent_notes="share summary",
        ),
    ]

    ranked = rank_matches(people, top_k=5)

    assert ranked[0].person_a.person_id == "founder"
    assert ranked[0].person_b.person_id == "community"
    assert ranked[0].score > 30
    assert all("blocked" not in {m.person_a.person_id, m.person_b.person_id} for m in ranked)


def test_score_pair_warns_when_consent_missing():
    a = Person(person_id="a", display_name="A", offers="mlops", needs="community", languages=("EN",))
    b = Person(person_id="b", display_name="B", offers="community", needs="mlops", languages=("EN",))

    candidate = score_pair(a, b)

    assert candidate is not None
    assert "consent notes are incomplete" in candidate.risk_notes


def test_read_people_csv_accepts_gitcoffee_aliases(tmp_path):
    csv_path = tmp_path / "people.csv"
    csv_path.write_text(
        "contact_id,name,domain,linkedin_profile_ref,discord,offer,need,languages\n"
        "alice,Alice,AI,https://www.linkedin.com/in/example,@alice,infra,distribution,EN\n",
        encoding="utf-8",
    )

    people = read_people_csv(csv_path)

    assert people[0].person_id == "alice"
    assert people[0].domains == ("AI",)
    assert people[0].linkedin_url.startswith("https://")
    assert people[0].discord_ref == "@alice"
