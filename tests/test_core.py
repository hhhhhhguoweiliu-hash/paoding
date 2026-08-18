from __future__ import annotations

import json
from pathlib import Path

from paoding.init_case import init_case
from paoding.reverse import reverse_case
from paoding.assemble import assemble_case
from paoding.reproduce import reproduce_case
from paoding.validate import validate_case


def test_non_video_case_structure_without_trace(tmp_path: Path):
    source = tmp_path / "artifact.mp4"
    source.write_bytes(b"not-a-real-video")
    case = init_case(source, tmp_path / "cases")
    assert (case / "PIPELINE_STATE.yaml").exists()
    assert json.loads((case / "EVIDENCE_LEDGER.json").read_text())["items"][0]["level"] == "O"


def test_mock_never_claims_verified(tmp_path: Path):
    source = tmp_path / "artifact.mp4"
    source.write_bytes(b"not-a-real-video")
    case = init_case(source, tmp_path / "cases")
    reverse_case(case)
    assemble_case(case)
    reproduce_case(case, "mock")
    runs = json.loads((case / "reproduction" / "runs.json").read_text())
    assert runs["runs"][0]["status"] == "unverified"
    assert runs["runs"][0]["empirical"] is False
    assert validate_case(case) == []


def test_bad_evidence_reference_is_rejected(tmp_path: Path):
    source = tmp_path / "artifact.mp4"
    source.write_bytes(b"x")
    case = init_case(source, tmp_path / "cases")
    hpdir = case / "hypotheses"
    hpdir.mkdir(exist_ok=True)
    hp = {
        "version": "0.1",
        "items": [{
            "id": "H1", "claim": "x", "level": "H", "evidence_ids": ["DOES-NOT-EXIST"],
            "attribution_confidence": 0.1, "reproduction_confidence": 0.1, "reproduction_impact": 0.5,
            "alternatives": [], "falsification_test": "test"
        }]
    }
    (hpdir / "hypotheses.json").write_text(json.dumps(hp))
    assert any("missing evidence" in e for e in validate_case(case))
