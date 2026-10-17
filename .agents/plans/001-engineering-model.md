# Plan 001: Engineering model for `docs/`

First run of the playbook [100-engineering-model-playbook.md](100-engineering-model-playbook.md)
on this repository. Defines the need-type model (types, fields, links), the
agentic workflow (stages, skills, templates, quality), the decision / risk
handling, the reports, the documentation of the model and the two CI
pipelines, for the ubCode / Sphinx-Needs project in `docs/`.

This is a **pilot**: every phase ends with a gate where the user reviews the
result, and the questions asked on the way go into the learning log (§9),
which feeds back into plan 100.

Referenced:
[100-engineering-model-playbook.md](100-engineering-model-playbook.md) (the
reusable recipe), [999-tool-bugs.md](999-tool-bugs.md) (tool bugs; new
findings go there), [998-tool-bug-recheck.md](998-tool-bug-recheck.md).

Rules that apply here:

- **ubc and Sphinx give the same result.** Every phase ends green in both
  toolchains (`ubc script ci`, `ubc script sphinx`). A parity break is a plan
  999 entry, not a silent workaround.
- **Installed (manifest) assets:** changed after P4 (user): the 11 unused
  profile skills are removed and `draft-requirement` / `draft-impl` carry
  this project's pattern; their manifest entries are gone. The remaining
  installed assets (generic review skills, `drive-workflow`,
  `change-request`, `ubc-agent-next`, `workflow-author`, `quality/*.toml`
  packs) stay untouched. **`ubc agent update` runs only in a shadow clone**
  (plan 998 §4.7, plan 999 PH-18).
- **Tool bugs go into plan 999** in the same session, with markers of this
  repository (`- **Origin:** product_demo`).
- Work on a branch (`feat/engineering-model`); plan changes and code stay
  uncommitted until the user asks.

## 0. Goal

At the end:

- `docs/schemas.json` validates elements and links (§4.1) in ubc and Sphinx;
- `docs/ubproject.toml` declares the types (§2), fields (§3), links (§4),
  the `[workflow]` (§5), `[quality]`, `[codelinks]` and `[test_reports]`;
  `ubc agent config-validate` and `ubc agent doctor` are `ok`;
- `src/` and `tests/` hold a small Python package with codelinks markers and
  pytest tests producing JUnit XML, mounted into the docs (§6);
- own skills and templates exist in `.agents/` and are mirrored to `.claude/`
  and `.github/agents/` (§5.3);
- `docs/engineering_model/` documents the model and the engineering process;
  `docs/reports/` has decision and risk overviews (§7);
- CI 1 (PR → `main`) and CI 2 (`main` → release) run as decided (§8);
- one full pilot chain exists and passes CI 2 locally (§6 phase P8);
- plan 100 is updated with the lessons of this run (§9).

## 1. Input brief and decisions

### 1.1 Input brief given by the user (plan 100 §2.1)

- **Types:** user story `us` (no two `us` on the same topic); requirement
  `req` (→ `us`); specification `spec` (→ `req`); implementation `impl` from
  code markers (→ `spec` at first); test specification `test_spec` (→
  `spec`); test results (Sphinx-Test-Reports / ubCode `test-file`);
  decisions (every element documents its decisions, embedded in the
  corresponding need); risks (documented as needs linked to the affected
  needs, including risks of the workflow itself).
- **Attributes, links:** suggestion requested, focused on safety and security
  relevant software development.
- **Workflow:** simple need-to-need stages; every skill states incoming and
  outgoing needs; a template per need type; every workflow defines how
  decisions and risks are documented, via templates and dedicated simple
  skills that get all information handed over by the workflow skill;
  evaluation jobs checking whether risks / decisions are resolved.
- **Overviews:** reporting RST pages for decisions and risks.
- **Results:** toml extended (types, fields, links, workflows, quality per
  type); model + engineering model documented in a docs section; CI updated.
- **Process:** discuss via `ubc agent install --detect --plan` or
  `pharaoh-onboard`; bring the user in to evaluate the configuration; GitHub
  CI per the ubCode CI/CD docs; repeatable via a plan folder in `.agents/`.

### 1.2 Decisions taken with the user (2026-10-17)

| Topic | Decision |
|---|---|
| Bootstrap | Model written by hand; `ubc agent install --detect --plan` and the blank `vmodel` profile only as reference / cross-check (detect sees only `req`/`spec`/`test` and drops `test`) |
| Integrity attributes | Generic: `safety_relevant`, `security_relevant` (bool); `integrity_level`, `owner`, `priority`, `verification_method`, `review_due` removed at G0 |
| `us` overlap | Review axis only (`no_overlap` in the `us` quality pack) |
| Decisions | **Nested** in the need they decide, plus explicit `decides` link; quality axis on `dec` **and** on every parent type ("decisions documented") |
| Code / tests | Python + pytest (JUnit XML for Sphinx-Test-Reports) |
| sphinx-mounts | Mount `src/` and `tests/` into the docs tree |
| Links | Rename + migrate the existing needs (`implements` → `refines`, `tests` → `verifies`) |
| Plans | This plan (001) + reusable playbook (100) |
| Evaluation | Model docs page; gate after every phase; ask more questions during this pilot |
| Risk / decision evaluation jobs | **Open** — spike phase P5 compares the options |
| Lifecycle | Built-in `status` **only on `dec` and `risk`** (G0, corrected after P2): `dec`: `proposed` / `accepted` / `superseded`; `risk`: `open` / `mitigated` / `accepted` / `closed`. No other type has a status. No default (explicit, required by the schema). The variant demo on `REQ_AUTH`'s status is dropped |
| Skills / templates | Source in `.agents/`, mirrored to `.claude/skills/` and `.github/agents/` |
| Schema (G0) | `docs/schemas.json` covering elements and links (§4.1); `violation` blocks both CI tiers, `info` (completeness) allowed on `main`, zero on release; coverage in schema **and** workflow; no safety / security propagation; decisions required on `us`, `req`, `spec`, `test_spec` |
| Decision / risk evaluation (G5, P5) | **Decisions:** nested; `decides` copied from the parent (`predicates`); `dec-nested` via derived field `parent`; staleness through the review gate (option F: `outgoing` trace edges on the `decisions` stage). **Risks:** hash-conditioned links `TARGET[fp=="…"]` on `affects` / `mitigated_by` (option E) instead of F; a stale risk is allowed on `main` (CI 1 suppresses `needs.link_condition_failed`) and blocks a release (CI 2). Unresolved items: schema `info` rules. Visibility: report A. Not used: B+, C, D |
| ubc license in CI | Repository `PhilipPartsch/product_demo` is **public** → no license key in CI. If it ever becomes private, the user adds `UBCODE_LICENSE_KEY` / `UBCODE_LICENSE_USER` as GitHub secrets and both pipelines pass them to the `ubc` steps |
| CI 1 (PR → `main`) | `open` topics allowed. Blocks on: build / lint errors, new structural gaps (ratchet), failing verdicts, pytest |
| CI 2 (`main` → release) | Runs on PRs / pushes to `release/*` **and** on `v*` tags. Requires: decisions / risks in a final status (§3), completeness for all other types — zero schema `info` findings, zero trace gaps, all verdicts present + fresh + passing, all test results `passed` |

### 1.3 Project context (plan 100 §1, filled in P0, 2026-10-17)

| Parameter | Value |
|---|---|
| `{DOCS}` | `docs/` (only `ubproject.toml` in the repository) |
| `{PLAN_DIR}` | `.agents/plans/`, `NNN-` |
| `{TOOL_BUGS}` | plan 999 (+ re-check plan 998) |
| `{MAIN}` | `main`; work branch `feat/engineering-model` |
| `{CI}` | GitHub Actions |
| `{REPO_VISIBILITY}` / `{UBC_LICENSE}` | public → no key |
| `{TOOLCHAINS}` | ubc 0.37.0 + Sphinx 9.1.0 / Sphinx-Needs 9.0.0 (resolved by `uv`), MyST-Parser 5.1.0 |
| Planned extensions | Sphinx-Codelinks 2.0.0, Sphinx-Test-Reports 3.0.0, sphinx-mounts 0.3.0 (PyPI latest) |
| `{HARNESSES}` | Claude Code (`.claude/`), GitHub Copilot (`.github/agents/`), generic (`.agents/`) |
| `{MANIFEST}` | `docs/.pharaoh/agent/install-manifest`, `vmodel` profile 21, 60 entries; `doctor`: `ok`, assets fresh |
| `{VARIANTS}` | yes (`variants.json`, `<{ var.* }>` in `platform_note`; the `<<…>>` status demo was dropped after P2) |
| `{EXISTING}` | `REQ_AUTH`, `REQ_LOG`, `SPEC_HASH`, `SPEC_AUDIT`, 2 `test` |
| `{CODE}` | none yet → Python + pytest, JUnit XML |

## 2. Types

| # | Directive | Title | Prefix | Authored as | Up-link |
|---|---|---|---|---|---|
| 1 | `us` | User Story | `US_` | RST | — |
| 2 | `req` | Requirement | `REQ_` | RST | `satisfies` → `us` |
| 3 | `spec` | Specification | `SPEC_` | RST | `refines` → `req` |
| 4 | `impl` | Implementation | `IMPL_` | codelinks one-line marker in `src/` | `implements` → `spec` |
| 5 | `test_spec` | Test Specification | `TSPEC_` | RST | `verifies` → `spec` |
| 6 | `test-file` / `test-suite` / `test-case` | Test results | (STR ids) | `.. test-file::` on the pytest JUnit XML | `executes` → `test_spec` (via `property_link_types`) |
| 7 | `dec` | Decision | `DEC_` | RST, **nested** in the parent need | `decides` → parent (and further needs) |
| 8 | `risk` | Risk | `RISK_` | RST | `affects` → any; `mitigated_by` → `req`/`spec`/`test_spec`/`dec` |

