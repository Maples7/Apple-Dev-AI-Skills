# Project Profile Reference

This skill is reusable only if project-specific localization policy is injected instead of hardcoded.

Use a small YAML profile file to describe local policy. A starter template is available at [assets/xcstrings-project-profile.yaml](./assets/xcstrings-project-profile.yaml).

## Recommended File Names

The skill should look for the first matching file in this order:

1. `./xcstrings-project-profile.yaml`
2. `./.ai/xcstrings-project-profile.yaml`
3. `./.github/xcstrings-project-profile.yaml`
4. a user-specified path

## Recommended Fields

### `catalogs`

Optional explicit catalog paths or discovery hints.

### `default_target_locales`

The project's shipped locales when the user asks for a broad translation pass without naming languages.

### `brand_tokens`

Literal tokens that must stay untranslated, plus spacing or punctuation rules around them.

### `english_only_keys`

Keys that should remain byte-identical to English in every locale.

### `glossary`

Canonical domain terms keyed by English concept and locale.

### `locale_rules`

Locale-specific overrides, such as punctuation policy, register, or phrase style.

## Behavior Without A Profile

If no profile exists:

- discover catalogs directly from the repository
- infer locales from existing `localizations` data
- preserve any visible established brand tokens literally
- avoid inventing app-specific English-only policies
- recommend adding a profile if the project has recurring terminology or non-obvious translation policy
