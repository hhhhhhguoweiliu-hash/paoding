from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

STATE_FILE = "PIPELINE_STATE.yaml"


def load_state(case_dir: Path) -> dict[str, Any]:
    path = case_dir / STATE_FILE
    if not path.exists():
        raise FileNotFoundError(f"Missing {STATE_FILE}: {case_dir}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def save_state(case_dir: Path, state: dict[str, Any]) -> None:
    path = case_dir / STATE_FILE
    path.write_text(yaml.safe_dump(state, allow_unicode=True, sort_keys=False), encoding="utf-8")


def mark_stage(case_dir: Path, stage: str, artifacts: list[str], next_action: str) -> None:
    state = load_state(case_dir)
    completed = list(state.get("completed_stages", []))
    if stage not in completed:
        completed.append(stage)
    produced = list(state.get("artifacts_produced", []))
    for artifact in artifacts:
        if artifact not in produced:
            produced.append(artifact)
    state["completed_stages"] = completed
    state["artifacts_produced"] = produced
    state["next_action"] = next_action
    save_state(case_dir, state)
