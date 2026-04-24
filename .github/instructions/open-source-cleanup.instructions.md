---
description: "Use when preparing tracked files for commit, release, or open-source publication. Prevents private paths, private terminology, temporary install commands, and local experiment content from entering shared files."
applyTo:
  - README.md
  - CONTRIBUTING.md
  - skills/**/*.md
  - skills/**/*.yaml
  - skills/**/*.yml
  - adapters/**/*.md
  - .github/**/*.md
  - .gitignore
  - .github/.gitignore
---

# Open-Source Cleanup

- Treat every tracked file in this repository as publishable.
- If a statement is only true on one machine, in one local checkout, or before one pending push, it does not belong in shared user-facing docs.

- Remove machine-local paths such as `/Users/...`, home-directory tool paths, and local checkout paths.
- Remove private project names, private source-material terminology, and leftover references copied from non-public repos unless they are intentionally public.
- Remove temporary install or test commands that depend on unpublished state, local-only scripts, or one-off experiments.

- Keep local experiments, personal AI prompts, and scratch notes under gitignored paths such as `.github/local/`, `.github/private/`, `*.local.md`, or `*.private.md`.
- Do not mention local-only maintenance workflow in `README.md`.

- Before finalizing a change, search tracked files for:
  - absolute paths
  - private repo names or app names
  - temporary install commands
  - references to local experiments or unpublished state

- Public installation examples should use a public repo URL, a public GitHub shorthand, or a clearly generic placeholder when a public address does not yet exist.
