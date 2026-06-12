# GitHub Issue Agent Workflow Checklist

This checklist provides step-by-step guidance for processing any GitHub issue end-to-end.

## Phase 1: Read and Validate (10–15 min)

- [ ] Fetch the full issue from GitHub (number, title, description, all comments)
- [ ] List linked PRs, issues, and labels
- [ ] Read the issue description and understand the required behavior
- [ ] Scan comments for additional context, clarifications, or edge cases
- [ ] Review the current relevant codebase sections
- [ ] Check if there is a linked test file or test surface
- [ ] Determine the correct base branch (usually from issue context or project conventions)

**Decision Gate**:
- Is the issue valid and actionable? → Continue to Phase 2
- Is the issue invalid, duplicate, or already fixed? → Comment with evidence and stop
- Is the issue missing critical detail? → Comment asking for clarification and stop

## Phase 2: Plan and Create Isolation (5 min)

- [ ] Confirm the base branch (e.g., `main`, `develop`, a feature branch)
- [ ] Plan the implementation: What code changes are needed? Are there tests to update?
- [ ] Create an isolated working branch from the base branch:
  - **Standard approach**: `git checkout -b issue/<number> origin/<base-branch>`
  - **Advanced**: If your project uses worktree tooling (`git worktree` or specialized CLI), use that instead for better isolation
- [ ] Navigate into the working branch or worktree

## Phase 3: Implement with TDD

### If a test surface exists (unit tests, integration tests, UI tests):

- [ ] Identify the failing test case or test file
- [ ] Write or update the minimal failing test (one assertion, smallest scope)
- [ ] Run the focused test and confirm it fails
- [ ] Make the minimal production code change to pass that test
- [ ] Rerun the focused test and confirm it passes
- [ ] Repeat for each distinct piece of functionality
- [ ] Run the full test suite and verify all tests pass

### If no test surface exists:

- [ ] Implement the feature or fix directly
- [ ] Document in the commit message why a test surface was not available
- [ ] Verify by running any existing validation (linters, builds, type checks)

## Phase 4: Local Verification (5–10 min)

- [ ] Run the project's standard verification command (e.g., `npm run test`, `swift test`, `scripts/quality.sh`)
- [ ] If the project has linters or formatters, run them and fix any violations
- [ ] If the project has type checking, run it and ensure no errors
- [ ] Run a focused integration test if applicable (e.g., build the app, run the feature end-to-end)
- [ ] Capture all verification output (test counts, pass/fail, any warnings)
- [ ] Confirm all checks pass before proceeding

## Phase 5: Code Review and Cleanup

- [ ] Invoke your project's code review skill or tool (e.g., `pre-commit-review`, `review-swarm`)
- [ ] Read every finding in the review report
- [ ] For each finding:
  - If it is actionable: fix it in the code, rerun verification, confirm it passes
  - If it is a false positive: comment in the skill session explaining why
  - If it is a style preference: apply it even if it seems minor
- [ ] Rerun the full verification after addressing all findings
- [ ] Confirm all checks still pass

## Phase 6: Commit and Land (5 min)

- [ ] Stage all changes: `git add -A` (or selective `git add <files>`)
- [ ] Write a clear, descriptive commit message following your project's conventions
  - Reference the issue (e.g., `Fixes #42` or `Resolves #42`)
  - Describe what changed and why in 1–2 sentences
  - If there are multiple logical changes, use separate commits
- [ ] Commit: `git commit -m "..."`
- [ ] Merge or rebase back to the base branch:
  - **Merge**: `git checkout <base-branch> && git merge issue/<number>`
  - **Rebase**: `git checkout <base-branch> && git rebase issue/<number>` (depending on your project's preference)
- [ ] Push the base branch: `git push origin <base-branch>`
- [ ] Clean up the working branch:
  - `git branch -d issue/<number>` (or `-D` to force-delete)
  - If you used advanced worktree tooling, use its cleanup command instead

## Phase 7: Close and Report (5 min)

- [ ] On GitHub, navigate to the issue
- [ ] Add a comment with the following structure:

```
## Issue Resolution

### What Changed
- [Describe the implementation in 2–3 bullets]
- [Example: Added validation logic in `src/utils/validators.ts`]
- [Example: Updated test suite with 3 new test cases]

### Verification
- Tests: ✅ All 42 tests pass
- Linter: ✅ No violations
- Type check: ✅ No errors
- Integration: ✅ Feature works end-to-end

### Code Review
- Review: ✅ Pre-commit review passed with 2 minor findings (all resolved)
  - Finding 1: Style adjustment (fixed)
  - Finding 2: Performance optimization (applied)

### Landing
- Commit: abc1234567 (main branch)
- Worktree cleanup: ✅ (or: ❌ Blocked by reason)

---

Closing this issue.
```

- [ ] Close the issue (GitHub UI: "Close with comment" or issue status dropdown)
- [ ] If any blockers or unexpected issues occurred, report them explicitly in the comment

## Common Blockers and Recovery

| Blocker | Recovery |
|---------|----------|
| Tests fail after implementation | Debug the failing test; check if the implementation logic is correct |
| Linter violations | Apply suggested fixes; if they conflict with requirements, document the exception |
| Verification timeout | Check for infinite loops or performance issues; run verification incrementally |
| Worktree cleanup fails | Report the failure; check if the worktree is still in use by a background process |
| Review findings are too numerous | Prioritize critical findings (security, performance, architecture); defer style to a follow-up issue |

## After Closing

- [ ] Confirm the issue is marked as closed on GitHub
- [ ] If using a worktree, verify cleanup with `git worktree list` (should not show the old worktree)
- [ ] Mention the issue in your project's release notes or changelog if applicable

---

**Time estimate**: 30–60 min per issue (depending on scope and review findings)  
**Dependencies**: Git, project's test framework, verification tools, code review skill/tool
