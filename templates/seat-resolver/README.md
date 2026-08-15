# Configuration-driven seat resolver reference

This directory is an optional, dependency-free reference implementation. The handbook clauses are authoritative; this example is not mandated by them and does not amend them. If code, configuration, vectors, and clauses disagree, the clauses win.

Maintain one seat implementation per family. Do not copy this resolver into several repositories owned by the same family. Sharing means running the common conformance vectors against the family-owned implementation, not distributing one implementation everywhere. Families using the future alpha-loom distribution runtime must use that runtime directly and must not layer this example beneath or above it.

The implementation accepts only abstract model and lineage IDs. The shipped IDs are placeholders and do not name services, vendors, people, or family members.

## Files

| Path | Purpose |
| --- | --- |
| `config.example.json` | Complete version-1 rule, vocabulary, notes, and validation configuration |
| `roster.example.json` | Availability example with a deliberately invalid catalog stamp |
| `seat_resolver/rules.py` | Pure operational selection and generic law evaluators |
| `seat_resolver/catalog.py` | Restricted catalog parser and validator |
| `seat_resolver/cli.py` | Document validation, stamp gate, output, and exit handling |
| `bin/seat-resolver` | Operational launcher |
| `bin/run-conformance` | Shared-vector adapter launcher |
| `tests/test_resolver.py` | Unit and integration regression suite |

Both launchers disable bytecode writes before importing the package. Runtime behavior is deterministic, uses only the standard library, emits no timestamps, and fails closed on invalid input.

## Setup and adaptation

1. Copy `config.example.json` and `roster.example.json` to one private, family-owned location. Do not commit live availability data.
2. Replace the abstract vocabulary in `models` and `model_lineages` with that family's own abstract IDs. Keep operational service names outside this resolver.
3. Define the accepted `sizes` and `risk_areas` vocabulary.
4. Define reusable `panel_strategies`. Every strategy declares `selection_path` as `named_panel` or `machine`. A `fixed` strategy has an ordered panel, ordered substitute pool, and substitution cap. A `standing_rotation` strategy has one standing seat, ordered standing substitutes, an ordered rotation pool, and a rotation count.
5. Map every size to both `absent` and `present` risk states in `rule_table`. Risk presence selects the `present` cell, regardless of size. This permits a four-seat panel, a different risk vocabulary, or a different size table without source edits.
6. Set the per-family `floor3.effective` fact and list the affected `floor3.sizes`. When `sizes` is non-empty, `pre_effect_strategy` is required; when `sizes` is empty, it may be omitted. When the fact is false for a listed floor size and risk is absent, the pre-effect strategy is selected. The shared vectors provide their own per-case effective fact but derive seat requirements from these same strategies.
7. Set the writer premise and same-family authorization. Authorized seats must be distinct models with the writer's configured lineage; the writer model can never authorize itself or count as a review seat.
8. Add any `correlated_seat_exceptions` as exact six-field records. `scope` names strategies, `pair` names two models sharing one lineage, and `writer_condition` must equal the writer premise. Invalid or out-of-scope records never permit a seat.
9. Add any `downgrade_records`. A record scopes one model to strategies, supplies at least two distinct agent IDs, and cites both explicit owner approval and the required review notation. It can fill a shortfall only when the currently eligible review lineages are fewer than the required seats.
10. Configure exclusions, citations, operational notes, and selection/rules versions.
11. Point the roster's `catalog.path` at an absolute path. Hash the exact raw catalog bytes and put the lowercase digest in `catalog.adopted_digest`. The example deliberately contains a non-hex placeholder, so unfinished setup returns `CATALOG-UNSTAMPED`.
12. Run unit tests and the conformance adapter before adoption.

```sh
python3 -B -m unittest discover -s templates/seat-resolver/tests -v
python3 -B templates/seat-resolver/bin/run-conformance
python3 -B templates/seat-resolver/bin/seat-resolver \
  --size S --config /absolute/config.json --roster /absolute/roster.json
```

`--risk` and `--absent` are repeatable. `--format text` selects the stable line-oriented form; compact JSON is the default. The command also honors `SEAT_RESOLVER_CONFIG` and `SEAT_RESOLVER_ROSTER`, while explicit flags take precedence.

## Configuration fields and clause inputs

This table states which clause inputs each field represents. It does not make the configuration normative.

