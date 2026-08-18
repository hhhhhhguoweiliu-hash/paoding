from __future__ import annotations

import json
from pathlib import Path

from .state import mark_stage


def reverse_case(case_dir: Path, input_json: Path | None = None) -> None:
    ledger = json.loads((case_dir / "EVIDENCE_LEDGER.json").read_text(encoding="utf-8"))
    evidence_ids = [item["id"] for item in ledger.get("items", [])]

    if input_json:
        payload = json.loads(input_json.read_text(encoding="utf-8"))
    else:
        payload = {
            "version": "0.1",
            "items": [
                {
                    "id": "H0001",
                    "claim": "Production decisions are unresolved until a human or external multimodal analyzer reviews the traced evidence.",
                    "level": "U",
                    "evidence_ids": evidence_ids[:3],
                    "attribution_confidence": 0.0,
                    "reproduction_confidence": 0.0,
                    "reproduction_impact": 1.0,
                    "alternatives": ["manual analysis", "external multimodal LLM analysis"],
                    "falsification_test": "Review timestamped evidence and replace this placeholder with evidence-backed hypotheses.",
                    "model_candidates": []
                }
            ]
        }

    out_dir = case_dir / "hypotheses"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "hypotheses.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    mark_stage(case_dir, "reverse", [out.relative_to(case_dir).as_posix()], "assemble")
