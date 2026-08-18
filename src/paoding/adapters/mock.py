from __future__ import annotations

from typing import Any


class MockAdapter:
    name = "mock"
    empirical = False

    def run(self, case_dir: str, workflow: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "unverified",
            "empirical": False,
            "notes": "Mock adapter validates pipeline plumbing only; it does not generate or compare a real artifact.",
        }