| Configuration field | Clause input represented |
| --- | --- |
| `sizes`, `risk_areas`, `rule_table` | L1-11 size-by-risk selection, including risk priority |
| `panel_strategies.*.required` | L1-9/L1-11 required seat floor |
| `panel_strategies.*.panel`, `standing`, `rotation_pool` | L1-10/L1-11 named or mechanically selected seats |
| `panel_strategies.*.selection_path` | L1-10 named-panel or machine-selection lineage path |
| `standing_substitutes`, `substitutes`, `substitution_cap` | L1-11 substitution limits and order |
| `models`, `model_lineages` | L1-10 abstract model and lineage vocabulary |
| `excluded_models` | Models that can never count as seats |
| `writer_assumed`, `same_family_authorization` | L1-10 writer exclusion premise and recorded same-family scope |
| `correlated_seat_exceptions` | L1-10 exact six-field, strategy-scoped correlated-lineage records |
| `downgrade_records` | L1-11 same-model/different-agent downgrade evidence and scope |
| `floor3.sizes`, `floor3.effective` | L1-11 per-family floor-3 scope and effective state; `sizes` may be empty for validation, but conformance v1 V02 expects pre-effective old floor 2 seats, so an empty list cannot satisfy every shared vector |
| `floor3.pre_effect_strategy` | L1-11 pre-effect strategy; required only when `floor3.sizes` is non-empty |
| `conformance.role_conflicts` | L1-10 designer, implementer, and orchestrator exclusions |
| `conformance.downgrade_fields` | L1-11 recorded downgrade conditions |
| `conformance.exception_fields` | L1-10 correlated-lineage record completeness |
| `conformance.seat_wait_*` | L1-11 lane-scoped wait record requirements |
| `citations`, `notes` | Human-readable provenance, availability boundary, writer premise, and wait guidance |
| `selection_fn_version`, `rules_version` | Local selection-function and adopted-rule identities |

Roster eligibility and repeatable `--absent` flags affect availability only; they never change the selected rule cell or required quorum. Missing configured roster entries are unavailable. Unknown roster keys fail before resolution. The configuration document itself is strictly validated and also fails closed.

Standing-seat substitution is resolved before rotation, reserving that replacement. Machine selection and substitute scans skip writer-conflicted, unauthorized same-family, duplicate-model, and unrecorded correlated-lineage candidates and continue to the next legal candidate. A named fixed panel does not count an unlawful named seat. Rotation shortfall is reported separately from a named missing standing seat. Fixed strategies preserve slot order and enforce their configured substitution cap.

`GO` means the resolved review seats can be started; it is not merge approval. `seat_instances` identifies model and agent instances, `uncountable` explains rejected candidates, and applied records appear in `applied_exception_records` and `applied_downgrade_records`. When an exception is applied, the eventual review record must cite that emitted record. Missing citation makes the completed review underseated even though the earlier panel-selection result was `GO`.

When a duplicated model appears, this implementation checks the first occurrence normally, including ordinary correlated-lineage exception handling. The clauses and conformance v1 still do not resolve whether later downgrade (demotion) duplicates in that situation also need correlated-seat treatment. This implementation does not lineage-check those later duplicates, so governing law must decide the behavior before a family implements or relies on that combination.

## Catalog gate

The catalog is hashed from exact raw bytes. Even when the adopted digest matches, the catalog is parsed and validated before seats can resolve. The restricted YAML profile rejects a byte-order mark, tabs, duplicate keys, anchors, aliases, tags, unsupported nesting, malformed dates, and missing, duplicated, or non-top-level `revision_effective_after`. It also validates the published top-level and row shapes needed by the reference gate.

When raw bytes differ from the adopted digest, `revision_effective_after` controls a closed adoption window. The grace window is inclusive: `today <= revision_effective_after` produces `catalog_state: grace` and an advisory note. A later day produces `CATALOG-STALE`. Grace does not mean adoption and does not independently imply `GO`.

## Output and frozen stamp meanings

JSON keys and text labels have a fixed order. Panel-derived arrays retain configured scan or slot order; risk inputs are sorted and deduplicated.

`risk_override` is the current name of the field formerly called `five_seat`. The rename avoids implying that a risk strategy must contain exactly five seats.

