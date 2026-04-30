# Performance Checklist

Apply this checklist to every Apple-platform diff. Skip items that clearly do not apply, but explain the skip in the report when the file's surface area would normally warrant the check.

## SwiftUI Rendering

- New `@State` / `@StateObject` / `@Observable` placement: state hoisted no higher than necessary; avoid invalidating large subtrees on small changes.
- `body` does not allocate expensive objects (formatters, regex, decoders) on every render — hoist to `static let` or `@State`.
- Heavy computation inside `body` is wrapped in a derived value or moved to a model.
- `List` / `LazyVStack` / `LazyHStack` used for unbounded collections; explicit `id:` is stable across renders.
- `.onChange` / `.task(id:)` ids are stable; no closures that recreate identity each render.
- Animations: no implicit animations on rapidly-changing state; `withAnimation` scoped to the transition only.
- Images: vectors or `Image(systemName:)` preferred; bitmap assets sized appropriately; remote images use a cache.

## Concurrency (Swift Concurrency / GCD)

- `Task { ... }` lifetimes are tied to a view or owner; no orphaned tasks, no missing cancellation on disappear.
- `await` calls inside `body` or `View` initializers are avoided — moved into `.task` or a model.
- Main-actor isolation respected: heavy work is off `@MainActor`; UI updates are on it.
- Actors do not serialize hot paths that should be parallel; no nested `await` on the same actor causing implicit reentrancy bugs.
- `Task.detached` only used with explicit justification (escaping isolation).
- No `DispatchQueue.main.async` from already-main-actor code.
- Combine pipelines: `receive(on:)` only where necessary; `.share()` / `.multicast` used to avoid duplicate work.

## Data Layer

- SwiftData / Core Data fetches: `fetchLimit`, predicates, and sort descriptors set; no fetch-all-then-filter in memory.
- Background contexts used for writes that touch many objects; merge policy explicit.
- `@Query` predicates and sort orders avoid recomputing on every view update.
- File / `UserDefaults` / Keychain reads not on the main thread when large or frequent.
- JSON / Plist decoding for large payloads happens off the main actor.

## Networking & I/O

- New URL requests have explicit timeouts and respect background / foreground state.
- Responses are streamed or paginated when payloads can grow.
- Image and asset downloads are deduplicated and cached.
- HealthKit / Core Location / sensors use the lowest-fidelity query that works.

## Widgets, Live Activities, Watch

- Timeline reload policy is appropriate (`.atEnd`, `.after(date:)`, `.never`); no aggressive `.atEnd` for slow-changing content.
- Widget memory budget respected; no large image decoding inside `TimelineProvider`.
- Watch app: `WCSession` messages are batched; no chatty per-tick sync.

## Launch & App Lifecycle

- New work in `App.init`, `@main`, or scene `onAppear` is justified; expensive setup is deferred.
- No new synchronous file I/O on the launch path.
- New dependencies: assess binary-size and dynamic-link impact for app extensions where size budgets are tight.

## Red Flags To Always Surface

- New `Thread.sleep`, busy loops, or polling timers.
- New `try!`, `as!`, force-unwrap on Optional results from I/O or decoding (also a crash-safety issue — note in UX section).
- New `@MainActor` annotations on types whose methods do CPU work.
- New synchronous calls from SwiftUI `body`.
- Removed `cancel()` or removed `Task` cancellation handling.
