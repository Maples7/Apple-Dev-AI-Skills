# xcstrings Translation Workflow

This workflow is the reusable core of the skill. It should work for any Apple app that uses Xcode string catalogs.

## 1. Resolve Scope First

Before translating anything, pin down:

- which catalogs are in scope
- which locales are in scope
- whether the request is additive, corrective, or a terminology review
- whether the user asked for one language, all shipped languages, or a brand-new locale

If the user did not specify scope, discover all `.xcstrings` files and enumerate existing localizations before choosing a default target set.

## 2. Load Project Policy Before Making Term Decisions

If a project profile exists, read it before translating.

Project policy should override generic defaults for:

- shipped-language set
- brand token handling
- English-only keys
- preferred glossary terms
- locale-specific style rules

If no profile exists, infer only what is visible in the catalog files and keep assumptions conservative.

## 3. Discover All Relevant Catalogs

Do not assume there is only one catalog.

At minimum, check whether the project includes any of these:

- `Localizable.xcstrings`
- `InfoPlist.xcstrings`
- `AppShortcuts.xcstrings`

If the user asks for a complete translation pass, cover every catalog that exists in the project, not just the first one you find.

## 4. Enumerate Languages and Missing Entries

Use the catalogs as the source of truth.

For each in-scope key:

- list which locales already exist
- list which locales are missing
- identify stale or inconsistent translations
- note whether the value is a `stringUnit`, `variations`, or `stringSet`

Do not start writing translations until the missing-work surface is clear.

## 5. Build or Reuse a Glossary

When adding a new language or normalizing inconsistent terminology:

- scan existing translations in that locale
- extract recurring domain terms
- choose one canonical translation for each term
- reuse those terms consistently across all catalogs in scope

If a project profile already defines a glossary, treat it as the starting point.

## 6. Translate by Catalog Structure

Apply the correct structure per key type:

- `stringUnit` for normal single-string values
- `variations` for plural or device/category variants
- `stringSet` for `AppShortcuts.xcstrings` phrase arrays

Do not flatten one structure into another.

## 7. Write Edits Surgically

Keep the on-disk Xcode formatting intact.

- preserve key order
- preserve unrelated locales and metadata
- preserve spacing around `:` and surrounding JSON layout
- change only the localization entries in scope

If the diff looks far larger than the number of intended keys, stop and redo the write more surgically.

## 8. Batch Long Runs

If the translation run is large enough to risk truncation:

- lock terminology decisions before batch 1
- split the work into contiguous key ranges
- write each batch back to disk immediately
- report what was completed and what remains

Never leave a long run only in scratch state.

## 9. Finish With a Useful Summary

Summarize:

- catalogs touched
- locales touched
- key counts added or updated per catalog
- terminology or style decisions worth remembering
- whether a project profile should be added or updated
