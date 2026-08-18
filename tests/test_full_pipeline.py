from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from paoding.init_case import init_case
from paoding.trace import trace_case
from paoding.reverse import reverse_case
from paoding.assemble import assemble_case
from paoding.reproduce import reproduce_case
from paoding.validate import validate_case


@pytest.mark.skipif(not shutil.which("ffmpeg") or not shutil.which("ffprobe"), reason="ffmpeg/ffprobe required")
def test_full_synthetic_video_pipeline(tmp_path: Path):
    video = tmp_path / "demo.mp4"
    subprocess.run([
        shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=black:s=160x120:d=2:r=12",
        "-f", "lavfi", "-i", "sine=frequency=440:duration=2",
        "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(video)
    ], check=True)
    case = init_case(video, tmp_path / "cases")
    trace_case(case, interval=0.5)
    reverse_case(case)
    assemble_case(case)
    reproduce_case(case, "mock")
    assert (case / "skill" / "SKILL.md").exists()
    assert validate_case(case) == []
