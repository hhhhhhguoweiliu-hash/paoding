from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


def ffprobe_metadata(source: Path) -> dict[str, Any]:
    exe = shutil.which("ffprobe")
    if not exe:
        return {"available": False, "error": "ffprobe not found"}
    cmd = [exe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(source)]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {"available": True, "error": proc.stderr.strip() or "ffprobe failed"}
    data = json.loads(proc.stdout)
    data["available"] = True
    return data


def duration_seconds(metadata: dict[str, Any]) -> float | None:
    try:
        return float(metadata.get("format", {}).get("duration"))
    except (TypeError, ValueError):
        return None
