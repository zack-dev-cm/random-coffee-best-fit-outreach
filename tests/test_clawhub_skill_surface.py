from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_SCRIPT = ROOT / "scripts" / "check_clawhub_skill_surface.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_clawhub_skill_surface", CHECK_SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_public_clawhub_skill_surface_avoids_risky_platform_terms() -> None:
    checker = _load_checker()

    assert checker.collect_issues(checker.SKILL_ROOT) == []
