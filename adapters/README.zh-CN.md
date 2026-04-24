# Adapters

[English](./README.md) | [简体中文](./README.zh-CN.md)

这个目录存放的是轻量级包装层，适用于那些不能原生发现 `SKILL.md` 文件夹的代理客户端。

规范且权威的内容仍然以 `skills/` 目录下的技能为准。

## 当前适配策略

- Copilot / VS Code：直接安装规范技能目录。
- Claude Code：直接安装规范技能目录。
- 其他代理：先从一个镜像规范工作流的单文件 prompt 包装器开始，再按目标代理的规则系统或提示词系统进行适配。

当前提供的包装器：

- [generic/translate-xcstrings.prompt.md](./generic/translate-xcstrings.prompt.md)
- [generic/commit-message.prompt.md](./generic/commit-message.prompt.md)
- [generic/app-store-preview-pipeline.prompt.md](./generic/app-store-preview-pipeline.prompt.md)
- [generic/eas-app-store-metadata.prompt.md](./generic/eas-app-store-metadata.prompt.md)