Notes:

- Type 6 is **not** declared in `[[needs.types]]`: `[test_reports]` adds the
  types itself; declaring them too aborts Sphinx (STR-03). `config-validate` /
  `doctor` count them as undeclared (PH-12) — expect and document that warning
  / error, or keep test results out of the `[workflow]` trace if it blocks.
- The existing `test` type is replaced by `test_spec` (migration, P1).
- `impl` is materialised by codelinks (`get_oneline_needs = true`) as in the
  blank `vmodel` profile: `# @<title>, <IMPL_ID>, impl, [<SPEC_ID>]`.
- Open check (P2): does a pytest `record_property("executes", "TSPEC_…")`
  reach the `test-case` need as a link via `[test_reports]
  property_link_types = { executes = "executes" }` in **both** toolchains?

## 3. Fields

Only decisions and risks have a lifecycle (G0, corrected after P2): the
built-in `status` is set on `dec` and `risk` only.

- **`ubproject.toml`** — `[needs.fields.status]` allows the union of the
  decision and risk values (`schema.enum = ["proposed", "accepted",
  "superseded", "open", "mitigated", "closed"]`), **no default** (a field
  default applies to every type — that is how all needs got `open` in P1 /
  P2).
- **`docs/schemas.json`** — `status-dec` / `status-risk` require the status
  and narrow its values; `status-none` (`maxLength: 0`) forbids it on every
  other type (§4.1).

| Type | Values | Final (release) |
|---|---|---|
| `dec` | `proposed` / `accepted` / `superseded` | `accepted`, `superseded` |
| `risk` | `open` / `mitigated` / `accepted` / `closed` | `mitigated`, `accepted`, `closed` |

`release_disallow_status = ["open", "proposed"]` therefore only concerns
decisions and risks. The other types are release-ready when complete (CI 2,
§1.2). The recording skills always write the status (`proposed` / `open`),
the templates show it.

Own fields (declared with `schema.type` / `schema.enum` in
`[needs.fields.*]`, so the enums hold for every type):

| Field | Types | Values | Purpose |
|---|---|---|---|
| `safety_relevant` | all except test results | `true` / `false` | safety relevance |
| `security_relevant` | all except test results | `true` / `false` | security relevance |
| `test_level` | `test_spec` | `unit` / `integration` / `system` | test level |
| `risk_category` | `risk` | `safety` / `security` / `technical` / `project` / `ai-workflow` | kind of risk |
| `severity` | `risk` | `low` / `medium` / `high` | impact |
| `likelihood` | `risk` | `low` / `medium` / `high` | probability |

Also from the profile (G0): `recovered_from` (array of repository-relative
source paths a need was recovered from, for `ubc agent reverse`), and
`[needs] id_required = true`, `id_regex = "^[A-Z]+_[A-Z][A-Z0-9_]*$"`.

Per-type rules on these fields (required fields, status values, risk
rules) are in the schema (§4.1).

Keep the variant data (`platform_note` with `<{ var.* }>`, `variants.json`)
working; `REQ_AUTH` uses it, which makes PH-01 / PH-02
**applies** as soon as `[workflow]` exists (record in plan 999 §2).

## 4. Links

| Link | Outgoing | Incoming | From → To |
|---|---|---|---|
| `satisfies` | satisfies | satisfied by | `req` → `us` |
| `refines` | refines | refined by | `spec` → `req` |
| `implements` | implements | implemented by | `impl` → `spec` |
| `verifies` | verifies | verified by | `test_spec` → `spec` |
| `executes` | executes | executed by | `test-case` → `test_spec` |
| `decides` | decides | decided by | `dec` → any |
| `affects` | affects | affected by | `risk` → any |
| `mitigated_by` | mitigated by | mitigates | `risk` → `req` / `spec` / `test_spec` / `dec` |

Each link has its own name per edge on purpose: PH-04 (two stages with the
same link + target are attributed to one stage) and PH-05 (traces apply per
type, no per-stage filter) bite when one link name serves several edges.
PH-13 (generic `links` satisfies `min = 1`) — do not use the generic `links`
field in the model.

### 4.1 Schema (`docs/schemas.json`) — elements and links

Sphinx-Needs schema validation
(<https://sphinx-needs.readthedocs.io/en/stable/schema/index.html>), loaded
with `[needs] schema_definitions_from_json = "schemas.json"`; checked by
`ubc check` / the IDE and by the Sphinx build. File shape: `$defs` (reusable
fragments) + `schemas` (rules with `id`, `severity`, `message`, `select`,
`validate.local` / `network` / `network_back`).

**`$defs`:** one `type-<t>` per type (`{"properties": {"type": {"const":
"<t>"}}}`) for `us`, `req`, `spec`, `impl`, `test_spec`, `dec`, `risk`,
`test-case`; `status-<s>` fragments where rules depend on the status.

**Severity mapping (G0):**

| Severity | Meaning | CI 1 (→ `main`) | CI 2 (→ release) |
|---|---|---|---|
| `violation` | always wrong: bad field value, missing required field, wrong link target type, missing mandatory up-link | blocks | blocks |
| `info` | completeness: coverage, decisions present, risk resolved | allowed | must be zero |

Sphinx logs `info` / `warning` as warnings and `violation` as errors (SN-01),
so the Sphinx parity build sets `suppress_warnings = ["sn_schema_info"]`
(still recorded in `schema_violations.json`); CI 2 reads
`schema_violations.json` (Sphinx) / the `ubc check` diagnostics and requires
no finding at all. `warning` is not used.

**Element rules (`validate.local`, severity `violation`):**

| Id | Select | Rule |
|---|---|---|
| `status-dec`, `status-risk` | `dec`, `risk` | `required: [status]` + the type's enum |
| `status-none` | all other types (incl. `impl`, test results) | `status` `maxLength: 0` (no status) |
| `fields-common` | `us`, `req`, `spec`, `impl`, `test_spec`, `dec`, `risk` | `required: [safety_relevant, security_relevant]` |
| `fields-test-spec` | `test_spec` | `required: [test_level]` |
| `fields-risk` | `risk` | `required: [risk_category, severity, likelihood]` |
| `dec-nested` | `dec` | has a parent need (`parent_need` set) — check P3 whether the schema sees it |

**Link rules (`validate.local` counts + `validate.network` target types,
severity `violation`):**

| Id | Select | Link | Rule |
|---|---|---|---|
| `link-req-us` | `req` | `satisfies` | `minItems: 1`; `items` → `type-us` |
| `link-spec-req` | `spec` | `refines` | `minItems: 1`; `items` → `type-req` |
| `link-impl-spec` | `impl` | `implements` | `minItems: 1`; `items` → `type-spec` |
| `link-tspec-spec` | `test_spec` | `verifies` | `minItems: 1`; `items` → `type-spec` |
| `link-result-tspec` | `test-case` | `executes` | `items` → `type-test_spec` (min 1 if P2 shows every case carries it) |
| `link-dec` | `dec` | `decides` | `minItems: 1`; `items` not `dec` |
| `link-risk-affects` | `risk` | `affects` | `minItems: 1` |
| `link-risk-mitigation` | `risk` | `mitigated_by` | `items` → `req` / `spec` / `test_spec` / `dec` (`anyOf`) |
| `risk-mitigated` | `risk` + `status-mitigated` | `mitigated_by` | `minItems: 1` |
| `risk-accepted` | `risk` + `status-accepted` | `decides_back` | `network_back`: `contains` a `dec` with `status` `accepted` |

**Completeness rules (`validate.network_back`, severity `info`):**

| Id | Select | Rule |
|---|---|---|
| `cov-us` | `us` | `satisfies_back` contains ≥ 1 `req` |
| `cov-req` | `req` | `refines_back` contains ≥ 1 `spec` |
| `cov-spec-impl` | `spec` | `implements_back` contains ≥ 1 `impl` |
| `cov-spec-test` | `spec` | `verifies_back` contains ≥ 1 `test_spec` |
| `cov-tspec-result` | `test_spec` | `executes_back` contains ≥ 1 `test-case` |
| `dec-present` | `us`, `req`, `spec`, `test_spec` (G0) | `decides_back` contains ≥ 1 `dec` |
| `risk-open` | `risk` + `status-open` | always reports (an open risk is a release finding) |
| `dec-proposed` | `dec` + `status-proposed` | always reports |

Coverage is checked **twice on purpose** (G0): by the workflow traces
(`ubc agent gaps`, the agent loop) and by these schema rules (IDE, plain
Sphinx build). Keep both in sync — one row per edge in §4 / §5.1 / here.

No propagation of `safety_relevant` / `security_relevant` along links (G0):
each need sets its own values.

To check in P1 / P3 (both toolchains; findings → plan 999):

- enum on core field `status` (done in P1: works in both);
- back-link names in `network_back` (`<link>_back`) for STR `test-case`
  needs and for nested `dec`;
- SN-05 (`contains` on a list field needs `items` in Sphinx);
- nesting depth (max 4 levels) is enough;
- ubc and Sphinx report the same findings (compare `schema_violations.json`
  with `ubc check` output).

## 5. Workflow

### 5.1 Stages (as built in P3)

All routes are relative to `docs/`, one file per stage (`granularity =
"single"`): the project is small, so no `streams/` layout. Regular stages use
`scope = "stream"` (P4): with `global` the prompt orders links to ALL needs
of the up type (PH-16).

| Stage | Produces | Depends on | Trace (up, link, direction, min) | Author skill | Review skill | Route |
|---|---|---|---|---|---|---|
| `user_stories` | `us` | — | — | `draft-us` (own, P4) | `review-feat` | `user_stories.rst` |
| `reqs` | `req` | `user_stories` | `us`, `satisfies`, both, 1 | `draft-requirement` | `review-requirement` | `requirements.rst` |
| `specs` | `spec` | `reqs` | `req`, `refines`, both, 1 | `draft-spec` (own, P4) | `review-spec` (own, P4) | `specifications.rst` |
| `code` | `impl` | `specs` | `spec`, `implements`, both, 1 | `draft-impl` | — | `../src` (global) |
| `test_specs` | `test_spec` | `specs` | `spec`, `verifies`, both, 1 | `draft-test-spec` (own, P4) | `review-test-spec` (own, P4) | `verification.rst` |
| `decisions` | `dec` | — (optional) | — | `record-dec` (own, P4) | `review-decision` | per-need `{id}` (not used for authoring) |
| `risks` | `risk` | — (optional) | — | `record-risk` (own, P4) | `review-risk` (own, P4) | `risks.rst` |

Results of the P3 checks (details in §10, plan 999):

- **No `test_results` stage:** `config-validate` does not know the types
  `[test_reports]` declares (PH-12). Test results are covered by
  `link-result-tspec`, `cov-tspec-result` and `result-passed` (schema).
- **Decisions / risks are created by the stage skills (G3).** A global stage's
  prompt asks for one element covering *all* needs of its `up` type, and
  routes name files, never a place inside a need (PH-16). So each stage skill
  hands a complete payload to `record-dec` (nests the `dec` in its parent) or
  `record-risk` (appends to `risks.rst`); the `decisions` / `risks` stages
  carry no trace and exist for review + verdicts. Their `authoring` text says
  not to author through them.
- **"Every need has decisions"** (`us`, `req`, `spec`, `test_spec`): schema
  rule `dec-present` (info) only — a trace edge has one `up` type, and
  `direction = "both"` would make each decision decide all four types.
- **No `[workflow.lifecycle]`:** its states gate judges every need, also the
  types without a status (PH-14). Status values are checked per type by the
  schema. `release_disallow_status = ["open", "proposed"]` stays.
- **Prompt status (G3):** the engine orders `:status: draft` for every stage
  (PH-15). Every stage's `authoring` text states the right rule (none /
  `proposed` / `open`) and that it overrides the generic line; the schema
  rejects a wrong value.
