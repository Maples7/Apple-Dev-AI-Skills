# Adapters

[English](./README.md) | [简体中文](./README.zh-CN.md)

This directory holds lightweight wrappers for agents that do not natively discover `SKILL.md` folders.

The canonical source of truth remains under `skills/`.

## Current Adapter Strategy

- Copilot / VS Code: install the canonical skill folder directly.
- Claude Code: install the canonical skill folder directly.
- Other agents: start from a single-file prompt wrapper that mirrors the canonical workflow and adapt it into the target agent's rule or prompt system.

Current wrappers:

- [`generic/translate-xcstrings.prompt.md`](./generic/translate-xcstrings.prompt.md)
- [`generic/app-store-preview-pipeline.prompt.md`](./generic/app-store-preview-pipeline.prompt.md)
- [`generic/eas-app-store-metadata.prompt.md`](./generic/eas-app-store-metadata.prompt.md)
- [`generic/pre-commit-review.prompt.md`](./generic/pre-commit-review.prompt.md)
- [`generic/commit-message.prompt.md`](./generic/commit-message.prompt.md)
