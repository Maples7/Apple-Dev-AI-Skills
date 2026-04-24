# Adapters

This directory holds lightweight wrappers for agents that do not natively discover `SKILL.md` folders.

The canonical source of truth remains under `skills/`.

## Current Adapter Strategy

- Copilot / VS Code: install the canonical skill folder directly.
- Claude Code: install the canonical skill folder directly.
- Other agents: start from a single-file prompt wrapper that mirrors the canonical workflow and adapt it into the target agent's rule or prompt system.

Current wrapper:

- [`generic/translate-xcstrings.prompt.md`](./generic/translate-xcstrings.prompt.md)
