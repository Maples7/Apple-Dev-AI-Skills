# Pre-Commit Review

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Review uncommitted Apple-platform changes (Swift / SwiftUI / AppKit / UIKit / WatchKit / widgets / intents / SwiftData) and return a structured report covering performance, user experience, test coverage, architecture, code style, security & privacy, and documentation. Do not edit code, run tests, or invoke `git commit`.

## Operating Rules

1. Pick a review scope and confirm with the user only if unclear:
   - `staged` — `git diff --cached` (default when staged changes exist)
   - `working` — `git diff HEAD`
   - `branch <base>` — `git diff <base>...HEAD`
2. Run `git status` and the appropriate `git diff`. For broad diffs, start with `git diff --stat` and read full hunks only for risky files (UI, async, data, networking, public API, `Info.plist`, entitlements, privacy manifest).
3. Tag each changed file with at least one Apple surface: `view`, `model`, `concurrency`, `io`, `widget`, `intent`, `tests`, `assets`, `config`, `entitlements-or-privacy`.
4. Apply seven review lenses in order: performance → user experience → test coverage → architecture → code style → security & privacy → documentation.
5. Grade each finding `blocker`, `major`, `minor`, or `info`.
6. Output exactly the structure in `references/report-template.md` and end with a `Recommendation` line: `proceed`, `proceed-with-followups`, or `hold`.

## Required Checks

- Use staged scope when staged changes exist; only fall back to working-tree scope when nothing is staged or the user asks for it.
- Skim every changed file at hunk-summary level before scoring; never score a file you have not read.
- For SwiftUI views, always check accessibility, Dynamic Type, and main-actor work.
- For async / actor / Task code, always check cancellation, priority, and main-actor hops.
- For new public APIs or user-visible behavior, flag missing test coverage as a finding.
- For every changed file, check layering and module boundaries (architecture) and naming / error-handling / DI style consistency (code style); flag drift even when the code works.
- When `Info.plist`, entitlements, `PrivacyInfo.xcprivacy`, network code, persistence code, or anything that looks like a secret changes, always run the security lens; upgrade severity to `blocker` for plausible secret leaks or ATS regressions.
- For new `public` / `open` API or build/run instruction changes, always run the documentation lens.
- Do not run `git commit`, `git push`, or any mutating command.
- Do not edit source files. Recommendations go in the report only.

## Out Of Scope

- Drafting the commit message (use the `commit-message` skill).
- Architectural review or refactor planning beyond drift-from-existing-style observations.
- Running the test suite or building the project.
- Deep security work: cryptography review, threat modeling, pen-testing.

## Canonical Source

The full reusable skill lives under [`skills/pre-commit-review/`](../../skills/pre-commit-review/).

Read these files when the wrapper alone is not enough:

- [`skills/pre-commit-review/SKILL.md`](../../skills/pre-commit-review/SKILL.md)
- [`skills/pre-commit-review/references/performance.md`](../../skills/pre-commit-review/references/performance.md)
- [`skills/pre-commit-review/references/user-experience.md`](../../skills/pre-commit-review/references/user-experience.md)
- [`skills/pre-commit-review/references/test-coverage.md`](../../skills/pre-commit-review/references/test-coverage.md)
- [`skills/pre-commit-review/references/architecture.md`](../../skills/pre-commit-review/references/architecture.md)
- [`skills/pre-commit-review/references/code-style.md`](../../skills/pre-commit-review/references/code-style.md)
- [`skills/pre-commit-review/references/security.md`](../../skills/pre-commit-review/references/security.md)
- [`skills/pre-commit-review/references/docs.md`](../../skills/pre-commit-review/references/docs.md)
- [`skills/pre-commit-review/references/report-template.md`](../../skills/pre-commit-review/references/report-template.md)
