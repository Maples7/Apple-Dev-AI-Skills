# Handle GitHub Issue

Use this wrapper with coding agents that do not natively support `SKILL.md` folders.

## Task

Process a GitHub issue end-to-end from reading through closing, using disciplined code review, test-driven development where applicable, local verification, and structured landing workflow.

## Operating Rules

1. **Read and Validate** (10–15 min): Fetch the full issue, comments, linked PRs, and labels from GitHub. Scan the codebase to understand context. Determine if the issue is valid, actionable, and not a duplicate.
   - If invalid/duplicate/already fixed: comment with evidence and stop.
   - If valid: proceed to Plan and Create Isolation.

2. **Plan and Create Isolation** (5 min): Identify the correct base branch (usually `main` or `develop`). Create an isolated working branch from that base.
   - **Standard approach**: `git checkout -b issue/<number> origin/<base-branch>`
   - **Advanced**: If your project uses worktree tooling (e.g., `git worktree` or specialized CLI), use that instead for better isolation

3. **Implement with TDD** (varies): If a test surface exists (unit tests, integration tests, UI tests), write the smallest failing test first, then make the minimal code change to pass it. Repeat for each piece of functionality. If no test surface exists, implement directly and document why in the commit message.

4. **Verify Locally** (5–10 min): Run the project's standard verification (e.g., `npm run test`, `swift test`, `scripts/quality.sh`). Run linters, formatters, type checkers, and any integration tests. Capture all output and confirm all checks pass.

5. **Code Review and Cleanup** (10–15 min): Invoke the project's review skill or tool (e.g., `pre-commit-review`, `review-swarm`). Address every actionable finding (fix, optimize, or explain). Rerun verification and confirm all checks still pass.

6. **Land and Push** (5 min): Commit inside the isolated branch with a clear message (reference the issue, e.g., `Fixes #42`). Merge or rebase back to the base branch. Push the base branch to GitHub. Clean up the working branch afterward.

7. **Close and Report** (5 min): Comment on the issue with a summary of what changed, verification results, review findings and resolutions, commit hash, and branch/PR reference. Close the issue on GitHub. Report any blockers explicitly.

## Required Checks

- Read the full issue and comments, not just the title
- Confirm the correct base branch before creating isolation
- Use TDD when a test surface exists; document why if not
- Run the full verification suite before proceeding to review
- Address every code review finding (fix, optimize, or explain)
- Verify after addressing review findings
- Include the issue reference in the commit message
- Comment on the issue with verification and review results before closing
- Clean up branches after landing

## Decision Gates

- **Is the issue valid?** → Yes: continue; No: comment with evidence and stop
- **Is the issue already fixed or a duplicate?** → Yes: comment and stop; No: continue
- **Do all verification checks pass?** → Yes: proceed to review; No: fix and rerun
- **Are all code review findings addressed?** → Yes: proceed to commit; No: go back and fix
- **Is the verification still passing after review?** → Yes: proceed to land; No: fix and rerun

## Canonical Source

The full reusable skill lives under [`skills/handle-github-issue/`](../../skills/handle-github-issue/).

Read these files when the wrapper alone is not enough:

- [`skills/handle-github-issue/SKILL.md`](../../skills/handle-github-issue/SKILL.md)
- [`skills/handle-github-issue/references/agent-issue-workflow.md`](../../skills/handle-github-issue/references/agent-issue-workflow.md)
