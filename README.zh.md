<div align="center">
  <img src="./assets/banner.svg" alt="Claude Code Wiki" width="100%">
</div>

# Claude Code Wiki

> **关于 Claude Code 架构、模式和竞争创新的完整指南 — 了解如何实现 2-5 倍更快的执行速度、无限对话内存和 90% 的成本节省**

[English](./README.md) | [Tiếng Việt](./README.vi.md) | **中文** | [Español](./README.es.md) | [日本語](./README.ja.md)

## 这个 Wiki 是什么

**Claude Code Wiki** 是理解 Claude Code 架构、工程模式和竞争优势的权威指南。通过分析 **512,000 行生产级 TypeScript 代码**，本 wiki 揭示了：

- **10 个架构创新**使 Claude Code 优于竞争对手
- **流式工具执行**在 LLM 流式传输时运行工具（UX 快 2-5 倍）
- **5 层上下文管理**实现无限对话内存
- **多代理编排**与缓存共享（降低 90% 成本）
- **React 终端 UI**在 CLI 中提供生产级 UX
- **AST 级安全**用于深度命令分析（非正则表达式）
- **生产工程模式**针对大规模经济优化

**这不仅仅是另一个 AI 编码工具** — 它由创建 Claude 的团队构建，拥有第一方 API 访问权限和竞争对手没有的优化机会。

## 为什么存在这个 Wiki

本 wiki 旨在记录使 Claude Code 出色的生产级模式和架构决策。了解它如何解决竞争对手难以解决的问题：

- **速度**：大多数工具在顺序运行工具之前等待 LLM 完成。Claude Code 在流式传输时并发运行工具，实现 2-5 倍更快的多工具操作。
- **内存**：竞争对手使用基本的上下文截断或需要手动清理。Claude Code 使用 5 层自动压缩管道实现无限对话。
- **成本**：运行多个代理成本高昂。Claude Code 的缓存分叉优化通过共享缓存实现 90% 的成本降低。
- **安全**：大多数工具使用正则表达式进行命令解析。Claude Code 使用 AST 级 Bash 解析进行深度安全分析。
- **规模**：为大规模经济而构建，在组织级别优化 Gtok/周。

本 wiki 记录了这些模式和技术，以便您可以学习并应用到自己的 AI 工具中。

## 你将学到什么

### 🚀 核心创新

1. **流式工具执行** - 如何在 LLM 流式响应时并发运行工具
2. **上下文管理** - 用于无限对话内存的 5 层管道与自动压缩
3. **多代理编排** - 6 个专门的代理与缓存共享架构
4. **提示缓存优化** - 在代理间实现 90% 成本降低的分叉模式
5. **React 终端 UI** - CLI 工具的生产级组件架构

### 🔒 生产工程

6. **AST 级安全** - 深度 Bash 命令解析和权限系统
7. **功能标志** - 零运行时成本的死代码消除
8. **启动优化** - 并行预取和延迟加载模式
9. **集成生态系统** - 双角色 MCP（客户端 + 服务器）、IDE 桥接、技能系统
10. **大规模思维** - 组织级别的成本优化（Gtok/周节省）

## Wiki 结构

```
claude-code-wiki/
├── docs/                           # 10 个综合 wiki 指南
│   ├── README.md                   # Wiki 导航和概述
│   ├── 01-competitive-advantages.md   # 10 个不公平优势
│   ├── 02-architecture-overview.md    # 系统设计和数据流
│   ├── 03-streaming-execution.md      # 实时工具执行
│   ├── 04-context-management.md       # 5层上下文管道
│   ├── 05-multi-agent-orchestration.md # 多代理系统
│   ├── 06-terminal-ux.md              # React 终端 UI
│   ├── 07-security-model.md           # AST 解析和权限
│   ├── 08-integration-ecosystem.md    # MCP、IDE 桥接、技能
│   ├── 09-production-engineering.md   # 优化模式
│   └── 10-lessons-learned.md          # 关键要点
└── claude-code/                    # 完整源代码（512K LOC）
    ├── src/                        # TypeScript 实现
    ├── skills/                     # 85+ 斜杠命令
    └── package.json                # 依赖和脚本
```

## 快速入门指南

根据您的目标导航 wiki：

### 🎯 构建 AI 编码工具

**从这里开始**: [竞争优势](./docs/01-competitive-advantages.md)

发现 10 个架构创新：
- 流式工具执行实现 2-5 倍更快的 UX
- 带缓存共享的多代理编排
- 无限对话的上下文管理
- 生产安全和成本优化

**然后探索**: [经验教训](./docs/10-lessons-learned.md) 获取可应用于您自己工具的可操作要点。

### 🔍 评估 Claude Code

**从这里开始**: [架构概述](./docs/02-architecture-overview.md)

