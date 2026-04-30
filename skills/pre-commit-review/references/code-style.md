# Code Style Checklist

Review the diff against the surrounding code's conventions and Swift / Apple-platform best practices. The goal is consistency and idiomatic code, not enforcing an external style guide.

## Consistency With Existing Code

- Naming follows the surrounding code (e.g., `loadX` vs `fetchX`, `is…` vs `has…`, suffix conventions like `…Store`, `…Service`, `…Repository`).
- File layout, type ordering (properties → init → methods → previews), and `// MARK:` usage match neighbors.
- Error type and propagation style matches the module: domain `enum: Error` + `throws`, or `Result`, or async-throws — pick whichever is already in use, do not mix.
- Logging uses the project's existing logger (`Logger`, `os.Logger`, OSLog category) at the established level; no stray `print(...)`.
- Dependency injection style matches: initializer injection vs `@Environment` vs property wrapper — do not introduce a third pattern.
- New SwiftUI view modifiers and styles use the project's existing `ViewModifier` / `ButtonStyle` / theme tokens, not ad hoc colors and fonts.
- Test naming, fixture style, and `setUp` / `tearDown` patterns match neighboring tests.

## Implementation Best Practices (Swift / Apple Platform)

- Value types preferred for models; reference types only when identity or shared mutable state is required.
- `let` over `var` whenever possible; mutability is local and short-lived.
- Optionals handled with `guard let` / `if let` / `??`; no force-unwrap on values that can change at runtime.
- Errors are typed when the call site cares; not swallowed with `try?` unless the discard is intentional and commented.
- `Sendable` conformance is correct for new types crossing concurrency domains; no `@unchecked Sendable` without justification.
- `Codable` keys, default values, and migration strategy match neighbors; custom `init(from:)` only when needed.
- Date / number / string formatting uses `FormatStyle`, not stringly-typed formatters re-instantiated per call.
- New file is named after its primary type; one primary type per file unless the codebase clearly nests helpers.
- Access control is the minimum needed (`private` > `fileprivate` > `internal` > `public`).

## Readability & Maintainability

- Functions are short and single-purpose; long ones are split at natural seams, not arbitrary cuts.
- Control flow uses early returns and `guard` instead of deep nesting.
- Magic numbers and strings are named constants when reused or non-obvious.
- Boolean parameters at call sites are labeled or replaced with enums for clarity.
- Dead code, commented-out code, and stub `// TODO: implement` are removed.
- Debug-only code (`print`, `dump`, breakpoints) is not committed.

## Change Hygiene

- Diff is focused: no unrelated reformatting, import reordering, or rename sweeps mixed into a feature change.
- Whitespace / line-ending changes are intentional, not editor-induced noise.
- Auto-generated reformatting (SwiftFormat) is applied uniformly, not on a few stray lines.

## Red Flags To Always Surface

- Style drift from the surrounding file (different naming, different error style, different DI style).
- New `print(...)`, `NSLog`, or `fatalError` on a code path the user can hit.
- `// swiftlint:disable` or similar directive added without justification.
- Copy-pasted block from another file with minor edits instead of extracting a shared helper.
- New `try!` / `as!` / force-unwrap on values from I/O, decoding, or user input.
