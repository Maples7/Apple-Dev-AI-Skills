# Report Template

Always produce the report in this exact structure. Keep it short, actionable, and grouped by lens.

## Format

```
## Pre-Commit Review

**Scope:** <staged | working | branch <base>>
**Files reviewed:** <N> (<list or summary>)
**Recommendation:** <proceed | proceed-with-followups | hold>

### Performance
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on impact>
  - Fix: <concrete suggestion, no code rewrite>

### User Experience
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on user impact>
  - Fix: <concrete suggestion>

### Test Coverage
- [<severity>] <file or behavior> — <one-line gap>
  - Suggested test: <framework> · <test name> · <arrange / act / assert>

### Architecture
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on layering / abstraction / module-boundary impact>
  - Fix: <concrete suggestion, no code rewrite>

### Code Style
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on consistency / best-practice / readability impact>
  - Fix: <concrete suggestion>

### Security & Privacy
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on security / privacy impact>
  - Fix: <concrete suggestion>

### Documentation & Comments
- [<severity>] <file>:<line-range> — <one-line finding>
  - Why: <one sentence on doc-hygiene impact>
  - Fix: <concrete suggestion>

### Notes
- <anything else worth flagging: skipped checks, broad diff, missing profile, etc.>
```

## Rules

- Use the severity tokens exactly: `blocker`, `major`, `minor`, `info`.
- One bullet per finding; do not combine multiple files into one bullet.
- Cite file paths relative to the repository root and include line ranges from the diff.
- If a lens has zero findings, write `- No findings.` under that section — do not omit the section.
- The `Recommendation` line is mandatory and must be one of:
  - `proceed` — no `blocker` or `major` findings.
  - `proceed-with-followups` — no `blocker`, but `major` items should be tracked.
  - `hold` — at least one `blocker`.
- When the diff is too broad to review in one pass, set `Recommendation: hold` and ask the user to split the commit before scoring further.
- Do not include code blocks of replacement code. Suggestions are described in prose.
- Do not invoke `git commit` or any mutating command at any point.
- Write prose (finding descriptions, `Why:` / `Fix:` sentences, `Notes`) in the user's current session language. Keep these anchors in English verbatim: section headings, field labels (`Scope:`, `Files reviewed:`, `Recommendation:`, `Why:`, `Fix:`, `Suggested test:`), severity tokens (`blocker` / `major` / `minor` / `info`), and recommendation tokens (`proceed` / `proceed-with-followups` / `hold`).
