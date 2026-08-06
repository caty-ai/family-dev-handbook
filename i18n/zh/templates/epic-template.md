> **机器翻译。**日文原文（[epic-template.md](../../../templates/epic-template.md)）是正本 — 本页与原文不一致时，以日文为准。

# EPIC Issue / Epic 通道 模板

Epic 通道（[docs/06](../docs/06-epic-lane.md)・E-1〜E-10）字段模式的正本。单个 Issue、WIP/HOLD 等评论格式仍沿用 [issue-template.md](issue-template.md)（Epic 内的子 Issue 也使用该文件）。

## EPIC Issue 正文（E-1 / E-2 / E-3 / E-10）

```markdown
## 目的 (Why) — 机能轴

<!-- 用人话写出价值。不是模块名，而是"能实现什么" -->

## 完成条件 (Done when) — Epic 层级

- [ ] <!-- 以能在整合状态下判定的形式描述（不要简单加总子项的 Done when） -->
- [ ] 整合审查（E-6③ 完整 L1-7）通过・epic→main 合并

## 子 Issue 一览 — 模块轴

<!-- 1 个子项 = 1 个模块或 1 个仓库。依赖关系用 Blocked-by 表示。
     契约冻结的第 0 号仅在触碰模块边界接口的 Epic 中为必须项（E-2）— 不涉及此类接口的 Epic 可省略第 0 行，
     E-3 的契约级判定通过 Done when・外部 IF 描述来进行 -->

| # | Issue | 模块 / 仓库 | Blocked-by |
|---|---|---|---|
| 0 | #<n> 契约冻结（边界接口确定） | <对象> | — |
| 1 | #<n> | <对象> | #0 |

## 实效声明集合（E-10 — 子项声明集合的并集 ∪ EPIC Issue 的 WIP 声明集合）

<!-- 用于 Epic 之间・与 Epic 外通道之间并行 GO 判定（准用 L2-4）的输入。随子项的增减、epic worktree 的整合作业对象（E-4 的 WIP）而更新 -->

- path/to/module-a/
- path/to/module-b/

## 人工检查点表（E-3 — 必须项）

<!-- 必须触发项（高风险领域的全部项 + 契约级偏离）必须列为对应行（若无对应情况，也要写明"无对应"）。
     添加行可由 agent 单独完成（但若内容缩小了现有行的范围，则视为放宽处理）。删除・放宽行需经 owner 重新批准前，旧表始终有效（FP-8 / L1-8）。
     通过批准仅限 owner 的明确评论 —— 仅改写状态栏本身不构成批准（E-3 / FP-8） -->

| # | 在哪里停下 | 需要展示什么 | 为何需要人工判断 | 状态 |
|---|---|---|---|---|
| 1 | <例：子#3 完成后・对外公开前> | <例：预发布 URL + 差分摘要> | 对外公开（高风险领域） | 未到达 / 已批准 YYYY-MM-DD + 批准评论 URL |

## 启动批准（E-1 — Epic 成立的凭证）

<!-- 附上 owner 批准评论的链接。批准前 Epic 尚未成立（无 E-4/E-5 的特权・FP-9）。
     设计审查的截止时间与 L1-9/E-6① 使用同一时钟（最晚不得晚于第一个子 Issue 开始实施前）— 不要另设独立截止时间。
     若启动时尚未进行，需写明"未实施"，且在完成实施并记录之前不得开始子项实施（L1-9 fail-closed） -->

- 设计审查记录（E-6①/L1-9 — 席位・requested/actual・verdict）: <URL 或"未实施（须在第一个子项开始实施前完成）">
- 批准评论: <URL>（YYYY-MM-DD）
```

## Epic 日志评论（E-7 — 每当子 Issue 终止时发到 EPIC Issue）

```markdown
📦 Epic log (<agent 名>, YYYY-MM-DD): 子 #<n> 终止

- 已实现的内容: <1〜3 行>
- 证据: <子→epic PR 链接 + 要点（如测试结果的终值等）>
- Done when 未达成事项・妥协事项: <列举。若无则明确写"无" —— 不可省略>
- 下一步: <接下来动手的子 Issue / 等待项>
```

## 子→epic 轻量门禁记录（E-6② — 写在子→epic PR 正文中）

```markdown
## 轻量门禁记录 (E-6②)

candidate SHA: <commit SHA>   <!-- 必须与合并时的 PR head 一致。若审查后发生变化需重新审查（准用 E-6②・L1-8） -->
implementer: <agent/model>
reviewers: <席位1: agent/model（requested/actual）> <席位2: …>   <!-- 席位数按子项的重量参照 L1-11 表。触及高风险领域的子项需要 5 个席位 -->
identity check: <不同 model | 不同 agent>   <!-- L1-3。留空即为 blocking -->

测试结果（内联终值）: <例：24 passed / exit 0 / YYYY-MM-DD>
要点: <用文字说明对 Done when 的应对情况。可省略表格形式。仅有链接的证据不合格（维持 L1-7 的"记录本身即可读出终止结果"原则）>

声明 vs 实际 diff（L0-6 — 子→epic 中同样必须）:
git diff --stat <epic>...<候选SHA>: <输出或摘要>
与声明文件集合的差异: 无 | <差异及说明>   <!-- diff 中存在但未声明的文件属于 blocking -->
```

## Epic 终止评论（E-9 — 发到 EPIC Issue。适用 L1-4 的 5 个词汇）

```markdown
🏁 <MERGED|SUPERSEDED|ABANDONED> (<agent 名>, YYYY-MM-DD): <1 行>

- epic 分支的处理: 废弃（删除） | 抢救 PR <URL>（适用 E-6③ 门禁）
- 子 Issue 状态收敛: <各子项的终止状态或拆分为独立 Issue 的去向>
- worktree 清理: 已完成（YYYY-MM-DD）
- evidence / successor: <整合审查记录・后继 Issue 等>
```