- **Existing files:** the prompt says "CREATE THE FILE" for existing
  single-file routes (PH-17); skills must append, never rewrite.
- **Fingerprint:** a nested `dec` changes the parent's content → parent
  verdict `outdated` → re-review; intended. Grandchildren (PH-03) checked in
  the pilot.
- `reqs` keeps the installed `draft-requirement` (unchanged); its decision /
  risk duties come from the stage's `authoring` text.

### 5.2 Templates and hand-over payloads

`.agents/templates/`:

- `us.rst`, `req.rst`, `spec.rst`, `test_spec.rst`, `dec.rst` (nested form,
  Context / Alternatives / Consequences / Rationale), `risk.rst` — RST with
  all fields of §3 and the links of §4, placeholders `{{…}}`;
- `impl.py`, `test.py` — the one-line marker + pytest `record_property`
  pattern;
- `handover/decision.json`, `handover/risk.json` — the payload a workflow
  skill hands to the recording skills.

Decision payload: `target_need`, `title`, `context`, `alternatives[]`,
`chosen`, `consequences`, `rationale`, `decides[]`, `status`,
`safety_relevant`, `security_relevant`.
Risk payload: `title`, `description`, `affects[]`, `risk_category`,
`severity`, `likelihood`, `mitigation` (text), `mitigated_by[]`,
`status`.

### 5.3 Skills (as built in P4 and its follow-up)

Source in `.agents/skills/<name>/SKILL.md`, mirrored byte for byte to
`.claude/skills/<name>/SKILL.md` and `.github/agents/<name>.agent.md` by
`scripts/mirror_skills.py` (every skill without a manifest entry; `--check`
in CI 1).

| Skill | Stage / use | Kind | Origin |
|---|---|---|---|
| `draft-us` | `user_stories` | stage author | own |
| `draft-requirement` | `reqs` | stage author | profile name, **this project's pattern** (manifest entry removed) |
| `draft-spec` | `specs` | stage author | own |
| `draft-impl` | `code` | stage author | profile name, **this project's pattern** (manifest entry removed) |
| `draft-test-spec` | `test_specs` (+ pytest test) | stage author | own |
| `record-dec`, `record-risk` | called by the stage skills | recording ("stupid"): validate the payload, render, nothing else | own |
| `review-feat`, `review-requirement`, `review-decision` | review of `us`, `req`, `dec` | generic review | installed, unchanged |
| `review-spec`, `review-test-spec`, `review-risk` | review of `spec`, `test_spec`, `risk` | generic review | own copies of `review-requirement` |
| `drive-workflow`, `ubc-agent-next` (command), `workflow-author` (Copilot agent) | drive the loop | engine-generic | installed, unchanged |
| `change-request` | change cascade (engine) | engine-generic | installed, unchanged — tested in the pilot (nested decisions!) |
| `evaluate-decisions`, `evaluate-risks` | evaluation | — | only if P5 picks the agent-skill option |

Removed (unused in this model): `draft-arch`, `review-arch`, `draft-test`,
`record-decision`, `pharaoh-onboard`, `record-recovery-ledger`,
`recover-architecture-from-code`, `recover-need-from-cluster`,
`recover-requirement-from-code`, `resolve-github-intent`,
`split-recovered-need`. Plan 002 builds its own architecture skills.

Every stage skill states its incoming needs (what to read, via `ubc agent
audit` / `context`), outgoing needs (type, template, route, links), the
status rule, append-only editing, and the **decision and risk triggers** of
its stage with the hand-over to `record-dec` / `record-risk`.

### 5.4 Quality packs

Own packs in `docs/quality/` (installed packs stay untouched):

- `us.toml` — based on `feat.toml` + axis `no_overlap` (no other `us`
  covers the same topic; the reviewer gets the list of existing `us` via
  `ubc agent context` / the brief);
- `spec.toml`, `test_spec.toml`, `risk.toml`;
- `dec.toml` — based on `decision.toml` (`context_present` required);
- the packs of `us`, `req`, `spec`, `test_spec` get axis
  `decisions_documented` (the need carries the nested `dec` for its relevant
  choices).

`[quality.type_configs.<type>] criteria_file = …` per type;
`[quality.required] parent_fit = 1`.

## 6. Phases

Each phase ends with a **gate**: show the result, ask the gate questions,
log answers in §9, wait for approval.

### P0 Baseline

1. Branch `feat/engineering-model`; versions (`ubc --version`, Sphinx-Needs
   resolved by `uv`, Sphinx-Codelinks, Sphinx-Test-Reports, sphinx-mounts) in §9.
2. Save `ubc agent install --detect --plan` output and the blank `vmodel`
   profile (`ubc agent install` in an empty scratch dir) as reference in the
   scratchpad; diff against §2–§5.
3. Gate G0: user confirms §1–§5 still match intent.

### P1 Ontology + migration + model page

1. `docs/ubproject.toml`: types (§2), fields with `schema.type` /
   `schema.enum` (§3), links (§4), `id_required`, `id_regex`,
   `schema_definitions_from_json`.
2. `docs/schemas.json`: `$defs`, element rules and link rules of §4.1
   (severity `violation`); the migrated needs must pass them.
3. Migrate `docs/specifications.rst` (`:implements:` → `:refines:`),
   `docs/verification.rst` (`test` → `test_spec`, `:tests:` → `:verifies:`,
   only to specs). Add one `us` per existing req (US for auth, logging),
   `satisfies` links.
4. Restructure into `docs/streams/<stream>/` if the routes of §5.1 require it
   (keep `index.rst` toctree working).
5. `docs/engineering_model/index.rst` first version: type diagram (check the
   renderer works in both toolchains — graphviz / mermaid / needflow), tables
   of types, fields, links and schema rules.
6. `ubc script ci` + `ubc script sphinx` green.
7. **Gate G1 (model docs page):** user reviews the rendered page incl. the
   schema rule table.

### P2 Code, tests, mounts

1. `pyproject.toml`, `src/product_demo/` (auth, audit modules), `tests/`
   with pytest; markers per `templates/impl.py`, `templates/test.py`.
2. `[codelinks]` project `code` (`src_dir` relative to `docs/`,
   `get_oneline_needs = true`, field `implements`) and `.. src-trace::` in
   `docs/implementations.rst`.
3. `[test_reports]` with `property_link_types`, pytest
   `--junitxml=docs/_test_results/junit.xml` (gitignored, generated in CI),
   `.. test-file::` in the results page.
