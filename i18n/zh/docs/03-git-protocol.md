> **机器翻译。**日文原文（[03-git-protocol.md](../../../docs/03-git-protocol.md)）是正本 — 本页与原文不一致时，以日文为准。

# L0 git 纪律 — 防止物理冲突的层级

面向**多个会话 / 多个 agent 并行操作同一仓库**这一前提的纪律（2026-07-03 达成一致・2026-07-21 契约化）。
每条规则附带稳定的 rule ID（`L0-1`〜`L0-9`）。摘要侧（[docs/04](04-adoption.md)）引用该 ID。无法验证时的姿态见 [docs/05](05-fail-posture.md)。

## L0-1 着手前的重叠确认 + WIP 声明（Issue = 软锁）

```bash
gh issue list --state open
gh pr list --state open
```

先用上述命令确认是否有重叠，然后在负责的 Issue 上写 WIP 评论（[模板](../templates/issue-template.md)）。

WIP 声明作为软锁生效的前提是**必须同时具备4个必填字段**：
`agent / date / Files to touch / Branch`

缺少字段的 WIP 视为无效锁 — 按 scope 不明处理，与该 lane 相关的作业一律直列化（[FP-7](05-fail-posture.md)）。其他会话不得着手与有效 WIP 的文件集合存在交叉的作业。

## L0-2 声明路径的语义 — 声明之外的不要碰（default-deny）

- 路径为**相对于仓库根目录**。文件名仅指该文件本身。末尾带斜杠的目录覆盖其下所有内容
- 禁止使用 glob・否定（`!` 排除）
- 声明为 `Files to touch: UNKNOWN` 的 lane **仅限直列**（不可并行）
- **未声明的文件视为 scope 之外**（default-deny）。如需触碰，须在写入 scope 外文件的*首次操作之前*重新声明 WIP，并重做与并行方的交叉检查（[L2-4](01-milestone-loop.md)）
- **实际文件集合**中需将 rename 的双路径・删除・lockfile・生成物一并计入（无论是声明还是交叉判定）
- **乐观式重读** — 在该 lane 的首次写入前重新读取当前活跃的 WIP 群，若在 GO 判定之后出现变化（WIP 增减・声明内容变更・重新声明），需重做交叉判定

## L0-3 锁的失效与交接（stale = 72h / TAKEOVER）

锁失效的情形包括：branch 已 merge / 已删除・stale・`RELEASE` 评论・`HANDED-OFF` 评论。
`RELEASE` / `HANDED-OFF` 是**锁生命周期的评论**，并非 L1-4 所指的 lane 状态（格式见[模板](../templates/issue-template.md)）。**只有锁的所有者（WIP 中的 agent）才能发出这类评论** — 他人发出的无效，他人解除锁的唯一途径是 stale + TAKEOVER。

- **stale = 72小时内无声明/更新**（以 GitHub 评论的时间戳衡量 — 只需发一条新评论即可完成更新。不要为了测量 staleness 而新增独立的时间戳字段：不要重复平台自带的元数据。WIP 声明本体中的 `date` 字段仍按 L0-1 要求必填）。预计会长时间沉默的 lane，可以在 WIP 声明时**附带理由**明确一个更长的窗口（这是例外而非默认。事后延长需以新评论的形式明确可见地进行）
- **stale ⇒ 所有者不明 ⇒ 不得默认视为空闲**。接手 stale lane 的流程：L0-9 恢复检查清单 + 引用该 stale WIP 的 **`TAKEOVER` 评论** + 新的 WIP 声明
- 72小时这个数字的调整，只能基于运营数据（周度 probe）**在本手册的 PR 中**进行（不得在 lane 内部私自更改）。不可调整的是「不得默认放宽 stale」这一不变式本身

HOLD **不是**锁的失效事由（非终态 — [L1-5](02-issue-loop.md)）。HOLD 评论必须明确写出**对锁的处理方式**（保留至 review-by 或释放） — 对锁的处理保持沉默的 HOLD 视为无效。

## L0-4 1个会话 = 1个 Issue = 1个 branch = 1个 worktree

每个 lane / 每个 worktree **同时只能有一个活跃写手**。不要在共享 checkout 上作业：

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

## L0-5 main 仅用于合并

禁止直接 push 到 main。一律通过 PR。

## L0-6 PR 正文中附上触碰文件清单 + diff 核对

让与 WIP 声明的差异（比声明多出/少了的文件）在 review 时能被看见。
merge 时需将声明的文件集合与 `git diff --stat` 对照 — **diff 中存在但清单中没有的文件视为 blocking**（属于 [L1-7](02-issue-loop.md) 完成证据门槛的一部分）。

## L0-7 一次只合并一个

```
git fetch → rebase origin/main → 再検証（typecheck / tests）→ merge
```

merge 之后，其他 open 的 branch 应尽快 rebase。不要同时 merge 两个。
**相邻 PR 被 merge 后，排队等待的 PR 有义务执行 rebase + 重新验证（重新跑 typecheck / tests）** — 仅仅 rebase 通过并不等于履行了这项义务。

## L0-8 branch 要小而短命

存活过久的 branch 会陷入 rebase 地狱。暂缓合并的 PR 需通过 **HOLD 评论**（必填字段见 [L1-5](02-issue-loop.md)）明确状态，不要默默搁置。

## L0-9 恢复检查清单 — 恢复・交接 lane 首次写入前

在恢复 / 交接 / TAKEOVER 的 lane 上，**首次写入之前**，需将以下4项确认结果整理为一条 Issue 评论发布（[模板](../templates/issue-template.md)）：

1. **锁** — 是否属于自己，按 L0-3 判断是否已失效
2. **文件 scope** — 声明的文件集合对照当前 origin/main 是否依然准确，**并且**与当前所有活跃的 WIP/PR 是否不存在交叉（重新执行 `gh issue list` + `gh pr list --state open`。该项将「我声明的 scope 是否仍然有效？」这一个门槛捆绑了两次查询）
3. **branch** — fetch / rebase 是否能干净通过（若落后・merge 之前需要 rebase）
4. **Done when** — 自 handoff 以来是否发生变化

出现不一致时：修复 / handoff・TAKEOVER / 直列化，三选一。**不要在其他 agent 存活的锁之上默默继续。**
检查清单**固定为这4项**。发布的评论本身即是可审计的成果物，不要增加项目（清单疲劳已被明确列为一种失败模式）。

## 出现事故时

- 出现 conflict → 不要慌，用 rebase 解决。若解决过程变得庞大，需将此事实评论到 Issue 上并切换为直列
- 需要触碰声明之外的文件 → **写入之前**重新声明 WIP，并重做交叉检查（L0-2）
- 误将内容 push 到 main → 用 revert commit 撤回，并将经过记录到 Issue
