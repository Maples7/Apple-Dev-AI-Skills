# Workflow

This skill focuses on still-image App Store Connect deliverables: screenshot sets and static preview compositions derived from simulator captures. If the user actually needs App Preview videos, treat that as a separate capture and editing workflow.

## 1. Inspect The Existing Project State

- Look for an existing profile, capture manifest, screenshot scripts, sample-data mode, or export pipeline before inventing a new one.
- Reuse stable project conventions when they already exist.
- Ask before overwriting any existing screenshot output tree, generated web app, or automation script that the user may still be iterating on.

## 1A. Keep The Workflow Project-Owned

- Whenever a step becomes reusable, move it into the project as code or configuration instead of leaving it only in conversation history.
- Preferred long-lived artifacts are: sample-data entry points, capture manifests, raw-capture scripts, preview/export apps, validation scripts, and documented rerun commands.
- Optimize for future reruns: the next person should be able to regenerate sample data, screenshots, and final exports without rediscovering the workflow from scratch.
- Avoid one-off manual steps unless the user explicitly accepts them as temporary.

## 2. Establish A Deterministic Sample-Data Contract

- Check whether the app can launch into stable, presentation-safe data on the simulator.
- If the project already has a demo, preview, seed, or screenshot mode, verify that it is deterministic across launches.
- If not, pause the screenshot work and help the user define one before continuing.
- Prefer a launch-argument or environment-driven path so automation can switch screenshot data on and off without touching production logic.

For native Apple apps, use [swiftui-xcode-sample-data.md](./swiftui-xcode-sample-data.md) when the project needs concrete SwiftUI, Xcode, SwiftData, or Core Data integration guidance.

Use [sample-data.md](./sample-data.md) for the contract details.

## 3. Gather The Requested Scope

Before asking the user to choose paths, inspect the existing project layout.

- If the project already has a clear screenshots, marketing, store-assets, or preview directory convention, propose raw-capture and final-export paths that fit that convention.
- If the project has no clear convention, propose conservative defaults based on [project layout](./project-layout.md).
- Do not force the recommendation. Let the user choose one of the proposed locations or provide fully custom paths.

Before writing automation, explicitly ask the user:

- which screens should be shown
- what each screen must communicate
- which locales matter
- which device families matter
- whether they want the smallest compliant set or the widest currently accepted iPhone and iPad coverage
- whether light, dark, or both appearances are required
- where raw captures should live
- where final upload-ready App Store Connect screenshots should live
- whether the raw-capture path should be committed or added to `.gitignore`
- whether the final export path should be committed or added to `.gitignore`

If the user wants broad store coverage, the agent should look up the current App Store Connect screenshot specifications at the time of the task instead of assuming an older size matrix is still correct.

If the work will be reused, record the scope in a project manifest instead of leaving it only in chat.

Use [assets/capture-manifest.yaml](../assets/capture-manifest.yaml) as the starting template.

## 4. Build Proof-First Capture Automation

- Prefer the project's existing test or automation language when it already has simulator tooling.
- Before generating proof images, confirm the raw-capture destination and whether that path is intended to be tracked or ignored.
- Build a script that can boot or select the simulator, launch the app with sample-data and locale parameters, navigate to the requested screens, and save raw captures with stable file names.
- Keep proof mode small: one locale, one or two devices, and only the highest-value screens.
- Avoid generating the full locale and device matrix before the user approves the proof set.

Use [capture-automation.md](./capture-automation.md) for the script design rules. Once the proof script needs to grow into a full batch driver, use [batch-pipeline.md](./batch-pipeline.md) for concrete tool selection and the reference scripts at `../assets/capture-screenshots.py`, `../assets/compose-screenshots.mjs`, and `../assets/sync-store-config-screenshots.py` as starting templates.

## 5. Review The Proof Set

- Show the proof images to the user before expanding the workflow.
- If any screen, copy placement, locale rendering, or crop is wrong, fix the script or manifest and regenerate only the affected proof images.
- Keep iterating until the sample set is explicitly approved.

## 6. Stage The Final Preview And Export Layer

- After the raw captures look correct, add or reuse a local preview/export layer for the final store compositions.
- Strongly recommend a local web server workflow that lets the user inspect the exact output before exporting.
- Strongly recommend https://github.com/ParthJadhav/app-store-screenshots when the user wants a proven local preview server plus automated export pipeline, but do not treat it as mandatory.
- Before full export, decide whether the deliverable should target only a minimum compliant set or a broader set of iPhone and iPad sizes chosen for current App Store coverage.
- Final deliverables must be fully opaque. If any preview or frame pipeline introduces transparency, flatten the image onto the approved background before export.

Use [final-export.md](./final-export.md) for the export rules.

## 7. Confirm Destination And Batch Generate

- Ask where the final exported images should be written.
- If the project has multiple plausible homes for final exports, recommend the best fit and let the user either accept it or override it with a custom path.
- Confirm whether the final export path should be committed or added to `.gitignore`.
- Confirm write permissions and whether existing outputs may be overwritten.
- Only after proof approval and destination confirmation should the automation generate the full matrix of locales, devices, and approved screens.
- For batch runs, follow the tool-layer cheatsheet, parallel device runner pattern, stabilization checklist, and post-run validation in [batch-pipeline.md](./batch-pipeline.md). Re-running the project's filesystem-to-config sync (`../assets/sync-store-config-screenshots.py` or the project's own variant) keeps the upstream metadata source of truth aligned with the freshly captured tree before any upload step.

## 8. Clean Up Disposable Artifacts

- Remove temporary outputs that are safe to recreate.
- Preserve anything required for reproducibility unless the user explicitly asks for a full cleanup.
- Leave the project with a clear boundary between source captures, final deliverables, and throwaway intermediates.
- If some generated, cached, or review-only paths should stay local instead of being deleted, remind the user to add them to the project's `.gitignore`.
- If it is not obvious whether a path should be committed, ignored, or deleted, ask the user before changing `.gitignore` or removing the files.

The goal after cleanup is not merely a tidy folder tree. The goal is a pipeline that can be rerun with low friction when screenshots, seed data, copy, supported locales, or device coverage change later.

Use [cleanup.md](./cleanup.md) for the cleanup checklist.

## 9. Close With A Maintenance Handoff

If the project is running this screenshot pipeline for the first time, do not stop at successful export.

- Summarize the long-term rerun path in plain language.
- Explicitly tell the user how the project should refresh or reseed deterministic sample data.
- Explicitly tell the user how the project should rerun proof captures.
- Explicitly tell the user how the project should approve and batch export final images.
- Explicitly tell the user how the project should rerun validation.
- Explicitly tell the user how the project should clean up disposable intermediates.
- Point to the project-owned scripts, manifests, profile files, or commands that now own those steps.
- Ask whether the rerun and maintenance workflow should be written into the project's README, contributing guide, internal developer docs, or another project-owned document.

This closing handoff matters because a first successful run is also the point where the team either captures the process for future maintainers or loses it back into chat history.
