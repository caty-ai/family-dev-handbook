> **机器翻译。**日文原文（[10-test-ci-baseline.md](../../../docs/10-test-ci-baseline.md)）是正本 — 本页与原文不一致时，以日文为准。

# T 测试与 CI 基准 — 用机制持续积累正确性证明的层级

L 层（L2 / L1 / L0）是「如何推进工作」的契约，R 层是「接受什么」的契约，与此相对，T 层规定的是**仓库为持续证明自身正确性所需的最低限度 — 初期整备、回归测试的积累、向委托格式的写入、不在红色状态下 merge、用标签为出货收尾、测试输出契约、徽章与数字的诚实性**这一契约。每条规则都附有稳定的 rule ID（`T-1`〜`T-7`），并在每条规则处用〔 〕明确其适用对象。摘要侧（[docs/04](04-adoption.md)）引用这些 ID。把 gate 升格为 check 的一般原则见 [R-6](09-rejection-rubric.md)，无法验证时的姿态见 [docs/05](05-fail-posture.md)。

背景: 公开仓库的可信度，外部会立刻依据「有没有测试、CI 是否为绿」来判定。合并的证据关卡（[L1-7](02-issue-loop.md)）与 check 强制（[R-6](09-rejection-rubric.md)）的思路已经存在，但**此前没有一层规定「必须整备并积累测试与 CI」**。测试的积累不是 CI 的功能所能造就的，只能靠运作规则来实现。另一方面，本协议的落地要经过委托简报（[B 层](07-delegation-brief.md)），因此只要写入格式，就能被贯彻执行。

## T-1 初期整备 — 先把框架搭好〔包含代码的新仓库 = MUST / 已有仓库 = 下一次触碰代码的车道 / 非代码仓库 = 附理由的 N/A〕

**包含代码的新仓库应在创建时整备测试运行器与 CI workflow。gate 必须包含 test；对于具备类型检查的语言，同一 gate 中也应包含 typecheck。即使测试为 0 个，也要先把框架搭好。**

理由: 事后再引入，会把「没有测试文化的仓库」变成既成事实。只要框架存在，此后的测试就会由 T-2 / T-3 自动积累起来。CI 的类型以 [templates/ci/](../../../templates/ci/README.md) 为既定（自建 workflow 只要满足本条也可）。整备好的 CI 应注册到 required status checks 中以进行机械确认（templates/ci 的落地步骤 5–6；无法设置 branch protection 的环境，靠运作来守住）。

对已有仓库的追溯整备是**opportunistic（伺机而为）** — 在下一次触碰代码的车道中，于该 Issue 中追加一行，同时整备 T-1。不设立专门的棚卸车道（不对未被使用的仓库预先支付工时 — [简单原则](why-simple-systems.md)）。

只有文档、素材、配置的**非代码仓库为附理由的 N/A**（与 [L1-7](02-issue-loop.md) 相同的词汇）— 在创建时的 Issue 中留下一行判断依据。不要用没有内容的空测试来填补框架（不要自造「对象 0 件也判绿」— [templates/ci/](../../../templates/ci/README.md) 中提到的坑点）。

## T-2 回归测试既定〔尺寸 M / L / H 的 bug 修复。Epic 内子 Issue 按子 Issue 的重量判定〕

**尺寸 M / L / H（[L2-1](01-milestone-loop.md) 的重量判定。Epic 内子 Issue 与 [E-6](06-epic-lane.md) 相同，按子 Issue 的重量判定）的 bug 修复 PR，默认同梱该 bug 的复现测试（fix 前变红・fix 后变绿）。**

