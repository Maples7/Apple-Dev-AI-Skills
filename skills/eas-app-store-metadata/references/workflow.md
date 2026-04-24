# Workflow

Use this sequence to manage App Store Connect metadata with EAS CLI while keeping the repository state reviewable and reproducible.

## 1. Confirm EAS Project Linkage

- Check whether the project is already linked to EAS by looking for `extra.eas.projectId` in app config or another explicit repository note.
- If linkage is missing, stop assuming metadata commands will work.
- Tell the user the project must first be created or linked with `eas init` or `eas project:init`.
- If the agent can safely run terminal commands and Expo authentication is already satisfied, the agent can execute that step instead of handing it off.
- If Expo login, SSO, 2FA, account selection, or policy approval is required, hand it off clearly.

## 2. Load Project Policy Before Editing

- Look for a project profile before making assumptions about the submit profile, metadata path, shipped locales, version source, or protected fields.
- If none exists, use conservative defaults and recommend adding a profile for repeatability.

Use [project-profile.md](./project-profile.md) for the profile contract.

## 3. Confirm The Credential Boundary

- Confirm where the App Store Connect `.p8` private key lives before touching submit config.
- If the current `ascApiKeyPath` or equivalent secret reference points anywhere inside the repository, stop and move it out before continuing.
- Recommended best default on macOS: keep the `.p8` file in a per-user private Application Support directory outside the checkout, then reference it from untracked local config or an environment variable.
- Do not treat a gitignored project-local `credentials/` folder as an acceptable long-term secret boundary.

## 4. Verify The Effective Metadata Surface

Before editing, make these explicit:

- which submit profile is in scope
- which `metadataPath` will be used
- whether the project uses `store.config.json` or a dynamic `store.config.js`
- which locales are shipped
- where screenshots live relative to the repository root
- where the user-facing release version is sourced from

If the app does not yet exist on App Store Connect, do not pretend `eas metadata:pull` can bootstrap it. Start from a new local template instead.

## 5. Reconcile Dashboard Drift First

- If someone edited metadata in App Store Connect directly, run `eas metadata:pull` before changing local files.
- Review the diff after pull so the local source of truth matches the dashboard before new edits start.

Do not skip this step when dashboard edits are known. Otherwise the next push may silently overwrite them.

## 6. Edit The Local Source Of Truth

- Make changes in the local metadata file, not only in prompts or one-off commands.
- Keep release-note updates explicit for every shipped locale when preparing a new version.
- Keep screenshot paths relative and reviewable.
- Avoid burying policy inside shell history or agent memory.

Use [assets/store.config.template.json](../assets/store.config.template.json) when the project needs a starting point.

## 7. Validate Before Push

- Run `eas metadata:lint` with the effective submit profile.
- Review the local diff.
- Check App Store field limits, keyword rules, locale coverage, screenshot paths, and version alignment.

Use [validation-rules.md](./validation-rules.md) for the required checks.

## 8. Push Metadata Deliberately

- Push only after lint and diff review are both clean enough for the requested change.
- If the release requires a new App Store Connect draft version, confirm that the draft exists first.
- Treat partial success as a state that must be reviewed and retried intentionally, not ignored.

## 9. Handoff The Release Boundary Explicitly

This skill manages listing metadata, not the full release pipeline.

After metadata is ready, make the next boundary explicit:

- create the target App Store Connect version draft if needed
- upload or process the binary through the project's native release workflow
- attach the build to the draft version in App Store Connect
- submit for review from the preferred workflow

If the user wants to automate those steps too, treat that as adjacent work instead of assuming it is included by default.
