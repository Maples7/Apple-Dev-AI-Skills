# Native Apple Capture Checklist

Use this checklist when turning a native Apple app's screenshot sample-data path into a reusable raw capture script.

The goal is not just to capture one set of screenshots. The goal is to leave the project with a repeatable path from deterministic app state to proof captures and then to full export.

## 1. Screenshot Mode Contract Exists

Before writing the raw capture script, confirm that the app already exposes a stable screenshot mode.

- a documented enable flag or environment variable exists
- seed names are explicit and stable
- optional route names are explicit and stable
- the app can be launched into screenshot mode without manual tapping first

If any of those are missing, finish the sample-data integration before automating capture.

## 2. Seed Data Is Deterministic

Confirm that repeated launches produce the same visible state.

- the same seed produces the same records, ordering, balances, dates, or chart shape
- the seed does not depend on leftover simulator data
- screenshot mode can start from a clean simulator and still render the target screen
- locale-sensitive values still look intentional in the supported screenshot locales

## 3. Unstable UI Is Suppressed Or Controlled

Before writing navigation code, make sure unstable UI is handled deliberately.

- first-run flows are skipped or scripted
- review prompts are disabled unless intentionally shown
- permission prompts are disabled or made deterministic
- sync and background refresh do not randomly change the visible state
- loading spinners, toasts, and transient banners are not left to chance

## 4. Screen Entry Is Stable

The raw capture script needs a dependable way to reach each requested screen.

Prefer this order:

1. launch route or deep link
2. existing UI tests or accessibility identifiers
3. accessibility tree queries by stable labels or identifiers
4. coordinate taps only as a last resort

If the app still requires fragile coordinate-only navigation, prefer adding stable identifiers or routes before scaling the pipeline.

## 5. Simulator Inputs Are Scriptable

Verify that the capture script can control the required simulator state from the command line.

- locale can be passed through launch arguments or script input
- appearance can be chosen intentionally
- target simulator and device family can be selected non-interactively
- any required status bar stabilization can be applied consistently

## 6. The Capture Script Has A Small Proof Mode

Do not jump straight to the full locale and device matrix.

The script should support a proof mode that can run:

- one locale
- one device
- one or a few screens
- one appearance when that is enough for review

The project should have a documented proof command that future maintainers can rerun quickly.

## 7. Output Naming Is Stable

Before batch capture, agree on a stable raw capture layout.

Recommended shape:

```text
app-store-assets/raw/{device}/{locale}/{screen}.png
```

The exact root can vary, but keep these rules:

- locale and device names are explicit in the path
- file names describe the screen intent, not temporary human notes
- raw captures are separate from review proofs and final exports

## 8. The Script Fails Early

A reusable capture script should refuse to run in obviously broken states.

Preflight checks should verify at least:

- simulator exists
- app is installed
- screenshot mode is reachable
- output directory is writable
- required tools are installed

Failing early is better than silently generating an incomplete screenshot set.

## 9. Project-Owned Rerun Commands Exist

When the checklist is complete, the project should own commands such as:

```text
make screenshot-proof
make screenshot-batch
python3 scripts/validate_exported_images.py --root app-store-export --require-opaque
```

The command runner can vary. What matters is that regeneration does not depend on remembered chat instructions.

## 10. Ready For Raw Capture Automation

You are ready to scale from sample data into a reusable raw capture script when all of these are true:

- screenshot mode is deterministic
- routes or identifiers exist for target screens
- proof mode can run quickly
- output naming is stable
- the project owns rerun commands for proof, batch, and validation

At that point, write or refine the raw capture script itself.
