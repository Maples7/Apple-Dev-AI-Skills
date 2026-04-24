# Editing Safety

## Preserve Xcode Formatting

`.xcstrings` files are JSON, but their on-disk formatting is effectively part of the workflow because Xcode emits a stable style.

Preserve:

- key order
- indentation
- spacing around `:`
- trailing newline
- unrelated metadata and locales

Avoid whole-file rewrites through generic JSON formatters unless the user explicitly wants that tradeoff.

## Prefer Surgical Edits

When possible:

- inspect with `jq`, Python, or other read-only tools
- write only the keys being changed
- avoid reserializing the entire document

If the resulting diff is much larger than the intended change surface, treat that as a failed write strategy.

## Long Runs Must Be Batched

Large translation requests are fragile if handled as one giant response.

Default batching rules:

- around 20 to 30 short keys per batch for one locale
- smaller batches for long strings, multiple locales, or many plural variants
- contiguous key ranges so it is obvious what has been completed

Before batch 1:

- lock glossary terms
- lock brand-token policy
- lock English-only key policy

Then keep those stable across all later batches.

## Do Not Leak Project-Specific Rules Into the Shared Skill

These belong in the project profile, not in the shared skill body:

- brand names
- shipped-language defaults
- app-specific English-only keys
- domain glossary terms
- app-specific punctuation or tone exceptions

If you discover one of these while working, add it to the project profile contract instead of hardcoding it into the shared workflow.

## Recommended Validation Mindset

After editing:

- confirm the file still parses
- confirm changed keys still have the expected structure
- confirm placeholders and Markdown survived intact
- confirm `AppShortcuts` entries still contain the token `${applicationName}`
- confirm the diff size roughly matches the requested scope
