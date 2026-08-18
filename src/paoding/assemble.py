from __future__ import annotations

import json
from pathlib import Path
import yaml

from .state import mark_stage


def assemble_case(case_dir: Path) -> None:
    hp = json.loads((case_dir / "hypotheses" / "hypotheses.json").read_text(encoding="utf-8"))
    material = [h for h in hp.get("items", []) if h.get("level") in {"S", "H"} and h.get("reproduction_impact", 0) >= 0.5]

    nodes = [
        {"id": "source", "capability": "source_asset", "requirements": ["preserve original artifact", "retain provenance"]},
        {"id": "analysis", "capability": "evidence_backed_reverse_analysis", "requirements": ["O/S/H/U separation", "alternatives", "falsification tests"]},
        {"id": "generation", "capability": "artifact_generation_or_transformation", "requirements": ["provider agnostic", "use only evidence-backed high-impact decisions"]},
        {"id": "edit", "capability": "edit_and_export", "requirements": ["timing", "audio/text/post-processing as applicable"]}
    ]
    workflow = {
        "version": "0.1",
        "capability_recipe": {"nodes": nodes, "edges": [{"from": "source", "to": "analysis"}, {"from": "analysis", "to": "generation"}, {"from": "generation", "to": "edit"}]},
        "tool_adapters": [],
        "reproduction": {"status": "unverified", "reason": "No real generator run has been validated."},
        "high_impact_hypothesis_ids": [h["id"] for h in material],
    }
    (case_dir / "WORKFLOW.yaml").write_text(yaml.safe_dump(workflow, allow_unicode=True, sort_keys=False), encoding="utf-8")

    recipe_lines = [
        "# Equivalent Production Recipe",
        "",
        "## Status",
        "`unverified` — no empirical reproduction has been validated yet.",
        "",
        "## Capability recipe",
        "1. Preserve and reference the source artifact without modifying it.",
        "2. Use timestamped evidence and keep observation separate from inference.",
        "3. Apply only high-impact S/H production decisions; unresolved U items remain open.",
        "4. Map capabilities to replaceable tools/adapters at execution time.",
        "5. Reproduce and compare before marking the recipe verified.",
        "",
        "## High-impact hypotheses",
    ]
    if material:
        for h in material:
            recipe_lines.append(f"- **{h['id']} [{h['level']}]** {h['claim']} (reproduction confidence {h['reproduction_confidence']:.2f})")
    else:
        recipe_lines.append("- None graduated yet. Complete reverse analysis before claiming a specific production workflow.")

    recipe_lines += [
        "",
        "## Quality gates",
        "- No unsupported concrete model attribution.",
        "- All core claims trace to evidence IDs or are explicitly U.",
        "- Mock runs never count as empirical verification.",
        "- Compare relevant dimensions before `verified` status.",
    ]
    (case_dir / "RECIPE.md").write_text("\n".join(recipe_lines) + "\n", encoding="utf-8")

    (case_dir / "RECONSTRUCTION_PLAN.md").write_text(
        "# Reconstruction Plan\n\n1. Replace unresolved hypotheses with evidence-backed S/H claims.\n2. Select replaceable tool adapters for required capabilities.\n3. Execute one minimum-cost reproduction.\n4. Compare relevant dimensions.\n5. Run one ablation on the highest-impact uncertain hypothesis.\n",
        encoding="utf-8",
    )

    skill_dir = case_dir / "skill"
    skill_dir.mkdir(exist_ok=True)
    source_name = json.loads((case_dir / "source-metadata.json").read_text(encoding="utf-8")).get("source_filename", "artifact")
    production_skill = f"""---
name: paoding-derived-{case_dir.name}
description: Reproduce the production pattern distilled from {source_name} using evidence-backed capabilities. Trigger for requests to create a new artifact with the same production logic or signature effect, not for exact historical attribution.
---

# Derived Production Skill — {case_dir.name}

## Status
`unverified` until a real generation and comparison pass succeeds.

## Inputs
- New subject/theme/content to transfer into the same production pattern.
- Any required source/reference assets.

## Execution
1. Load `../RECIPE.md` and `../WORKFLOW.yaml`.
2. Preserve capability-level decisions; choose current tool adapters separately.
3. Do not turn unresolved `U` items into hard requirements.
4. Generate a minimum-cost test first.
5. Compare relevant dimensions before claiming success.

## Boundaries
- Do not claim this is the original creator's exact model, prompt, seed, LoRA or private workflow.
- Do not count mock runs as empirical reproduction.
- Do not copy unauthorized private assets or a real person's identity.
"""
    (skill_dir / "SKILL.md").write_text(production_skill, encoding="utf-8")
    repro_tests = {
        "version": "0.1",
        "tests": [
            {"id": "route-positive-1", "type": "routing-positive", "prompt": "Use the same production logic on a new topic.", "expected": "trigger"},
            {"id": "route-negative-1", "type": "routing-negative", "prompt": "Tell me the exact private seed the original creator used.", "expected": "do_not_claim"},
            {"id": "boundary-1", "type": "boundary", "prompt": "Reproduce the pattern but with a different subject.", "expected": "trigger_with_transfer"},
            {"id": "transfer-1", "type": "transfer", "prompt": "Apply the distilled recipe to a new theme and compare the signature effect.", "expected": "empirical_test_required"}
        ]
    }
    (skill_dir / "repro-tests.json").write_text(json.dumps(repro_tests, ensure_ascii=False, indent=2), encoding="utf-8")
    mark_stage(case_dir, "assemble", ["WORKFLOW.yaml", "RECIPE.md", "RECONSTRUCTION_PLAN.md", "skill/SKILL.md", "skill/repro-tests.json"], "reproduce")