| Field/state | Frozen meaning |
| --- | --- |
| `size` | Canonical configured size selected by the case-insensitive CLI size lookup |
| `risk_areas` | Sorted, deduplicated configured risk inputs |
| `risk_override` (formerly `five_seat`) | `true` when at least one risk area is present and the rule table's `present` strategy is selected; it does not imply a five-seat count |
| `strategy` | Exact configured strategy name selected by the rule table or applicable pre-effect floor |
| `selection_path` | Exact configured `named_panel` or `machine` path for the selected strategy |
| `required` | Required seat count declared by the selected strategy |
| `panel` | Ordered named panel, or standing model followed by the mechanically selected rotation models |
| `unavailable` | Ordered configured candidates unavailable because of exclusion, explicit absence, missing roster entry, or roster ineligibility |
| `uncountable` | Deterministic model/reason entries rejected from quorum |
| `substitutions` | Ordered absent/replacement pairs actually applied |
| `final_seats` / text `seats` | Ordered models counted after selection, substitutions, and any recorded downgrade |
| `seat_instances` | Ordered seat model, agent identity when applicable, and ordinary/downgrade kind |
| `applied_exception_records` | Exact six-field records used to permit correlated lineage; later review citation is mandatory |
| `applied_downgrade_records` | Exact configured downgrade records used to fill lineage-constrained shortfall |
| `same_family_seats` | Ordered counted seats sharing the writer lineage under the configured authorization |
| `writer_assumed` | Writer model premise read from the exact configuration used |
| `missing` | Ordered named seats still unfilled after permitted substitution and downgrade processing |
| `rotation_shortfall` | Number of mechanically selected rotation seats still unfilled |
| `quorum_met` | `true` exactly when the final counted seat total equals `required` |
| `status: GO` | Valid rule row and complete quorum |
| `status: SEAT-WAIT` | Valid rule row but incomplete quorum |
| `note` | Empty on an ordinary `GO`; otherwise the configured seat-wait note and/or catalog grace advisory |
| `availability_note` | Exact configured explanation of the availability boundary |
| `writer_note` | Exact configured same-family writer premise note |
| `citations` | Ordered configured provenance and procedure citations |
| `roster_path` | Absolute resolved path of the roster consumed |
| `config_path` | Absolute resolved path of the configuration consumed |
| `catalog_digest` | Digest adopted in the roster; during grace it is not replaced with the current digest |
| `catalog_state: matched` | Adopted digest equals the exact catalog raw-byte digest, and the restricted document is valid |
| `catalog_state: grace` | Digests differ, the restricted document is valid, and today is inside the inclusive window |
| `selection_fn_version` | Selection-function version read from the exact configuration used |
| `config_digest` | SHA-256 of the exact raw configuration bytes consumed |
| `rules_version` | Rule-table identity read from configuration |
| `CATALOG-UNSTAMPED` | Missing or malformed path/digest stamp |
| `CATALOG-UNREADABLE` | Catalog cannot be read or fails the restricted format/schema gate |
| `CATALOG-STALE` | Digest differs after the inclusive adoption window |
| Catalog-failure `message` | Deterministic explanation of the catalog gate failure |
| Catalog-failure `roster_path` | Absolute resolved roster path associated with the catalog failure |

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | `GO` |
| 1 | `SEAT-WAIT` |
| 2 | Invalid command-line size, risk, absence, option, or format |
| 3 | Missing, unreadable, or invalid configuration/roster document; includes unknown roster keys |
| 4 | Catalog failure states: `CATALOG-UNSTAMPED`, `CATALOG-UNREADABLE`, or `CATALOG-STALE` |

## Conformance

`bin/run-conformance` reads `../conformance/vectors-v1.json` by default; `--vectors` overrides it. Every vector is mapped by kind to a generic evaluator. The adapter does not branch on vector IDs or copy expected fixture values into implementation logic.

Panel evaluation covers effective and pre-effect floors, high-risk override, writer and role-conflict exclusion, model-to-lineage consistency, malformed fact rejection, repeated models with the recorded downgrade conditions, and correlated lineages with six-field presence, well-formed values, validated pair and writer condition, lane scope, and review citation. Named and machine selection receive the same exception treatment. Separate evaluators validate lane wait records and requested/actual review records.

Each vector prints `PASS` or `FAIL`, followed by `passed`, `failed`, and `unrepresentable` totals. Unrepresentable inputs count as failures. Exit zero requires a non-empty vector set in which every loaded vector passes; empty vector sets fail closed.