4. sphinx-mounts for `src/` and `tests/` in `conf.py`; Sphinx script deps:
   `sphinx-codelinks`, `sphinx-test-reports`, `sphinx-mounts`. Check what ubc
   does with the mounts (parity → 999 entry if it differs).
5. Re-check CL-03, CL-07, UB-01, UB-14 now that codelinks is used (plan 999
   §2 **Here** column).
6. **Gate G2:** user sees `impl` and test-case needs in both HTML builds.

### P3 Workflow + quality + schemas

1. `[workflow]` per §5.1, `exempt_status`, `orphan_exempt_types`,
   `release_disallow_status = ["open", "proposed"]`, lifecycle states (§3).
2. `[quality]` + own packs (§5.4).
3. `docs/schemas.json` per §4.1 (completeness rules + risk / decision
   rules; element and link rules are already in from P1); Sphinx
   `suppress_warnings = ["sn_schema_info"]`; compare ubc and Sphinx findings.
4. `ubc agent config-validate`, `doctor`, `status`, `gaps`, `trace`.
5. Resolve the open checks of §5.1; new tool findings → plan 999.
6. **Gate G3 (validator output):** user reviews validate / doctor / status /
   gaps output and the list of accepted gaps.

### P4 Templates + skills

1. Templates + payloads (§5.2).
2. Skills (§5.3) + `scripts/mirror-skills.sh`.
3. Wire `author_skill` / `review_skill` / `authoring` text into `[workflow]`.
4. Dry run: `ubc agent prompt --stage <each stage>` renders a sensible brief.
5. **Gate G4:** user reads one stage skill and both recording skills.

### P5 Spike: risk / decision evaluation jobs

Compare (prototype each briefly, cost / benefit table in §9):

| Option | How | Pros / cons to check |
|---|---|---|
| A CI report | `needtable` / `needlist` filters (`type == "risk" and status == "open"`, no `mitigated_by`, `type == "dec" and status == "proposed"`, linked needs changed since the decision) + `ubc report` / Jinja | cheap, visible, non-blocking; "today" in filters? |
| B CI gate | script on `needs.json` (or schemas) failing CI 2 on unresolved risks / proposed decisions | strict; fits CI 2 only |
| C Agent skill | `evaluate-risks` / `evaluate-decisions`: read the open items, check whether the linked needs changed / mitigations exist, propose status updates for human approval | judgment, catches stale decisions; costs tokens |
| D Scheduled | weekly GitHub Action running A (+ C via `ubc agent run`) and opening an issue | catches stale items without a push |

**Gate G5:** user picks the option(s); P6 / P7 implement them.

### P6 Reports + engineering-model docs

1. `docs/reports/decisions.rst`, `docs/reports/risks.rst`: tables (open,
   by category / stage), pies, needflow of risks → affected needs;
   decision log (all `dec` with their parents).
2. Extend `docs/reports/needs_overview.html.j2` if useful.
3. `docs/engineering_model/`: types, fields, links, workflow (stage table,
   which skill, which template), decision / risk handling, quality packs, the
   two CI pipelines, how to run `ubc agent next` / `prompt` / `run`.
4. **Gate G6:** user reviews the docs section.

### P7 CI

Replace `.github/workflows/docs.yml` by:

- `ci-main.yml` — on `pull_request` to `main`, `push` to `main`:
  `ubc script check`, `ubc script html`, Sphinx `-W` build, pytest (JUnit
  first, docs after), `ubc agent config-validate`, `ubc agent doctor`,
  schema `violation`s fail (ubc check, Sphinx errors), `info` allowed,
  `ubc agent release-check` against `.pharaoh/release-baseline` (ratchet: new
  gaps fail), verdict gate **failing / malformed only** (`verdict-check` exits
  non-zero on `missing` too — filter its JSON with `jq`), skill mirror check.
  `open` needs allowed — verify that `release-check` without
  `--with-verdicts` does not apply `release_disallow_status`; otherwise run
  `gaps` + a baseline diff instead.
- `ci-release.yml` — on `pull_request` / `push` to `release/*` and `push`
  of tags `v*`: everything of CI 1, plus `ubc agent gaps` (zero gaps, no
  baseline), `ubc agent verdict-check` (nothing missing / failing / outdated),
  no schema finding of any severity (`schema_violations.json` + `ubc check`),
  no decision / risk with `status` `open` / `proposed`, every test result `passed` (from `release_disallow_status` or a
  `needs.json` check), plus the P5 result if it is a gate.
- Both upload the HTML site; ubc pinned via `UBC_VERSION` (keep in sync with
  plan 998), tools of the Sphinx build pinned.
- **Gate G7:** user sees a green CI 1 run on the PR and a CI 2 run on a test
  `release/*` branch.

### P8 Pilot chain

First review the 8 existing needs (`us`, `req`, `spec`, `test_spec`) with
the review skills + `verdict-submit` (G3), so CI 1 starts without review
debt. Then, using `ubc agent next` / `prompt` (propose-first, user approves
each artefact): one new feature end to end, e.g. "password reset":
`us` → `req` → `spec` (with a nested `dec`, e.g. token lifetime) → `impl`
→ `test_spec` → pytest result, plus one `risk` (e.g. token brute force,
`mitigated_by` the spec) and one `ai-workflow` risk. Reviews via the review
skills + `verdict-submit`. Then bring the decisions / risks to a final status (§3), complete the chain and run CI 2
locally / on a test `release/*` branch.

During the pilot **ask more**: after each stage ask the user what was
missing in the brief, the template, the skill, the review — log in §9.

**Gate G8:** user accepts the chain and CI 2 result.

### P9 Retro

1. Fold §9 into plan 100 (questions catalogue, steps, pitfalls).
2. Plan 999: Here column for every entry that became applies (PH-01…05, PH-08,
   PH-12, PH-13, UB-14, UB-19, SN-01, SN-05, STR-03, STR-05, CL-*); new entries.
3. Plan 998: triggers T3 / T6 updated for the adopted features.

## 7. Files touched

`docs/ubproject.toml`, `docs/schemas.json`, `docs/conf.py`, `docs/*.rst` (migration),
`docs/streams/**`, `docs/engineering_model/**`, `docs/reports/**`,
`docs/quality/{us,spec,test_spec,risk,dec}.toml`, `src/**`, `tests/**`,
`pyproject.toml`, `.agents/templates/**`, `.agents/skills/<own>/**` (+
mirrors), `scripts/mirror-skills.sh`, `.github/workflows/{ci-main,ci-release}.yml`
(replacing `docs.yml`), `.gitignore`, `README.md`, plans 100 / 998 / 999.

## 8. Risks of this plan

| Risk | Handling |
|---|---|
| Nested decisions not supported by routes | P3 check, workaround + 999 entry |
| Test results not traceable in `[workflow]` (PH-12) | keep them out of the trace, check in CI 2 via `needs.json` |
| Variant fields + verdicts (PH-01 / PH-02) | keep pilot needs variant-free; document |
| ubc / Sphinx parity for mounts, codelinks, STR | parity check each phase; 999 entries |
| CI 2 too strict to ever pass | pilot (P8) proves a passing release before merge |

## 9. Learning log

Filled during the run. Per entry: phase, question / finding, answer /
decision, consequence for plan 100.

