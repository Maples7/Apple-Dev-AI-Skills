# Apple Dev AI Skills

[English](./README.md) | [简体中文](./README.zh-CN.md)

Installable AI skills for Apple-platform work.

Use this repo when you want sharper help for Xcode string catalogs, App Store screenshots, App Store metadata, and git commit messages without re-explaining the workflow every time.

## Why This Repo

- Ship faster with reusable, task-specific skills instead of one-off prompts.
- Keep Apple workflows consistent across projects, releases, and collaborators.
- Install one skill for a focused job, or install the full catalog at once.

## Quick Install

Install the full collection:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills
```

Install one skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

Install globally:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills -g
```

## Skills

Ordered by likely user appeal, starting with the most immediately useful Apple-specific workflows.

### `translate-xcstrings`

Translate or normalize Xcode `.xcstrings` catalogs without breaking placeholders, formatting, or Apple-specific files like `InfoPlist.xcstrings` and `AppShortcuts.xcstrings`.

Why it stands out: localization work is repetitive, fragile, and expensive to redo. This skill turns it into a safer repeatable workflow.

[Open skill folder](./skills/translate-xcstrings)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

### `app-store-preview-pipeline`

Plan and generate App Store screenshots through a proof-first pipeline with stable sample data, review checkpoints, automation hooks, and final export guidance.

Why it stands out: screenshot production usually becomes a last-minute mess. This skill gives you a reusable pipeline instead of another ad hoc capture session.

[Open skill folder](./skills/app-store-preview-pipeline)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill app-store-preview-pipeline
```

### `eas-app-store-metadata`

Manage App Store Connect metadata with EAS CLI using a versioned local workflow for `store.config.json`, release notes, screenshots, linting, and safer push review.

Why it stands out: metadata drift is easy to miss and painful to clean up. This skill keeps listing changes reviewable and repeatable in git.

[Open skill folder](./skills/eas-app-store-metadata)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill eas-app-store-metadata
```

### `pre-commit-review`

Review uncommitted Apple-platform changes through seven lenses — performance, user experience, test coverage, architecture, code style, security & privacy, and documentation — and return a structured, severity-graded report before you run `git commit`.

Why it stands out: most pre-commit checks are either a linter or a free-form review. This skill gives Swift / SwiftUI work a focused, repeatable triage that calls out perf risk, UX regressions, missing tests, layering and style drift, surface-level security or privacy issues, and stale docs in one pass.

[Open skill folder](./skills/pre-commit-review)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill pre-commit-review
```

### `commit-message`

Draft a strong English Conventional Commit message from your current diff and session context, with support for scopes, footers, and monorepo conventions.

Why it stands out: it is broadly useful, but less Apple-specific than the skills above. Install it when you want faster, cleaner commit hygiene across projects.

[Open skill folder](./skills/commit-message)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill commit-message
```

### `handle-github-issue`

Process any GitHub issue end-to-end using disciplined code review, TDD when applicable, local verification, and structured landing workflow.

Why it stands out: GitHub issue automation is ad hoc and error-prone. This skill provides a reusable checklist for read → implement → verify → review → land → close, ensuring consistent quality and transparent communication.

[Open skill folder](./skills/handle-github-issue)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill handle-github-issue
```

## Compatibility

This repository follows the [Agent Skills specification](https://agentskills.io/specification).

- Works best with clients that support `SKILL.md`-based skills.
- If your client does not support `SKILL.md` directly, start with the wrappers in [adapters/](./adapters).

## License

MIT. See [LICENSE](./LICENSE).


