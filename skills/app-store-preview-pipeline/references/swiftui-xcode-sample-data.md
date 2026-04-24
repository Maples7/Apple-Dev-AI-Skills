# SwiftUI And Xcode Sample Data

Use this reference when the target app is a native Apple app built with Xcode.

The goal is not merely to make screenshots possible once. The goal is to give the project a maintainable sample-data path that future screenshot refreshes can reuse.

## What This Reference Covers

- launch arguments and environment variables for screenshot mode
- app bootstrap patterns in SwiftUI or UIKit lifecycle code
- stable sample-data injection for SwiftData, Core Data, or custom stores
- locale-aware fixture generation
- suppressing unstable UI during screenshot runs
- leaving behind project-owned rerun commands instead of chat-only knowledge

## Design Principles

- screenshot mode should be explicit in project code, and screenshot-only container switching should not be accidentally available in public production builds
- seed generation should be deterministic and safe for public display
- the app should bootstrap into screenshot mode before user-facing UI appears
- sample-data code should live with the project and be easy to update when screens change
- screenshot automation should be able to switch seeds, locales, and routes without source edits

## Release Safety Boundary

Default recommendation: gate screenshot-only seed providers, alternate data containers, and screenshot bootstrap overrides behind `#if DEBUG` or another internal-only compile-time condition.

That prevents a user-shippable production build from switching to screenshot data just because someone passed a launch argument.

If the project truly needs release-like screenshot builds, use a dedicated internal build configuration or compile-time flag for that workflow. Do not let the same public App Store build choose between production and screenshot containers at runtime.

## Recommended Integration Shape

Use four project-owned pieces:

1. A launch-options parser that reads screenshot arguments or environment variables.
2. A screenshot seed provider that can build deterministic app state.
3. An app bootstrap path that installs the screenshot seed before the main UI renders.
4. A documented rerun command that future maintainers can use without reconstructing the workflow.

## Launch Options Pattern

Prefer explicit launch arguments or environment variables so simulator automation can control screenshot mode.

Use [assets/swiftui-xcode-screenshot-config.yaml](../assets/swiftui-xcode-screenshot-config.yaml) as a project template for stable launch flags, seed names, routes, and rerun commands.

Typical options:

```text
-UseScreenshotSampleData
-ScreenshotSeed default
-ScreenshotRoute reports-monthly
-AppleLanguages (de)
-AppleLocale de_DE
SCREENSHOT_MODE=1
```

Keep the option names stable once the project starts depending on them.

## Example: Parse Screenshot Launch Options

```swift
import Foundation

struct ScreenshotLaunchOptions {
    let isEnabled: Bool
    let seedName: String?
    let routeName: String?

    static func current(processInfo: ProcessInfo = .processInfo) -> Self {
        let arguments = processInfo.arguments
        let environment = processInfo.environment

        func value(after flag: String) -> String? {
            guard let index = arguments.firstIndex(of: flag), arguments.indices.contains(index + 1) else {
                return nil
            }
            return arguments[index + 1]
        }

#if DEBUG
        let isEnabled = arguments.contains("-UseScreenshotSampleData") || environment["SCREENSHOT_MODE"] == "1"
#else
        let isEnabled = false
#endif

        return Self(
            isEnabled: isEnabled,
            seedName: value(after: "-ScreenshotSeed"),
            routeName: value(after: "-ScreenshotRoute")
        )
    }
}
```

This keeps simulator automation and app bootstrap speaking the same contract.

## Example: Install Screenshot Data In A SwiftUI App

```swift
import SwiftUI

@main
struct ExampleApp: App {
    private let launchOptions = ScreenshotLaunchOptions.current()
    private let appContainer: AppContainer

    init() {
#if DEBUG
        if launchOptions.isEnabled {
            appContainer = .makeScreenshotContainer(seed: launchOptions.seedName)
        } else {
            appContainer = .makeProductionContainer()
        }
#else
        appContainer = .makeProductionContainer()
#endif
    }

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(appContainer)
        }
    }
}
```

