---
description: "Use when adding a new skill, scaffolding a skill folder under skills/, or updating the README skill catalog. Enforces the minimum structure for skills/<name>/SKILL.md, references/, assets/, and concise catalog entries."
applyTo:
  - README.md
  - skills/**/SKILL.md
  - skills/**/references/**
  - skills/**/assets/**
---

# Add New Skill

- Put each canonical skill under `skills/<skill-name>/`.
- The folder name and the `name` field in `SKILL.md` must match exactly.
- Use lowercase, hyphenated skill names.

- Minimum expected structure:
  - `skills/<skill-name>/SKILL.md`
  - `skills/<skill-name>/references/` only when longer guidance is needed
  - `skills/<skill-name>/assets/` only when templates, config samples, or static resources are needed

- Keep `SKILL.md` focused on discovery and operating procedure.
- Put deeper reference material in `references/` instead of bloating `SKILL.md`.
- Put reusable templates or sample config in `assets/`.
- Do not put agent-specific wrappers inside the canonical skill folder; keep those under `adapters/`.

- In `README.md`, add one short catalog entry per skill.
- The catalog entry should link to `skills/<skill-name>/` and describe the skill in one sentence.
- Do not copy the full workflow, validation steps, maintainer notes, or long examples into `README.md`.

- New skills must stay publishable.
- Do not hardcode local paths, unpublished repo assumptions, or project-private terminology into shared skill docs unless they are intentionally public.
