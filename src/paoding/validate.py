from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator

REQUIRED = ["PIPELINE_STATE.yaml", "ARTIFACT_OVERVIEW.md", "source-metadata.json", "EVIDENCE_LEDGER.json"]
SCHEMAS = {
    "EVIDENCE_LEDGER.json": "evidence.schema.json",
    "SHOT_MANIFEST.json": "shot_manifest.schema.json",
    "hypotheses/hypotheses.json": "hypotheses.schema.json",
    "WORKFLOW.yaml": "workflow.schema.json",
    "reproduction/runs.json": "reproduction.schema.json",
}


def _schema_dir() -> Path:
    bundled = Path(__file__).resolve().parent / "schemas"
    if bundled.exists():
        return bundled
    return Path(__file__).resolve().parents[2] / "schemas"


def validate_case(case_dir: Path) -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED:
        if not (case_dir / rel).exists():
            errors.append(f"missing required file: {rel}")

    schema_dir = _schema_dir()
    for rel, schema_name in SCHEMAS.items():
        path = case_dir / rel
        if not path.exists():
            continue
        try:
            data: Any
            if path.suffix in {".yaml", ".yml"}:
                data = yaml.safe_load(path.read_text(encoding="utf-8"))
            else:
                data = json.loads(path.read_text(encoding="utf-8"))
            schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
            for err in Draft202012Validator(schema).iter_errors(data):
                loc = "/".join(str(x) for x in err.absolute_path)
                errors.append(f"schema {rel}{('/' + loc) if loc else ''}: {err.message}")
        except Exception as exc:  # validation should report rather than crash
            errors.append(f"could not validate {rel}: {exc}")

    evidence_ids: set[str] = set()
    ledger = case_dir / "EVIDENCE_LEDGER.json"
    if ledger.exists():
        try:
            evidence_ids = {x["id"] for x in json.loads(ledger.read_text(encoding="utf-8")).get("items", [])}
        except Exception:
            pass
    hp = case_dir / "hypotheses" / "hypotheses.json"
    if hp.exists():
        try:
            for item in json.loads(hp.read_text(encoding="utf-8")).get("items", []):
                for ref in item.get("evidence_ids", []):
                    if ref not in evidence_ids:
                        errors.append(f"hypothesis {item.get('id')} references missing evidence: {ref}")
        except Exception:
            pass

    state_path = case_dir / "PIPELINE_STATE.yaml"
    if state_path.exists():
        state = yaml.safe_load(state_path.read_text(encoding="utf-8")) or {}
        completed = set(state.get("completed_stages", []))
        stage_requirements = {
            "trace": ["SHOT_MANIFEST.json"],
            "reverse": ["hypotheses/hypotheses.json"],
            "assemble": ["WORKFLOW.yaml", "RECIPE.md", "RECONSTRUCTION_PLAN.md", "skill/SKILL.md", "skill/repro-tests.json"],
            "reproduce": ["reproduction/runs.json", "reproduction/comparison.md"],
        }
        for stage, rels in stage_requirements.items():
            if stage in completed:
                for rel in rels:
                    if not (case_dir / rel).exists():
                        errors.append(f"state says {stage} complete but {rel} is missing")

        source_path = Path(state.get("source_path", ""))
        expected_hash = state.get("source_hash")
        if source_path.is_file() and expected_hash:
            h = hashlib.sha256()
            with source_path.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    h.update(chunk)
            if h.hexdigest() != expected_hash:
                errors.append("source file hash changed since case initialization")

        if state.get("reproduction_status") == "verified":
            runs = case_dir / "reproduction" / "runs.json"
            if not runs.exists():
                errors.append("state says verified but reproduction/runs.json is missing")
            else:
                payload = json.loads(runs.read_text(encoding="utf-8"))
                if not any(r.get("status") == "verified" and r.get("empirical") is True for r in payload.get("runs", [])):
                    errors.append("state says verified but no empirical verified run exists")
    return errors
