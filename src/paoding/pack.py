from __future__ import annotations

from pathlib import Path
import shutil


def package_case(case_dir: Path, output: Path | None = None) -> Path:
    if output is None:
        output = case_dir.parent / f"{case_dir.name}-bundle.zip"
    base = output.with_suffix("")
    created = shutil.make_archive(str(base), "zip", root_dir=case_dir)
    return Path(created)
