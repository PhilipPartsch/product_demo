# Plan 002: Add an architecture level (`arch`) to the engineering model

Model change "option B" (discussion after plan 001 P4): insert an
architecture level between requirements and specifications.

```
before:  us ← req ← spec ← impl / test_spec
after:   us ← req ← arch ← spec ← impl / test_spec
```

(`←` = "links up to"; decisions and risks attach as before.)

> The architecture elements and the rest of the demo content were removed
> by [plan 003](003-remove-test-data.md); the model change itself stays.

This is the first **model change** on an existing configuration, so besides
the change itself it tests how the playbook handles changes: migrating
existing needs, keeping links / schema / workflow in sync, re-reviewing.
Lessons go into the learning log (§8) and then into plan 100.

Referenced: [001-engineering-model.md](001-engineering-model.md) (the model
being changed — its §2–§5 describe the current state),
[100-engineering-model-playbook.md](100-engineering-model-playbook.md),
[999-tool-bugs.md](999-tool-bugs.md).

Rules (as in plan 001):

- **ubc and Sphinx give the same result** after every phase.
- **Installed assets:** the profile's `draft-arch` / `review-arch` were
  removed in plan 001 (P4 follow-up); this plan builds its own. The installed
  pack `docs/quality/arch.toml` stays untouched; `ubc agent update` only in a
  shadow clone (plan 998 §4.7).
- **One link name per edge**; links, workflow traces and schema rules change
  together (plan 100 §4).
