# Commit Message

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Draft a single high-quality git commit message from the current repository changes and session context.

## Operating Rules

1. Before drafting, look for a commit profile at `commit-message-profile.yaml`, `.ai/commit-message-profile.yaml`, or `.github/commit-message-profile.yaml`.
2. If a profile exists, apply its rules for scope requirements, footer conventions, monorepo package naming, allowed types, and body expectations.
3. If no profile exists, fall back to standard Conventional Commit behavior and treat repository policy as unspecified.
4. Run `git status` first, prefer staged changes, and only fall back to unstaged diff when nothing is staged unless the user explicitly asks to include all local changes.
5. Use the conversation to explain why the change was made, not only what changed.
6. Check the current branch name and recent conversation for likely issue references such as `#123`, `gh-123`, or `fix/123-name`.
7. Generate a Conventional Commit in idiomatic English.
8. Produce the message only; do not run `git commit`.

## Required Checks

- prefer staged scope whenever staged changes exist
- state or infer the effective commit scope policy before drafting
- use `git diff --stat` when the diff is broad before reading the most important hunks in full
- use repository package or workspace names as scope only when the profile or diff supports that choice
- keep the subject imperative, concise, and without a trailing period
- add required footers from the profile when the evidence is present
- note after the message if the diff looks broad enough to split into multiple commits or if a missing profile forced conservative fallback

## Canonical Source

The full reusable skill lives under [`skills/commit-message/`](../../skills/commit-message/).

Read these files when the wrapper alone is not enough:

- [`skills/commit-message/SKILL.md`](../../skills/commit-message/SKILL.md)
- [`skills/commit-message/references/workflow.md`](../../skills/commit-message/references/workflow.md)
- [`skills/commit-message/references/message-rules.md`](../../skills/commit-message/references/message-rules.md)
- [`skills/commit-message/references/profile.md`](../../skills/commit-message/references/profile.md)
- [`skills/commit-message/assets/commit-message-profile.yaml`](../../skills/commit-message/assets/commit-message-profile.yaml)
