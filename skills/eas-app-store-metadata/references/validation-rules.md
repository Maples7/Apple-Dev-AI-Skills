# Validation Rules

Validate locally before writing to App Store Connect.

## Mandatory Push Checks

Before `eas metadata:push`, verify all of these:

- EAS project linkage is present
- the intended submit profile is explicit
- the effective `metadataPath` is explicit
- `eas metadata:lint` passes or any warnings are consciously accepted
- the local diff matches the requested scope
- no `.p8` App Store Connect private key lives under the repository tree
- any `ascApiKeyPath` or equivalent secret reference resolves outside the repository
- credentials files and real user-private key paths are not being committed

## Version Alignment

When preparing a new release, make the user-facing version explicit.

Verify that:

- the App Store metadata version target matches the native version source the project uses
- release notes correspond to the same version being prepared
- the App Store Connect draft version state matches what the metadata push expects

Do not hide version drift behind a metadata-only patch.

## Locale Coverage

- If the project ships multiple locales, confirm which locales are in scope.
- When the task is “prepare a new release,” update release notes for every shipped locale unless the project says otherwise.
- Do not silently leave shipped locales stale if the user asked for a broad release-preparation pass.

## Screenshot Path Checks

- Keep screenshot paths relative to the repository root.
- Confirm that each referenced path exists before push.
- Keep screenshot roots consistent with repository policy.
- Do not swap large screenshot trees casually without calling it out in the summary.

## App Store Field Limits

Use these field limits during review:

- Title: 30 characters
- Subtitle: 30 characters
- Keywords: 100 characters total
- Promo Text: 170 characters
- Description: 4000 characters
- Release Notes: 4000 characters

## Keyword Rules

When reviewing keywords:

- do not duplicate terms already present in title or subtitle
- avoid generic terms such as app, game, free, best, or new
- avoid competitor or trademarked names
- prefer compact comma-separated values with no spaces after commas when using string form

These checks come from standard App Store ASO constraints and should be applied conservatively.

## Dashboard Drift Rule

If metadata was edited in the App Store Connect web UI since the last local sync, run `eas metadata:pull` first.

Do not validate or push against stale local state and assume it is safe.

## Dynamic Metadata Rule

If `metadataPath` points to a dynamic store-config file such as `store.config.js`:

- confirm the dynamic inputs are reproducible
- avoid depending on hidden machine-local values
- make sure validation still reflects the generated result, not only the template inputs
