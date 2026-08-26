> **机器翻译。**日文原文（[publication-checklist.md](../../../templates/publication-checklist.md)）是正本 — 本页与原文不一致时，以日文为准。

# 仓库公开检查清单

## 目的

这份检查清单是记录仓库公开车道以逐项判定与证据 artifact，通过 [PB-1](../docs/11-publication.md#pb-1) 门禁的正本。

⟨RS-n⟩ = 源自各家本地公开前门禁的出处注记。即使没有参照对象，每一项也是自成一体的。

条目 ID 不是 rule ID，但同样按稳定 ID 处理，新增放在各节末尾，删除则留空号。

## 版本规则

遵循 [PB-2](../docs/11-publication.md#pb-2)，原则上记录所参照的 handbook release tag，仅当在 tag 尚未包含该状态时运行，才记录 commit SHA，并在包含该状态的 tag 发布后把 tag 追记到完成记录。

```text
checklist version: <handbook release tag>
# タグ未包含時だけ
checklist commit: <full commit SHA>
checklist release tag (追記): <その状態を含む handbook release tag>
```

## 消费者步骤

1. 针对 A1〜E4 全部28项，收集各项指定的证据 artifact。
2. 在车道 Issue 的完成记录中恰好放置一份下表。判定为 `PASS` / `FAIL` / 带理由的 `N/A` 之一，证据栏记录各项指定的证据 artifact 本体或可解析的指针。

   ```markdown
   | ID | 判定 | 証拠 artifact | 注記 |
   |---|---|---|---|
   | A1 | PASS / FAIL / N/A（理由） | <項目指定の証拠> | <必要な補足> |
   ```

3. 在 public→private→public 的再公开中，引用最近一次完成记录，重走前次以后发生变化的项目，以及再公开可能改变结果的项目。新表须列出全部28项，复用的证据注明引用来源，重走的证据记录本次的 artifact。
4. 发现含混、不足或分类错误时，作为落差报告到 [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100)。

(c) 类项目所需时间的计测，只由 [PB-5](../docs/11-publication.md#pb-5) 所指的消费者车道进行。

(b) 类项目在机械化实现后，应把该行的手动步骤替换为 run URL。

分类栏保留 [Phase 2 确定版](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694) 的原文: **(a)** = 由今天既有的 handbook reusable 完成的机器检查，**(b)** = 可机械化但尚未实现，**(c)** = 只靠 owner 的标签或决定记录才能通过的人工判断。

## A — 仓库的初期构成（结构与入口）

| ID | 项目 | 分类 | 今天如何通过 | 证据 artifact |
|---|---|---|---|---|
| A1 | 从仓库创建之初就放置以 test 为 gate 的 CI（T-1）。CI 尚未整备时不得伪装成绿色，须在 README 中写明 `CI: not yet` | (b) — no bootstrap conformance check exists; T-1 is prose | 目视确认 test-lint caller 的存在，并执行。尚未整备时确认 README 中的 `CI: not yet` | test-lint caller 的首次 run URL，或 README 中明确写出的 `CI: not yet` |
| A2 | `make test` / `make lint` 的入口存在，且能传播终止代码（campaign rule 4。须确认强制失败时 make 会变成 Error） | (b) — checkable by a bootstrap script; today proven only by seat sandbox runs | 执行 `make test` 与 `make lint`，在隔离的作业状态中故意引入失败，确认返回非 0 终止代码 | 本地执行 transcript + 强制失败的证明 |
| A3 | 不把 lint target 设为 no-op。不把无法失败的 lint 藏在绿色徽章背后 | (b) — mechanizable as "lint job must have ≥1 failable step / placeholder-echo detector" | 临时引入 lint 违规，在隔离的作业状态中确认 lint 变红 | 引入 lint 违规的 mutation 会变红的证明 |
| A4 | 存在5个 gate caller（test-lint / pr-size / review-labels / gitleaks / history-check），均 pin 在 `@ci-v1`，与 `templates/ci` 的正本 byte-identical，且没有把扫描逻辑复制进仓库内 | (a) today the *identity* is seat-verified by hand; caller presence is machine-fact | 记录 5 个 caller 的首次 run URL，并将各文件的 SHA256 与正本比对 | 与正本的 SHA256 比对 + 首次 run URL |
| A5 | 接线 T-6 的 reconciliation，以 `require_suite_reconciliation: true` 启用。保持既定值 false 就是 inert gate | (b) — flag presence is greppable; today unchecked | 确认 caller 的输入值，执行 test-lint，确认摘要三值互相吻合 | 显示 `declared=N executed=N skipped=K` 的 green run |
| A6 | 登记 branch protection / required checks，让 gate 成为 blocking 而非仅供参考（确认 `branches/main/protection` 的状态） | (c) today (owner-only settings) / (b) verifiable half: a read-only API probe can red-flag absence | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | API probe 输出 + owner 行动的记录。`branches/main/protection` 的 404 无法区分"无保护"与"权限不足"，因此含混的 probe 结果不予通过。`rulesets` 也一并测量（Phase 1 §3.5 的实绩形式） |

## B — 展示的诚实性（README・徽章・数字）

| ID | 项目 | 分类 | 今天如何通过 | 证据 artifact |
|---|---|---|---|---|
| B1 | 绿色徽章只能由机器涂色。静态徽章遵循 T-7 的闭合颜色许可清单，全部徽章 URL 均可解析 | (b) — badge-lint (slug points at this repo, endpoint 200, color allowlist) is a concrete gap | 逐个徽章获取 URL，将目标仓库・HTTP 响应・静态颜色与 T-7 比对 | 逐个徽章的 curl transcript |
| B2 | 手写的实测值须附上日期与可解析的出处。以"没有日期的件数 = 0"为原则 | (c) with a (b) assist: a date-adjacency lint can flag bare numbers; truth needs a human | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | grep sweep + 记录 |
| B3 | 具备对应环境表 ⟨RS-1⟩、hero image ⟨RS-2⟩、带相互 nav 的4语言 README ⟨RS-4⟩、docs 的三层结构 | (b) — presence/cross-link lint is trivial; content quality stays (c) | 存在与相互链接通过运行 publication-gate 并记录目标文件清单来确认。内容质量仅以 owner 的标签 / 满足 PB-3 发行者要件的决裁记录通过 | publication-gate run（今天的部分适用范围）+ 文件清单 |
| B4 | 把 social preview 设为 1280×640 ⟨RS-3⟩，在 Settings 中把 description 设置为英语 ⟨RS-10⟩ | (c) — API-readable but set by owner; (b) probe possible | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | API probe（如 `gh api repos/OWNER/REPO --jq .description`） |
| B5 | 让关于 OS 的主张保持准确，并让 skip 可见。使用 `run_macos` / `macos_skip_reason`，没有理由的 skip 判红 | (a) — reusable enforces once caller adopts matrix inputs | 记录 test-lint reusable 的 matrix 首次 run URL | 包含 skip lane 的首个 matrix run URL |
| B6 | 不把 Issue label 留在既定的9个，须自行设计 ⟨RS-11⟩。具备 component: / platform: / severity: 三轴，不让 priority 与 severity 并存 | (b) — label-census script exists in spirit (.github#19: 11/11→14/14 measured by seats); no reusable | 获取 `gh api repos/OWNER/REPO/labels` 的输出，确认轴与并存禁止 | `gh api .../labels` 的 census 输出 |

## C — 密钥信息与历史

| ID | 项目 | 分类 | 今天如何通过 | 证据 artifact |
|---|---|---|---|---|
| C1 | 把 gitleaks caller 一路推进到实际的首次 run。须明记 reusable 扫描的是 merge-base..HEAD 的 PR range，而非 full history；另须把公开前的全历史扫描 ⟨RS-6⟩ 定为 **must-pass** | (a) for PR-range; **(b) gap: one-shot full-history scan as a publication-time job** | 记录 PR-range reusable 的 run URL。在全历史 job 实现之前，在仓库 root 执行 `gitleaks git --no-banner --redact --log-opts="--all" .`，把命令・gitleaks version・终止代码・全部输出记录到 transcript 中 | PR-range caller 的 run URL + 手动 full-history 扫描 transcript |
| C2 | 把 history-check caller 一路推进到实际的首次 run（merge-base / unrelated histories gate。空 range 时 fail-closed） | (a) | 记录 history-check reusable 的首次 run URL | 首次 run URL |
| C3 | 放置 `.publication-denylist`，并使其符合 D8。commit 的 denylist 不得暴露受保护对象的 literal，须从公开安全的写法／gitignore + 向 CI 注入密钥／记录在案的明示接受，这3种形式中选择 | (a) for gate execution; **(c) for D8 choice** (which of the 3 options, recorded per repo); (b) gap: a literal-exposure self-scan on the denylist file itself | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | publication-gate run + 记录在案的 D8 选择 |
| C4 | 对内部信息进行 sweep ⟨RS-5⟩。把家族名、个人路径、`_handoffs/`、截图、Issue / PR 内的测试日志都纳入对象 | (c) — judgment; publication-gate covers denylist-declared patterns only | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | 列举对象范围的 sweep 记录 |
| C5 | 把 publication-gate script 以与正本 byte-identical 的方式 vendoring，让 embedded selftest 作为 T-6 的 counted suite 变绿 | (a) | 记录 publication-gate selftest 的 run URL，并把 blob identity 与正本比对 | blob identity 注记 + selftest run URL |

把 C1 的 full-history 扫描定为 must-pass 的理由，以及在 job 实现之前用手动 transcript 满足要求的依据，放在 [#100 的 owner 专属决定2](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954)。

## D — 评审与 merge 的规律

Phase 2 原文中的顺序是 D1, D2, D3, D7, D4, D5, D6，这里在不改变 ID 的前提下按升序重新排列。

| ID | 项目 | 分类 | 今天如何通过 | 证据 artifact |
|---|---|---|---|---|
| D1 | 按尺寸确保评审席位（L1-9 / L1-10），记录 requested / actual。fallback 与无效票原样记录，verdict 缺失的拒绝不计入票数 | (c) — quorum is human process; (a) assist: review-labels reusable enforces label presence | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | 完成记录内的 seat table |
| D2 | 把人工批准 gate 束缚到 head SHA / event。不把 close→reopen 之前的批准当作仍然有效，须逐个仓库验证一次这份束缚 | (a) — the gate behaves this way today; checklist item is "verify the binding once per repo" | 记录 review-labels reusable 的 run URL，确认 head SHA 与标签事件的对应关系 | timeline 摘录 |
| D3 | merge 采用带 noreply identity 的本地 `--no-ff`，并记录与 PR manifest 的 diff 比对。noreply email 的前例，与因 API merge 的 identity 事故而改采本地 merge 的前例，是两件各自独立的事 | (c) process + (b) gap: a post-merge probe could verify merge-commit authorship/email pattern | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | merge SHA + 完成记录内的 identity 注记 |
| D4 | 制作具备 L1-7 字段与 **T-5 release / previous release 连锁**的完成记录。记录 deferred 的 Issue 引用、N/A 的闭合类型、tag 是 annotated 这几件事 | (c) today; **(b) gap: T-5 record-linter** (parse completion comments; verify tag exists+annotated+dereferences to merge SHA; walk 1-hop chain) — the fos#64 L1-8 record fixed exactly what this linter would catch (skipped v0.2.1 hop, non-resolving run IDs) | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | 完成记录 URL + tag 验证 |
| D5 | 确认记录中全部 run URL 都能解析到实际存在的 run，且 head SHA 与候选 SHA 一致 | (b) — resolvable-evidence linter is a concrete, high-value gap | 重新获取各个 run URL，记录其实际存在与 head SHA 的一致性 | 手动重新获取的注记 |
| D6 | 把完成记录放在车道 Issue 中，每条车道只保留1份记录 | (b) partial: "exactly one completion record per closed lane Issue" is machine-checkable | 确认车道 Issue 的评论，记录完成记录恰好只有1份 | 完成记录 URL |
| D7 | 超过 pr-size 的 vendored canonical file，宣告形式只能是**owner 授予的 `size-exempt` 标签 + 与正本的 blob identity 依据**这一种。过去接受 advisory-red・无标签的历史属于 grandfathered，不作为前例 | (c) choice of form is owner rule-making; (a) assist: pr-size gate + blob check | owner 的标签 / 满足 PB-3 发行者要件的决裁记录 | owner 账号的 `size-exempt` 标签事件 + 与正本的 blob SHA identity 注记 |

D7 唯一的宣告形式，是反映 [#100 的 owner 专属决定1](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) 的有意差分。

## E — 组织与 registry 的整合

| ID | 项目 | 分类 | 今天如何通过 | 证据 artifact |
|---|---|---|---|---|
| E1 | 在 family-os 的 `modules.json` 中放置具备 published 状态与 #62 契约 pin fields 的 registry entry，让下一次 weekly run 的 orphan check 变绿 | (a) — family-os machine checks + weekly lane | 记录 family-os 的 registry check run URL | registry diff + check run URL |
| E2 | 以确定性方式 render family footer，确认重新执行的 diff 为0 | (a) — renderer + idempotence pattern (fma#24) | 执行 renderer，记录以同一输入重新执行的 diff 为0 | 重新执行的 diff transcript |
| E3 | 选择继承 org-default template，或有意覆盖，并用 GraphQL 的 `repository.issueTemplates` 确认结果 | (b) — probe script exists as recorded practice, not a reusable | 执行 GraphQL query，记录返回的 template 清单 | GraphQL 输出 |
| E4 | 具备 community health files ⟨RS-9⟩、LICENSE=MIT/Sho Jikumaru ⟨RS-8⟩，quickstart 可复制粘贴执行 ⟨RS-7⟩ | LICENSE presence (b)-trivial; quickstart (c) — human execution | LICENSE 与 community health files 的存在通过 API / community standards 页面确认并记录。quickstart 的执行判定仅以 owner 的标签 / 满足 PB-3 发行者要件的决裁记录通过 | community standards 的 screenshot / API + 执行 transcript |