| # | Phase | Question / finding | Answer | → Plan 100 |
|---|---|---|---|---|
| L1 | discussion | detect plan only knows existing types; drops `test` | write model by hand, detect as cross-check | §2 step B |
| L2 | discussion | CI must allow open topics on `main` but be strict on release | two pipelines | §1.2 Q-CI |
| L3 | plan review | the playbook took run 001's basic model as given instead of asking for it | input brief step added | §2.1, §3 C |
| L4 | plan review | the playbook also hard-wired run 001's context (paths, CI platform, language, CI tiers, release markers, skill names) and used its answers as defaults | parameters table, "ask when" + "seen in runs" columns, conditional phases | §1, §2.2, §3 D, §5, §6 |
| L6 | P0 | stage routes are relative to `{DOCS}` (profile: `specs/{stream}/…`, `src`), plan had `docs/…` | routes fixed in §5.1; code roots `../src`, `../tests` | §3 B: "routes and `src_dir` are relative to `{DOCS}`" |
| L7 | P0 | manifest mixes path bases: harness copies relative to repo root, `quality/*.toml` relative to `docs/`; empty leftover `.pharaoh/agent/` + `quality/` at repo root | `doctor` ok; leftovers to be removed (G0) | §6 pitfall; plan 999 candidate if `update` mis-resolves |
| L8 | P0 | blank profile differs from the brief (see §10 P0) | asked at G0 | §3 B: diff the brief against the blank profile, ask each deviation |
| L9 | G0 | user removed `integrity_level`, `owner`, `priority`, `verification_method`, `review_due` from the suggested fields | lean field set; evaluation jobs cannot use due dates | §2.1 b: offer the suggestion as a pick list, not a package |
| L10 | G0 | user: no own status fields for decisions / risks, use built-in `status` | per-type status values via schemas; release blocks `open` + `proposed` | §2.2 Q-LIFE: ask for per-type values on the one `status` field |
| L11 | G0 | status values: toml declares the union, `schemas.json` narrows per type | two-layer status model | §4 rule: shared fields = union in toml, per-type values in schemas |
| L12 | G0 | user had not asked for a schema of elements + links up front | schema section §4.1: severity per CI tier, element / link / completeness rules, coverage in schema + workflow, no propagation, decisions on us / req / spec / test_spec | §2.1 e, §2.2 Q-SCHEMA…Q-XREQ, §4, §5, §6 (already folded in) |
| L13 | P1 | ubc supports only `allOf`, `properties`, `required`, `type`, `unevaluatedProperties` in `select` / `local`; `not` breaks both toolchains | allow-lists in `$defs` (`type-decidable`) | §4 rule: write schemas with allow-lists, no `not` / `anyOf`; negative-test every rule in a scratch copy |
| L14 | P1 | diagrams: ubc renders `mermaid` (and `needflow` via mermaid), `graphviz` only as placeholder; Sphinx `needflow` uses graphviz (`dot` needed in CI) | mermaid + `sphinxcontrib-mermaid` | §4 rule: diagrams in mermaid; CI installs graphviz for Sphinx `needflow` — **correction (P6):** Sphinx-Needs' default `needflow` engine is PlantUML, not graphviz; without PlantUML the page showed "PlantUML is not available!" and `-W` passed (SN-09); fixed with `[needs] flow_engine = "graphviz"` + `sphinx.ext.graphviz` |
| L15 | P1 | existing variant values (`win_auth`) violated the new status set | changed to `done` / `open` | §3 A: check `{EXISTING}` values against new enums before migration |
| L16 | P2 | sphinx-mounts mounts documents only (`.rst` / `.md`), not code; "mount src/ + tests/" = docs next to code (`src-trace` / `test-file` pages) | pages moved into `src/` and `tests/` | §2.2 Q-MOUNT: explain that mounts carry docs, not code |
| L17 | P2 | test-result needs require the JUnit file: every build (local, CI, Sphinx) must run the tests first | `tests` script first in `ci` | §5: tests before any docs build; §3 D P2 done-criterion |
| L18 | P2 | test-result type names are `testcase` etc., not the documented `test-case` | schema fixed | §4 rule: take type names from `needs.json`, not from docs; negative-test every `select` |
| L19 | P2 | codelinks one-line fields are positional; required after optional is refused | all marker fields required | §4 rule |
| L20 | P2 | lifecycle meant for decisions and risks only; applied to all types, and a field default spread it to generated needs | status only on `dec` / `risk`, no default | §2.2 Q-LIFE: ask *which types* have a lifecycle; §4 rule: a field default applies to every type |
| L21 | P2 | `properties.X.const` in a `select` matches needs without `X` | `required: [X]` in conditional selects | §4 rule; negative-test with the field absent |
| L22 | P2 | forbidding a field without `not`: `maxLength: 0` works in both, `type: null` refused for a string field | `status-none` | §4 rule |
| L23 | P3 | Pharaoh's stage model assumes every stage covers a whole upstream type and authors into files; per-need cross-cutting elements (nested decisions) do not fit | created by stage skills + recording skills; review-only stages | §2.2 Q-XCUT: explain the engine limits before the user picks "nested" |
| L24 | P3 | lifecycle gate and prompt status are global, not per type | no lifecycle; status rules in authoring texts + schema | §4 rule; §6 pitfall |
| L25 | P3 | schema `info` = completeness works as a tier split: `--deny warning` passes, `--deny info` fails; Sphinx needs `suppress_warnings` | CI 1 / CI 2 commands | §5 CI blueprint |
| L26 | P4 | `scope = "global"` makes every new need link ALL upstream needs; `stream` anchors on one | regular stages `stream` | §4 rule: regular stages `scope = "stream"`; dry-run every stage with `ubc agent prompt --stage` |
| L27 | P4 | only `ubc agent` takes `-p`; `ubc check` / `build` take a path, `ubc script` `--path` | skills fixed | §4 rule: test every command a skill names |
| L28 | P4 | review skills are generic (name only) — own review skills are copies | copies + mirror script | §3 B / §4 |
| L29 | after P4 | installed skills not adapted (by rule); comparing them with the model raised the question of an architecture level | model change "B" planned in [plan 002](002-add-arch-level.md); runs **after P9** (user, 2026-10-17) | §2.2 Q-TYPES; plan 100 "changing a model later" |
| L30 | P4 follow-up | installed author skills contradict the model (status line, `code_trace.rst`, no hand-over); `update` cannot be told to leave removed / replaced skills alone | removed + replaced; `update` only in a shadow clone | §2.2 new question Q-PRESET (keep / own copies / replace + remove); §5 / plan 998 T3 |
| L31 | P4 follow-up | the engine runs an installed skill by name (`change-request`) — it cannot be swapped for an own copy | test in the pilot | §6 pitfall |
| L32 | P5 / P6 | the engine's review gate can detect stale cross-cutting needs once their stage has `outgoing` trace edges; hash conditions work for non-nested needs only | decisions: trace edges; risks: hash conditions | §2.2 Q-JOBS: options and limits (nesting vs. hashes) |
| L33 | P6 | derived fields need Sphinx-Needs >= 9.0 and raise an `info` that `--deny info` turns into a failure | pin + lint ignore | §4 rule |
| L34 | P7 | `release-check` cannot implement a tier that allows missing reviews / open statuses, and cannot adopt existing debt | own gate script on `ubc agent gaps` / `verdict-check` | §5 CI blueprint: own gate script per tier |
| L35 | P7 | tier switches: ubc `UBCODE_CONFIG_OVERRIDE` (`lint.ignore`, safe because `[lint]` has nothing else) and an env var read by `conf.py`; local default = strict | CI 1 env | §5 |
| L36 | P8 | a headless runner needs explicit tool permissions; without them the engine reports "no change" | `--allowedTools` in `[agent.runner]` | §1 Q-RUNNER: include the permissions; dry-run `ubc agent run` once |
| L37 | P8 | `change-request` must be tested against a *committed* baseline; uncommitted chains look new, not changed | scratch clone with a commit | §3 D P8 |
| L38 | P8 | the cascade's code stage is unreliable, and tests that read code constants hide it | tests use specified values literally | §4 rule |
| L39 | P8 | user chose an autonomous pilot with HTML review instead of per-artefact approvals | agent authors and reviews, user reviews the result | §2.2 Q-EVAL: offer "autonomous pilot + HTML review" |
| L5 | plan review | how CI gets the ubc license | ask open vs. closed repo; key only for closed repos, stored by the user as CI secrets | §1 `{REPO_VISIBILITY}`, `{UBC_LICENSE}`, §5 |

## 10. Run log

### P0 Baseline (2026-10-17)

- Branch `feat/engineering-model`; versions and context in §1.3.
- References (scratchpad, not committed): `ubc agent install --detect --plan`
  output and the blank `vmodel` 21 profile (`ubproject.toml` + quality packs)
  from an empty scratch dir.
- `ubc agent doctor`: `ok` (config-validity, asset-freshness);
  `ubc agent status`: "no `[workflow]` section" (expected).
- Detect plan: stages `req` → `spec` only (`implements`), `test` dropped,
  3 open questions (fan-in `test` → req / spec; req, spec stage vs label).
  Confirms: hand-written model needed.

Brief vs. blank `vmodel` profile:

| Topic | Blank profile | Plan 001 | Status |
|---|---|---|---|
| levels | `user_story` → `req` → `arch` → `impl` / `test` | `us` → `req` → `spec` → `impl` / `test_spec` | brief wins (no arch) |
| test arm | `test` = codelinks marker in `tests/` (`verifies` → arch) | `test_spec` in RST + STR results (`executes`) | brief wins |
| req → us link | `traces_to` | `satisfies` | decided (Q-LINKS) |
| decisions | `decision` → `affects` → arch, global `specs/_global/decisions.rst`, `record-decision` | `dec` nested, `decides` | brief wins; nested route open (§5.1) |
| risks | `risk` → `mitigates` → req (outgoing), no author / review skill | `risk` → `affects` any, `mitigated_by` | brief wins |
| ids | `id_required = true`, `id_regex = "^[A-Z]+_[A-Z][A-Z0-9_]*$"` | **adopted** (G0); UB-19 now applies | P1 |
| provenance | field `recovered_from` (reverse recovery) | **adopted** (G0) | P1 |
| orphan gate | `orphan_exempt_types = [user_story, req, arch]` | to define | P3 |
| decision quality | `[quality.type_configs.decision.required] context_present = 1` | `dec.toml` based on it | as planned |
| diagram gate | `[workflow.diagram] enabled = false` | — | adopt (off) in P3 |
| runner | `[agent.runner]` commented out | — | P4 (needed for `ubc agent run`) |

### P1 Ontology + migration + model page (2026-10-17)

- `docs/ubproject.toml`: 7 types (`us`, `req`, `spec`, `impl`, `test_spec`,
  `dec`, `risk`), 8 links, fields with `schema.type` / `schema.enum`,
  `status` with union enum + `default = "open"`, `id_required`, `id_regex`,
  `schema_definitions_from_json`; `sphinx` script + `conf.py` gain
  `sphinxcontrib-mermaid` (2.1.1).
- `docs/schemas.json`: 16 rules, all `violation` (element + link rules of
  §4.1); completeness rules (`info`) follow in P3.
- Migration: new `user_stories.rst` (`US_LOGIN`, `US_AUDIT`); `REQ_*` →
  `satisfies`; `SPEC_*` → `refines`; `TEST_*` → `TSPEC_HASH`, `TSPEC_AUDIT`
  (`verifies` the spec only, `test_level: unit`); all needs carry
  `safety_relevant` / `security_relevant`. `REQ_AUTH` variant status now
  resolves to `done` / `open` (was `win_auth` / `default_auth`, outside the
  status set).
