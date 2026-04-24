# Apple Dev AI Skills

### `app-store-preview-pipeline`

Build a public, proof-first App Store Connect screenshot pipeline with deterministic sample data, review checkpoints, broad device coverage guidance, and final opaque export rules.

[Open skill folder](./skills/app-store-preview-pipeline)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill app-store-preview-pipeline
```

Build better Apple apps, faster.

A growing catalog of installable AI skills for Swift, SwiftUI, Xcode, testing, automation, and App Store delivery.

## Quick Install

Install the full collection:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills
```

Install a specific skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

Install globally:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills -g
```


Translate or normalize Xcode `.xcstrings` catalogs, including `Localizable.xcstrings`, `InfoPlist.xcstrings`, and `AppShortcuts.xcstrings`.

[Open skill folder](./skills/translate-xcstrings)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

### `commit-message`

Draft an idiomatic English Conventional Commit message from the current diff and session context, with optional repository profile support for scopes, footers, and monorepo naming.

[Open skill folder](./skills/commit-message)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill commit-message
```

### `eas-app-store-metadata`

Manage and version App Store Connect listing data with EAS CLI, including store.config.json, release notes, screenshots, linting, and push-safe review.

[Open skill folder](./skills/eas-app-store-metadata)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill eas-app-store-metadata
```

## Compatibility

This repository follows the [Agent Skills specification](https://agentskills.io/specification).

- Works best with clients that support `SKILL.md`-based skills.
- For clients without native `SKILL.md` support, use the wrappers under [`adapters/`](./adapters) or convert the skill into that client's native rule or prompt system.

## License

MIT. See [`LICENSE`](./LICENSE).


