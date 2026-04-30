# Test Coverage Checklist

Goal: confirm the diff's behavior change is observable from a test, and flag gaps with a recommended test name and target framework.

## Detect The Test Stack

- XCTest target(s): `*Tests/`, files importing `XCTest`.
- Swift Testing: files importing `Testing`, using `@Test` and `#expect`.
- UI tests: targets importing `XCUITest` or `XCTest` with `XCUIApplication`.
- Snapshot / screenshot tests: look for snapshot libraries or recorded fixtures.

Use whichever framework already exists in the changed module; do not propose introducing a new framework.

## Coverage Questions Per Changed Surface

### Models / Pure Logic
- Is there a test that exercises the new branch, edge case, or error path?
- Are boundary inputs (empty, max, negative, unicode, very long) covered?
- For new `Decodable` types: a fixture-based round-trip test exists.

### View Models / `@Observable` / Stores
- A test drives the view model through the new state transition.
- Async paths are awaited and asserted, not fire-and-forget.
- Errors surfaced to the UI are asserted as a specific case, not just `XCTAssertNotNil`.

### SwiftUI Views
- If the view encodes non-trivial logic, prefer testing the underlying view model.
- For visual changes, a snapshot test or preview-based assertion is updated.
- Accessibility identifiers added in the diff are referenced from a UI test or are clearly reserved for future tests.

### Persistence
- New SwiftData / Core Data migrations have a migration test.
- New queries / predicates have a test that inserts known data and asserts the result.

### Concurrency
- Cancellation behavior is tested where the diff introduces a new long-running `Task`.
- Actor reentrancy or ordering is tested when the diff relies on a specific order.

### App Intents / Shortcuts
- Each new `AppIntent.perform` path has at least one happy-path test.
- Parameter resolution (entity queries, disambiguation) is tested.

### Widgets / Live Activities
- Timeline provider produces the expected entries for representative dates / states.

## What Counts As "Covered Enough"

- Every new public function or `@Test`-able entry point has at least one assertion that would fail if the function returned a stub value.
- Every new branch (`if`, `switch case`, `guard else`) on a non-trivial code path has at least one test exercising it.
- Every new bug fix has a regression test that fails without the fix.
- Pure UI styling changes do not require tests, but call this out explicitly in the report.

## Common Gaps To Surface

- Code change with zero file changes under any test target — usually a `blocker` for non-trivial logic, `info` for pure styling.
- New error type added with no test asserting it is thrown.
- New `async throws` function with only happy-path coverage.
- Behavior change inside an existing test's subject without the test being updated (silent semantic drift).
- New `@MainActor` boundary that breaks an existing test's assumption (look for tests that may now hang or fail).

## Recommendation Format

For each gap, propose:

- The target framework (XCTest or Swift Testing) — match the existing tests in that module.
- A suggested test name in the project's style (`test_<unitOfWork>_<scenario>_<expected>` for XCTest; `@Test func <unitOfWork>_<scenario>()` for Swift Testing).
- The minimal arrange-act-assert it should perform.

Do not write the test in this skill — propose only.
