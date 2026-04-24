# Project Profile Reference

This skill stays reusable only if project-specific release policy and file layout are injected instead of hardcoded.

Use a small YAML profile file to describe local policy. A starter template is available at [assets/eas-app-store-metadata-project-profile.yaml](../assets/eas-app-store-metadata-project-profile.yaml).

## First-Run Expectation

For a new project, the first serious metadata pass should usually establish this file rather than depending on one-off prompts or repository-specific instructions.

At minimum, fill these high-value fields:

- `submit_profile`
- `metadata_path`
- `shipped_locales`
- `native_version.source`
- `release.require_new_asc_draft_before_push`

Without those fields, the skill can still operate conservatively, but it cannot promise stable defaults across future runs or across different agent clients.

## Recommended File Names

The skill should look for the first matching file in this order:

1. `./eas-app-store-metadata-project-profile.yaml`
2. `./.ai/eas-app-store-metadata-project-profile.yaml`
3. `./.github/eas-app-store-metadata-project-profile.yaml`
4. a user-specified path

## Recommended Fields

### `submit_profile`

The default EAS submit profile to use for metadata commands. In many projects this is `production`.

### `metadata_path`

The effective metadata file path. This may be a static `store.config.json` or a dynamic `store.config.js`.

### `app_config_paths`

Explicit app-config files to inspect when checking `extra.eas.projectId` or version metadata.

### `eas_project`

Linkage expectations such as whether linkage is mandatory and which config path usually carries the project ID.

### `native_version`

The source of truth for the user-facing app version, for example Xcode `MARKETING_VERSION`, Expo config `expo.version`, or another documented native path.

### `shipped_locales`

The locales the project actually ships. Use this to decide whether release-note or screenshot updates must touch every locale.

### `metadata.protected_fields`

Fields that should not be casually rewritten without explicit user intent, such as support or privacy URLs.

### `metadata.review_fields`

The highest-sensitivity fields to mention in summaries and review steps, such as title, subtitle, keywords, promo text, release notes, and screenshots.

### `screenshots.roots`

Allowed relative roots for screenshot assets referenced from the store config.

### `release.require_new_asc_draft_before_push`

Whether the project expects a fresh App Store Connect version draft before metadata push.

### `release.update_release_notes_for_all_locales`

Whether release-note updates are required for every shipped locale when preparing a new version.

### `credentials`

Repository policy for whether a shared `eas.json` exists, where untracked local credential overrides live, and how App Store Connect API key paths should be described without committing secrets.

For this skill, the App Store Connect `.p8` file should be treated as outside-repo secret material:

- never store it under the project tree, even in a gitignored folder
- recommended best default on macOS: a per-user private Application Support directory outside the checkout
- commit only policy and placeholder values, not the real local key path

#### Minimal Local Reference Pattern

Keep the real key path in untracked local configuration, not in tracked project files.

Recommended macOS path pattern:

```text
$HOME/Library/Application Support/eas/credentials/<apple-team-id>/AuthKey_<key-id>.p8
```

Minimal local environment example:

```sh
export ASC_API_KEY_PATH="$HOME/Library/Application Support/eas/credentials/<apple-team-id>/AuthKey_<key-id>.p8"
```

Use that variable only from untracked local shell config, direnv, or another local-only runner setup. Tracked files should keep placeholder text or documented policy only.

If a project generates local submit config from templates, resolve `ASC_API_KEY_PATH` into the final local-only config at generation time rather than committing the resolved absolute path.

## Behavior Without A Profile

If no profile exists:

- inspect app config directly for EAS linkage
- assume `production` as the default profile only when the repository already uses that convention
- assume `store.config.json` at the repository root unless `metadataPath` says otherwise
- avoid inventing project-specific locale or version policy
- explicitly recommend adding a profile when the project ships more than one locale or has a non-trivial release process
