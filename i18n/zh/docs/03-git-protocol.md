> **机器翻译。**日文原文（[03-git-protocol.md](../../../docs/03-git-protocol.md)）是正本 — 本页与原文不一致时，以日文为准。

# L0 git纪律 — 防止物理冲突的层

这是**多个会话 / 多个 agent 并行操作同一个仓库**这一前提下的纪律（2026-07-03 达成一致・2026-07-21 契约化）。
每条规则都带有稳定的 rule ID（`L0-1`〜`L0-9`）。摘要侧（[docs/04](04-adoption.md)）会引用这些 ID。无法验证时应采取的姿态见 [docs/05](05-fail-posture.md)。

## L0-1 开工前确认是否有重叠 + 声明 WIP（Issue = 软锁）

```bash
gh issue list --state open
gh pr list --state open
```

先用上面的命令确认是否存在重叠，然后在负责的 Issue 上写下 WIP 评论（[模板](../templates/issue-template.md)）。

WIP 声明作为软锁生效的前提是，**必须具备4个必填字段**，且缺一不可：
`agent / date / Files to touch / Branch`

缺少字段的 WIP 作为锁是无效的——应视为范围不明，与该 lane 相关的工作一律串行处理（[FP-7](05-fail-posture.md)）。其他会话不应着手与有效 WIP 的文件集合存在交叉的工作。

## L0-2 声明路径的语义 — 未声明的不要碰（default-deny）

- 路径是**相对仓库根目录**的。文件名只指向那一个文件。以斜杠结尾的目录则覆盖其下的全部内容
- 禁止使用 glob・否定（`!` 排除）
- 声明为 `Files to touch: UNKNOWN` 的 lane **只能串行**（不可并行）
- **未声明的文件视为范围外**（default-deny）。如果确实需要碰到范围外的文件，必须在对该文件*首次写入之前*重新声明 WIP，并重新做一遍与并行方的交叉检查（[L2-4](01-milestone-loop.md)）
- **实际生效的文件集合**（无论是声明还是交叉判定）都要把 rename 涉及的两个路径・删除操作・lockfile・生成物都计算在内
- **乐观式重读** — 在 lane 的首次写入之前，要重新读取当前所有活跃的 WIP；如果在 GO 判定之后出现变化（WIP 增减・声明内容变更・重新声明），要重新做一遍交叉判定

## L0-3 锁的失效与交接（stale = 72h / TAKEOVER）

锁会失效的情形包括：branch 已被 merge / 删除・stale・出现 `RELEASE` 评论・出现 `HANDED-OFF` 评论。
`RELEASE` / `HANDED-OFF` 是**锁生命周期上的评论**，并不是 L1-4 所说的 lane 状态（格式见[模板](../templates/issue-template.md)）。**只有锁的所有者（WIP 中的 agent）才能发出这两种评论**——其他人发出的无效，其他人想解开锁只能走 stale + TAKEOVER 这一条路径。

- **stale = 72h 内无声明/更新**（以 GitHub 评论的时间戳来衡量——只要写一条新评论就算完成更新。不要为了衡量 staleness 而新增独立的时间戳字段：不要重复维护平台已有的元数据。WIP 声明本体里的 `date` 字段仍按 L0-1 的规定是必填项）。如果某个 lane 事先就知道会有较长时间的沉默，可以在声明 WIP 时**附上理由**明确标出较长的时间窗（这是例外情况，不是默认设置。事后延长要以新评论的形式公开进行）
- **stale ⇒ 所有者不明 ⇒ 不能默默当作空闲处理**。接手 stale lane 的流程是：走一遍 L0-9 复工检查清单 + 引用该 stale WIP 的 **`TAKEOVER` 评论** + 重新声明 WIP
- 调整 72h 这个数字，只能**通过对本手册的 PR**、并以运营数据（每周 probe）为依据来进行（不能在 lane 内部随意更改）。不可调整的是「不能默默放任 stale 自由化」这一不变量本身

HOLD **不属于**锁的失效事由（非终态——[L1-5](02-issue-loop.md)）。HOLD 评论必须明确写出**锁的处理方式**（保留到 review-by 为止，还是解除）——对锁只字未提的 HOLD 是无效的。

## L0-4 1个会话 = 1个 Issue = 1个 branch = 1个 worktree

每个 lane / 每个 worktree**只能有一个活跃的写入方**。不要在共享的 checkout 上工作：

```bash
git worktree add ../<repo>-wt/<issue> -b fix/<issue>-<slug> origin/main
```

## L0-5 main 只用于合并

禁止直接 push 到 main。一律通过 PR。

## L0-6 PR 正文中要写明触及的文件列表 + 与 diff 核对

要让审查时能看到与 WIP 声明之间的差异（比声明多出来/少掉的文件）。
merge 时要将声明的文件集合与 `git diff --stat` 做核对——**出现在 diff 里但不在列表里的文件属于 blocking**（属于[L1-7](02-issue-loop.md)完成证据关卡的一部分）。

## L0-7 一次只合并一个

```
git fetch → rebase origin/main → 重新验证（typecheck / tests）→ merge
```

merge 之后，要尽快让其他处于 open 状态的分支执行 rebase。不要同时 merge 两个。
**相邻的 PR 一旦被 merge，排在队列中等待的 PR 就有义务执行 rebase + 重新验证（重新跑 typecheck / tests）**——仅仅是 rebase 通过并不代表已经履行了这项义务。

## L0-8 分支要小而短命

存活时间长的分支会陷入 rebase 地狱。需要暂缓合并的 PR 要用 **HOLD 评论**（必填字段见 [L1-5](02-issue-loop.md)）明确标出状态，不要默默搁置。

## L0-9 复工检查清单 — 复工 / 交接 lane 首次写入前

在复工 / 交接 / TAKEOVER 的 lane 中，必须**在首次写入之前**，将以下4项确认结果整合成一条 Issue 评论发出（[模板](../templates/issue-template.md)）：

1. **锁** — 是否属于自己，依据 L0-3 判断是否已失效
2. **文件范围** — 声明的文件集合对照当前的 origin/main 是否依然准确，**并且**是否与当前所有活跃的 WIP/PR 都不存在交叉（重新执行 `gh issue list` + `gh pr list --state open`。这一项其实是把「我声明的范围是否依然有效？」这一个关口，捆绑了两次查询）
3. **branch** — fetch / rebase 是否能干净通过（如果落后了・或在 merge 之前，要执行 rebase）
4. **Done when** — 相较交接时是否有变化

一旦发现不一致：修复 / 交接・TAKEOVER / 改为串行，三选一。**绝不能在其他 agent 存活的锁之上默默继续。**
检查清单**固定为这4项**。发出的评论本身就是可审计的成果物，不要增加项目（「检查清单疲劳」是被明确点名的失败模式）。

## 出现事故时

- 出现 conflict → 不要慌，用 rebase 解决。如果解决过程变得很大，就把这个事实评论到 Issue 上，切换为串行
- 出现需要碰范围外文件的情况 → **在写入之前**先重新声明 WIP，再重新做交叉检查（L0-2）
- 不小心 push 到了 main → 用 revert commit 撤销，并把经过记录到 Issue 上
