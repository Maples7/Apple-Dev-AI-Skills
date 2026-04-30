---
name: pre-commit-review
description: Review uncommitted Apple-platform changes across seven lenses — performance, user experience, test coverage, architecture, code style, security & privacy, and documentation — and produce a structured report with severity-graded findings before the user runs git commit. Use when the user asks to review a diff before committing, audit pending Swift / SwiftUI / Apple-platform changes for regressions, layering or style drift, security or privacy issues, missing tests, or stale docs.
---

# Pre-Commit Review

Review pending changes in an Apple-platform repository (Swift, SwiftUI, AppKit, UIKit, WatchKit, widgets, intents, SwiftData, etc.) before commit, and return a structured report covering performance, user experience, test coverage, architecture, code style, security & privacy, and documentation.

This skill does not edit code, run tests, or invoke `git commit`. It analyzes the diff and produces a report the user can act on.

## When To Use

- The user asks to review changes before committing.
- The user mentions pre-commit review, change review, perf check, UX check, security check, test coverage check, architecture review, or doc-comment review.
- The user wants a sanity pass on a Swift / SwiftUI change before opening a PR.

## Operating Procedure

1. **Pick a review scope.** Ask the user only if it is unclear:
   - `staged` — `git diff --cached` (default when staged changes exist)
   - `working` — `git diff HEAD` (staged + unstaged)
   - `branch <base>` — `git diff <base>...HEAD` (typically `main` or `develop`)
2. **Collect the diff.**
   - Run `git status` and the appropriate `git diff` for the chosen scope.
   - For broad diffs, start with `git diff --stat` and read full hunks only for files that look risky (UI, async code, data layer, networking, public API, `Info.plist`, entitlements, privacy manifest).
3. **Identify the Apple surface area.** Tag each changed file with at least one surface: `view` (SwiftUI/UIKit/AppKit), `model` (SwiftData/Core Data), `concurrency` (async/await/actors/Tasks), `io` (network/disk/HealthKit/etc.), `widget`, `intent`, `tests`, `assets`, `config`, `entitlements-or-privacy`.
4. **Apply the seven review lenses** in this order:
   1. Performance — see [`references/performance.md`](./references/performance.md)
   2. User experience — see [`references/user-experience.md`](./references/user-experience.md)
   3. Test coverage — see [`references/test-coverage.md`](./references/test-coverage.md)
   4. Architecture — see [`references/architecture.md`](./references/architecture.md)
   5. Code style — see [`references/code-style.md`](./references/code-style.md)
   6. Security & privacy — see [`references/security.md`](./references/security.md)
   7. Documentation & comments — see [`references/docs.md`](./references/docs.md)
5. **Grade each finding** with a severity:
   - `blocker` — likely regression, crash risk, data loss, broken UX, untested critical path, secret leak, or privacy violation. Recommend not committing until addressed.
   - `major` — meaningful risk worth fixing in this commit if cheap, otherwise file a follow-up.
   - `minor` — nit, style, or low-impact improvement.
   - `info` — observation only, no action required.
6. **Produce the report** using the structure in [`references/report-template.md`](./references/report-template.md).
7. **Do not auto-fix.** End with a clear recommendation: `proceed`, `proceed-with-followups`, or `hold`.

## Required Checks

- Use staged scope when staged changes exist; only fall back to working-tree scope when nothing is staged or when the user explicitly asks for it.
- Skim every changed file at least at hunk-summary level before scoring; do not score a file you have not read.
- For SwiftUI views, always check accessibility, Dynamic Type, and main-actor work (UX reference).
- For async / actor / Task code, always check cancellation, priority, and main-actor hops (performance reference).
- For any new public API, type, or user-visible behavior, check whether there is a corresponding test change; if not, raise it as a coverage finding.
- For every changed file, sanity-check layering and module boundaries (architecture reference) and naming / error-handling / DI consistency with the surrounding code (code-style reference); flag drift even when the code works.
- When `Info.plist`, entitlements, `PrivacyInfo.xcprivacy`, network code, persistence code, or anything that looks like a secret or credential changes, always run the security lens (security reference); upgrade severity to `blocker` for plausible secret leaks or ATS regressions.
- For new `public` / `open` API or build/run instruction changes, always run the docs lens (docs reference).
- Never run `git commit`, `git push`, or any mutating command. This skill only reads.
- Never edit source files. Recommendations go in the report only.
- Write the report's prose (finding descriptions, `Why:` and `Fix:` sentences, `Notes`) in the user's current session language. Keep structural anchors in English so the report stays machine- and human-parseable: section headings (`## Pre-Commit Review`, `### Performance`, etc.), field labels (`Scope:`, `Files reviewed:`, `Recommendation:`, `Why:`, `Fix:`, `Suggested test:`), severity tokens (`blocker`, `major`, `minor`, `info`), and recommendation tokens (`proceed`, `proceed-with-followups`, `hold`).

## Out Of Scope

- Drafting the commit message itself — defer to the `commit-message` skill.
- Full architectural review or refactor planning beyond drift-from-existing-style observations.
- Running the test suite or building the project.
- Deep security work: cryptography review, threat modeling, pen-testing. This skill performs surface-level Apple-platform security checks only.

## References

- [`references/performance.md`](./references/performance.md) — Apple-platform performance checklist
- [`references/user-experience.md`](./references/user-experience.md) — SwiftUI / HIG-aligned UX checklist
- [`references/test-coverage.md`](./references/test-coverage.md) — XCTest / Swift Testing coverage checklist
- [`references/architecture.md`](./references/architecture.md) — Layering, abstractions, module boundaries
- [`references/code-style.md`](./references/code-style.md) — Consistency, Swift best practices, readability
- [`references/security.md`](./references/security.md) — Apple-platform security & privacy checklist
- [`references/docs.md`](./references/docs.md) — DocC, in-code comments, project-level docs
- [`references/report-template.md`](./references/report-template.md) — Required report structure
