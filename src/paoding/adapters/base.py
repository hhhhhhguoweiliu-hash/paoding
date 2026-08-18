from __future__ import annotations

from typing import Protocol, Any


class GeneratorAdapter(Protocol):
    name: str
    empirical: bool

    def run(self, case_dir: str, workflow: dict[str, Any]) -> dict[str, Any]: ...
