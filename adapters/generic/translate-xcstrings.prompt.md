# Translate xcstrings

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Translate or normalize Xcode `.xcstrings` catalogs, including `Localizable.xcstrings`, `InfoPlist.xcstrings`, and `AppShortcuts.xcstrings`.

## Operating Rules

1. Before translating, look for a project profile at `xcstrings-project-profile.yaml`, `.ai/xcstrings-project-profile.yaml`, or `.github/xcstrings-project-profile.yaml`.
2. If no project profile exists, discover the `.xcstrings` files and current locales directly from the repository before making assumptions.
3. Preserve placeholders, Markdown, literal tokens, and Xcode JSON formatting.
4. Treat `AppShortcuts.xcstrings` as `stringSet` phrase arrays, not normal single strings.
5. Keep terminology consistent within each locale and across all catalogs touched in the same pass.
6. Split large runs into small batches and write each batch back before starting the next one.

## Required Checks

- enumerate in-scope catalogs before translating
- enumerate existing locales and missing locales before translating
- build or reuse a glossary when adding a new locale or normalizing inconsistent terms
- keep `${applicationName}` verbatim in shortcut phrases
- keep Chinese punctuation full-width near CJK text unless inside preserved tokens
- summarize touched catalogs, locales, and terminology decisions at the end

## Canonical Source

The full reusable skill lives under [`skills/translate-xcstrings/`](../../skills/translate-xcstrings/).

Read these files when the wrapper alone is not enough:

- [`skills/translate-xcstrings/SKILL.md`](../../skills/translate-xcstrings/SKILL.md)
- [`skills/translate-xcstrings/references/workflow.md`](../../skills/translate-xcstrings/references/workflow.md)
- [`skills/translate-xcstrings/references/catalog-rules.md`](../../skills/translate-xcstrings/references/catalog-rules.md)
- [`skills/translate-xcstrings/references/editing-safety.md`](../../skills/translate-xcstrings/references/editing-safety.md)
- [`skills/translate-xcstrings/references/project-profile.md`](../../skills/translate-xcstrings/references/project-profile.md)
