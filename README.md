# Apple Dev AI Skills

Build better Apple apps, faster.

A growing catalog of installable AI skills for Swift, SwiftUI, Xcode, testing, automation, and App Store delivery.

## Quick Install

Install the full collection:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills
```

Install a specific skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

Install globally:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills -g
```

The same CLI also accepts the full GitHub URL:

```bash
npx skills add https://github.com/Maples7/Apple-Dev-AI-Skills
```

If your client does not use `npx skills add`, copy the relevant skill folder into one of that client's supported skill locations.

## Skills

### `translate-xcstrings`

Translate or normalize Xcode `.xcstrings` catalogs, including `Localizable.xcstrings`, `InfoPlist.xcstrings`, and `AppShortcuts.xcstrings`.

[Open skill folder](./skills/translate-xcstrings)

Install only this skill:

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

## Compatibility

This repository follows the [Agent Skills specification](https://agentskills.io/specification).

- Works best with clients that support `SKILL.md`-based skills.
- For clients without native `SKILL.md` support, use the wrappers under [`adapters/`](./adapters) or convert the skill into that client's native rule or prompt system.

## License

MIT. See [`LICENSE`](./LICENSE).