- **Tool bugs go into plan 999** in the same session.
- Work on branch `feat/arch-level` (from `main` after PR #2); nothing is
  committed until the user asks; the model change lands on `main` in **one**
  merge (CI 1 ratchets structural gaps).

## 0. Goal

At the end:

- type `arch` exists with its link to `req` and the changed `spec` link, in
  `docs/ubproject.toml`, `docs/schemas.json`, `[workflow]` and `[quality]`;
- the existing needs are migrated (every `spec` refines an `arch`, every
  `req` is fulfilled by an `arch`);
- template, stage skill and quality pack for `arch` exist and are mirrored;
  `draft-spec` reads its parent from `arch`;
- the model page, plan 001 and plan 100 describe the new model;
- `ubc script ci`, `ubc script sphinx`, `config-validate`, `doctor`, `trace`
  are clean; every new rule is negative-tested in both toolchains.

## 1. When

To be decided at G0 (Q-WHEN):

| Option | Effect |
|---|---|
| **a. Now** — between plan 001 P4 and P5 | the pilot (P8) and the CI (P7) are built on the final model; plan 001 P5–P9 continue afterwards |
| **b. Later** — after plan 001 P9, as a second playbook run | plan 001 finishes on the briefed model; this plan then also tests the CI tiers and the review gate on a model change (verdicts get `outdated`) |

**Decided (2026-10-17): b**, after plan 001 P9. Original recommendation: **a** if architecture (components, interfaces, trust
boundaries) is central to the demo; **b** if the first goal is a validated
end-to-end pilot.

## 2. Proposed design (to confirm at G0)

### 2.1 Type

| Directive | Title | Prefix | Authored as | Up-link |
|---|---|---|---|---|
| `arch` | Architecture Element | `ARCH_` | RST in `docs/architecture.rst` | `fulfills` → `req` |

An architecture element is one component (or interface) with its
responsibility, its interfaces to other elements and — where relevant — the
trust or safety boundary it sits on. A component diagram (mermaid) on the
page shows how the elements relate.

### 2.2 Links

| Link | Outgoing | Incoming | From → To | Change |
|---|---|---|---|---|
| `fulfills` | fulfills | fulfilled by | `arch` → `req` | **new** (`satisfies` is taken by `req` → `us`; the profile's arch → req `satisfies` would break one-link-per-edge) |
| `refines` | refines | refined by | `spec` → `arch` | **target changes** from `req` to `arch` |
| `decides`, `affects`, `mitigated_by` | — | — | — | `arch` added to their allowed targets |

`spec` no longer links to `req` directly: the chain goes through `arch`.

### 2.3 Fields

`arch` gets `safety_relevant`, `security_relevant` (required, like every
authored type) and no status (`status-none`). Optional new field, Q-FIELD:

| Field | Values | Purpose |
|---|---|---|
| `trust_boundary` | `true` / `false` | the element sits on a trust boundary (input from outside, privilege change) — drives security review and risks |

### 2.4 Schema (`docs/schemas.json`)

| Rule | Change |
|---|---|
| `$defs/type-arch` | new |
| `type-authored`, `type-no-status`, `type-decidable`, `type-decision-required`, `type-mitigation` | add `arch` |
| `link-arch-req` (violation) | new: `fulfills` `minItems: 1`, items `type-req` |
| `link-spec-req` → `link-spec-arch` (violation) | `refines` items `type-arch` |
| `cov-req` (info) | now: `fulfills_back` contains ≥ 1 `arch` |
| `cov-arch` (info) | new: `refines_back` contains ≥ 1 `spec` |
| `dec-present` (info) | now also on `arch` (Q-DEC) |

### 2.5 Workflow and quality

- New stage `archs`: `produces = "arch"`, `depends_on = ["reqs"]`, trace
  `up = "req"`, `link = "fulfills"`, `direction = "both"`, `min = 1`, route
  `scope = "stream"`, `granularity = "single"`, `path = "architecture.rst"`,
  author skill `draft-architecture` (own), review skill `review-arch` (own
  copy of the generic `review-requirement`, like `review-spec`), authoring text with the status rule and the
  decision / risk duty.
- Stage `specs`: `depends_on = ["archs"]`, trace `up = "arch"`,
  `link = "refines"`.
- Quality: own pack `docs/quality/architecture.toml` (the installed
  `arch.toml` + `decisions_documented`, and `trust_boundary_addressed` if
  Q-FIELD = yes); `[quality.type_configs.arch]` points to it.
- Diagram gate stays off (`[workflow.diagram] enabled = false`); the diagram
  is mermaid, rendered by both toolchains (plan 001 L14).

### 2.6 Templates and skills

- `.agents/templates/arch.rst` (fields, `fulfills`, body: responsibility,
  interfaces, boundary).
- Own skill `draft-architecture`, built like `draft-spec` (the name
  `draft-arch` would collide with the removed profile skill that
  `ubc agent update` restores in a shadow clone): incoming `req`, outgoing `arch` + updated
  component diagram, propose-first, status rule, append-only, decisions /
  risks hand-over (typical decisions: component split, technology,
  interface style; typical risks: trust boundary without input validation,
  single point of failure, unclear ownership of an interface).
- `draft-spec`: incoming becomes `arch` (`:refines:` → `ARCH_…`).
- `scripts/mirror_skills.py`; templates README table.

### 2.7 Test levels

Proposal (Q-TEST): unchanged — `test_spec` verifies `spec` only. Integration
tests that verify `arch` need their own link and stage (a trace edge has one
`up` type, PH-04 / PH-05) and are a later change.

### 2.8 Re-check against the state plan 001 left (2026-10-17, before Q0)

| Point | As written (after 001 P4) | State after 001 P9 | Consequence |
|---|---|---|---|
| Needs to migrate | `REQ_AUTH`, `REQ_LOG` | + `REQ_LOCKOUT`; specs `SPEC_HASH`, `SPEC_AUDIT`, `SPEC_LOCKOUT` | a third `arch` (lockout guard) or the guard inside the auth component (Q-MIG) |
| Decisions | attach as before | `dec-present` on us / req / spec / test_spec; `decisions` stage has one `outgoing` `decides` edge per parent type | Q-DEC = yes → `arch` in `type-decision-required` **and** a `decides` edge `up = "arch"`; each new `arch` gets a nested decision |
| Reviews | specs outdated | 28 verdicts | re-linking the specs outdates them, their nested decisions (option F) and probably their requirements (one-hop); new verdicts for `arch` + decisions |
| Risks | — | hash conditions on `SPEC_*` (`RISK_LOCKOUT_DOS`, `RISK_LOCKOUT_RESTART`, `RISK_AUDIT_VOLATILE`) | re-linking changes the specs' `fp` → these risks go stale → re-evaluate, `refresh_risk_links.py` (a real test of the mechanism) |
| CI | — | CI 1 ratchets structural gaps, CI 2 strict | one merge for the whole change |
| Further places | model page, `draft-spec` | + `engineering_model/workflow.rst`, `decisions_risks.rst`, `reports/decisions.rst` (type list of "needs without a decision"), template `spec.rst` (`:refines: {{REQ_ID}}`), `draft-requirement` ("specs refine the requirement"), playbook §8.1 (parent types) | added to Q1–Q4 |

## 3. Migration of the existing needs

Proposal (Q-MIG):

| New need | Fulfills | Refined by (changed) |
|---|---|---|
| `ARCH_AUTH` Authentication component | `REQ_AUTH` | `SPEC_HASH` (`:refines:` `REQ_AUTH` → `ARCH_AUTH`) |
| `ARCH_AUDIT` Audit log component | `REQ_LOG` | `SPEC_AUDIT` (`:refines:` `REQ_LOG` → `ARCH_AUDIT`) |

plus a component diagram (authentication writes to the audit log).

How (Q-HOW):

- **by hand**, in one step with the config change; or
- **through the workflow**: add the stage first, let `ubc agent next` /
  `draft-architecture` author the two `arch` needs (propose-first), then
  re-link the specs with the installed `change-request` skill — this also
  tests `change-request` (open point "group B" of the skills discussion).

Review effect: the two specs change (new parent) → their verdicts become
`outdated`; the new `arch` needs need verdicts. If plan 001 P8 has not run
yet (Q-WHEN = a), there are no verdicts yet and nothing is lost.

## 4. Phases

Each phase ends with a gate (show, ask, log in §8, wait for approval).

### Q0 Decisions

Ask (interactive question tool): Q-WHEN (§1), link names (§2.2), Q-FIELD
(§2.3), Q-DEC (decisions required on `arch`: yes / no), Q-TEST (§2.7),
Q-MIG (§3 split into components), Q-HOW (§3). Record the answers in §7.
**Gate G0.**

### Q1 Ontology, schema, migration, model page

1. `docs/ubproject.toml`: type `arch`, link `fulfills`, field
   `trust_boundary` (if chosen).
2. `docs/schemas.json` per §2.4.
3. Migration per §3 (Q-HOW = by hand) or only the config (Q-HOW = through
   the workflow, migration in Q3).
4. `docs/architecture.rst` in the toctree (between requirements and
   specifications).
5. Model page: diagram, types, links, schema rules, current needs.
6. Negative tests in a scratch copy (arch without `fulfills`, arch fulfilling
   a `us`, spec refining a `req`, arch with a status, arch without a
   decision) — ubc and Sphinx.
7. `ubc script ci`, `ubc script sphinx`, `needs.json` parity.
**Gate G1** (model page).

### Q2 Workflow and quality

1. Stage `archs`, changed stage `specs` (§2.5).
2. Own pack `docs/quality/architecture.toml`.
3. `config-validate`, `doctor`, `status`, `gaps`, `trace` (5 edges, all
   covered); `review-brief arch` loads the own pack.
**Gate G2** (validator output).

### Q3 Templates and skills

1. `.agents/templates/arch.rst`; README table.
2. `draft-architecture`; `draft-spec` changed; mirrors in sync
   (`scripts/mirror_skills.py --check`).
3. Q-HOW = through the workflow: author `ARCH_AUTH` / `ARCH_AUDIT` with
   `draft-architecture`, re-link the specs with `change-request`.
4. Dry run `ubc agent prompt --stage archs --id REQ_AUTH` and
   `--stage specs --id ARCH_AUTH` (scratch copy without review holds): right
   skill, status override, one parent only.
**Gate G3** (skill text, dry-run output).

### Q4 Plans

1. Plan 001: §2 / §4 / §4.1 / §5 tables point to the new state (or a note
   "changed by plan 002" where the history matters); §10 run log entry.
2. Plan 100: a section "Changing a model later" (order: links → schema →
   workflow → quality → templates → skills → migration → re-review; negative
   tests; dry run), and Q-TYPES asks for an architecture level explicitly.
3. Plan 999: new findings; Here column for PH-04 / PH-05 if the new edges
   touch them.
4. Plan 998: trigger T3 gains "diff installed skills against own copies"
   (`draft-arch` vs `draft-architecture`, `draft-requirement`, …).
**Gate G4.**

## 5. Files touched

`docs/ubproject.toml`, `docs/schemas.json`, `docs/architecture.rst` (new),
`docs/index.rst`, `docs/specifications.rst`,
`docs/engineering_model/index.rst`, `docs/quality/architecture.toml` (new),
`.agents/templates/arch.rst` (new), `.agents/templates/README.md`,
`.agents/skills/draft-architecture/`, `.agents/skills/review-arch/` (new) + mirrors,
`.agents/skills/draft-spec/` + mirrors, plans 001 / 100 / 998 / 999.

## 6. Risks of this plan

| Risk | Handling |
|---|---|
| `refines` changes its target type: an old `spec` → `req` link would pass the trace gate of a stage that still expects `req` | schema `link-spec-arch` (violation) catches it; negative test in Q1 |
| the removed profile `draft-arch` comes back with an `ubc agent update` in the repository | `update` only in a shadow clone (plan 998 §4.7) |
| own `review-arch` must score the component diagram too | rubric from the own pack (`architecture.toml`); check the brief in Q2 |
| more needs per chain make the pilot longer | migration needs only 2 `arch` needs |

## 7. Decisions (filled at G0)

| Question | Answer |
|---|---|
| Q-WHEN | **b — after plan 001 P9**, as a second playbook run (user, 2026-10-17). Before Q0: re-check §2–§3 against the state plan 001 leaves (verdicts exist then, CI tiers are active) |
| link names | `fulfills` (arch → req, new) + `refines` (spec → arch, target type changes) |
| Q-FIELD | yes — `trust_boundary` (bool, required on `arch`); review axis `trust_boundary_addressed` |
| Q-DEC | **no** — decisions on `arch` optional: `arch` not in `dec-present`, no `decisions_documented` axis in its pack; the `decisions` stage still gets an `outgoing` `decides` edge → `arch` so an optional decision is watched for staleness (no gaps) |
| Q-TEST | not now — `test_spec` verifies `spec` only |
| Q-MIG | "does not matter, all test data are removed later" → three elements matching the modules: `ARCH_AUTH` (`REQ_AUTH`), `ARCH_LOCKOUT` (`REQ_LOCKOUT`), `ARCH_AUDIT` (`REQ_LOG`) |
| Q-HOW | through the workflow: `draft-architecture` via the headless runner, re-link with `change-request`; failures fixed and logged |
| Evaluation | autonomous run of Q1–Q4 incl. reviews; the user reviews the HTML at the end (as plan 001 P8) |

## 8. Learning log

| # | Phase | Question / finding | Answer | → Plan 100 |
|---|---|---|---|---|
| M2 | Q0 | the demo content is test data that is removed later (user) | migration kept minimal | plan 100: ask early whether the content is real or demo data (it decides how much migration care is needed) |
| M3 | migration | the headless runner skipped a skill step (`record-risk` sign-off) in 2 of 3 runs | operator re-ran the step | plan 100: verify every runner output against the skill's checklist (here: risk links without `fp`) |
| M4 | migration | `draft-architecture` invented an HTTP / session design not in requirements or code; `change-request` turned it into new specs | reverted; grounding rule in the skill | plan 100 §4: stage skills ground new elements in requirements + existing code |
| M5 | migration | `change-request` cannot re-link existing needs to a new parent (PH-23) | re-link by hand | plan 100 "changing a model later": re-linking is a manual (or scripted) step |
| M6 | reviews | re-linking a spec outdated only the spec, not its nested decision or its requirement | re-reviewed the specs | plan 100: expect re-reviews where content or parents change |
| M1 | discussion | an architecture level was not asked for in the brief; it came up when comparing the installed skills with the model | plan 002 | §2.2 Q-TYPES: ask explicitly whether an architecture level is needed |

## 9. Run log

### Q1–Q4 (2026-10-17, autonomous; branch `feat/arch-level`)

- Q0: decisions in §7 (links `fulfills` / `refines`; `trust_boundary`;
  decisions on `arch` optional; no integration test level; three elements;
  migration through the workflow; autonomous + HTML review). Re-check §2.8.
- Q1: type `arch` (`ARCH_`), link `fulfills`, field `trust_boundary`;
  `schemas.json`: `type-arch`, `link-arch-req`, `link-spec-req` →
  `link-spec-arch`, `fields-arch`, `cov-req` (now `fulfills_back` arch),
  `cov-arch`, `arch` in the shared type lists (not in
  `type-decision-required`); `docs/architecture.rst` in the toctree.
- Q2: stage `archs` (`draft-architecture` / `review-arch`, trace
  `fulfills` up `req`, scope stream), `specs` depends on `archs` and traces
  `refines` up `arch`; `decisions` stage edge `decides` → `arch`; pack
  `docs/quality/architecture.toml` (installed `arch.toml` +
  `trust_boundary_addressed`); config-validate ok.
- Q3: template `arch.rst`; skills `draft-architecture` (from `draft-spec`)
  and `review-arch` (copy); `draft-spec` (parent `arch`),
  `draft-requirement` (downstream `archs`), template `spec.rst`; 12 own
  skills mirrored. Docs: model page, `workflow.rst`, `decisions_risks.rst`.
- Migration through the workflow (`ubc agent run --id REQ_*`, runner
  sonnet): `ARCH_AUTH_SERVICE`, `ARCH_LOCKOUT_GUARD`, `ARCH_AUDIT_LOGGER`
  with nested decisions (`DEC_ARCH_AUTH_SESSION`, `…_LOCKOUT_SEPARATION`,
  `…_AUDIT_SEPARATION`, all `proposed`) and 4 risks (`open`). Operator
  fixes: `record-risk` sign-off missing on 3 risks → refreshed (M3);
  `ARCH_AUTH_SERVICE` invented `POST /login` + server-side sessions → trimmed
  to the real scope, `DEC_ARCH_AUTH_SESSION` removed, transport risk
  reworded (M4); `**Responsibility**` labels added.
- Re-link: `change-request --id ARCH_AUTH_SERVICE` authored `SPEC_SESSION` /
  `TSPEC_SESSION` (`:status: draft`) instead of re-linking `SPEC_HASH`
  (PH-23) → reverted; the 3 specs re-linked by hand (`:refines: ARCH_…`);
  risks re-evaluated and signed off.
- Reviews: 12 verdicts (3 `arch`, 2 decisions, 4 risks, 3 re-reviewed
  specs); `verdict-check` clean. Honest findings kept as 1-scores:
  `ARCH_AUTH_SERVICE` / `ARCH_LOCKOUT_GUARD` `consistency` (the code does not
  wire the three modules; the guard's interface is one `attempt()` call).
- Checks: CI 1 steps all green; CI 2 blocks only on the user's items (2
  proposed decisions, 4 open risks); 46 needs identical in ubc and Sphinx.
- Findings → plan 999: PH-23; plan 998: §4.7 / §6.4 updated.
- HTML review (user): "i do not care about the test data" → content
  decisions delegated: `DEC_ARCH_LOCKOUT_SEPARATION`,
  `DEC_ARCH_AUDIT_SEPARATION` accepted; the 4 new risks accepted by the new
  accepted `DEC_ARCH_ACCEPT_DEMO_GAPS` (nested in `ARCH_AUTH_SERVICE`);
  consistency gaps left as review findings. 13 re-reviews; CI 2 steps
  locally all green.
