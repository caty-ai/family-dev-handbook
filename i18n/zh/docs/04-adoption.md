> **机器翻译。**日文原文（[04-adoption.md](../../../docs/04-adoption.md)）是正本 — 本页与原文不一致时，以日文为准。

# 导入方法 — 集成到各 Agent 环境

## 原则

- **正本是这个仓库**。各 Agent 在自己"始终加载的上下文位置"放置**摘要**，详细内容参照本仓库
- 摘要与本仓库内容不一致时，**以本仓库为准**。摘要一方应跟进修改
- 为了在模型变更后依然有效，应放在"始终会被读取的配置文件"中（不依赖特定模型的记忆或临时状态）

## 摘要块的规范

- **带版本刻印的紧凑摘要，其 owner 唯一是本页面（docs/04）**。下游副本（各 CLAUDE.md / AGENTS.md / system prompt）采用 owner-applies 方式——由干事 Agent 提出建议，由各运行时的 owner 自行贴入
- 下游本地摘要的修改，只能比正本**更严格，不允许放宽**（tighten only）。这一原则的跨 Agent 通用规范的 owner 是 family-os 的 operations-policy（config trust 一节 — 参见 [README](../../../README.zh.md) 的"Caty AI ファミリー"一节）。本页面是该协作协议的具体应用。若在没有 sister projects 的情况下导入，直接套用 tighten-only 原则即可
- 摘要不誊抄正文，仅用 **rule ID + 一行 posture** 来引用。ID 的定义正文在 docs/01〜03・05〜07，注释样式的字段 schema 在 templates/issue-template.md・templates/epic-template.md・templates/brief-template.md

## 各 Agent 的集成位置

不同运行时"始终会被读取的配置文件"各不相同。导入台账按以下形式维护：

| Agent | 始终加载的上下文 | 状态 |
|---|---|---|
| `<agent-a>`（例如：Claude Code 系） | `~/.claude/CLAUDE.md` 等用户全局配置（permanent 处理的章节） | 例如：✅ 已导入（YYYY-MM-DD） |
| `<agent-b>`（例如：常驻 agent 运行时） | 各 Agent 的 system prompt / 工作区的 `AGENTS.md` | 例如：✅ 已导入 — rule-ID 版通过 owner-applies 方式分发 |
| `<agent-c>`（例如：运维笔记驱动的 agent） | 运维笔记 / 技能集的参考文档 | 例如：⬜ 未导入 — 待分发摘要块 |

> 实际导入的活台账由各团队自行管理。导入对象增多后，请在自己的仓库中维护此表（也可以用 Issue 评论作为台账）。

## 用于分发的摘要块（可直接复制粘贴）

请将以下内容原样粘贴到各 Agent 始终加载的上下文中：

