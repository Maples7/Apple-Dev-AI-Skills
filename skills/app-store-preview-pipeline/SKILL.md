---
name: app-store-preview-pipeline
description: "Plan and generate App Store Connect screenshots and static preview compositions from deterministic simulator captures. Use when preparing Apple marketing screenshots, defining stable sample data, automating localized capture flows, choosing broad device coverage, or reviewing proof images before final batch export."
compatibility: "Designed for Agent-Skills-compatible clients such as VS Code/Copilot and Windsurf. Cursor requires a rules or prompt wrapper instead of direct SKILL.md installation."
---

# App Store Preview Pipeline

Plan and produce App Store Connect previews and screenshots through a proof-first workflow.

## Use This Skill When

- the user wants App Store Connect previews or screenshots for an Apple app
- simulator screenshots should be repeatable across locales or devices
- the project needs stable sample data before marketing capture can begin
- the user wants automation for navigating to specific screens and saving raw captures
- a local preview and export layer is needed before generating final store assets
- the project should own a maintainable screenshot pipeline that can be rerun later without reconstructing steps from chat
- the workflow should pause for review after a small proof set instead of generating everything at once

## Required Operating Model

1. Treat final store assets as the output of a multi-stage pipeline, not a one-shot screenshot script.
2. Convert reusable work into project-owned scripts, manifests, sample-data hooks, preview layers, and validation commands so future reruns do not depend on agent memory or chat history.
3. Inspect whether the app already supports deterministic simulator sample data before authoring capture automation.
4. If stable sample data does not exist, ask the user what is available and help define a repeatable seed path before taking screenshots.
5. Ask which screens, locales, devices, coverage goals, and visual requirements matter before writing automation.
6. Generate a small proof set first, get user approval, then expand to batch export.
7. Research the current App Store Connect screenshot specifications before final export when the user wants coverage across as many iPhone or iPad classes as possible.
8. Confirm the final output location, target size strategy, and opaque image requirement before writing large batches of exported images.
9. Clean up temporary outputs and intermediate artifacts that are safe to remove after delivery.

## Project Profile

Look for a screenshot pipeline profile in one of these places before making assumptions:

- `app-store-preview-pipeline-profile.yaml`
- `.ai/app-store-preview-pipeline-profile.yaml`
- `.github/app-store-preview-pipeline-profile.yaml`
- another path explicitly provided by the user

If no profile exists, use the conservative defaults in [workflow](./references/workflow.md) and recommend creating a project profile before this workflow becomes routine.

Use [assets/app-store-preview-pipeline-profile.yaml](./assets/app-store-preview-pipeline-profile.yaml) as the template when a project needs one.

## Procedure

1. Follow the end-to-end sequence in [workflow](./references/workflow.md).
2. Use [sample data](./references/sample-data.md) to establish a deterministic simulator state contract.
3. Use [capture automation](./references/capture-automation.md) to design app-specific scripts for proof captures.
4. Use [project layout](./references/project-layout.md) to keep source captures, preview sources, reviews, and exports separate.
5. Use [final export](./references/final-export.md) to stage preview review, optional web preview tooling, current size coverage checks, and final batch generation.
6. Use [assets/validate-exported-images.py](./assets/validate-exported-images.py) as a template for a project-owned pre-delivery validation command.
7. Use [cleanup](./references/cleanup.md) to remove disposable intermediate artifacts after delivery.
8. Use [public examples](./references/public-examples.md) only as outcome references, never as implementation dependencies.

## Exit Criteria

- the project has a documented path to deterministic simulator sample data
- the requested screens, locales, devices, and review checkpoints are explicit
- the target size strategy is explicit, especially when the user wants broad iPhone or iPad coverage
- a proof set is generated and reviewed before full batch export
- final App Store Connect screenshots or static preview compositions are exported to a confirmed destination
- the project owns reusable scripts or commands for regenerating sample data, raw captures, validation, and final export
- final exported images are flattened and do not contain transparent alpha
- disposable intermediate outputs are identified and cleaned up when safe
