# Message Rules

## Policy Precedence

- Repository commit-profile rules override generic preferences when both apply.
- If the profile is silent on a detail, fall back to standard Conventional Commit practice.
- If evidence is ambiguous, choose the most conservative valid message.

## Commit Format

- Always use Conventional Commits.
- Respect any allowed-type list from the profile.
- Prefer `type(scope): subject` when the profile requires a scope or when a useful scope is clearly supported by the diff.
- Choose the best fitting type: `feat`, `fix`, `refactor`, `perf`, `docs`, `style`, `test`, `build`, `ci`, or `chore` unless the profile narrows that list.
- Use `!` in the type or a `BREAKING CHANGE:` footer only for real breaking changes.

## Scope Selection

- If the profile requires scope, do not omit it.
- In monorepos, prefer the changed package, app, workspace, or feature area indicated by the profile.
- If multiple packages changed and the profile does not define a composite rule, choose the narrowest honest shared scope and note possible commit splitting.
- Do not invent a precise scope when the diff does not support one.

## Subject Line

- Write in idiomatic English, regardless of the conversation language.
- Use imperative mood.
- Keep the subject concise, with no trailing period.
- Aim for 50 characters or fewer and keep it under 72 characters.
- Keep the subject lowercase except for proper nouns, type names, or acronyms.

## Body

- Add a body when required by the profile or when the subject is not enough.
- Insert one blank line between the subject and body.
- Wrap lines around 72 characters.
- Explain why the change was made and any non-obvious impact.
- Do not restate the diff hunk by hunk.
- Use bullet points only when the body contains multiple independent changes.

## Footers

- Add footers required by the profile when the evidence is present.
- Put issue trailers on their own lines at the end.
- Use `BREAKING CHANGE: <explanation>` only when applicable.
- Do not add unsupported or speculative footers.
- Do not add AI attribution, emojis, or extra trailers unless the diff already contains them.

## Final Output

- Return the commit message in a single fenced code block with no language tag.
- If needed, add one short caveat line after the block, such as a suggestion to split unrelated changes or a note that conservative fallback rules were used.
- Do not include extra commentary before the message.
