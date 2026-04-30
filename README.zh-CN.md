# Apple Dev AI Skills

[English](./README.md) | [简体中文](./README.zh-CN.md)

适用于 Apple 平台工作的可安装 AI 技能集合。

当你希望在 Xcode 字符串目录、App Store 截图、App Store 元数据以及 git 提交信息这些任务上获得更专业的帮助，而不必每次都重新解释工作流时，可以使用这个仓库。

## 这个仓库能解决什么问题

- 用可复用、任务明确的技能替代一次性提示词，更快完成交付。
- 让 Apple 平台相关工作流在不同项目、版本和协作者之间保持一致。
- 既可以只安装单个技能完成特定任务，也可以一次安装完整技能目录。

## 快速安装

安装完整集合：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills
```

只安装一个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

全局安装：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills -g
```

## 技能列表

按对大多数用户的实用价值排序，优先展示最直接、最偏 Apple 工作流的技能。

### `translate-xcstrings`

翻译或规范化 Xcode `.xcstrings` 字符串目录，同时避免破坏占位符、格式，以及 `InfoPlist.xcstrings`、`AppShortcuts.xcstrings` 这类 Apple 特定文件。

它的价值在于：本地化工作重复、脆弱，而且返工成本高。这个技能把它变成一个更安全、可重复执行的流程。

[打开技能目录](./skills/translate-xcstrings)

只安装这个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill translate-xcstrings
```

### `app-store-preview-pipeline`

通过先验证再扩展的流程来规划和生成 App Store 截图，包含稳定的示例数据、审核检查点、自动化挂钩以及最终导出指引。

它的价值在于：截图制作通常会在最后阶段变得混乱。这个技能提供的是一套可复用流水线，而不是又一次临时拼凑的截图流程。

[打开技能目录](./skills/app-store-preview-pipeline)

只安装这个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill app-store-preview-pipeline
```

### `eas-app-store-metadata`

使用 EAS CLI 以本地版本化工作流管理 App Store Connect 元数据，覆盖 `store.config.json`、版本说明、截图、校验以及更安全的推送前审查。

它的价值在于：元数据漂移很容易被忽略，清理起来也很痛苦。这个技能让商店列表相关变更在 git 中保持可审查、可重复。

[打开技能目录](./skills/eas-app-store-metadata)

只安装这个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill eas-app-store-metadata
```

### `pre-commit-review`

在执行 `git commit` 之前，从性能、用户体验、测试覆盖、架构、代码风格、安全与隐私、以及文档七个维度审查未提交的 Apple 平台改动，并输出按严重度分级的结构化报告。

它的价值在于：常见的提交前检查要么是 linter，要么是自由形式的代码评审。这个技能给 Swift / SwiftUI 改动提供了一次聚焦、可复用的分级审查，能在同一遍中点出性能风险、UX 回归、测试缺口、分层与风格漂移、表层安全与隐私问题、以及遗漏的文档更新。

[打开技能目录](./skills/pre-commit-review)

只安装这个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill pre-commit-review
```

### `commit-message`

结合当前 diff 和会话上下文，起草高质量的英文 Conventional Commit 提交信息，并支持 scope、footer 以及 monorepo 约定。

它的价值在于：适用面很广，但相比上面的技能没有那么强的 Apple 专属性。适合在你想更快写出干净、统一的提交信息时安装。

[打开技能目录](./skills/commit-message)

只安装这个技能：

```bash
npx skills add Maples7/Apple-Dev-AI-Skills --skill commit-message
```

## 兼容性

本仓库遵循 [Agent Skills specification](https://agentskills.io/specification)。

- 最适合支持基于 `SKILL.md` 技能格式的客户端。
- 如果你的客户端暂不直接支持 `SKILL.md`，可以先使用 [adapters/](./adapters) 中的适配包装。

## License

MIT。详见 [LICENSE](./LICENSE)。
