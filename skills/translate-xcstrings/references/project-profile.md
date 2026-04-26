# Project Profile Reference

This skill is reusable only if project-specific localization policy is injected instead of hardcoded.

Use a small YAML profile file to describe local policy. A starter template is available at [assets/xcstrings-project-profile.yaml](./assets/xcstrings-project-profile.yaml).

## First-Run Expectation

For a new project, the first serious translation pass should usually establish this file rather than depending on one-off prompts or repository-specific instructions.

If the project already has shipped locales, protected brand wording, English-only strings, or stable domain terminology, explicitly prompt for a profile and capture those decisions there.

The minimum high-value fields to fill are:

- `default_target_locales`
- `supported_platforms`
- `english_only_keys`
- `brand_tokens`
- `glossary`

Without those fields, the skill can still operate conservatively, but it cannot promise project-specific defaults will stay stable across future runs or across different agent clients.

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

### `supported_platforms`

The Apple platforms the app ships on, used when deciding whether action wording may need device variations.

### `brand_tokens`

Literal tokens that must stay untranslated, plus spacing or punctuation rules around them.

### `english_only_keys`

Keys that should remain byte-identical to English in every locale.

### `glossary`

Canonical domain terms keyed by English concept and locale.

### `locale_rules`

Locale-specific overrides, such as punctuation policy, register, or phrase style.

### `variation_policy`

Rules for when to ask before changing catalog structure, especially adding plural or device variations to keys that are currently plain `stringUnit` values.

## Behavior Without A Profile

If no profile exists:

- discover catalogs directly from the repository
- infer locales from existing `localizations` data
- infer supported platforms from visible project targets, manifests, and Info.plist files before suggesting device variations
- preserve any visible established brand tokens literally
- avoid inventing app-specific English-only policies
- explicitly recommend adding a profile if the project has recurring terminology or non-obvious translation policy
- treat that fallback as a temporary bootstrap state, not the ideal steady state for repeated use
