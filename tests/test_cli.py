import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "random_coffee_matcher", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def test_rank_json_cli_outputs_candidates():
    result = run_cli("rank", "examples/participants.csv", "--format", "json", "--top-k", "2")
    data = json.loads(result.stdout)

    assert data
    assert {"person_a", "person_b", "score", "reasons", "risk_notes", "agenda"} <= set(data[0])


def test_packet_cli_writes_review_gate(tmp_path):
    out = tmp_path / "packet.md"
    run_cli("packet", "examples/participants.csv", "founder-ai", "growth-host", "--channel", "discord", "--out", str(out))
    text = out.read_text(encoding="utf-8")

    assert "Live Send Gate" in text
    assert "both sides opt in" in text
    assert "reviewed Discord outreach" in text