The exact container type depends on the project. The important points are:

- screenshot mode is decided during bootstrap, not after interactive UI has already appeared
- public production builds still resolve to the production container unconditionally
- if the project needs release-like screenshot builds, that should be done with a separate internal build boundary instead of letting a public release choose the screenshot container at runtime

## SwiftData Pattern

For SwiftData-backed apps, prefer one of these:

- an in-memory container for screenshot runs
- a resettable on-disk store that is recreated before each capture run

Good SwiftData screenshot setup usually means:

- seed all models in one place
- avoid network fetches as the source of truth for visible data
- keep IDs, ordering, and list lengths stable
- ensure currency, dates, and localized labels look intentional in each shipped locale
- keep screenshot-only container factories or alternate stores behind an internal compile-time boundary by default

## Core Data Pattern

For Core Data-backed apps, use the same rules:

- a dedicated in-memory persistent store for screenshot mode when possible
- or a resettable sqlite store that automation can delete and recreate
- fixture loading that runs before the first visible screen is rendered
- screenshot-only persistent store switching guarded so public production builds cannot activate it

Avoid relying on leftover simulator state from prior runs.

## Custom Store Or Service Pattern

If the app does not use SwiftData or Core Data, keep the same structure:

- inject a screenshot-safe repository or service implementation
- populate it from fixtures stored with the project
- keep seed variants named and versioned so future UI changes can update them deliberately
- avoid letting a production-shippable build swap to that repository purely from runtime launch flags

## Locale-Aware Fixture Guidance

A screenshot seed should support the app's actual screenshot locales.

Do not stop at translating UI strings. Also think about:

- number and date formatting
- currency and measurement formatting
- text length and truncation behavior
- list density and visual balance
- whether seed content itself should be localized or remain intentionally neutral

If one seed cannot make every locale look good, use named seed variants rather than manual per-locale patching.

## Suppress Unstable UI

During screenshot mode, consider suppressing or stabilizing:

- onboarding interruptions
- review prompts
- permission prompts
- paywall interruptions that are not part of the intended screen
- background sync or live refresh
- transient banners, snackbars, or loading indicators

If a prompt must appear in screenshots, treat it as part of the requested screen plan rather than leaving it to chance.

## Route And Screen Selection

If the app can support it, keep screenshot navigation stable by adding one of these:

- a deep link for important screens
- a bootstrap route name such as `-ScreenshotRoute reports-monthly`
- accessibility identifiers that automation can depend on

This usually scales better than coordinate taps once the app evolves.

Use [native-apple-capture-checklist.md](./native-apple-capture-checklist.md) when turning this sample-data path into a raw capture script for a native Apple project.

## Long-Term Maintenance Checklist

When the project finishes integrating screenshot sample data, future contributors should be able to answer these without reading old chat logs:

- Which launch argument turns screenshot mode on?
- Which seed names exist, and what screens are they for?
- Where is the sample-data code stored?
- Which command regenerates raw captures?
- Which command validates final exports?
- Which prompts or background effects are intentionally suppressed during capture?

If those answers only exist in memory or conversation history, the integration is not finished.

## Suggested Project-Owned Commands

Document concrete commands such as:

```text
make screenshot-seed-check
python3 scripts/generate_screenshots.py --locale en-US --device iphone --proof
python3 scripts/validate_exported_images.py --root app-store-export --allowed-size 1320x2868 --require-opaque
```

The exact command runner can be `make`, `just`, npm scripts, Fastlane, shell scripts, or another project-native tool. The key is that rerun steps live with the project.

## Exit Criteria

- screenshot mode is enabled by a stable, documented contract
- sample data is seeded before visible UI depends on it
- the seed path is deterministic across repeated launches
- routes or identifiers exist for the screens that matter
- future screenshot refreshes can reuse project-owned commands instead of rebuilding the workflow from scratch