- `docs/engineering_model/index.rst`: mermaid type diagram, tables of types,
  status, fields, links, schema rules, `needflow` of the current needs.
- Results: `ubc script check` and `ubc script html` clean; `ubc script
  sphinx` (`-W`) clean, schema validation 0 findings; `needs.json` of ubc
  and Sphinx: same 8 needs, same fields and links.
- Negative test (scratch copy, one broken need per rule): every rule fires in
  both toolchains; an enum on core field `status` works in both, and a
  variant `status` is validated after resolution.
- Deferred: `docs/streams/` layout → P3 (depends on the stage routes);
  README update → P6.

Findings → plan 999: UB-20 (ubc reports a missing required link twice),
UB-21 (`not` and other keywords outside ubc's subset: ubc drops all rules
with a warning, Sphinx aborts), SN-08 (Sphinx console names the link target
for network failures); UB-05 confirmed (`-c` replaced `[needs.fields]`),
UB-19 now applies (`id_regex`).

### P2 Code, tests, mounts (2026-10-17)

- Code: `pyproject.toml` (pytest config, `junit_family = "xunit1"` — needed
  for `record_property`), `src/product_demo/auth.py` (salted scrypt,
  `IMPL_HASH`), `src/product_demo/audit.py` (append-only log, `IMPL_AUDIT`),
  `tests/test_auth.py`, `tests/test_audit.py` (2 passed); JUnit XML in
  `tests/_results/junit.xml` (gitignored).
- Marker grammar: `# @<title>, <IMPL_ID>, impl, [<SPEC_ID>, …], <safety>,
  <security>` — all six fields required (ubc warns when a required field
  follows one with a default: values are positional).
- `[codelinks]`: project `code`, `src_dir = "../src"`, one-line needs,
  `set_local_url = false` (no absolute paths, UB-01 / UB-14),
  `set_remote_url = true` with the GitHub pattern.
- `[test_reports]`: `rootdir = "../tests"` (UB-22 workaround),
  `property_link_types = { executes = "executes" }`; `test-file` id
  `TF_PYTEST` → suite `TF_PYTEST_0EA`, cases `TF_PYTEST_0EA_<HASH>` (upper
  case, fit `id_regex`).
- `[[source.mounts]]`: `../src` at `code/` (`implementations.rst` with
  `src-trace`), `../tests` at `tests/` (`test_results.rst` with
  `test-file`), only `*.rst`; `docs/implementations.rst` removed. Contrary
  to the schema description, `ubc check` does lint the mounted files.
- `conf.py`: `sphinx_codelinks`, `sphinx_test_reports` (new name; the old
  `sphinxcontrib.test_reports` is deprecated), `sphinx_mounts`; `sphinx`
  script deps: sphinx-codelinks 2.0.0, sphinx-test-reports 3.0.0,
  sphinx-mounts 0.3.0.
- Scripts: new `tests` (pytest via uv); `ci` = `tests` → `check` → `html`.
  `.github/workflows/docs.yml`: setup-uv + `ubc script tests` before the
  check (minimal fix; CI redesign in P7).
- Schema: `type-test-case` → `"testcase"` (STR-06); `link-result-tspec`
  negative-tested (wrong `executes` target) in both toolchains.
- Results: `ubc script ci` clean, `ubc script sphinx` (`-W`) clean, schema
  0 findings; ubc and Sphinx: same 14 needs, same type / status / fields /
  links / `remote-url` (only `docname` missing in ubc, UB-01).
- ~~Open for P3: test-result needs get `status = open`~~ — resolved after P2
  (below).

### P2 follow-up: status only on decisions and risks (2026-10-17)

- User: only `dec` and `risk` carry a status (as intended at G0). Cause of
  the drift: the "minimal open / done" lifecycle answer was applied to all
  types, and `[needs.fields.status] default = "open"` (P1) put a status on
  every need, also generated ones.
