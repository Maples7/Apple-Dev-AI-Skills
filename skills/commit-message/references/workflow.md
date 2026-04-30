# Workflow

Use this sequence to gather signal before drafting the message.

## Commit Profile Loading

1. Look for a commit profile at `commit-message-profile.yaml`, `.ai/commit-message-profile.yaml`, or `.github/commit-message-profile.yaml`.
2. If the user provided a different path, use that path instead.
3. If no profile exists, use the conservative defaults from [commit profile reference](./profile.md).
4. Determine the effective rules for required scope, allowed types, required footers, and monorepo scope mapping before drafting.

## Diff Selection

1. Run `git status` first so you know whether the repository has staged content.
2. If staged content exists, use `git diff --staged` as the sole source of code changes.
3. Only when nothing is staged, fall back to `git diff` for unstaged changes.
4. If the user explicitly asks to consider all local changes, include both staged and unstaged diffs regardless of staging state.

## Read Order

1. Start with `git status`.
2. Read `git diff --staged` or `git diff`, depending on the scope rules above.
3. For larger changes, use `git diff --stat` to understand breadth before reading the most important hunks in full.
4. In monorepos, inspect changed top-level packages, apps, or workspace directories before deciding the scope when the profile requires it.
5. Stop reading once you have enough signal to explain the purpose and main effects of the change.

## Context Enrichment

1. Use the current conversation to explain why the change was made.
2. Prefer user intent and stated goals over guessing from filenames alone.
3. Prefer repository package names, workspace names, or configured aliases when the profile requires a scope.
4. Avoid repeating the diff line by line in the final message body.

## Footer Detection

Check the effective profile first, then look for issue or ticket references in this order:

1. current branch name, such as `issue-123`, `fix/123-name`, `gh-123`, or similar
2. recent conversation turns mentioning `#123`, `GH-123`, a ticket ID, or an issue URL
3. repository context that makes a closure footer versus a reference footer clear

When a reference exists:

- use `Closes #123` if the change clearly resolves the issue
- otherwise use `Refs #123`

## Output Discipline

- Return the drafted message only; do not create a commit.
- If the diff is unusually broad or mixes unrelated concerns, add a short note suggesting a split after the message.
- If diff inspection reveals a high-confidence commit-relevant issue, such as accidental secrets, unrelated changes, temporary or debug artifacts, generated files, or an obvious need to split the commit, add one short note after the message.
- Do not perform a full code review or include speculative improvement suggestions.
- If no profile exists and the user asked for repository-specific rules, note that conservative fallback rules were used.

## Split Plan Suggestion

The default output is always a single best commit message. Only when the diff shows strong, unambiguous split signals, append an additional split plan after that message.

Qualifying signals (any one is enough):

- the change cleanly spans more than one Conventional Commit type that are not causally related, for example a `feat` mixed with an unrelated `chore`, `refactor`, `docs`, or dependency bump
- multiple independent scopes or packages change with no dependency between them
- a functional change is mixed with obviously separable noise such as bulk formatting, renames, or generated-file updates

Do not suggest a split when:

- the changes share a single purpose even if they touch several files or types
- splitting would require breaking a hunk in a way that could leave intermediate commits non-buildable in a non-obvious way
- evidence is weak or speculative

When you do suggest a split, output a section titled `Suggested split plan` after the primary commit message with:

1. an ordered list of proposed commits in the order they should be applied
2. for each proposed commit: a one-line scope description (files, directories, or hunks it covers) and a draft Conventional Commit message in a fenced code block
3. a closing line stating that this is a proposal only, that no `git` commands have been or will be run, and that the user is responsible for performing the split and verifying no regressions afterward

Never execute `git add`, `git add -p`, `git commit`, `git reset`, `git stash`, or any test or build command as part of this skill. Validation of the split belongs to the project's own test, build, or CI workflow, not to this skill.
