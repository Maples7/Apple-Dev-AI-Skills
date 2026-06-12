---
name: handle-github-issue
description: Handle a GitHub issue end-to-end using disciplined code review, TDD when applicable, local verification, and structured landing workflow.
---

# Handle GitHub Issue

Process any GitHub issue through a structured end-to-end workflow: read → validate → implement with TDD → review → land → cleanup.

Use this skill when you need to:
- Implement a feature or bug fix from a GitHub issue
- Ensure disciplined process (isolated changes, review gates, verification)
- Coordinate across verification, testing, landing, and issue closure

## Required Workflow

### 1. Read and Validate
- Fetch the full issue, comments, linked PRs, and labels from GitHub
- Review the current repository code and context
- Determine if the issue is valid, actionable, and not a duplicate
- If invalid/duplicate/already fixed, comment with evidence and stop

### 2. Plan and Create Isolation
- Confirm the base branch (e.g., `main`, `develop`, a feature branch)
- Plan the implementation: What code changes are needed? Are there tests to update?
- Create an isolated working branch from the base branch:
  - **Standard approach**: `git checkout -b issue/<number> origin/<base-branch>`
  - **Advanced**: If your project uses worktree tooling (e.g., `git worktree`, specialized CLI), use that instead for better isolation
- Navigate into the working branch or worktree

### 3. Implement with TDD (When Applicable)
- Identify if a test surface exists (unit tests, integration tests, UI tests)
- If a test exists:
  1. Write or update the smallest failing test case first
  2. Make the minimal production code change to pass that test
  3. Rerun the focused test and verify green
- If no test surface exists:
  1. Implement the feature/fix directly
  2. Document rationale in commit message

### 4. Verify Locally
- Run relevant test suites, build checks, linters, or integration tests
- Capture and report all verification output
- Ensure all checks pass before proceeding

### 5. Code Review and Cleanup
- Invoke `review-swarm` or `pre-commit-review` on the uncommitted or staged diff
- Address every actionable finding
- Resolve style, performance, security, and architectural concerns
- Verify review resolution before commit

### 6. Land and Push
- Commit inside the isolated branch with a clear, descriptive message
- Merge or rebase back to the base branch (use `git merge` or `git rebase` depending on your project)
- Push the base branch to GitHub
- Clean up the working branch or worktree:
  - **Standard**: `git branch -d issue/<number>` or `git branch -D issue/<number>`
  - **Advanced**: If you used worktree tooling, use its cleanup command

### 7. Close and Report
- Comment on the issue with:
  - What changed (features/fixes implemented)
  - Verification results (tests passed, lints passed, etc.)
  - Review findings and how they were resolved
  - Commit hash and branch/PR reference
- Close the issue (via GitHub UI or comment with `/close` if supported)
- Report any blockers or cleanup issues explicitly

## Key Principles

**Validate before committing**: Always run review and verification BEFORE landing.

**Isolated changes**: Use branches or worktrees to isolate work from the mainline, preventing accidental interference.

**TDD when applicable**: If a test surface exists, prioritize writing the test first. If not, implement directly and document why.

**Transparent communication**: Every step produces reportable evidence (test output, review results, commit hash).

**Cleanup discipline**: Remove temporary worktrees or branches to keep the repository clean.

## When to Stop

Stop early and comment on the issue if any of these are true:
- The issue is a duplicate of another (link the canonical issue)
- The issue is already fixed (cite the commit/PR)
- The issue is invalid or lacks sufficient detail to implement
- The issue requests unsafe or policy-violating behavior
- The verification or review discovers a fundamental blocker

## Adapting to Your Project

Projects may customize this workflow via:
- **Test framework**: XCTest, Swift Testing, Jest, pytest, Vitest, etc.
- **Verification tools**: SwiftFormat, SwiftLint, cargo test, npm run test, eslint, etc.
- **Branch isolation**: Standard `git checkout -b`, or advanced worktree tools (`git worktree` or project-specific CLI)
- **Review gates**: Pre-commit reviews, code review automation, linting, or static analysis
- **Base branch strategy**: `main`, `develop`, release branches, or other branch hierarchies

Read your project's contribution guide or `CONTRIBUTING.md` for specifics.

## References

See [GitHub Issue Agent Workflow](./references/agent-issue-workflow.md) for a step-by-step checklist.
