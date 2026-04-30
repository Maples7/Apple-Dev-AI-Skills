# User Experience Checklist

Reviewers should look at the diff through the eyes of the user. Apply Apple Human Interface Guidelines and platform conventions.

## Visible Behavior Changes

- Any user-visible string, label, or button title changed: is the wording clear, localized through `String(localized:)` or `.xcstrings`, and free of developer jargon?
- Any new flow added: does it have a clear entry point, success state, error state, and empty state?
- Destructive actions: confirmation dialog, clear consequence wording, and undo path when possible.
- Modal presentation makes sense (`sheet` vs `fullScreenCover` vs push); dismissal is obvious.

## Accessibility

- New interactive elements have meaningful `accessibilityLabel`, `accessibilityHint` when needed, and group-able traits.
- Tap targets are at least 44×44 pt on iOS, 28×28 pt on watchOS.
- Color is not the only signal (state shown by icon / shape / label too).
- Dynamic Type: text uses semantic styles (`.body`, `.headline`, etc.); custom sizes scale with `@ScaledMetric` or `Font.custom(_:size:relativeTo:)`.
- Reduce Motion respected for non-essential animations; Reduce Transparency respected for materials.
- VoiceOver order is logical for new layouts; decorative images are `accessibilityHidden(true)`.

## Localization

- New user-visible strings are in the string catalog, not hardcoded.
- Pluralization uses `LocalizedStringResource` / `.stringsdict`-style entries when count varies.
- Date, number, and currency formatting uses `Date.FormatStyle`, `Decimal.FormatStyle`, etc., not hand-built strings.
- Right-to-left layouts not broken by hardcoded leading/trailing alignment or fixed-direction icons.

## Platform Conventions & HIG

- Navigation matches platform idioms (NavigationStack with clear titles; toolbars in expected positions).
- System materials and colors used over hardcoded values where appropriate.
- Haptics used sparingly and meaningfully (`SensoryFeedback`); not for routine taps.
- Liquid Glass / system blur used following current iOS / macOS guidance, not as decoration.
- Symbol images use `Image(systemName:)` with current SF Symbols names; rendering modes match content.

## Error & Empty States

- Network or async failures present a user-readable message, not a raw `Error.localizedDescription` from a system error.
- Retry path is offered when the action is retryable.
- Empty states use `ContentUnavailableView` (or platform equivalent) with a primary action when actionable.
- Permission denials route the user toward Settings with an explicit reason string.

## Privacy & Trust

- New permission prompts have a clear `NSXxxUsageDescription` justifying access in user terms.
- Sensitive data (health, location, contacts, photos) is not logged.
- New onboarding screens explain why information is requested before requesting it.

## Cross-Surface Consistency

- Widget / Live Activity / Watch view reflects the same state model and labels as the main app.
- Shortcut / App Intent phrasing matches in-app terminology.
- Notifications use the same wording style and respect Focus / Do Not Disturb where relevant.

## Red Flags To Always Surface

- Hardcoded English strings in user-visible code.
- New screen with no error or empty state path.
- New animation without `accessibilityReduceMotion` consideration.
- Force-unwrap that can crash on a user-driven path.
- Navigation changes that drop deep-link or state-restoration support.
