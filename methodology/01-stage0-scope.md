# Stage 0 — Scope & Provenance

## Goal
Establish what artifact is being analyzed, what the user wants to reproduce, and what is known about source provenance before inference begins.

## Required outputs
- Source path or stable identifier.
- SHA256 for local files.
- Media metadata.
- User goal: analysis only / equivalent reproduction / reusable skill.
- Rights / privacy constraints if relevant.

## Rules
- Never modify the source artifact in place.
- Separate user-provided provenance from machine-observed metadata.
- Do not infer hidden author workflow in this stage.