- toml: `status` enum = decision ∪ risk values, no default, no
  `parse_variants` (variant demo on `REQ_AUTH`'s status dropped).
- `schemas.json`: `status-dec` / `status-risk` with `required: [status]`;
  `status-open-done` replaced by `status-none` (`maxLength: 0`; `type: null`
  is refused by ubc because the field is a string, `not` is unsupported).
- Bug found and fixed: `$defs/status-mitigated` / `status-accepted` (used in
  `select`) matched needs **without** a status (`properties.status.const`
  passes when the field is absent) → added `required: [status]`.
- Negative tests (scratch): status on a `req`, `dec` / `risk` without status,
  mitigated / accepted risks — same findings in ubc and Sphinx.
- `ubc script ci` and `ubc script sphinx` clean; model page updated.

Findings → plan 999: UB-22 (`:file:` base differs between reading and mount
check), UB-23 (unknown keys in `[parse.parsers.*]` silent), STR-06 (docs
type names `test-case` vs `testcase`); UB-01 and UB-14 confirmed (applies);
CL-03, CL-07 n/a here.

### P3 Workflow + quality + schemas (2026-10-17)

- `[workflow]`: 7 stages (§5.1), `orphan_exempt_types = ["us"]`,
  `release_disallow_status = ["open", "proposed"]`, diagram gate off
  (mermaid format), no lifecycle (PH-14), no `test_results` stage (PH-12).
- `[quality]`: own packs `docs/quality/{us,req,spec,test_spec,dec,risk}.toml`
  (installed packs untouched); `parent_fit` ≥ 1 everywhere, `no_overlap` = 2
  on `us`, `context_present` ≥ 1 on `dec`; `decisions_documented` on us /
  req / spec / test_spec.
- `schemas.json`: 9 `info` rules (`cov-us`, `cov-req`, `cov-spec-impl`,
  `cov-spec-test`, `cov-tspec-result`, `dec-present`, `result-passed`,
  `risk-open`, `dec-proposed`), all negative-tested; `conf.py`
  `suppress_warnings = ["sn_schema_info"]`.
- Gates: `ubc check --deny warning` passes (CI 1), `ubc check --deny info`
  fails on the 8 missing decisions (CI 2); Sphinx `-W` passes,
  `schema_violations.json` records the 8.
- `ubc agent config-validate`: ok. `doctor`: errors only for the own skills
  of P4 (a skill on disk without manifest entry is accepted — tested in a
  scratch copy). `gaps`: 8 `review` (no verdicts yet). `trace`: 4 edges,
  all covered both ways.
- G3 decisions: decisions / risks via stage skills; status rule in every
  `authoring` text + schema; existing needs reviewed in the pilot.

Findings → plan 999: PH-14 (lifecycle gate judges all needs), PH-15
(prompt hard-codes `:status: draft`), PH-16 (cross-cutting stages cover all
upstream needs; no nested route), PH-17 ("CREATE THE FILE" for existing
files); PH-12 applies; UB-05 again (`-c` replaced `[workflow]`).

### P4 Templates + skills (2026-10-17)

- `.agents/templates/`: `README.md`, `us.rst`, `req.rst`, `spec.rst`,
  `test_spec.rst`, `dec.rst` (nested form), `risk.rst`, `impl.py`, `test.py`;
  `handover/decision.json`, `handover/risk.json` (JSON Schemas of the
  payloads). Only `dec.rst` / `risk.rst` carry `:status:`.
- Own skills in `.agents/skills/` (mirrored to `.claude/skills/` and
  `.github/agents/` by `scripts/mirror_skills.py`, `--check` for CI):
  - stage skills `draft-us`, `draft-spec`, `draft-test-spec` — incoming /
    outgoing needs, propose-first outline incl. decisions and risks, status
    rule, append-only, decision / risk hand-over, confirm;
    `draft-test-spec` also writes the pytest test (`executes`);
  - recording skills `record-dec` (nests the `dec` at the end of its parent's
    body, found via `ubc agent audit` `source`), `record-risk` (appends to
    `docs/risks.rst`) — validate the payload, stop on gaps, render only;
  - review skills `review-spec`, `review-test-spec`, `review-risk` — copies of
    the generic installed `review-requirement` (only the stage name differs).
- `docs/risks.rst` created (empty page, in the toctree) so `record-risk`
  only appends.
- Command syntax fixed in the skills: `ubc check <project path>`,
  `ubc script --path <project path> tests`, `ubc build needs <project path>`
  (only `ubc agent` takes `-p`).
- Routes: regular stages switched to `scope = "stream"` — the dry run showed
  `global` ordering links to all upstream needs (PH-16 extended).
- Checks: `doctor` ok (25 checks, own skills accepted from disk);
  `config-validate` ok; `gaps` 8 `review`; `trace` ok. Dry run
  (`ubc agent prompt --stage …`, scratch copy without review holds): every
  stage loads its skill, its authoring text with the status override, and
  links only its own parent. `review-brief` per type: right review skill and
  own pack (us 7, req 7, spec 7, test_spec 5, dec 4, risk 4 axes).
- Not built: `evaluate-decisions` / `evaluate-risks` — wait for the P5
  spike.

Findings → plan 999: PH-16 extended (scope decides the number of parents),
PH-09 applies (drift of own skills' copies not detected).

### P4 follow-up: installed skills (2026-10-17)

- Facts (skills read in full): the installed `draft-requirement` writes
  `:status:` and has no decision / risk hand-over; the installed `draft-impl`
  defers to the prompt's marker shape but would create `src/code_trace.rst`
  with a second `src-trace` (every `impl` twice) and has no risk hand-over;
  `change-request` edits a parent's whole body (nested decisions!), skips the
  decisions stage, needs a license (`ubc query filter`) and a runner.
- User decisions: remove the unused profile skills; give the used author
  skills this project's pattern; test `change-request` in the pilot;
  configure a headless runner; plan 998 gets a profile-update procedure.
- Scratch tests of `doctor` / `update` (plan 999 PH-18): edited installed
  skill = `doctor` error unless its manifest entries are removed; `update`
  re-adds removed entries and restores removed files on the next run →
  `update` only in a shadow clone (plan 998 §4.7).
- Done: 11 skills × 3 copies removed; manifest 60 → 21 entries;
  `draft-requirement`, `draft-impl` rewritten (`.agents/skills`, mirrored —
  10 own skills); `[agent.runner]` = headless `claude -p …`, model `sonnet`,
  900 s (`ubc agent run` not executed yet — the pilot does).
- Checks: `doctor` ok (21 checks), `config-validate` ok, `ubc check --deny
  warning` ok; dry run `reqs` / `code`: own skill loaded, one parent linked.
- Correction: `.github/agents/workflow-author.agent.md` exists (an earlier
  listing was cut off) — no finding.

Findings → plan 999: PH-18 (no opt-out from preset skills).

### P5 Spike: evaluation jobs for decisions and risks (2026-10-17)

Scratch copy with sample data: `DEC_HASH_ALGO` (accepted, nested in
`SPEC_HASH`), `DEC_AUDIT_STORE` (proposed, nested in `SPEC_AUDIT`),
`RISK_AUDIT_LOSS` (open), `RISK_SCRYPT_PARAMS` (mitigated by
`DEC_HASH_ALGO`, `TSPEC_HASH`). Nested decisions parse cleanly in both
toolchains.

Two questions the jobs have to answer: **unresolved** (risk `open`,
decision `proposed`, risk without mitigation) and **stale** (a resolved
decision / risk whose linked needs changed since it was resolved).

| Option | Prototype | Unresolved | Stale | Cost | Result |
|---|---|---|---|---|---|
| A CI report | `reports/evaluation.rst`: needtables "open risks", "risks without a mitigation link" (`len(mitigated_by) == 0`), "proposed decisions", decision log (`parent_need`) | yes | no | none | same rows in ubc and Sphinx |
| B CI gate | existing schema `info` rules `risk-open`, `dec-proposed` (+ CI 2 `--deny info`) | yes | — | none | already built (P3) |
| B (engine) verdicts | verdicts for dec, risk, parent; change the parent / the mitigation | — | **no** | none | only the changed need goes `outdated`; dec / risk stay fresh (PH-19) |
| B+ ledger script | `evaluate_xcut.py`: `--record ID` stores a content hash of each linked need (body without nested directives) when a dec / risk is resolved; the check reports `open` / `UNRECORDED` / `STALE` / `ok`, exit 1 on problems | yes | **yes** | none (deterministic) | detects parent and mitigation changes; an edit of the decision itself does not mark it stale, but marks the risk it mitigates stale |
| C agent skill | design only: `evaluate-decisions` / `evaluate-risks` read the item, its linked needs and the B+ reason (`ubc agent audit` / `context`), judge whether it still holds / is resolved, propose a status change or a re-record for human approval | yes | judges *whether* stale matters | tokens per item | needs the runner; triggered by B+ |
| D scheduled | design only: weekly GitHub Action running A + B+, opening / updating an issue with the open and stale items | yes | yes | CI minutes; AI only if C runs in CI (API key secret) | catches items nobody touches |

Findings: PH-19 (verdict fingerprints ignore `decides` / `affects` /
`mitigated_by`; `impact` misses nested decisions; parent fingerprint
includes nested decisions). PH-10 still applies (`submit_command` without
`-p`).

#### P5 addendum: option E — conditional links with a derived fingerprint

User question: use Sphinx-Needs conditional links
(`TARGET[condition]`, 8.0) with the derived-field kinds `hash` /
`fingerprint` (`functions/common.py`; ubc 0.37 and Sphinx-Needs 9.0.0 both
support them).

- Setup: `[needs.fields.fp] derive = { kind = "fingerprint" }` (SHA-256 of
  id, type, title, status, tags, content, every declared field and link).
  Decision / risk link to `TARGET[fp=="<value at evaluation>"]`.
- `fp` is identical in ubc and Sphinx for every need (incl. `impl`, test
  results). A changed target → `needs.link_condition_failed` warning in
  both, naming source, link and target; the link stays in `needs.json`
  (schema link rules still hold). Changing a mitigation (`TSPEC_HASH`) or the
  mitigating decision itself flags the risk — exactly like B+.
- **Does not work for nested decisions:** the parent's content contains the
  nested decision incl. its `:decides: PARENT[fp=="…"]` line, so writing the
  hash changes the hash — 3 refresh rounds, never converged. Works once the
  decision is not nested (tested with `decisions.rst`).
- Short hashes: `ID[fp[:12]=="…"]` drops the condition silently in both;
  `ID[[fp[:12]=="…"]]` is invalid in ubc, valid in Sphinx (UB-24) → only the
  full 64-character value works.
- Severity: `link_condition_failed` is a warning → `ubc check --deny warning`
  (CI 1) and Sphinx `-W` fail on every stale item, unless suppressed on
  `main`.
- Re-evaluation = rewrite the condition with the target's current `fp`
  (script or skill), visible in the diff.

| | B+ ledger script | E conditional links |
|---|---|---|
| detection | own script in CI | native in both builds, IDE (ubCode diagnostics) |
| nested decisions | works (strips nested directives) | **parent link cannot be checked** |
| state | `.pharaoh/evaluations/<ID>.json` | in the RST link itself (64-hex hashes) |
| stale on `main` | report (CI 1), block (CI 2) | warning → blocks CI 1 unless suppressed |
| re-evaluation | `--record ID` | rewrite the conditions (script / skill) |

Findings → plan 999: UB-24.

#### P5 addendum 2: option F — review gate with outgoing trace edges

- Decision structure tested alongside (scratch): `[needs.links.decides]
  predicates = [["type == 'dec'", "[[copy('parent_need')]]"]]` — a nested
  decision decides its parent without writing `:decides:` (explicit values
  replace it); no warning in ubc or Sphinx (`default` instead of
  `predicates` warns `needs.dynamic_function` on every need without a
  parent). Rule `dec-nested` via a derived field `parent`
  (`derive = { kind = "copy", field = "parent_need" }`): only a decision
  outside a need fails, in both toolchains (`parent_need` directly: UB-25).
- Option F: the `decisions` stage gets `[[workflow.stages.trace]]` edges
  `link = "decides"`, `direction = "outgoing"`, `min = 1`, one per
  `up` = us / req / spec / test_spec; the `risks` stage `affects` → us / req
  / spec / test_spec and `mitigated_by` → req / spec / test_spec / dec.
  `config-validate` ok, no trace gaps (outgoing is not gated).
- Verdicts for `DEC_HASH_ALGO`, `RISK_SCRYPT_PARAMS`, `SPEC_HASH`,
  `TSPEC_HASH`, then:

  | Change | `verdict-check` `outdated` |
  |---|---|
  | `SPEC_HASH` body | `DEC_HASH_ALGO`, `RISK_SCRYPT_PARAMS`, `SPEC_HASH`, `TSPEC_HASH` |
  | `TSPEC_HASH` (mitigation) | `RISK_SCRYPT_PARAMS`, `TSPEC_HASH` |
  | `DEC_HASH_ALGO` itself | `DEC_HASH_ALGO`, `SPEC_HASH` (nested text), `RISK_SCRYPT_PARAMS`, `TSPEC_HASH` |

  Same result with the `decides` link copied by `predicates`.
- So the engine's review gate detects stale decisions and risks once the
  stages carry outgoing edges (PH-19 workaround); re-evaluation = the normal
  re-review with `review-decision` / `review-risk` (axes `rationale_quality`,
  `mitigation_fit`); CI 2 (`verdict-check`) blocks outdated verdicts. No own
  script, no hashes in the RST.
- Cost: wider re-review — editing a decision also re-reviews its parent and
  the parent's children (one hop).

#### G5 result (2026-10-17)

- Decisions: option F + structure (`predicates`, `parent`, `dec-nested`).
- Risks: option E — conditional links with the derived fingerprint `fp`
  on `affects` and `mitigated_by` (risks are not nested, so the hashes
  converge — tested in addendum 1); the `risks` stage keeps no trace edges
  (F not used for risks), its review stays (`review-risk`).
- Stale risk: allowed on `main`, blocks a release.
- Report A; no B+ script, no `evaluate-*` skills, no scheduled job (for now).

To build in P6 / P7:

1. `ubproject.toml`: derived fields `fp` (`kind = "fingerprint"`) and
   `parent` (`kind = "copy"`, `field = "parent_need"`); `decides`
   `predicates`; `decisions` stage trace edges (`decides`, outgoing, us /
   req / spec / test_spec); `sphinx` script `sphinx-needs>=9.0` (derive).
2. `schemas.json`: `dec-nested` (`parent` required).
3. `scripts/refresh_risk_links.py <RISK_ID>`: rewrite the risk's
   `TARGET[fp=="…"]` conditions with the targets' current `fp` (the
   sign-off after re-evaluation); used by `record-risk` on creation and after
   a `review-risk` re-evaluation.
4. Skills / templates: `record-dec` + `dec.rst` without the parent
   `:decides:` (only further targets, then incl. the parent); `record-risk`
   + `risk.rst` with conditions (via the script); `review-risk` note on
   refreshing; stage skills unchanged otherwise.
5. CI 1: ubc `[lint] ignore` / Sphinx `suppress_warnings` for
   `needs.link_condition_failed`; CI 2: not suppressed (P7).
6. Report A (`docs/reports/evaluation.rst`) and model docs (P6).
7. Plan 999: UB-25 → applies once `dec-nested` exists; plan 100: the
   evaluation options and their limits (nesting vs. hashes, PH-19 / F).

### P6 Decision / risk structure, reports, model docs (2026-10-17)

- `docs/ubproject.toml`: derived fields `fp` (fingerprint) and `parent`
  (copy of `parent_need`); `decides` `predicates` (nested decision decides
  its parent); `decisions` stage with `outgoing` trace edges (`decides` → us
  / req / spec / test_spec); `[lint] ignore = ["config.derive_sphinx_minimum"]`
  (an `info` that would fail CI 2); `sphinx` script `sphinx-needs>=9.0`.
- `docs/schemas.json`: `dec-nested` (`parent` required) — negative-tested
  (decision outside a need: violation in both toolchains; nested one without
  `:decides:` gets `decides` and `parent`).
- `scripts/refresh_risk_links.py` (`RISK_ID …` / `--all`): writes the
  targets' current `fp` into a risk's `affects` / `mitigated_by` conditions;
  idempotent; a changed target fails the condition, the refresh clears it;
  refreshing does not outdate the risk's verdict (conditions are not part of
  the engine fingerprint), so review → sign-off has no loop.
