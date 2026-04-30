# Final Export

After the raw simulator captures are correct, generate the final App Store compositions through a local preview and export layer.

## Recommended Default

Strongly recommend a local web preview workflow that can:

- load the raw screenshots
- show device-framed final compositions
- let the user inspect the exact copy and layout before export
- export the approved images in batch after sign-off

Strongly recommend https://github.com/ParthJadhav/app-store-screenshots when the user wants a proven public tool for this stage. Treat it as the default recommendation, not as a hard dependency.

## Size Coverage Strategy

Before the final batch export, ask the user whether they want:

- a minimum compliant set of screenshot sizes
- the widest currently accepted iPhone coverage
- the widest currently accepted iPad coverage
- both broad iPhone and broad iPad coverage

When the user wants broad coverage, look up the current App Store Connect screenshot specifications at the time of the task instead of relying on stale hardcoded assumptions.

As of current public references, export tooling commonly targets large accepted iPhone slots such as 6.9", 6.5", 6.3", and 6.1" because those sizes map cleanly onto a wide portion of the iPhone catalog. Treat that as a useful starting point, not as a permanent rule. Re-check Apple's current specification before batch export.

Apply the same rule to iPad: prefer the largest currently accepted iPad slots when the goal is broad coverage, but verify the current accepted sizes before generating the final matrix.

## Opaque Output Requirement

Final App Store Connect deliverables must be fully opaque.

- Do not ship final screenshots with transparent alpha.
- If a mockup, frame, or exported PNG contains transparency, flatten it onto the approved background before delivery.
- Validate the final batch so the exported files are upload-ready without additional manual cleanup.

## Project-Owned Validation Command

Do not leave final export validation as an ad-hoc manual inspection step.

- Add a project-owned validation command that can be rerun whenever images are regenerated.
- Validate at least dimensions, file format, and opaque output rules.
- Keep the command close to the project so future export refreshes can reuse it without asking the agent to reinvent the check.

Use [assets/validate-exported-images.py](../assets/validate-exported-images.py) as a starting template when the project needs one.

## Why A Preview Layer Matters

The raw simulator screenshots are not the final store deliverables.

The preview layer gives the user a place to review:

- copy hierarchy
- image crops
- device framing
- locale overflow
- background treatment
- final export dimensions

## Proof-First Export Rules

- After any significant design or copy change, regenerate only one locale first.
- Ask the user to approve that example before exporting the full locale and device matrix.
- If the user requests changes, iterate on the proof composition instead of wasting time on full batch exports.

## Batch Export Rules

Only batch export when all of these are true:

- the raw proof captures are approved
- the final preview composition is approved
- the target size strategy has been confirmed
- the final output root is confirmed
- overwrite behavior is confirmed
- the final files will be exported without alpha transparency

## Destination Confirmation

Before writing the final batch, confirm:

- whether output belongs inside the project or at another path
- whether the target directory already contains prior exports
- whether the automation has write permission there
- whether the user wants the final output grouped by locale, device, or store upload slot
- whether the user wants the smallest compliant set or broader iPhone and iPad coverage
- whether the final export path should be committed or added to `.gitignore`

The raw-capture destination should already have been confirmed earlier in the workflow. If it was not, pause and ask before proceeding with batch export so both the source captures and the final upload-ready images have an explicit home and an explicit commit-vs-ignore decision.

## Deliverable Boundary

Keep these layers separate:

- raw captures
- preview or composition source
- final exported store images
- temporary archives, validation previews, or intermediate build artifacts

That separation makes review and cleanup much safer.

## Final Validation Checklist

Before delivery, verify:

- dimensions match the approved App Store Connect slots
- file format is accepted by App Store Connect
- final images are fully opaque with no transparent alpha
- locale and device groupings match the approved export plan
- the validation command itself is stored in the project or otherwise documented as part of the long-term pipeline
