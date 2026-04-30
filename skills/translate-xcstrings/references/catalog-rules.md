# Catalog Rules

These rules are Apple-specific and should apply across projects unless a project profile adds narrower policy.

## Catalog Types

### Localizable.xcstrings

The main user-facing string catalog. Most keys store a single `stringUnit`, but some use `variations`.

### InfoPlist.xcstrings

Carries user-visible system strings such as:

- app display name variants
- permission usage descriptions
- App Intent titles and system-exposed phrases

It is easy to skip because it is usually smaller. Do not skip it in a full translation pass.

### AppShortcuts.xcstrings

Stores voice-oriented phrases exposed through Siri, Spotlight, Action Button integration, and the Shortcuts app.

Every localization here uses a `stringSet` under `values`, not a single `stringUnit`.

## Placeholder Rules

Preserve placeholders verbatim:

- `%@`
- `%lld`
- `%d`
- `%1$@`
- `%2$lld`
- `%.2f`

Do not translate, quote, or drop them. Only switch to positional placeholders when word order genuinely requires it.

## No-Op Translation Rule

Some keys contain only placeholders, punctuation, symbols, or other non-translatable tokens. Examples:

- `%@`
- `%@ (%@)`
- `%@%@`
- `+%@`
- `-%@`
- `"%@"`
- `.`
- `-`

Do not skip these keys. Write the source string verbatim into every target locale so the catalog state moves from `NEW` to translated. Skipping them leaves persistent `NEW` rows in Xcode, drags down the per-locale completion percentage, and can stall release / screenshot pipelines that gate on full translation.

A key qualifies for no-op translation when, after stripping placeholders and Markdown / formatting tokens, no human-readable text remains. If any natural-language fragment is present (even a single word like `at` in `%@ at %@`), translate normally instead.

## Markdown and Formatting Rules

Preserve these verbatim:

- `**bold**`
- `*italic*`
- `` `code` ``
- `[text](url)` link targets
- `\n`
- list markers
- leading and trailing whitespace

Translate only the human-readable text portions.

## Literal Token Rules

Do not translate:

- URLs
- file paths
- email addresses
- code identifiers
- SF Symbol names
- `${applicationName}` in `AppShortcuts.xcstrings`

## AppShortcuts Rules

For each localized shortcut phrase set:

- keep `${applicationName}` verbatim
- produce natural spoken commands, not stiff literal translations
- keep roughly the same phrase count as English unless the project profile states otherwise
- reuse the same domain terminology as the rest of the catalog
- avoid trailing punctuation unless it is clearly idiomatic in that locale

## Chinese Defaults

For `zh-Hans` and `zh-Hant`, use full-width punctuation when it appears next to CJK text:

- `，`
- `。`
- `；`
- `：`
- `！`
- `？`
- `（）`
- `「」`
- `『』`
- `、`

Keep ASCII punctuation only inside preserved tokens, code-like syntax, Markdown, URLs, and placeholders.

## Plurals and Variations

When a key already uses `variations`:

- translate every plural category required by the target locale
- do not collapse multiple categories into one
- do not replace `variations` with a plain `stringUnit`

When a key is still a plain `stringUnit` but appears to need variants, treat that as a structure-change candidate rather than a routine translation edit.

Plural variation candidates include strings where:

- a count placeholder or explicit number controls noun form or sentence shape
- the English source has singular/plural forms such as `1 transaction` and `2 transactions`
- target locales need different grammar for one, few, many, or other locale-specific plural categories

For these candidates, ask the user whether to add plural variations before changing the catalog structure.

Device variation candidates include strings where an action, control, or interaction verb should differ by platform. Before suggesting device variations, determine the project's supported platforms from the project profile, package or project targets, Info.plist files, or the user's stated scope. For example, macOS wording may need `click`, while touch platforms may need `tap`.

For these candidates, ask the user whether to add device variations before changing the catalog structure. If the user declines, use a natural platform-neutral wording only when one is available.

When adding new variations after user confirmation:

- use Xcode-supported variation axes and category names
- preserve any existing variant categories exactly as Xcode emitted them
- keep placeholders, Markdown, and literal tokens identical across variants unless grammar requires positional placeholder changes

## Style Matching Rule

Before adding or changing translations in a locale, skim a sample of existing entries in that same locale and match:

- tone
- punctuation
- casing
- sentence shape
- honorific or formality level

The goal is for new strings to feel native to the existing catalog, not machine-added.
