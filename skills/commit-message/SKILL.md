---
name: commit-message
description: "Draft a git commit message from current repository changes, current conversation, and session context. Use when writing a Conventional Commit, applying repository or team policy for scopes and footers, generating monorepo-aware commit text, or adding issue trailers without running git commit."
argument-hint: "Scope or policy request, for example: 'staged only', 'all local changes', 'use the repo commit profile', or 'include issue reference if present'."
compatibility: "Designed for Agent-Skills-compatible clients such as VS Code/Copilot and Windsurf. Cursor requires a rules or prompt wrapper instead of direct SKILL.md installation."
---

# Commit Message

Generate a single high-quality git commit message from the current repository changes.

## Use This Skill When

- the user asks for a commit message for current local changes
- the user wants the commit message to reflect the current conversation, not only the diff
- staged changes should take priority over unstaged work
- a Conventional Commit subject, body, or footer is needed
- the repository expects commit scopes, constrained commit types, or specific footers
- the repository is a monorepo and scope selection should follow package or workspace names
- the change should reference an issue from the branch name or conversation
- the user wants help deciding whether a diff should be split before committing

## Required Operating Model

1. Load the repository commit profile before drafting when one exists.
2. Prefer staged changes whenever staged content exists.
3. Use the actual diff plus session context so the message explains why the change happened, not only what changed.
4. Detect likely issue references from the current branch name and recent conversation.
5. Produce a commit message plus only the allowed short caveats; do not run `git commit`.

## Commit Profile

Look for a commit profile in one of these places before drafting:

- `commit-message-profile.yaml`
- `.ai/commit-message-profile.yaml`
- `.github/commit-message-profile.yaml`
- another path explicitly provided by the user

If no profile exists, fall back to the conservative defaults in [commit profile reference](./references/profile.md) and recommend adding a profile after the change when repository-specific rules matter.

Use [assets/commit-message-profile.yaml](./assets/commit-message-profile.yaml) as the template when a repository needs one.

## Procedure

1. Follow the inspection order in [workflow](./references/workflow.md).
2. Apply the drafting rules in [message rules](./references/message-rules.md).
3. If the diff covers unrelated concerns, still produce the best single message you can. When strong split signals are present, also append a suggested split plan as described in [workflow](./references/workflow.md#split-plan-suggestion).
4. Never run `git add`, `git commit`, or otherwise modify the index or working tree. Splitting and validation are the user's decision.

## Exit Criteria

- exactly one primary Conventional Commit message is produced for the current diff
- the message is written in idiomatic English
- the message satisfies the effective repository profile or conservative fallback rules
- staged versus unstaged scope is handled correctly
- required scope and footer conventions are applied when the evidence supports them
- any note after the message is high-confidence, commit-relevant, and non-speculative
- when split signals are strong, an additional `Suggested split plan` section is appended; it is a proposal only and no `git` commands are executed
- the output is ready for the user to copy into `git commit`
