> **机器翻译。**日文原文（[11-publication.md](../../../docs/11-publication.md)）是正本 — 本页与原文不一致时，以日文为准。

# PB 公开准备 — 用检查清单为仓库公开把关的一层

L 层（L2 / L1 / L0）是「如何推进工作」的契约，R 层是「接受什么」的契约，T 层是「如何积累正确性的证明」的契约，与此相对，PB 层规定的是**公开仓库的车道，如何用逐项证据证明公开前的确认已经完成**这一契约。每条规则都附有稳定的 rule ID（`PB-1`〜`PB-5`），并在每条规则处用〔 〕明确其适用对象。完成记录的正本见 [docs/02](02-issue-loop.md)，无法验证时的姿态见 [docs/05](05-fail-posture.md)，出货与证据的规律见 [docs/10](10-test-ci-baseline.md)。正本的置放遵循 [R-5](09-rejection-rubric.md) 的放置阶梯，后续升格为 check 遵循 [R-6](09-rejection-rubric.md) 的一般规律，价值判断不超越 [R-1](09-rejection-rubric.md)。

本层的 `PB-1`〜`PB-5` 与 README 的核心契约 `P1`〜`P5`（v0.1.0・冻结）是两回事。

背景: 在家系仓库的整合 campaign 中，展示的诚实性、CI 的实效性、密钥与历史、评审、完成记录、组织联动，都是逐个仓库靠人工验证的。这份实绩在 [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100) 的 Phase 1〜4 中被盘点，整理成 [Phase 2 的28项](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694) 与 [Phase 4 的条文骨架](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355215540) 之后，经 [owner 专属决定](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) 确定了宣告形式、必须度与试点顺序。本章把这份结果定为公开车道的门禁。

<a id="pb-1"></a>

## PB-1 门禁束缚 — 公开靠逐项证据来把关〔private→public 切换・新建 public = MUST〕