尺寸 S（typo、局部单一文件程度）予以豁免。为规避该豁免而故意低报尺寸，由尺寸判定一侧的「拿不准就往重的一侧靠」（L2-1）来约束。功能新增的测试义务不在本条范围内 — 由 [T-3](#t-3) 与各 Issue 的 Done when 负责。

无法同梱时的理由应写成**两段结构**：

1. **既定的3种类型**（闭合列举 — 可机械判定）：
   - **环境依赖** — 只能在实机、实体设备、特定 OS 上复现
   - **外部服务依赖** — 需要外部 API、外部系统的真实响应
   - **复现成本过高** — 搭建成本与修复价值不相称（仅限 owner 认可的情况）
2. **不属于3种类型的情形由 owner 专属决定** — 在 PR 中留下一行记录专属决定的事实与理由。自由描述的理由仅限于 owner 专属决定的情形

之所以采用列举形式，是为了防止自由描述的「写不出理由」作为借口无限增殖。

<a id="t-3"></a>

## T-3 与简报对接 — 把积累写入格式〔包含代码变更的委托 = B-1 适用对象中会变更仓库代码的部分〕

**包含代码变更的委托简报，其「实现检查（Self-verification）」应将「新增/变更的测试及其运行结果」列为标准项目**（格式正本: [templates/brief-template.md](../../../templates/brief-template.md)）。

未新增测试的委托，应在交付报告中包含「未新增 + 理由」。理由应按**闭合列举**书写：

1. **符合 T-2 的豁免**（尺寸 S） — 一行说明即可
2. **该变更没有测试对象**（仅配置、声明等）
3. **既有测试已覆盖该变更** — 需能指出该测试
4. **属于 T-2 的3种类型之一**（环境依赖 / 外部服务依赖 / 复现成本过高 = owner 认可）
5. **属于 T-2 第2段的 owner 专属决定** — 需能指出该专属决定的记录

理由: 测试的积累，只有写入委托格式之后才会自动化。委托对象是 fresh context，简报中没写到的期望就等同于不存在（与 [B-4](07-delegation-brief.md) 方向一致）。

## T-4 fail-closed merge — 不在红色状态下 merge〔全体仓库 = MUST〕

**禁止在 CI 处于红色状态下 merge。** 本条对 [docs/02](02-issue-loop.md)「完成的定义」中「测试、lint 均已通过」规定了**唯一的明文例外**，CI 状态应记载在完成记录（L1-7）中。

例外只有一个：**已知且与当次 PR 无关的红**（例如: main 一侧既有 bug 导致的红）。成立条件**全部必须满足**：

1. **证明无关** — 在完成记录中以内联形式附上「在 base（不含当次 PR 变更的状态）下复现出相同的红」的记录（是证据而非主张 — L1-7②）
2. **红色 identity 的绑定** — 写明失败的 check 名称 + workflow run 识别符 + 观测日期，并与候选 SHA 对应
3. **关联到对应 Issue** — 没有可关联的 Issue 时应先创建。Issue 必须附有 [LC-1](08-lifecycle.md) 的退场触发条件（期限或完成条件），触发条件失效后该例外也随之失效
4. **owner 专属决定的真实性验证** — 需以**第三方可确认真实性**的形式留存，例如 owner 本人账号在 PR 上的评论。仅在完成记录正文中描述不能使例外成立（[FP-8](05-fail-posture.md) / [R-6](09-rejection-rubric.md)）

边界的明文化：

- **间歇性的红（flaky）不属于「已知且无关」** — 若想纳入，需在满足上述4个条件的基础上，由 owner 每次专属决定并记录
- **不得把没有 CI 的状态写成 green** — 在没有整备 CI 的仓库中触碰代码的车道，应在同一车道内满足 T-1 之前不得 merge（紧急修复等来不及时，可由 owner 专属决定给予宽限，并留下带 LC-1 退场触发条件的 T-1 整备 Issue。该专属决定同样要以与条件4相同的、可验证其实际存在的形式留下记录）
- **`CI: N/A` 仅限于 CI 不检查该变更的情形**（理由应写明其属于检查对象之外的依据）。凡 CI 会运行的变更，即便是非代码也不得写 N/A
- 已设置 required status checks 的仓库，**不得通过解除 required 来行使该例外** — 应以 owner 的明确操作留下记录

没有关联记录的红、无法验证的例外都不能成立为例外（fail-open 不等于「通过」 — [docs/05](05-fail-posture.md)）。

## T-5 发布既定 — 用标签为出货收尾〔包含出货级变更的 merge = MUST / 其余 = 附理由的 N/A〕

**所有完成记录（[L1-7](02-issue-loop.md)）都应设置 release 栏。** 值须为以下 3 个闭合词汇之一，把**出货级变更**（改变用户会用到的行为・公开 API・发布物・用户须遵循的规范的 merge）并入 main 的车道不得选择 `N/A`。**难以判断的 merge 一律按出货级处理**（与 [L2-1](01-milestone-loop.md)「拿不准就往重的一侧靠」同向 —— 不允许把犹豫逃到更轻的一侧 N/A）：

1. **`release: vX.Y.Z`** —— 以本次 merge 的稳定点切 tag 的宣告。tag 须为 **annotated + SemVer**，并切在**该 merge 留在 main 上的提交**（squash / rebase merge 时为 main 上的新 SHA）。记录当下 tag 尚未创建 —— 栏中写的是宣告，**只有在切好 tag 并把 tag URL 写入 MERGED 评论（[L1-4 终结](../templates/issue-template.md)）之后，车道才能宣告 MERGED**。这项 tag URL 义务须连同 **GitHub Releases 上 Release 的实际存在**才算履行（即使只有裸 tag，`/releases/tag/<名称>` 的 URL 也会返回 200 —— URL 存在并不代表 Release 存在）。装有 release-sync 载体（[templates/ci/](../../../templates/ci/README.md)）的仓库通常会由 tag push 后的 **green run** 完成，但确认履行仍是车道的义务 —— **run 未触发、为红或载体不存在，都不代表已经履行**。未履行的车道**不会终结，会以 WIP 状态留存**，因此会挂在 [L0-3](03-git-protocol.md) 的 stale 时钟上，即便该仓库之后没有新车道，忘切 tag 的问题也会一直可见（缺少 tag URL 或 Release 实际存在的 MERGED 属于**不合法格式**，终结不成立 = [L1-4](02-issue-loop.md) 的非活跃处理）。补记这份履行报告属于对宣告的履行，不属于 [L1-8](02-issue-loop.md) 的订正。tag 名**原则上应与所宣告的标识符同名**——仅当评审后范围发生变动、版本随之改变时，**才**可以用别的名字切 tag，并在 MERGED 评论中用一行写明差异与理由（不得悄悄切成别的版本）。要把宣告本身改成 `deferred`，须走 L1-8 的差替记录（不做悄悄改写）。在车道自身没有切 tag 权限的运作方式下，以 owner 作为 tag 权限持有者的 **HOLD**（[L1-5](02-issue-loop.md) 的 5 个字段）是合法出口
2. **`release: deferred`** —— 现在不切 tag 的宣告。须**一并写明理由 + 带退场触发条件（期限或完成条件 = [LC-1](08-lifecycle.md)）的 Issue 引用**——没有可引用的 Issue 就先建一个（与 **T-4** 第③点同型：merge 过的 PR 正文不会重新出现在任何人的视野中，因此把它放在会重新浮现的地方 —— Issue）。缺少 Issue 引用或触发条件的 deferred 无效（= 与空栏同等地 blocking）。**触发条件失效的 deferred 会失去「不切 tag 的特权」**——该车道自身的 MERGED 仍然有效，但**下一次出货级 merge 不得再选 `deferred`（须为 `vX.Y.Z`）**。失效本身不会阻塞下一份完成记录（若阻塞，就没有办法解除一个既无已宣告标识符、也无目标提交的未履行状态——这与 **T-4** 第③点只让例外失效、而不阻塞记录，是同一个理由）。让过期的 deferred 可见，由所引用的 Issue 承担。deferred 会在**后续出货级 merge 履行了 `vX.Y.Z` 之时解除**，并关闭所引用的 Issue（如仍有未尽事宜，用新的触发条件重新宣告）
3. **`release: N/A`** —— 仅限非出货级的 merge。理由须按**闭合列举**书写：①仅为不含用户须遵循规范的 docs ②不改变行为、公开 API、发布物中任何一项的内部整理 ③仅为 CI 或开发环境的接线 ④尚未到达 main 的中间 merge（Epic 的子→epic 关卡 = [E-6](06-epic-lane.md)②）。**不属于这些类型的情形由 owner 专属决定**——把该专属决定的事实与理由留一行（与 **T-2** 同型）。没有理由的 N/A 无效（= 与空栏同等地 blocking）。在发布规范的仓库（例如本手册）中，docs 的变更本身就是出货级——不要拿「仅是 docs」当作选 N/A 的借口

**栏位本身缺失・值为空・未编辑的占位符・3 词汇之外的值，一律视为未填写而 blocking**（与 **T-4** 的 CI 栏同等强度）。做法不是「设法不忘记」，而是「一旦忘记，完成记录就无法通过」——这正是 T 层一贯的思路（写入格式即可贯彻执行）的应用：CI 已经由 T-1〜T-4 形成分层，唯独 release 此前没有分层，本条补上这个缺口。

tag 的内容与签名：

- **tag message 的格式 — 第 1 行 = 标题（120 字以内）・第 2 行 = 空行・第 3 行起 = 正文**。第 1 行是一句话点明该 release 的主题，release-sync 载体（[templates/ci/](../../../templates/ci/README.md)）会**去掉首尾空白后原样用作 Release 标题**。超过 120 字时 Release 标题会 fallback 为 tag 名，且事后无法恢复（改写 annotated tag 等于改写共享历史，因此不做 — [Issue #118](https://github.com/caty-ai/family-dev-handbook/issues/118) 中实测有 4 个 release 因此无法恢复）。120 这个值是按 git subject 惯例（约 50〜72 字）的约 2 倍设定的上限，并且**与 `reusable-release-sync.yml` 的实现值一致** — 不得只动其中一方；要改数值时，实现与本条须在同一 PR 中一起改。正文仍按下一项放置证据指针
- release notes（tag message 或 Releases）须引用**至少一个可验证证据的指针**（CI run、带完成记录的 PR 等）——与「不放置无法验证的数字」这一原则（[R 层](09-rejection-rubric.md)）保持一致。这与完成记录本体的证据规律（[L1-7](02-issue-loop.md)②「仅有链接的证据不合格」）属于不同语境——记录本身以内联为准，tag 只需指针即可
- **拥有签名验证机制的仓库（updater 等・由机器验证 tag 签名的场景）须使用签名 tag，密钥按仓库各自管理**。要求签名的仓库，应在 MERGED 的履行报告中用一个词写明是否已签名（让签名的缺失从记录层面就能看见）。其余情况 annotated 即可，签名为 SHOULD
- 版本号的升幅（MAJOR / MINOR / PATCH）遵循 SemVer 的一般规则，本条不作约束

边界的明文化：

- **防止 deferred 被滥用**——同一仓库中出货级 merge 的 deferred 连续出现 2 次后，第 3 次出货级 merge 不得再选 deferred（须切 tag）。连续次数按**出货级 merge 这一列**计数（N/A 的 merge 不计入该列），并**在履行 `vX.Y.Z` 时重置**。为了让计数可以事后核验，**所有完成记录**都应在同一仓库中，用一行并记上一次出货级 merge 的 release 值与履行状态（`previous release` 栏）。次数**只需沿上一条车道的 `previous release` 回溯一步即可确定**——若上一次是 deferred，且上上次也是 deferred，那么这一次须为 `vX.Y.Z`（与 [R-6](09-rejection-rubric.md)「让计数可以事后核验」同向的升级机制）
- **履行的接线**——完成记录除了自身的 release 栏之外，还须确认**同一仓库上一次出货级 merge 的 release 宣告已经履行**（[L1-7](02-issue-loop.md)⑦）。**「已履行」的判定由以下收口**：`vX.Y.Z` = tag 已切好、MERGED 中带有 URL 且 Release 实际存在（**tag、URL、Release 实际存在三者缺少任意一项，都属于未履行 = blocking**）／`deferred` = 只要触发条件仍存活就属于待履行，不构成阻塞；即便失效也不作 blocking，而是按上文第 2 点收窄下一次的可选项／`N/A` = 不属于出货级这一列，不在此列范围内。release 栏**并非 tag 运作的替代品**——栏位记录的是判断本身，未履行的 `vX.Y.Z` 宣告会从两个方向被堵住：MERGED 无法成立（上文第 1 点），以及阻塞下一条车道
- **执行强度全仓库一致**——没有出货级变更的仓库，所有 merge 自然都会落在 N/A，因此私有的 scratch 仓库不会有实质负担。公开/私有是否应区分强度，留待另行盘点，一旦有结论，再让本条的〔 〕跟进
- **Epic 的子→epic 关卡（[E-6](06-epic-lane.md)②）不在打 tag 义务的范围内**——栏位本身与所有记录一样必须存在，值取上文第 3 点的类型④（`N/A（epic 集成前）`）。要求打 tag 的是 epic→main 的整合 merge（E-6③，完整 L1-7）
- 对过去未打 tag 部分的追溯不属于本条范围（本条只对「今后的 merge」生效，过去的部分由各仓库 owner 自行判断）
- record-vs-reality 的 PR-side check 与 scheduled drift sweep 在 [Issue #106](https://github.com/caty-ai/family-dev-handbook/issues/106) 中追踪（带 LC-1 退场触发条件的 follow-up）

## T-6 测试输出契约 — 把执行事实写成机器可读的一行〔包含代码的新仓库 = MUST / 既有仓库 = 下次触碰代码、测试、CI test job 中任一项的车道，在同一 Issue 内整备（与 T-1 相同的 opportunistic）/ 没有运行器的非代码仓库 = 附理由的 N/A〕

**测试运行器必须满足一份输出契约，使机器能够判断「哪些运行了、哪些没有运行、为什么」。** 成立条件共 5 点：

1. **摘要行（契约本体）** — 运行器应在输出中给出下面这一行。格式正本就是这条正则表达式本身：

   ```
   suites: declared=([0-9]+) executed=([0-9]+) skipped=([0-9]+)
   ```

   含义定义：`declared` = 已注册的 suite 总数 / `executed` = 实际运行到 PASS 或 FAIL 的数量 / `skipped` = 如实申报为 SKIP 的数量。**不变条件为 `declared = executed + skipped`**。破坏该条件即为漏失（silent drop）= 红。数值须由运行器动态汇总 —— **嵌入固定值（例如用 echo 输出常数）违反本条**（机器无法验证其导出过程，因此这是采用评审中的检查项）。输出中至少出现一次该行；出现多次时，**以最后一次匹配为准**。决定把某个 suite 从 declared 中移除（取消注册）时，应在执行该决定的车道 Issue 中留一行记录 —— 没有记录的取消注册按漏失同等处理
2. **结果词汇** — **家族编写的运行器、wrapper 所显示的结果**须使用 `PASS` / `FAIL` / `SKIP` 三种词汇。pytest / unittest / vitest 等**框架原生的原始输出不受此限制**（机器 gate 读取的是摘要行与 exit code，框架输出可原样透传）
3. **exit code 的闭合集** — `0` = 没有 FAIL / `1` = 存在 FAIL / `2` = 用法或输入错误 / `127` = **缺少必需依赖**（在 preflight 中检测，先在 stderr 以 `missing-dep: <名称>` 点名原因再退出 —— 不得把依赖缺失误报为测试失败或输入错误）。缺少可选环境（例如没有实机）不使用 127，而是记为 **SKIP**（计入摘要行的 skipped）
4. **异常退出时也输出摘要** — 运行器即使中途死亡，也须采用能输出摘要行的结构（bash 的 `trap finish EXIT` 仅为非规范性示例；Python atexit、Makefile 合成及其他同等机制均可）。缺少摘要 = 无法判定 = 红（[FP-6](05-fail-posture.md)）—— 但该红实际触发是在下述第 5 点接线完成之后
5. **CI 对账接线（采用完成条件）** — 只有 CI 侧对账 gate（[templates/ci/](../../../templates/ci/README.md) 的 test-lint；reusable 的 `require_suite_reconciliation: true`）**已启用**时，才能把本条称为「已整备」。仅输出摘要行、仅引用条文都不能称为已整备（「只是放上去」= [FP-5](05-fail-posture.md)）。不在适用范围的仓库，应在 Issue 中明确留下 N/A —— 沉默不构成 N/A。skipped 形式（三字段摘要）的接线须在对账 gate 的 skipped 支持（#80 delta）进入 main 后进行；顺序相反会把诚实的 SKIP 判红

**SKIP 率上限** — `skipped × 5 > declared`（= 超过 20%，且 declared > 0）即为红。调整上限的仓库须**把数值正本放在 CI caller 输入（机器读取的位置）**，并在 PR 中用一行记录变更依据，或记在带 [LC-1](08-lifecycle.md) 触发条件的 Issue 中（与 [LC-3](08-lifecycle.md) 相同的「数值在本地配置、变更必须记录」型）。没有记录的变更无效，按默认 20% 判定。对于 declared ≤ 4 的仓库，该公式意味着「默认 SKIP 为 0」—— 这是有意为之（仓库越小，越应能全部运行；若确需恒常 SKIP，应宣告并修改上限值）。SKIP 是对「缺少环境」的诚实申报，不是恒常逃生口 —— 超过上限的红是在催促「修好环境，或记录把对象移出范围的决定」

理由：「测试已经运行」很容易沦为自我申报。declared / executed / skipped 三个值及其不变条件，把「假装运行过」的路径（suite 悄然脱落、把 SKIP 混入 executed、通过取消注册操纵分母、误报依赖缺失）收敛成一行机器检查。把格式固定为正则表达式，是为了让 CI 侧对账（W0-3 reusable test-lint）能以一套共通实现覆盖所有仓库。

边界的明文化：

- 本条是**输出契约**，不约束测试内容、粒度或框架选择（推荐运行器见附录）
- 以 suite 为单位即可（无需细到测试用例 —— 粒度由仓库自行裁量。suite 内的 SKIP 可通过拆分 suite 来表达）
- 测试为 0 的新仓库（只有 T-1 框架的状态），可以不输出摘要行（尚未接线，所以不会判红），也可输出 `declared=0 executed=0 skipped=0`（executed=0 判红 = 倒向不自制「对象为 0 却是绿」的一侧）—— 两者皆可，推荐后者
- 本手册自身的运行器是本条的**首个适用对象**（发布条文的车道，应先让本仓库的 `make test` 符合契约再 merge —— pilot 原则）

## T-7 徽章与数字的诚实性 — 只有机器涂出的颜色才是绿〔带 README 的公开仓库 = MUST / 其他仓库 = 放置数字或徽章时遵守同一纪律（不放这些内容的私有 scratch 仓库自然为 N/A）〕

**README、docs 中任何「看起来已验证」的展示，都必须连接到机器检查结果。** 成立条件共 3 点：

1. **明确 CI 状态（不得用无徽章隐藏「未检查」）** — 带 README 的公开仓库必须以以下**二者之一**显示 CI 状态：①执行 **T-1 测试 gate 的 workflow** 的 live badge（GitHub Actions 的 badge.svg，或指向该 workflow 的同等 live endpoint；**不运行测试的其他 workflow，即使 badge 为绿也不满足本条**）②CI 尚未整备时，使用灰色静态 badge `CI: not yet`。不显示、以其他 workflow 的绿色替代，均属违反
2. **颜色的闭合集** — 静态 badge 可用的颜色仅限 **`lightgrey` / `blue`（包含语言、许可证等事实展示类）**，这是闭合列举。`green` / `brightgreen` / `success` / `passing` 系列及同等绿色 hex 均不得用于静态 badge（检查实质而非拼写 —— [R-6](09-rejection-rubric.md)）。只有机器涂出的 live badge 才能宣称绿色
3. **实测数字与 Project status 节** — README / docs 中写入读起来像实测的数字（测试数量、覆盖率、性能值）时，必须附上**该次实测的 run URL 与实测日期**。无法附上时就不要写该数字（不放置无法验证的数字 —— [R 层](09-rejection-rubric.md)）。数字若与该 workflow 更新 run 中的**实测值不同**，即为 stale —— 应更新或删除（只要数值未变，仅 run 更新不构成 stale）。设计值、目标值可在明确标注「目标」后书写，但不得伪装成实测展示（例如没有 run URL 的「passed」）。README 设置状态节时的标准形式如下（**该形式为正本** —— 不以外部仓库为参考模型）：

   ```markdown
   ## Project status

   [live badge（T-1 测试 workflow 的 badge.svg）或 CI: not yet（灰）]

   - CI: <有无 test-lint gate，以及所连接的 workflow 名>
   - 已验证环境: <实际测量的 OS / runtime>
   - maturity: <stable / beta / reference 等>
   - 已知限制: <列举；没有时明确写「无」>
   ```

理由：外部会根据「badge 是否为绿」立即判断仓库可靠性。手写绿色与机器绿色无法区分，一个手写绿色就会**损害家族所有仓库中绿色的证据能力**。反过来，不放 badge 以隐藏「未检查」，也是同一谎言的另一面（实测：9 个手写绿色 badge 与「没有 CI 且无展示」的仓库并存）。把展示限制为机器连接的状态，才能让「绿 = 检查运行过 / 灰 = 没有检查」在所有仓库中保持同一含义。

边界的明文化：

- 对象是「可能伪装成检查结果的展示」—— 事实展示类 badge（语言、许可证、版本；blue 系）可自由使用
- **始终可以选择不写数字**（本条是「写就要诚实」+「仅 CI 状态是公开仓库义务」）
- 不带 README、也不公开的私有 scratch 仓库自然为 N/A。**已经公开却没有 README** 的仓库，会在整备 README 的车道（B8 等）进入本条适用范围 —— README 缺失不构成本条的永久豁免
- 把本条升格为 check（检测静态绿色 badge、stale 数字等）时，按 [R-6](09-rejection-rubric.md) 以 Issue 追踪

## 附录（非规范） — 推荐运行器速查表

条文所要求的仅止于「整备运行器 + CI」。工具的选型由实现者自行裁量，本表为**非规范性参考**。表格的更新不计入条文改订。

| 语言 / 运行时 | 推荐运行器 | 补充 |
|---|---|---|
| TypeScript / JavaScript (Node) | vitest | 若标准库已够用，也可用 `node:test` |
| Python | pytest | — |
| Shell | bats-core | — |
| Go | `go test` | 语言标准 |
| Rust | `cargo test` | 语言标准 |
| Swift / iOS | XCTest | 执行方式为 `xcodebuild test` |
| CI 执行环境 | GitHub Actions | 仓库位于 GitHub 时的既定选择 |
