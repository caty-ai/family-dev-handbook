> **Machine translation.** The Japanese original ([architecture-parallel-map.md](../../../templates/architecture-parallel-map.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Parallel Safety Map Template (section to append to each repo's ARCHITECTURE.md)

```markdown
## Parallel Safety Map

> Input for parallel-GO decisions (family-dev-handbook L2-4).
> When a PR moves module boundaries, update this map in the same PR.

### Module Boundaries

| Module | Path | Primary responsibility | Notes |
|---|---|---|---|
| <!-- e.g.: iOS app --> | `ios-app/` | UI, audio input/output | |
| <!-- e.g.: gateway --> | `gateway/` | Session management, LLM relay | |

**Issues that don't cross module boundaries can generally run in parallel** (checking for file-set overlap is still mandatory).

### Hotspots (files needing parallel-work caution)

| File | Approx. line count | Co-located responsibilities | Split-off Issue |
|---|---|---|---|
| <!-- e.g.: MainView.swift --> | 2,500+ | UI + gestures + engine calls | #NNN |

**An Issue touching a hotspot must not run in parallel with other Issues in the same module.**
Prioritize working through split-off Issues (investments toward future parallelizability).

### Wide-Scope Issue History

| Issue | Description | When run | Run standalone? |
|---|---|---|---|
| <!-- e.g.: #NNN --> | Full UI overhaul | | |
```