**公开仓库的车道，应以 [PB-2](#pb-2) 的正本检查清单来把关。完成记录中应放置以检查清单的表头为样式正本的逐项 PASS / FAIL / N/A 表，以及每一项所指定的证据 artifact。无法验证的项目视为未通过。只要仍有 FAIL 或未通过的项目，就不予公开。**

理由: 在 campaign 中，全部项目都出现过真实的失败案例，仅靠散文式的提醒无法防住。要求逐项证据，就能堵住把"未确认"的状态当成"已确认"的路径。这是把 [docs/05](05-fail-posture.md) 的 fail-closed 姿态应用到公开车道，让展示的诚实性与 [T-7](10-test-ci-baseline.md) 保持同一含义。

边界的明文化:

- 家系仓库的 fork，或新建第二个 public remote 时，属于适用对象
- 外部第三方公开的仓库的 fork 不适用。是否适用的价值判断由 owner 专属决定（[R-1](09-rejection-rubric.md) 的价值判断规律）
- public→private→public 的再公开须重新走一遍检查清单。引用最近记录的差分重走方法，遵循检查清单表头的规定
- GitHub 之外的镜像与包注册中心的公开不适用
- 对已经公开的仓库不追溯适用。但下一次触碰相关部分的车道，应按 [T-1](10-test-ci-baseline.md) 同型的 opportunistic 方式顺带整备，不设立专门的盘点车道

<a id="pb-2"></a>

## PB-2 检查清单的置放与版本 — 把所依据的正本固定下来〔公开检查清单本体・全部公开车道〕

**检查清单的正本是 [templates/publication-checklist.md](../templates/publication-checklist.md)，其版本从属于 handbook 的 release tag。公开车道原则上应在完成记录中记下所参照的 release tag。仅当在该状态尚未被纳入 tag 时运行，才记录 commit SHA，之后应在同一份完成记录中补记包含该状态的 release tag。**

理由: 在 [handbook#80](https://github.com/caty-ai/family-dev-handbook/issues/80#issuecomment-5344053714) 中，发布方 caller 在 `ci-v1` tag 尚未存在前就被 pin 住，出现了竞态。仅固定正本的位置还不够，若不把实际运行的内容固定到可解析的版本，同名的检查清单就会产生不同的判定。

<a id="pb-3"></a>

## PB-3 分类的边界 — 让每种分类的通过形态各自封闭〔公开检查清单的全部项目〕

**(a) 类项目为机器证据即 run URL，(b) 类项目为机械化尚未实现前、由检查清单逐项指定的手动步骤及其记录，(c) 类项目只能靠 owner 的标签或记录在案的专属决定来通过。(c) 类项目绝对不能靠自我申报通过。**

(c) 的发行者要件仅限以下 3 种形式:

1. owner 账号发出的标签事件
2. owner 本人发布的评论
3. owner 事后对中继记录做出的、可验证的追认（必须附追认链接）

除此之外一律视为未通过。每项的必须度・宣告形式由检查清单规定。

理由: 在 harness#121 中，写着"owner 专属决定"的自我申报，实际上不存在可验证的 owner 本人许可，造成了真实损害，经 [事后追认](https://github.com/caty-ai/caty-agent-harness/issues/121#issuecomment-5341374987) 才得以一次性挽救。若第三方无法验证的不只是决定的内容、还包括发行者本身，owner 专属决定（[R-1](09-rejection-rubric.md) 的价值判断规律）就无法成立。

<a id="pb-4"></a>

## PB-4 记录的完整性 — 让"一条车道一份记录"保持可解析〔公开车道的完成记录〕

**公开车道每条恰好只有一份完成记录，置于车道 Issue 中。这是把 [L1-7](02-issue-loop.md) 完成记录置放位置定为车道 Issue 的特则，仅适用于公开车道；PR 正文中放置的不是记录本体，而是指向车道 Issue 的一行指针。适用 [T-5](10-test-ci-baseline.md) 的 release / previous release 连锁，run URL 必须能解析到实际存在的 run，且 head SHA 须与候选 SHA 一致。**

理由: 在 [family-memory-architecture#33](https://github.com/caty-ai/family-memory-architecture/issues/33#issuecomment-5354966162) 中，完成记录被放在了追踪 Issue 里，只看 PR 的 scanner 因而漏看。另一方面，persona-growth-loop#16 出现过[事前记录](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5341012500)与[事后记录](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5345278041)两份相互矛盾的完成记录同时留存的异常情况。把置放位置与数量固定下来，并把 [L1-8](02-issue-loop.md) 的订正处理为同一连锁中的差替记录，就能保住单一的审计入口。证据的可解析性采用与 campaign 的 [L1-8 订正记录](https://github.com/caty-ai/family-os/issues/64#issuecomment-5353192649) 相同的基准。

<a id="pb-5"></a>

## PB-5 试点条款（时限） — 把实际运作中的落差还流回正本〔检查清单运作的启动期〕

**由 owner 指名的第 1・第 2 消费者车道，应把各项目的运作落差报告到 [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100)，并反映进正本检查清单。在落差反映之前运行的车道，应按 PB-2 的规定，记录当时实际运行的检查清单状态。**

消费者的指名记录见 [#100 的 owner 专属决定评论](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954)。本条的合并提案，原则上应在第 1 消费者的落差还流反映进检查清单之后进行。提前进行由 owner 专属决定（[R-1](09-rejection-rubric.md) 的价值判断规律）。

当第 1・第 2 消费者车道的落差报告都汇总到 #100，并反映进正本检查清单后，本条即告失效。条文的删除放到后续 PR 中进行，规范变更 = 出货相当，适用 [T-5](10-test-ci-baseline.md)。

理由: 手动步骤的成本与含混之处，只有在实际的公开车道中才能被测出。一方面从两条消费者车道还流修正正本，一方面留下判定时所依据的状态，以避免让试点期间的变更悄悄追溯改写过去的判定。
