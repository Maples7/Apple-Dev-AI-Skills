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

When a key uses `variations`:

- translate every plural category required by the target locale
- do not collapse multiple categories into one
- do not replace `variations` with a plain `stringUnit`

## Style Matching Rule

Before adding or changing translations in a locale, skim a sample of existing entries in that same locale and match:

- tone
- punctuation
- casing
- sentence shape
- honorific or formality level

The goal is for new strings to feel native to the existing catalog, not machine-added.
