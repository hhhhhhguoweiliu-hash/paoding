# Architecture

## Three-layer data model

### A. Evidence Layer
Only directly observed or machine-read facts: metadata, timestamp, shot boundary, visible element, audio event, text, motion.

### B. Hypothesis Layer
Possible production decisions that explain evidence: model category, I2V/T2V/V2V, reference strategy, post-production, prompt structure, editing logic.

### C. Recipe Layer
The executable equivalent method to reproduce the effect now. It does not have to equal the author's historical workflow, but it must be executable and testable.

**Never jump Evidence → Recipe without explicit hypothesis/evidence links.**

## Two confidence axes

- `attribution_confidence`: confidence that the original creator historically used this decision.
- `reproduction_confidence`: confidence that the proposed method can reproduce a similar result now.

Low attribution + high reproduction can still be a successful Paoding result.

## Workflow DAG

Typical capability nodes: `source_asset`, `prompt_spec`, `image_generation`, `video_generation`, `video_transform`, `identity_reference`, `audio_generation`, `voice`, `sfx`, `edit`, `subtitle`, `color_grade`, `upscale`, `export`.

Core nodes declare capability, not vendor. Vendor/model choices belong in `tool_adapter`.

## Validation

- Structural: schema, required files, evidence refs, confidence ranges, state consistency.
- Empirical: actual generation + comparison. If not executed, status remains `unverified`.
