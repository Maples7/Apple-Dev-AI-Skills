# App Store Preview Pipeline

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Plan and generate App Store Connect screenshots and static preview compositions through a proof-first pipeline.

## Operating Rules

1. Before writing automation, look for a screenshot pipeline profile at `app-store-preview-pipeline-profile.yaml`, `.ai/app-store-preview-pipeline-profile.yaml`, or `.github/app-store-preview-pipeline-profile.yaml`.
2. Convert reusable work into project-owned scripts, manifests, sample-data hooks, preview layers, and validation commands so future reruns do not depend on chat history.
3. Inspect whether the app already supports deterministic simulator sample data. If not, ask the user what exists and help define a repeatable screenshot-safe seed path first.
4. Ask which screens, locales, devices, and visual requirements matter before generating any scripts.
5. Prefer a reusable manifest-driven capture script in Python, JavaScript, or the project's existing automation language.
6. Generate only a small proof set first. Do not generate the full locale and device matrix until the user has approved the proof images.
7. Ask whether the user wants the smallest compliant export set or the widest currently accepted iPhone and iPad coverage, and look up the current App Store Connect screenshot specifications before the final batch when broad coverage matters.
8. Strongly recommend a local preview and export layer for final compositions. Strongly recommend https://github.com/ParthJadhav/app-store-screenshots when the user wants a proven public tool, but do not make it a hard dependency.
9. Confirm the final output location, overwrite behavior, and opaque output requirement before writing batch exports.
10. Keep a project-owned validation command for dimensions and alpha rules, and clean up disposable intermediate artifacts after delivery while preserving anything needed for reproducibility.

## Required Checks

- verify the app can launch into deterministic sample data before screenshot work
- record the requested screens and proof scope in a reusable manifest when the workflow will be reused
- prefer stable identifiers, deep links, or accessibility queries before coordinate taps
- keep raw captures separate from final exported store assets
- pause after proof generation for user review
- ensure final exported files are fully opaque and contain no transparent alpha
- leave behind project-owned rerun commands for sample data, raw capture, validation, and final export whenever the workflow is meant to persist
- treat public examples only as outcome references, never as implementation dependencies

## Canonical Source

The full reusable skill lives under [`skills/app-store-preview-pipeline/`](../../skills/app-store-preview-pipeline/).

Read these files when the wrapper alone is not enough:

- [`skills/app-store-preview-pipeline/SKILL.md`](../../skills/app-store-preview-pipeline/SKILL.md)
- [`skills/app-store-preview-pipeline/references/workflow.md`](../../skills/app-store-preview-pipeline/references/workflow.md)
- [`skills/app-store-preview-pipeline/references/sample-data.md`](../../skills/app-store-preview-pipeline/references/sample-data.md)
- [`skills/app-store-preview-pipeline/references/swiftui-xcode-sample-data.md`](../../skills/app-store-preview-pipeline/references/swiftui-xcode-sample-data.md)
- [`skills/app-store-preview-pipeline/references/native-apple-capture-checklist.md`](../../skills/app-store-preview-pipeline/references/native-apple-capture-checklist.md)
- [`skills/app-store-preview-pipeline/references/capture-automation.md`](../../skills/app-store-preview-pipeline/references/capture-automation.md)
- [`skills/app-store-preview-pipeline/references/project-layout.md`](../../skills/app-store-preview-pipeline/references/project-layout.md)
- [`skills/app-store-preview-pipeline/references/final-export.md`](../../skills/app-store-preview-pipeline/references/final-export.md)
- [`skills/app-store-preview-pipeline/references/cleanup.md`](../../skills/app-store-preview-pipeline/references/cleanup.md)
- [`skills/app-store-preview-pipeline/assets/app-store-preview-pipeline-profile.yaml`](../../skills/app-store-preview-pipeline/assets/app-store-preview-pipeline-profile.yaml)
- [`skills/app-store-preview-pipeline/assets/capture-manifest.yaml`](../../skills/app-store-preview-pipeline/assets/capture-manifest.yaml)
- [`skills/app-store-preview-pipeline/assets/swiftui-xcode-screenshot-config.yaml`](../../skills/app-store-preview-pipeline/assets/swiftui-xcode-screenshot-config.yaml)
- [`skills/app-store-preview-pipeline/assets/validate-exported-images.py`](../../skills/app-store-preview-pipeline/assets/validate-exported-images.py)
