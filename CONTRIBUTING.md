# Contributing

This repository is meant to stay publishable, reusable, and safe to copy into different coding-agent environments.

## Scope Split

Keep repository-level docs and skill-level docs separate.

- `README.md` is for people discovering, browsing, and installing skills.
- `skills/<skill-name>/` is the canonical home for that skill's workflow, assets, and references.
- `adapters/` contains compatibility wrappers for clients that do not natively load `SKILL.md` folders.

Do not turn the root README into a maintainer handbook or duplicate a skill's detailed workflow there.

## Authoring Rules

- Do not add machine-local absolute paths.
- Do not hardcode user-profile-specific tool locations into shared docs.
- Do not assume one private installer or one local workflow is the repository standard.
- Keep adapters optional and secondary; the canonical source remains the skill directory.
- Keep project-specific policy inside the relevant skill, not in repository-level docs.

## Adding A New Skill

1. Create a new directory under `skills/<skill-name>/`.
2. Add a `SKILL.md` file whose `name` matches the folder name.
3. Put extended references in `references/` and templates or static resources in `assets/` when needed.
4. Add adapters only when a target client lacks native `SKILL.md` support or needs a better native wrapper.
5. Add a short catalog entry to `README.md` without copying the full skill workflow into it.

## Validation

Validate one skill directory at a time.

Recommended checks:

- validate frontmatter and folder structure with an Agent Skills validator such as `skills-ref`
- confirm all referenced files remain relative to the skill root
- test discovery in at least one documented target client when practical
- ensure no private machine-specific data appears in shared files

Example:

```bash
skills-ref validate skills/<skill-name>
```

## Local Maintainer Notes

If you keep personal AI prompts, maintenance notes, or local-only experiments for this repository, store them under gitignored paths inside `.github/`.

Default ignored patterns are documented in [`.github/.gitignore`](./.github/.gitignore).

## Open-Source Hygiene

Before publishing or merging:

- search for machine-local paths such as `/Users/...`
- search for project-private names copied in from source material
- search for references to private helper scripts or local-only install flows
- make sure repository-level docs still read as generic documentation for future users
