# Troubleshooting

Use these checks when EAS metadata commands fail or when the repository state and App Store Connect drift apart.

## Project Is Not Linked To EAS

Common symptoms:

- metadata commands do not resolve the current project correctly
- `extra.eas.projectId` is missing from app config
- the project was never initialized for EAS services

What to do:

- run `eas init` or `eas project:init`
- verify the expected app config now contains `extra.eas.projectId`
- if the project belongs to a different Expo account or organization, make that ownership explicit before continuing

## Expo Authentication Blocks Automation

Common symptoms:

- `eas login` is required
- SSO or 2FA prompts interrupt non-interactive execution
- the user is not in the correct Expo account or organization

What to do:

- log in with the correct Expo account or set `EXPO_TOKEN` when appropriate
- hand off the login step when the agent cannot complete the required interactive authentication safely
- resume the metadata flow only after authentication is confirmed

## Private Key Lives Inside The Repository

Common symptoms:

- `ascApiKeyPath` points to `./credentials/...` or another path under the checkout
- the team relies on `.gitignore` instead of a real secret boundary

What to do:

- move the `.p8` file to a user-private local directory outside the repository
- recommended best default on macOS: a per-user private Application Support directory outside the checkout
- update only the untracked local config or environment variable that references that key
- if the key was ever committed or shared, rotate it instead of assuming deletion is enough

## App Does Not Exist On App Store Connect Yet

Common symptoms:

- `eas metadata:pull` cannot bootstrap a local config because there is no existing app listing

What to do:

- start from a new local store-config template instead of expecting pull to generate it
- make app creation or first-submission prerequisites explicit in the release handoff

## Push Fails Because No Target Draft Exists

Common symptoms:

- metadata push expects a version draft or processed binary state that is not ready yet

What to do:

- create the target App Store Connect version draft first if the project requires it
- make sure the binary upload and processing state matches the release step you are attempting
- retry the metadata push only after the listing state is ready

## Partial Metadata Upload

Common symptoms:

- some locales or screenshots upload while others fail

What to do:

- review the exact failing fields or assets
- correct the local source of truth
- rerun lint and push intentionally instead of assuming the partial result is acceptable

## Dashboard Drift After Manual UI Edits

Common symptoms:

- the App Store Connect web UI and local files disagree
- a fresh push would overwrite recent manual edits

What to do:

- pull first with `eas metadata:pull`
- review the diff
- only then make new local edits and push again

## Screenshot Paths Or Locale Assets Fail

Common symptoms:

- screenshot upload fails for one locale or one device family
- relative paths in metadata do not exist locally

What to do:

- verify file existence from the repository root
- confirm the locale and device directory layout matches the metadata references
- keep path conventions consistent instead of patching one path at a time without a policy
