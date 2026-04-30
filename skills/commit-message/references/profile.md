# Commit Profile Reference

Use a commit profile to inject repository-specific commit conventions into the reusable skill.

## Purpose

The profile lets a team define commit conventions without hardcoding one repository's policy into the shared skill.

Typical uses:

- require or forbid commit scopes
- restrict the allowed Conventional Commit types
- choose monorepo scope sources such as package names or app folders
- require issue or ticket footers
- require a body for certain types or change sizes

## Conservative Defaults

If no profile exists, use these defaults:

- `require_scope: false`
- `allowed_types`: all standard Conventional Commit types
- `scope_strategy: optional`
- `required_footers: []`
- `body_policy: auto`

Under this fallback, generate a valid Conventional Commit and mention that no profile was available if the user asked for repository-specific rules.

## Suggested Fields

- `require_scope`: boolean
- `allowed_types`: ordered list of allowed commit types
- `default_type`: optional default when the diff is ambiguous
- `scope_strategy`: `optional`, `required`, `monorepo-package`, `top-level-dir`, or a documented custom rule
- `scope_aliases`: map repository paths or package names to preferred scope labels
- `required_footers`: ordered list of footer prefixes that must be added when evidence exists
- `closing_footer_prefix`: footer prefix to use when a change clearly resolves an issue, such as `Closes` or `Fixes`
- `reference_footer_prefix`: footer prefix to use for non-closing references, such as `Refs`
- `body_policy`: `auto`, `always`, or `types:<list>`
- `split_hint_threshold`: optional hint for when the diff is broad enough to recommend multiple commits

## File Names

Preferred file names:

- `commit-message-profile.yaml`
- `.ai/commit-message-profile.yaml`
- `.github/commit-message-profile.yaml`

## Authoring Guidance

- Keep the profile declarative and repository-specific.
- Prefer stable package or workspace names over ephemeral branch or ticket labels for scopes.
- Only require footers that the repository can reliably infer from branch names, conversation context, or explicit user input.
- If the profile uses custom ticket prefixes or custom scope rules, document them inline in the YAML comments.