了解系统设计和生产就绪性：
- 高级架构和数据流
- 核心子系统和职责
- 技术栈分析（Bun、React、TypeScript）

**然后审查**:
- [安全模型](./docs/07-security-model.md) 企业关注点
- [集成生态系统](./docs/08-integration-ecosystem.md) 可扩展性

### 💡 学习高级模式

**从这里开始**: [经验教训](./docs/10-lessons-learned.md)

获取生产级 TypeScript/React 的可操作模式：
- CLI 中的 React 架构
- 大规模状态管理
- 成本优化技术
- 大规模工程

**然后深入**:
- [终端 UX](./docs/06-terminal-ux.md) React/Ink 模式
- [生产工程](./docs/09-production-engineering.md) 优化技术

## Wiki 索引

| 指南 | 描述 | 关键主题 |
|------|------|----------|
| [01. 竞争优势](./docs/01-competitive-advantages.md) | 使 Claude Code 脱颖而出的 10 个创新 | 流式执行、缓存优化、AST 安全 |
| [02. 架构概述](./docs/02-architecture-overview.md) | 系统设计和数据流 | 核心子系统、技术栈、生产架构 |
| [03. 流式执行](./docs/03-streaming-execution.md) | 工具如何在 LLM 流式传输时并发运行 | 异步协调、错误处理、2-5 倍加速 |
| [04. 上下文管理](./docs/04-context-management.md) | 无限对话的 5 层管道 | 自动压缩、提示缓存、内存优化 |
| [05. 多代理编排](./docs/05-multi-agent-orchestration.md) | 6 个专门的代理与缓存共享 | 分叉模式、协调器模式、代理类型 |
| [06. 终端 UX](./docs/06-terminal-ux.md) | React 终端 UI 架构 | 组件设计、状态管理、85+ 命令 |
| [07. 安全模型](./docs/07-security-model.md) | AST 级 Bash 解析和权限 | 命令分析、沙盒集成、威胁模型 |
| [08. 集成生态系统](./docs/08-integration-ecosystem.md) | MCP、IDE 桥接和技能系统 | 双角色 MCP、VS Code/JetBrains、条件技能 |
| [09. 生产工程](./docs/09-production-engineering.md) | 优化模式和大规模思维 | 启动速度、功能标志、成本优化 |
| [10. 经验教训](./docs/10-lessons-learned.md) | 顶级要点和可借鉴的模式 | 可操作的见解、设计决策、权衡 |

## 关键统计

| 指标 | 值 |
|------|-----|
| **总代码行数** | ~512,000 |
| **TypeScript 文件** | ~1,900 |
| **内置工具** | 40+ |
| **斜杠命令** | 85+ |
| **代理类型** | 6 个专门 |
| **运行时** | Bun（高性能） |
| **UI 框架** | React + Ink |
| **Wiki 页面** | 10 个综合指南 |

## 这个 Wiki 适合谁

### 构建 AI 编码助手的开发者
学习流式执行、上下文管理和多代理编排的生产级模式。了解如何实现 2-5 倍更快的 UX 和 90% 的成本降低。

### 评估 AI 工具的产品团队
比较 Claude Code、Cursor、Continue 和 Aider 之间的架构方法。了解速度、成本和功能方面的可衡量竞争优势。

### 学习高级 TypeScript/React 的工程师
探索 CLI 中的 React 架构、大规模状态管理和来自 512K LOC 代码库的生产优化模式。

### 技术架构师
研究系统设计决策、安全架构和生产 AI 工具的大规模工程模式。

## Wiki 方法论

本 wiki 构建自：

- **完整源代码分析** Claude Code npm 包源映射（2026 年 3 月）
- **实践探索** 和测试所有主要功能
- **比较研究** Cursor、Continue 和 Aider 架构
- **代码级调查** 512,000 行 TypeScript
- **模式提取** 来自注释、类型和实现细节

所有文档都来自实际代码，而非营销材料或黑盒测试。

## 为 Wiki 贡献

发现有趣的东西？有额外的见解？本 wiki 是一个活文档，旨在捕获：

- 架构中的"哇"时刻
- 构建 AI 工具的可操作模式
- 设计决策和权衡
- 竞争见解和差异化

欢迎针对以下内容提交 Issues 和 Pull Requests：
- 额外的文档或更正
- 代码库中的新发现
- 模式解释和示例
- 与其他工具的比较见解

## 许可和归属

**源代码**: Claude Code 是 Anthropic 的专有软件。本 wiki 仅用于教育目的。

**Wiki 内容**: 文档和分析 © 2026。为教育和研究目的共享。

**方法论**: 源代码从 npm 源映射中提取，并通过代码审查记录，而非逆向工程。

---

**准备好学习了吗？** 从 [🔥 竞争优势](./docs/01-competitive-advantages.md) 开始，发现使 Claude Code 与众不同的 10 个创新。