```markdown
## 并行开发协议摘要（handbook-revision: 2026-08-06 / owner: 贴入者本人姓名 / last-verified: 贴入日期）
正本: <本手册正本仓库 URL（如已 fork，则为 fork 目标）> — 不一致时以正本为准。
本摘要可以更严格，但不允许放宽。ID 的正文在正本 docs/01〜03・05〜07，样式见 templates/issue-template.md・epic-template.md・brief-template.md。

L2 并行可否: L2-1 目标一致・权重判断（迷茫时选偏重的一侧）・让设计变复杂的需求要重新质疑一次（删除的决定权在委托方） / L2-2 边界变更先行一个边界PR /
  L2-3 Issue 中必须预测将触碰的文件 / L2-4 并行GO=声明的文件集合互不相交 /
  L2-5 大范围Issue单独执行 / L2-6 热点区域需要并行安全地图+拆分投入
L1 Issue完成: L1-1 Issue-first / L1-2 Why・Done when・触碰文件预测 /
  L1-3 merge review=不同模型或不同Agent・禁止 self-approve /
  L1-4 lane 状态用 WIP/HOLD/MERGED/SUPERSEDED/ABANDONED 这5个词汇・状态不明=按非活动处理 /
  L1-5 HOLD 必须包含 owner/reason/review-by/lock disposition/剩余工作或后继方案 /
  L1-6 重试次数有限・用尽后需带证据转为 HOLD/ABANDONED / L1-7 merge 必须有完成记录（Done when→PASS/FAIL/附理由的N/A・
  证据・候选SHA・diff核对） / L1-8 更正需以替换记录方式进行（禁止悄悄修改） /
  L1-9 Epic・架构・需求在实施前需要异构 review（单个Issue不强制要求） /
  L1-10 席位需相互异构+writer异构・设计者/实现者不计入席位・合格模型名单为本地配置・记录 requested/actual /
  L1-11 席位数 S/M=异构2・L/H=异构3・高风险领域=5（优先级高于规模）・Epic上游=实施着手前需L/H・无法确保席位时需owner批准的降级或SEAT-WAIT
L0 git: L0-1 确认无冲突+WIP 4个字段（agent/date/Files to touch/Branch）=软锁 /
  L0-2 不触碰声明之外的内容・UNKNOWN=串行 / L0-3 stale=72小时・接手需TAKEOVER+复核清单+重新声明WIP /
  L0-4 1个session=1个Issue=1个branch=1个worktree / L0-5 main 只用于merge /
  L0-6 PR 需附文件清单+diff核对 / L0-7 merge一次一个 / L0-8 branch保持短命・明示HOLD /
  L0-9 恢复・交接需先在Issue中发布4点检查清单再撰写
B 委托简报: B-1 实质性委托（实施・修复・生成）必须包含3层（实施规格/实施检查/review标准・样式见brief-template.md） /
  B-2 一次性调查・简短提问可豁免・迷茫时应附上 / B-3 Issue为正本・简报为衍生物（不一致时先修正Issue） /
  B-4 上下文需前置提供・不让受托方自行探索・review委托需指明最坏的失败形态・独立席位间不得混入结论 /
  B-5 标题需保持可机器判定的固定字符串形式・即使没有检查环境该契约依然有效
E Epic lane: E-1 Epic经owner的kickoff批准后成立（批准前按普通Issue运作） /
  E-2 功能轴Epic×模块轴子Issue・先行冻结契约#0并在Epic内串行直至merge完成 /
  E-3 人工检查点表=仅在事先约定的节点停止・高风险领域+契约级偏离为必须行・
  表的放宽需owner重新批准前旧表持续有效・无表=Epic不成立 /
  E-4 epic整合分支・子→epic以每次一个PR合并・向main默认在完成时合并一次（中途merge需事先记载+作为全量gate的例外） /
  E-5 sandbox自由权=除明确列举的禁止事项外均自由（禁止直接push main・超出范围・跨lane操作・改写epic历史・外泄机密・未经批准执行CP） /
  E-6 沙漏式review：设计=每个Epic一次（实施着手前）・实施=按子任务权重进行轻量gate（高风险子任务优先5席位・保持证据底线：
  merge时head一致SHA・diff核对・identity・inline证据）・整合=epic→main执行完整L1-7 /
  E-7 Epic日志（必须列出未达成项・妥协点）+最终确认摘要 /
  E-8 生命周期1〜2周（起点=kickoff批准）・staleness使用L0-3的独立计时 / E-9 终止同样使用5个词汇・ABANDONED必须处理分支+收敛子任务 /
  E-10 Epic并行=子任务声明的并集∪EPIC WIP声明・比照L2-4处理
FP: 无法验证时转为串行（写入・merge 也一律倒向停止一侧）。fail-open 并不意味着"通过"。Epic检查点表不存在或未获批准时应上报给人工处理（FP-9）。（详情见正本 docs/05）
```

## 仓库侧的准备工作

对于新仓库（或首次应用本协议的仓库）：

1. 在 `ARCHITECTURE.md` 中创建"并行安全地图"章节（[模板](../templates/architecture-parallel-map.md)）
2. 将 Issue 模板（[templates/issue-template.md](../templates/issue-template.md)）放入 `.github/ISSUE_TEMPLATE/`（可选但推荐）
3. 全员共同遵守避免直接 push main 的运作方式（若能设置 branch protection 则设置）

## 角色分工由各 Agent 自行决定

实施 / review / 验证分配给哪个模型・工具，交由各 Agent 的工具链自行决定（例如：implementer=Codex / reviewer=GLM / verifier=Claude 这样的不同模型三角色配置）。**需要遵守的是协议本身（3层 + 交叉review + fail-posture），而不是具体工具的选型。**
