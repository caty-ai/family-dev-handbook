> **Machine translation.** The Japanese original ([brief-template.md](../../../templates/brief-template.md)) is canonical — if this page and the original disagree, the Japanese text wins.

# Delegation Brief Template

The single source of truth for the format of layer B ([docs/07](../docs/07-delegation-brief.md)). Every time you delegate, copy the following into the request text and fill it in. The heading strings are checked by machine, so don't deviate from the wording each family has settled on ([B-5](../docs/07-delegation-brief.md)).

## Brief body (B-1)

```markdown
## Implementation spec

<!-- Goal: what to build / fix, in 1-3 lines. Owning Issue: #number or URL (B-3: the Issue is the source of truth) -->
<!-- Scope allowed to touch: list of files / directories (must match the Issue's file prediction). Don't touch anything outside this scope -->
<!-- Front-loaded context: the facts, paths, specs, constraints, and environment quirks needed. Don't make the delegate go探索 for them (B-4) -->
<!-- Deliverable format: output file path(s), how much to report, what the report must include -->

## Implementation checks

<!-- Verification the worker runs on their own before delivering. Write it so it can be checked mechanically -->
- [ ] Tests / lint green (state the exact command and expected result)
- [ ] No diff outside the allowed scope
- [ ] (task-specific verification items)

## Review criteria

<!-- What the later review looks at. Show this to the worker up front too -->
- Correctness: <what counts as "correct" for this task>
- Scope: does it stay inside the declared file set?
- Worst failure mode: <the worst thing that could go wrong with this change is XYZ happening (B-4: name it explicitly)>
```

## Key points on writing it

- **Write assuming the delegate cannot read this conversation's history** (fresh context). "With the approach from before" or "that thing" don't exist as far as they're concerned
- **Preserve blindness for independent review seats** (B-4): hand every seat the identical brief, and don't mix in other seats' findings, your own prior analysis, or the conclusion you expect
- **Don't inline a long body into the request text**: it's fine to put the body in a file and give the request text just "read <path> and follow it." Depending on the execution environment, argument length limits can otherwise make the request die silently
- **Retries are finite** ([L1-6](../docs/02-issue-loop.md)): don't keep re-dispatching with the same brief. Add the observed failure to the front-loaded context and re-dispatch; if that's exhausted too, stop with evidence attached
