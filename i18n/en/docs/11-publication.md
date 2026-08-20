> **Machine translation.** The Japanese original ([11-publication.md](../../../docs/11-publication.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# PB Publication Readiness — the Layer that Gates Repository Publication with a Checklist

Where the L layers (L2 / L1 / L0) are the contract for **how work proceeds**, the R layer is the contract for **what gets accepted**, and the T layer is the contract for **how proof of correctness is accumulated**, the PB layer sets the contract for **how a lane publishing a repository shows that its pre-publication checks are complete, item by item, with evidence**. Each rule carries a stable rule ID (`PB-1` through `PB-5`), and the scope of application for each clause is noted in 〔 〕. The canonical home for completion records is [docs/02](02-issue-loop.md), the stance to take when verification isn't possible is [docs/05](05-fail-posture.md), and the discipline of shipping and evidence is [docs/10](10-test-ci-baseline.md). The canonical placement follows [R-5](09-rejection-rubric.md)'s placement ladder, promoting a policy to a check afterward follows [R-6](09-rejection-rubric.md)'s general discipline, and value judgment never goes beyond [R-1](09-rejection-rubric.md).

Background: in the family-repository consistency campaign, display honesty, CI effectiveness, secrets and history, review, completion records, and org integration were each verified by hand, repository by repository. [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100)'s Phase 1–4 took stock of that track record, organized it into [Phase 2's 28 items](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355210694) and [Phase 4's clause skeleton](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5355215540), and then [an owner ruling](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954) settled the declaration forms, required-ness, and pilot order. This chapter defines the result as the gate for a publication lane.

<a id="pb-1"></a>

## PB-1 Gate Binding — Publication Stops on Item-by-Item Evidence〔a private→public switch, or creating a new public repo = MUST〕

**A lane that publishes a repository is gated by [PB-2](#pb-2)'s canonical checklist. Its completion record carries an item-by-item PASS / FAIL / N/A table — whose canonical format is the checklist's own header — plus the evidence artifact each item specifies. An item that can't be verified counts as not passed, and the repository does not get published.**

Reason: in the campaign, every item had a real-world failure example, and a prose caveat alone did not prevent it. Requiring evidence per item closes off the route where an unverified state gets treated as "verified." This applies [docs/05](05-fail-posture.md)'s fail-closed stance to the publication lane, and keeps display honesty meaning the same thing as [T-7](10-test-ci-baseline.md).

Making the boundary explicit:

- Forking a family repository, or newly publishing a second public remote, is in scope
- A fork of a repository some external third party already publishes is out of scope. The value judgment for whether it applies is the owner's call alone ([R-1](09-rejection-rubric.md)'s value-judgment discipline)
- Republishing after public→private→public re-runs the checklist. The method for a delta re-run that cites the most recent record follows the checklist's own header
- Publishing to a mirror outside GitHub, or to a package registry, is out of scope
- Retroactively applying this to an already-published repository is out of scope. However, the next lane that touches the relevant area applies it opportunistically, the same shape as [T-1](10-test-ci-baseline.md) — don't stand up a lane dedicated to inventory sweeps

<a id="pb-2"></a>

## PB-2 Checklist Location and Version — Pin Down the Canonical Text That Actually Ran〔the publication checklist itself · every publication lane〕

**The checklist's canonical source is [templates/publication-checklist.md](../templates/publication-checklist.md), and its version is subordinate to the handbook's release tags. A publication lane, in principle, records in its completion record the release tag it referenced. Only when it ran in a state not yet included in a tag does it record the commit SHA, later appending to that same completion record the release tag that comes to include that state.**

Reason: in [handbook#80](https://github.com/caty-ai/family-dev-handbook/issues/80#issuecomment-5344053714), a race occurred where a distributed caller got pinned before the `ci-v1` tag actually existed. Unless you pin down not just where the canonical source lives but a version that resolves to what actually ran, a checklist of the same name can yield different verdicts.

<a id="pb-3"></a>

## PB-3 Classification Boundaries — Close the Passing Form per Classification〔every item on the publication checklist〕

**A (a) item passes on the machine evidence of a run URL. A (b) item passes on the manual procedure the checklist names item-by-item, plus its record, until mechanization is implemented. A (c) item passes only on the owner's label or a recorded ruling. A (c) item never, ever passes on self-report.**

(c)'s issuance requirement takes exactly these 3 forms:

1. A label event from the owner's own account
2. A comment the owner personally posted
3. A verifiable after-the-fact ratification by the owner of a relayed record (a link to the ratification is required)

Anything outside these counts as not passed. Each item's required-ness and declaration form are set by the checklist.

Reason: in harness#121, real harm occurred where a self-report labeled "owner ruling" carried no verifiable permission actually from the owner, and it was rescued only once by [after-the-fact ratification](https://github.com/caty-ai/caty-agent-harness/issues/121#issuecomment-5341374987). Unless a third party can verify not just the content of a ruling but its issuer, the owner's-call-alone principle ([R-1](09-rejection-rubric.md)'s value-judgment discipline) does not hold.

<a id="pb-4"></a>

## PB-4 Record Integrity — Keep One Record per Lane Resolvable〔the completion record of a publication lane〕

**Exactly one completion record per publication lane, placed on the lane Issue. This is a special case, for publication lanes only, that sets [L1-7](02-issue-loop.md)'s completion-record location to the lane Issue — the PR body carries not the record itself but a one-line pointer to the lane Issue. [T-5](10-test-ci-baseline.md)'s release / previous-release chain applies, and each run URL must resolve to a run that actually exists, with its head SHA matching the candidate SHA.**

Reason: in [family-memory-architecture#33](https://github.com/caty-ai/family-memory-architecture/issues/33#issuecomment-5354966162), the completion record was placed on a tracking Issue, and a scanner that looks only at PRs turned out to miss it. Meanwhile, persona-growth-loop#16 had an anomaly where two conflicting completion records were left behind — a [preceding record](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5341012500) and an [after-the-fact record](https://github.com/caty-ai/persona-growth-loop/issues/16#issuecomment-5345278041). Pinning down the location and the count, and keeping [L1-8](02-issue-loop.md) corrections in the same chain as a replacement record, preserves a single audit entry point. The resolvability standard for evidence is the same one used by the campaign's [L1-8 replacement record](https://github.com/caty-ai/family-os/issues/64#issuecomment-5353192649).

<a id="pb-5"></a>

## PB-5 Pilot Clause (Time-Limited) — Feed Real-World Operational Gaps Back to the Canonical Source〔the checklist's operational startup period〕

**The 1st and 2nd consumer lanes the owner designates report each item's operational gaps to [Issue #100](https://github.com/caty-ai/family-dev-handbook/issues/100) and get them reflected into the canonical checklist. A lane that runs before the pilot feedback is reflected records, per PB-2, the checklist state it actually ran against.**

The consumer designation record is [#100's owner-ruling comment](https://github.com/caty-ai/family-dev-handbook/issues/100#issuecomment-5359570954). In principle, a merge proposal for this clause happens after the 1st consumer's gap feedback has been reflected into the checklist. Going ahead of that is the owner's call alone ([R-1](09-rejection-rubric.md)'s value-judgment discipline).

This clause lapses once the 1st and 2nd consumer lanes' gap reports are both in on #100 and reflected into the canonical checklist. Removing it from the statute happens in a follow-up PR, and [T-5](10-test-ci-baseline.md) applies to it as a norm change = a ship-equivalent change.

Reason: the cost and ambiguity of a manual procedure can only be measured against a real publication lane. Feeding back from the two consumer lanes fixes the canonical source, while recording which state a verdict was judged against keeps a mid-pilot change from silently applying backward to past verdicts.
