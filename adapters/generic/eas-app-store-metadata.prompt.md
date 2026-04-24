# EAS App Store Metadata

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Manage and version App Store Connect metadata with EAS CLI and a repository-local store configuration.

## Operating Rules

1. Before editing metadata, look for a project profile at `eas-app-store-metadata-project-profile.yaml`, `.ai/eas-app-store-metadata-project-profile.yaml`, or `.github/eas-app-store-metadata-project-profile.yaml`.
2. On the first substantial use in a new project, verify that the repository is linked to an EAS project. Prefer checking app config for `extra.eas.projectId` or a documented successful `eas init`.
3. If the project is not linked yet, tell the user to run `eas init` or `eas project:init`, or execute it directly when terminal access and Expo authentication are already available.
4. If metadata was edited in App Store Connect directly, run `eas metadata:pull` before making new local edits.
5. Prefer `eas metadata:lint` and a local diff review before `eas metadata:push`.
6. Keep the release target version, shipped locales, screenshot roots, and `metadataPath` explicit.
7. Do not commit `.p8` API key files, real private-key paths, or other secret-bearing local credential variants. A shared `eas.json` is acceptable only when it stays secret-free.
8. The App Store Connect `.p8` key must live outside the repository. Recommended best default on macOS: a per-user private Application Support directory outside the checkout, referenced from untracked local config or an environment variable.
9. Treat binary upload, build attachment, and final review submission as explicit handoff steps unless the user asks to automate those too.

## Required Checks

- verify EAS project linkage before assuming metadata commands will work
- verify the submit profile and effective `metadataPath`
- verify any `ascApiKeyPath` or equivalent secret reference resolves outside the repository
- if the app does not yet exist on App Store Connect, start from a local template instead of expecting `eas metadata:pull` to bootstrap it
- update release notes for shipped locales when preparing a new version unless the project profile says otherwise
- verify screenshot paths exist and remain relative
- enforce title, subtitle, keywords, promo text, and release-note limits during review
- pull before push when dashboard edits are known

## Canonical Source

The full reusable skill lives under [`skills/eas-app-store-metadata/`](../../skills/eas-app-store-metadata/).

Read these files when the wrapper alone is not enough:

- [`skills/eas-app-store-metadata/SKILL.md`](../../skills/eas-app-store-metadata/SKILL.md)
- [`skills/eas-app-store-metadata/references/workflow.md`](../../skills/eas-app-store-metadata/references/workflow.md)
- [`skills/eas-app-store-metadata/references/project-profile.md`](../../skills/eas-app-store-metadata/references/project-profile.md)
- [`skills/eas-app-store-metadata/references/validation-rules.md`](../../skills/eas-app-store-metadata/references/validation-rules.md)
- [`skills/eas-app-store-metadata/references/troubleshooting.md`](../../skills/eas-app-store-metadata/references/troubleshooting.md)
- [`skills/eas-app-store-metadata/assets/eas-app-store-metadata-project-profile.yaml`](../../skills/eas-app-store-metadata/assets/eas-app-store-metadata-project-profile.yaml)
- [`skills/eas-app-store-metadata/assets/eas.example.json`](../../skills/eas-app-store-metadata/assets/eas.example.json)
- [`skills/eas-app-store-metadata/assets/store.config.template.json`](../../skills/eas-app-store-metadata/assets/store.config.template.json)
