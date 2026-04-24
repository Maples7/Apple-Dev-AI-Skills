---
description: "Use when editing README.md, CONTRIBUTING.md, or .github docs in this repository. Keeps README fully user-facing, moves generic maintenance and development guidance into CONTRIBUTING.md, and keeps private or local-only maintainer notes under gitignored paths in .github/."
applyTo:
  - README.md
  - CONTRIBUTING.md
  - .github/**/*.md
  - .github/.gitignore
---

# Repository Doc Boundaries

- Keep `README.md` fully user-facing.
- `README.md` is for discovery, installation, compatibility, available skills, and where users should look next.
- Do not put maintainer workflow, pre-push caveats, validation steps, local development notes, or repository housekeeping guidance in `README.md`.

- Put generic repository maintenance and development guidance in `CONTRIBUTING.md`.
- Use `CONTRIBUTING.md` for contribution flow, validation expectations, open-source hygiene, and repo-wide authoring rules.
- Do not duplicate a skill's detailed workflow in `CONTRIBUTING.md`; keep skill-specific operational guidance inside that skill folder.

- Treat `.github/` as the home for repository metadata, templates, automation, and optional maintainer-only notes.
- Private or local-only maintainer notes under `.github/` must live in gitignored paths or filenames.
- Do not place personal machine-specific constraints, private prompts, or local-only experiments in tracked user-facing docs.

- When moving content between files, preserve the boundary rather than copying the same guidance into multiple places.
- When in doubt: users read `README.md`, contributors read `CONTRIBUTING.md`, and private local notes stay under gitignored `.github/` paths.
