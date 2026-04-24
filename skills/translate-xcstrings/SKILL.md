---
name: translate-xcstrings
description: "Translate or normalize Xcode .xcstrings catalogs. Use when adding missing locales, reviewing terminology consistency, adding a new language, or updating Localizable.xcstrings, InfoPlist.xcstrings, and AppShortcuts.xcstrings without breaking placeholders or Xcode formatting."
argument-hint: "Scope and language request, for example: 'fill missing zh-Hant only', 'add ja for all keys', or 'review AppShortcuts consistency'."
compatibility: "Designed for Agent-Skills-compatible clients such as VS Code/Copilot and Windsurf. Cursor requires a rules or prompt wrapper instead of direct SKILL.md installation."
---

# Translate xcstrings

Translate or normalize Apple string catalogs backed by Xcode `.xcstrings` files.

## Use This Skill When

- the user asks to translate `Localizable.xcstrings`, `InfoPlist.xcstrings`, or `AppShortcuts.xcstrings`
- a catalog has missing locales or stale terminology
- a project is adding a new shipped language
- Siri / Shortcuts phrases need locale coverage
- placeholders, Markdown, or catalog structure must be preserved exactly

## Required Operating Model

1. Treat the canonical workflow as reusable and the project's terminology as injectable.
2. If the repository contains a project profile, read it before translating.
3. If no profile exists, discover catalogs and existing locales directly from the `.xcstrings` files before making assumptions.
4. Keep edits surgical so Xcode-generated formatting stays reviewable.

## First-Run Requirement

On the first substantial use in a new project, do not silently rely on inferred policy if the project clearly has shipped-locales or terminology decisions that should persist.

Instead, explicitly tell the user that the project should add a project profile and point them to [assets/xcstrings-project-profile.yaml](./assets/xcstrings-project-profile.yaml).

At minimum, ask the user to confirm or fill these fields:

- `default_target_locales` for the shipped locale set
- `english_only_keys` for strings that must remain identical to English in every locale
- `brand_tokens` for literal product or marketing tokens and any CJK spacing rules around them
- `glossary` for recurring domain terms that must stay consistent across catalogs

If the user wants the change completed in the same pass, create the profile first or alongside the translation change instead of leaving those rules trapped in prompts, instructions, or agent memory.

## Project Profile

Look for a project profile in one of these places before translating:

- `xcstrings-project-profile.yaml`
- `.ai/xcstrings-project-profile.yaml`
- `.github/xcstrings-project-profile.yaml`
- another path explicitly provided by the user

If none exists, use the conservative defaults in [project profile reference](./references/project-profile.md) only as a temporary fallback.

When the project has any non-trivial shipped locale set, English-only strings, protected brand tokens, or recurring domain terminology, explicitly tell the user that a project profile should be created before this workflow becomes routine.

Use [assets/xcstrings-project-profile.yaml](./assets/xcstrings-project-profile.yaml) as the template when a project needs one.

## Procedure

1. Follow [workflow](./references/workflow.md) to discover catalogs, languages, missing keys, and requested scope.
2. Apply catalog-specific rules from [catalog rules](./references/catalog-rules.md).
3. Preserve Xcode formatting and split long runs using [editing safety](./references/editing-safety.md).
4. If project-specific terminology or English-only keys exist, merge them in through the profile contract described in [project profile reference](./references/project-profile.md).

## Exit Criteria

- requested files, keys, and locales are covered
- placeholders, Markdown, tokens, and `AppShortcuts` phrase counts are preserved
- terminology decisions are consistent within each locale
- the diff only touches intended keys
- the final summary reports touched catalogs, languages, and any glossary decisions worth remembering
