---
name: eas-app-store-metadata
description: "Manage and version App Store Connect metadata with EAS CLI. Use when creating or maintaining store.config.json, syncing App Store Connect listing data with eas metadata:pull or eas metadata:push, versioning release notes and screenshots in git, or validating Apple listing changes before release handoff."
compatibility: "Designed for Agent-Skills-compatible clients such as VS Code/Copilot and Windsurf. Cursor requires a rules or prompt wrapper instead of direct SKILL.md installation."
---

# EAS App Store Metadata

Manage and version App Store Connect metadata with EAS CLI and a repository-local store configuration.

## Use This Skill When

- the user wants to manage App Store Connect listing data with EAS CLI
- `store.config.json` should become the versioned source of truth in git
- metadata must be pulled from App Store Connect with `eas metadata:pull`
- metadata must be linted, reviewed, and pushed with `eas metadata:lint` or `eas metadata:push`
- a release needs synchronized version numbers, localized release notes, or screenshot paths
- someone edited App Store Connect in the web UI and local metadata now risks drift
- the project wants a reusable profile for EAS metadata paths, release policy, and credential hygiene

## Required Operating Model

1. Treat the local store config as the versioned source of truth once this workflow is established.
2. If anyone edits metadata in App Store Connect directly, pull those changes back before the next local edit or push.
3. Verify EAS project linkage before assuming metadata commands will work.
4. Prefer `eas metadata:lint` plus a local diff review before `eas metadata:push`.
5. Keep the metadata workflow separate from binary build, binary upload, and final review submission unless the user explicitly asks to automate those too.
6. Do not commit `.p8` API key files, real private-key paths, or other secret-bearing local credential variants. A shared `eas.json` is acceptable only when it stays secret-free.
7. Do not store the App Store Connect API private key anywhere under the project root, even in a gitignored `credentials/` folder. Keep it outside the repository in a user-private local directory.
8. In tracked `eas.json`, prefer `"ascApiKeyPath": "$ASC_API_KEY_PATH"` over a machine-specific absolute path. EAS CLI supports environment-variable evaluation for this iOS submit field.
9. After the `.p8` file is placed in its outside-repo location, ask whether the user wants `ASC_API_KEY_PATH` persisted in local shell config, direnv, or another local-only environment setup so they do not need to export it manually every time.
10. Keep the release target version explicit and aligned with the native app version source.
11. Before ending, tell the user the concrete EAS commands they can use later for ASC sync, metadata changes, and version-preparation steps, then ask whether those steps should be written into README, development docs, or another user-specified location.

## First-Run Requirement

Do not assume a new project is already linked to EAS.

On the first substantial use in a repository, explicitly check whether the project is already linked to an EAS project. Typical signals are:

- `app.json`, `app.config.js`, or `app.config.ts` contains `extra.eas.projectId`
- the repository has already successfully run `eas init` or `eas project:init`
- the repository's release docs already reference an existing EAS project link

If the project is not linked yet, tell the user that the project must first be created or linked on EAS by running `eas init` or `eas project:init`.

Do not phrase this as "the user must manually create the project on expo.dev first." The official EAS flow supports creating or linking the project from the CLI, and that is the correct default guidance.

If the agent has terminal access and Expo authentication is already satisfied, this step can be executed automatically. If Expo login, SSO, 2FA, account selection, or organization policy blocks automation, hand it off clearly.

For repeated use in one project, recommend creating a project profile from [assets/eas-app-store-metadata-project-profile.yaml](./assets/eas-app-store-metadata-project-profile.yaml) instead of leaving policy trapped in chat.

## Credential Boundary

Treat the App Store Connect `.p8` private key as workstation-local secret material, not as project source.

- Never keep the `.p8` file under the repository tree, even if that folder is gitignored.
- Recommended best default on macOS: a per-user private Application Support directory outside the checkout, then reference that path from untracked local config or an environment variable.
- In tracked `eas.json`, prefer the supported EAS submit pattern `"ascApiKeyPath": "$ASC_API_KEY_PATH"` instead of a resolved absolute path.
- EAS CLI also supports environment-variable evaluation for `ascApiKeyIssuerId` and `ascApiKeyId` if a project chooses to source those locally too.
- Commit only secret-free templates and policy notes. Do not normalize in-repo secret storage by shipping examples such as `./credentials/AuthKey_...p8`.

## Project Profile

Look for a project profile in one of these places before making assumptions:

- `eas-app-store-metadata-project-profile.yaml`
- `.ai/eas-app-store-metadata-project-profile.yaml`
- `.github/eas-app-store-metadata-project-profile.yaml`
- another path explicitly provided by the user

If no profile exists, use the conservative defaults in [project profile reference](./references/project-profile.md) as a temporary fallback and recommend adding a profile before this workflow becomes routine.

## Procedure

1. Follow the end-to-end sequence in [workflow](./references/workflow.md).
2. Load or establish project rules using [project profile reference](./references/project-profile.md).
3. Apply push-safety and App Store field checks from [validation rules](./references/validation-rules.md).
4. Use [troubleshooting](./references/troubleshooting.md) when EAS linkage, authentication, ASC draft state, partial uploads, screenshot order drift, or transient App Store Connect API failures bite. The same reference covers the wrapper pattern at [assets/eas-metadata-push-retry.sh](./assets/eas-metadata-push-retry.sh) for stdout-aware retry on long pushes.

## Exit Criteria

- EAS project linkage is verified or initialized
- the effective submit profile and metadata path are explicit
- requested metadata fields, locales, and screenshot paths are updated in the local source of truth
- lint and diff review happen before any push
- release handoff steps for ASC draft creation, binary upload, build attachment, and review submission are explicit
- after the `.p8` file is placed, the user is asked whether `ASC_API_KEY_PATH` should be persisted in local-only environment setup
- the user receives a concrete future-use command handoff for sync, metadata edits, and version-preparation steps
- the user is asked whether those steps should be written into README, development docs, or another specified location
- no secrets, no in-repo `.p8` storage pattern, and no project-private values are committed into shared templates