- Skills / templates: `record-dec` + `dec.rst` without the parent
  `:decides:` (explicit only for further targets, parent first);
  `record-risk` renders plain ids, then runs the refresh script;
  `review-risk` explains stale risks and the sign-off; templates README;
  `handover/decision.json`. Mirrored (10 own skills).
- Reports: `docs/reports/decisions.rst` (proposed decisions, needs without a
  decision, decision log), `docs/reports/risks.rst` (open, without
  mitigation, security / safety, all) — sample data in a scratch copy: same
  rows in ubc and Sphinx (also `len(decides_back) == 0`); hashes are not
  rendered.
- Model docs: `engineering_model/index.rst` (fields `fp` / `parent`,
  automatic `decides`, hash conditions, `dec-nested`, completeness rules),
  new `workflow.rst` (stages, loop commands, skills, templates, quality
  packs), `decisions_risks.rst`, `ci.rst` (the two tiers, built in P7).
- `README.md` rewritten for the current model (the old one described `test`,
  `implements` spec → req and a non-existent `tests.md`).
- Checks: `ubc script ci` and `ubc script sphinx` clean; `needs.json`
  parity: 14 needs, no field difference (incl. `fp`, `parent`);
  `config-validate`, `doctor`, `trace` ok; mirrors in sync.
- Not yet: CI 1 / CI 2 workflows incl. suppressing
  `needs.link_condition_failed` on `main` (P7).

Findings → plan 999: UB-25 applies.
- G6 review (user): Sphinx page showed "PlantUML is not available!" for the
  `needflow` on the model page → `[needs] flow_engine = "graphviz"`,
  `sphinx.ext.graphviz` in `conf.py`; P7 CI installs graphviz (`dot`). Found
  by looking at the page, not by a check: plan 100 §4 gets "inspect rendered
  diagrams, `-W` does not catch a missing engine" (SN-09).

### P7 CI (2026-10-17)

- `.github/workflows/docs.yml` replaced by `ci-main.yml` (CI 1: PR / push
  `main`) and `ci-release.yml` (CI 2: PR / push `release/**`, tags `v*`),
  shared setup `.github/actions/setup/action.yml` (ubc pinned `0.37.0`, uv,
  graphviz for the Sphinx `needflow`).
- Both: tests first, `ubc script check` / `html`, Sphinx `-W`,
  `config-validate`, `doctor`, skill mirror check, site upload.
- CI 1: `CI_TIER=main` (`conf.py` suppresses `needs.link_condition_failed`)
  and `UBCODE_CONFIG_OVERRIDE` adding it to `lint.ignore` — stale risks
  reported (`ci_gates.py stale-risks`), not blocking; structural gaps
  ratcheted (`ci_gates.py gaps --tier main`, baseline
  `docs/.pharaoh/gaps-baseline.json`, starts empty); only failing /
  malformed verdicts block.
- CI 2: `ubc check --deny info`, `schema_violations.json` empty, zero gaps
  (incl. `review`, `status_disallowed`), every verdict present / fresh /
  passing.
- `scripts/ci_gates.py` instead of `release-check` (PH-20: baseline format
  undocumented, cannot capture debt, counts reviews and open statuses);
  negative-tested (a spec without implementation → 2 new gaps, exit 1;
  baselined → exit 0).
- Locally: all CI 1 steps pass; CI 2 fails exactly on the pilot's work (8
  missing decisions as `info` / in `schema_violations.json`, 8 `review`
  gaps, 8 missing verdicts).
- References to `docs.yml` updated in plans 998 / 999; `ci.rst` documents
  the gates.
- G7: commit `8a34c92`, PR #2 (`feat/engineering-model` → `main`):
  `ci-main` green on GitHub (run 39055932589, 38 s) — tests 2 passed, ubc
  check / html, Sphinx `-W`, `config-validate` / `doctor` ok, gaps 0 new (8
  open allowed), 0 blocking verdicts, 0 stale risks, 10 skills in sync. The
  `ubc agent` commands need no license key in CI (public repository).
  `ci-release` not run yet (fails by design until P8).
- **G7 closed (user, 2026-10-17)** on the green CI 1 run; the CI 2 run moves
  to P8 (it must pass once the pilot is done).

Findings → plan 999: PH-20.

### P8 Pilot (2026-10-17)

Run autonomously (user: no per-artefact approvals, review of the HTML at
the end); the agent played author and reviewer, following the skills.

- New feature "login lockout": `US_LOCKOUT` → `REQ_LOCKOUT` (5 failures,
  15 minutes) → `SPEC_LOCKOUT` (900 s, injectable clock) → `IMPL_LOCKOUT`
  (`src/product_demo/lockout.py`) → `TSPEC_LOCKOUT` → 2 pytest tests
  (`executes`). Risks: `RISK_LOCKOUT_DOS` (accepted by
  `DEC_REQ_LOCKOUT_LIMITS`), `RISK_LOCKOUT_RESTART` (accepted by
  `DEC_LOCKOUT_STATE`), `RISK_AUDIT_VOLATILE` (accepted by
  `DEC_AUDIT_FORMAT`), `RISK_AI_LOCKOUT_VALUES` (`ai-workflow`, mitigated by
  the recorded decision + the user's HTML review).
- Decisions: 12, nested, all `accepted`; every `us` / `req` / `spec` /
  `test_spec` has one; `decides` copied from the parent except where a
  decision also accepts a risk (explicit, parent first).
- Review findings acted on: `SPEC_HASH` (salt, stored format, constant-time
  compare) and `SPEC_AUDIT` (record fields, order) made precise; the two old
  test specs rewritten to the template. A spec change made
  `RISK_AUDIT_VOLATILE` stale → re-evaluated, signed off.
- Reviews: 28 verdicts (us 3, req 3, spec 3, test_spec 3, dec 12, risk 4),
  scores with reasons; `verdict-check` clean. Lower scores (1) kept with
  suggestions (e.g. `TSPEC_HASH` / `TSPEC_AUDIT` spec coverage,
  `RISK_AI_LOCKOUT_VALUES` mitigation pending the user).
- `change-request` (scratch clone, lockout chain committed, 15 → 10
  minutes): run 1 / 2 — runner blocked on Bash, all stages "no change",
  `ok: true` (PH-21); run 3 with `--allowedTools` — spec, code and test spec
  reconciled, also the decision nested in the test spec; not reconciled: the
  decision nested in the edited requirement and the risk texts (PH-22) —
  flagged by option F / hash conditions; run 4 (permanent config) — spec and
  test spec changed, code **not**, tests stayed green because they read the
  code's constant → tests now use the specified values literally (a mismatch
  fails), rule added to `draft-test-spec`.
- Runner config: `--allowedTools "Bash(*/ubc *)" "Bash(ubc *)" "Bash(python3
  scripts/*)"` (`Bash(*/ubc:*)` does not match absolute paths).
- Sphinx incremental build kept old test results (STR-07) → `sphinx`
  script uses `-E`.
- Final state: CI 2 steps locally all green (`--deny info`, empty
  `schema_violations.json`, 0 gaps, all verdicts fresh and passing, trace
  ok, mirrors in sync); 37 needs identical in ubc and Sphinx; option F seen
  in practice (a changed test spec outdated its nested decision).

- **G8 (user, 2026-10-17): "ok"** on the HTML review — lockout values (5
  failures, 15 minutes) and the accepted risks confirmed;
  `RISK_AI_LOCKOUT_VALUES` set to `closed`, re-reviewed.

Findings → plan 999: PH-21, PH-22, STR-07.
