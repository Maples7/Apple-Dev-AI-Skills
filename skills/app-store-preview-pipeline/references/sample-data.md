# Sample Data

Good App Store screenshot automation depends on a deterministic simulator state.

## Requirements

The screenshot data path should be:

- stable across repeated launches
- safe to show publicly
- representative of the app's real value
- fast to initialize on a clean simulator
- compatible with the locales the user plans to ship
- isolated from real user data and cloud state

## Preferred Contract

Prefer a dedicated screenshot or sample-data mode that can be enabled from automation.

Default recommendation: keep screenshot-only container wiring, fixture seeding, and test-data-only bootstrap paths behind `#if DEBUG` or another internal-only compile-time guard.

If the project intentionally captures screenshots from a release-like build, do not rely on a user-shippable production build switching containers purely from launch arguments. Use a dedicated internal build configuration or compile-time flag so public production builds cannot boot into screenshot data by accident.

Typical inputs are:

```text
-UseScreenshotSampleData
-ScreenshotSeed default
-AppleLanguages (ja)
-AppleLocale ja_JP
```

Environment variables are also acceptable when the project already uses them.

For native Apple apps built with Xcode, SwiftUI, UIKit, SwiftData, or Core Data, use [swiftui-xcode-sample-data.md](./swiftui-xcode-sample-data.md) for a project-owned integration pattern.

## Good Patterns

- dedicated in-memory or resettable local store
- seed fixtures stored with the project
- launch arguments that enable screenshot mode without recompiling
- screenshot-only container switching gated by `#if DEBUG` or another internal build guard by default
- locale-aware fixture generation so copy, currency, dates, and list length still look intentional
- a way to disable background sync, alerts, or first-run interruptions during capture

## Fallback Order When No Stable Data Exists

1. Reuse an existing preview or demo mode.
2. Reuse an existing importer or fixture loader and make it automation-friendly.
3. Add a dedicated screenshot seed mode guarded by launch arguments or environment.
4. As a last resort, help the user create a deterministic setup script that builds the required state in the simulator before each capture run.

## Questions To Ask When The Project Has No Screenshot Data Path

- Do you already have demo, preview, onboarding, or QA seed data?
- Should screenshot mode use an in-memory store, a local fixture database, or a setup script?
- Which locales must render correctly from the same seed?
- Which notifications, paywalls, sync flows, or permission prompts must be suppressed?
- Does the user want screenshot mode shipped only in debug builds, or hidden behind a non-public launch flag in release-like builds too?

## Definition Of Done

- launching the app into screenshot mode does not require manual setup
- the same seed produces the same visible state across repeated runs
- localized screens render without obviously empty or broken content
- automation can switch screenshot mode on and off without editing source code each time

