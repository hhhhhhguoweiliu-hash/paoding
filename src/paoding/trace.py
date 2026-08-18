from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

from .probe import duration_seconds
from .state import load_state, mark_stage


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"Command failed: {' '.join(cmd)}")


def trace_case(case_dir: Path, interval: float = 2.0, extract_audio: bool = True) -> None:
    if interval <= 0:
        raise ValueError("interval must be > 0")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for trace")

    state = load_state(case_dir)
    source = Path(state["source_path"])
    if not source.exists():
        raise FileNotFoundError(f"Source file no longer exists: {source}")
    metadata = json.loads((case_dir / "source-metadata.json").read_text(encoding="utf-8"))
    dur = duration_seconds(metadata.get("ffprobe", {}))
    if dur is None:
        raise RuntimeError("Could not determine video duration from ffprobe metadata")

    frames_dir = case_dir / "evidence_frames"
    frames_dir.mkdir(exist_ok=True)
    frame_pattern = frames_dir / "frame_%05d.jpg"
    _run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(source), "-vf", f"fps=1/{interval}", "-q:v", "2", str(frame_pattern)])

    files = sorted(frames_dir.glob("frame_*.jpg"))
    frames = []
    evidence_items = []
    for i, path in enumerate(files):
        ts = min(i * interval, max(dur, 0.0))
        frame_id = f"F{i+1:04d}"
        evidence_id = f"E-FRAME-{i+1:04d}"
        rel = path.relative_to(case_dir).as_posix()
        frames.append({"id": frame_id, "timestamp_sec": round(ts, 3), "path": rel})
        evidence_items.append({
            "id": evidence_id,
            "kind": "frame_sample",
            "level": "O",
            "description": f"Evidence frame sampled at approximately {ts:.3f}s.",
            "timestamp_sec": round(ts, 3),
            "source": rel,
            "details": {"sampling_interval_sec": interval},
        })

    manifest = {"version": "0.1", "sampling": {"method": "fixed_interval", "interval_sec": interval, "duration_sec": dur}, "frames": frames}
    (case_dir / "SHOT_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    ledger_path = case_dir / "EVIDENCE_LEDGER.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["items"] = [item for item in ledger.get("items", []) if item.get("kind") != "frame_sample"] + evidence_items
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")

    artifacts = ["SHOT_MANIFEST.json", "EVIDENCE_LEDGER.json"]
    if extract_audio:
        audio_dir = case_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        wav = audio_dir / "source.wav"
        proc = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-i", str(source), "-vn", "-ac", "1", "-ar", "16000", str(wav)], capture_output=True, text=True, check=False)
        if proc.returncode == 0 and wav.exists():
            artifacts.append(wav.relative_to(case_dir).as_posix())

    mark_stage(case_dir, "trace", artifacts, "reverse")
