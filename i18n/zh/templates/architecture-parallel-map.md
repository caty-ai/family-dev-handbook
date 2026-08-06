> **机器翻译。**日文原文（[architecture-parallel-map.md](../../../templates/architecture-parallel-map.md)）是正本 — 本页与原文不一致时，以日文为准。

# 并行安全地图模板（添加到各仓库 ARCHITECTURE.md 的章节）

```markdown
## 并行安全地图 (Parallel Safety Map)

> 并行 GO 判定（family-dev-handbook L2-4）的判断依据。
> 合并改动模块边界的 PR 时，应在同一个 PR 中同步更新此地图。

### 模块边界

| 模块 | 路径 | 主要职责 | 备注 |
|---|---|---|---|
| <!-- 例: iOS app --> | `ios-app/` | UI・语音输入输出 | |
| <!-- 例: gateway --> | `gateway/` | 会话管理・LLM 中转 | |

**不跨越边界的 Issue 之间原则上可以并行**（文件集合的交叉检查是必须的）。

### 热点区域（并行时需注意的文件）

| 文件 | 大致行数 | 混杂的职责 | 拆分 Issue |
|---|---|---|---|
| <!-- 例: MainView.swift --> | 2,500+ | UI + 手势 + 引擎调用 | #NNN |

**触碰热点区域的 Issue，不与同模块的其他 Issue 并行。**
优先消化拆分 Issue（这是对并行可能性的投资）。

### 大范围 Issue 的历史记录

| Issue | 内容 | 执行时期 | 是否单独执行 |
|---|---|---|---|
| <!-- 例: #NNN --> | UI 全面重构 | | |
```
