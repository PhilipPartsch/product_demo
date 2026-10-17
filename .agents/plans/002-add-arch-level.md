# Plan 002: Add an architecture level (`arch`) to the engineering model

Model change "option B" (discussion after plan 001 P4): insert an
architecture level between requirements and specifications.

```
before:  us ← req ← spec ← impl / test_spec
after:   us ← req ← arch ← spec ← impl / test_spec
```

(`←` = "links up to"; decisions and risks attach as before.)

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
- Work on branch `feat/engineering-model`; nothing is committed until the
  user asks.

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
| link names | |
| Q-FIELD | |
| Q-DEC | |
| Q-TEST | |
| Q-MIG | |
| Q-HOW | |

## 8. Learning log

| # | Phase | Question / finding | Answer | → Plan 100 |
|---|---|---|---|---|
| M1 | discussion | an architecture level was not asked for in the brief; it came up when comparing the installed skills with the model | plan 002 | §2.2 Q-TYPES: ask explicitly whether an architecture level is needed |
