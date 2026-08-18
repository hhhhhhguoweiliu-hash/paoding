from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .probe import ffprobe_metadata, duration_seconds
from .state import save_state


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _slug(name: str) -> str:
    stem = Path(name).stem.lower()
    stem = re.sub(r"[^a-z0-9\-_]+", "-", stem).strip("-")
    return stem or "artifact"


def init_case(source: Path, cases_dir: Path, slug: str | None = None) -> Path:
    source = source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    case_slug = slug or _slug(source.name)
    case_dir = cases_dir.expanduser().resolve() / case_slug
    case_dir.mkdir(parents=True, exist_ok=False)
    for rel in ["hypotheses", "prompts", "reproduction", "skill"]:
        (case_dir / rel).mkdir()

    digest = _sha256(source)
    ffprobe = ffprobe_metadata(source)
    metadata = {
        "version": "0.1",
        "source_path": str(source),
        "source_filename": source.name,
        "sha256": digest,
        "file_size_bytes": source.stat().st_size,
        "ffprobe": ffprobe,
    }
    (case_dir / "source-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    dur = duration_seconds(ffprobe)
    overview = [
        "# Artifact Overview",
        "",
        f"- Source: `{source.name}`",
        f"- SHA256: `{digest}`",
        f"- Duration: {dur:.3f} s" if dur is not None else "- Duration: unknown",
        "- Scope: finished-artifact reverse distillation",
        "- Reproduction status: `unverified`",
        "",
        "## Provenance note",
        "This file records machine-observed metadata only. Historical model/prompt attribution requires separate evidence.",
    ]
    (case_dir / "ARTIFACT_OVERVIEW.md").write_text("\n".join(overview) + "\n", encoding="utf-8")

    evidence = {
        "version": "0.1",
        "items": [
            {
                "id": "E-META-0001",
                "kind": "source_metadata",
                "level": "O",
                "description": "Local source file metadata and SHA256 were recorded during init.",
                "timestamp_sec": None,
                "source": "source-metadata.json",
                "details": {"sha256": digest, "filename": source.name},
            }
        ],
    }
    (case_dir / "EVIDENCE_LEDGER.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")

    (case_dir / "AUDIT.md").write_text("# Audit\n\n- Case initialized.\n- No production hypotheses have been asserted yet.\n", encoding="utf-8")
    (case_dir / "skill" / "repro-tests.json").write_text(json.dumps({"version": "0.1", "tests": []}, indent=2), encoding="utf-8")
    (case_dir / "skill" / "test-results.md").write_text("# Test Results\n\nNo transfer tests executed yet.\n", encoding="utf-8")

    state = {
        "version": "0.1",
        "source_path": str(source),
        "source_hash": digest,
        "completed_stages": ["init"],
        "artifacts_produced": ["source-metadata.json", "ARTIFACT_OVERVIEW.md", "EVIDENCE_LEDGER.json", "AUDIT.md"],
        "unresolved_hypotheses": [],
        "reproduction_status": "unverified",
        "next_action": "trace",
    }
    save_state(case_dir, state)
    return case_dir
