# Architecture Checklist

Review the diff at the structural level: where new code lives, how it talks to existing code, and whether new abstractions earn their keep.

## Layering & Boundaries

- New code lives in the right layer (View / ViewModel / Model / Service / Repository / Persistence) for this codebase. View code does not reach into persistence directly when a service or store layer exists.
- Cross-layer dependencies flow in one direction; lower layers do not import higher ones.
- Feature modules / Swift packages do not gain new dependencies on sibling features that previously stayed isolated.
- Shared types are placed in the lowest module that needs them, not duplicated.
- `@MainActor` / `nonisolated` boundaries match the existing layering convention; new types do not silently become `@MainActor` just to compile.
- New SwiftUI views do not own business logic that belongs in a view model / store; new view models do not own UI types.

## Abstractions

- New abstraction (protocol, generic, type-erasing wrapper) earns its keep — at least two real call sites, or a clear seam for testing / mocking.
- Existing abstraction is extended instead of being shadowed by a parallel one with a similar name.
- No premature generics: a single concrete type would have been clearer.
- No "manager" / "helper" / "utility" grab-bag types added when an existing domain type could own the behavior.
- Public API surface is the minimum needed; internal helpers stay `private` / `fileprivate` / `internal`.
- Protocol additions have a default implementation only when most conformers genuinely share that behavior.

## Module & Dependency Hygiene

- New external dependency (SwiftPM, CocoaPods) is justified, actively maintained, and licensed compatibly; no duplicate of a dependency the project already has.
- Generated files (`project.pbxproj`, `Package.resolved`) only change when the change demands it.
- New files are added to the correct target(s) only — no accidental inclusion in test or extension targets, no missing inclusion in app targets.

## Red Flags To Always Surface

- New God-type / huge view / huge view model that violates existing decomposition.
- New cross-layer reach (View calling persistence, Model importing UI framework).
- New singleton (`static let shared`) where a passed dependency would do.
- New protocol with one conformer added "for testability" without an actual test using a fake.
- Feature code reaching across to another feature's internals instead of going through a shared abstraction.
