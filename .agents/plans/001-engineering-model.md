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
- **Installed (manifest) assets stay untouched.** Files listed in
  `docs/.pharaoh/agent/install-manifest` (the `vmodel` profile 21 skills,
  `quality/*.toml` packs) are not edited, so `ubc agent update` stays
  conflict-free. Own skills and packs get their own names (§4.4, §4.5).
- **Tool bugs go into plan 999** in the same session, with markers of this
  repository (`- **Origin:** product_demo`).
- Work on a branch (`feat/engineering-model`); plan changes and code stay
  uncommitted until the user asks.

## 0. Goal

At the end:

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
| Integrity attributes | Generic: `safety_relevant`, `security_relevant` (bool), `integrity_level` (low / medium / high) |
| `us` overlap | Review axis only (`no_overlap` in the `us` quality pack) |
| Decisions | **Nested** in the need they decide, plus explicit `decides` link; quality axis on `dec` **and** on every parent type ("decisions documented") |
| Code / tests | Python + pytest (JUnit XML for Sphinx-Test-Reports) |
| sphinx-mounts | Mount `src/` and `tests/` into the docs tree |
| Links | Rename + migrate the existing needs (`implements` → `refines`, `tests` → `verifies`) |
| Plans | This plan (001) + reusable playbook (100) |
| Evaluation | Model docs page; gate after every phase; ask more questions during this pilot |
| Risk / decision evaluation jobs | **Open** — spike phase P5 compares the options |
| Lifecycle | Minimal: `open` / `done` (risks and decisions add their own status field) |
| Skills / templates | Source in `.agents/`, mirrored to `.claude/skills/` and `.github/agents/` |
| ubc license in CI | Repository `PhilipPartsch/product_demo` is **public** → no license key in CI. If it ever becomes private, the user adds `UBCODE_LICENSE_KEY` / `UBCODE_LICENSE_USER` as GitHub secrets and both pipelines pass them to the `ubc` steps |
| CI 1 (PR → `main`) | `open` topics allowed. Blocks on: build / lint errors, new structural gaps (ratchet), failing verdicts, pytest |
| CI 2 (`main` → release) | Runs on PRs / pushes to `release/*` **and** on `v*` tags. Requires: all needs `done`, zero gaps, all verdicts present + fresh + passing |

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

Built-in `status` carries the minimal lifecycle `open` / `done` for every
type. Own fields:

| Field | Types | Values | Purpose |
|---|---|---|---|
| `safety_relevant` | all except test results | `true` / `false` | safety relevance |
| `security_relevant` | all except test results | `true` / `false` | security relevance |
| `integrity_level` | `us`, `req`, `spec`, `impl`, `test_spec` | `low` / `medium` / `high` | rigor needed (review depth, test coverage) |
| `owner` | all | string | accountable person / role |
| `priority` | `us`, `req` | `low` / `medium` / `high` | ordering |
| `verification_method` | `req`, `spec` | `test` / `analysis` / `review` / `inspection` | how it is verified |
| `test_level` | `test_spec` | `unit` / `integration` / `system` | test level |
| `decision_status` | `dec` | `proposed` / `accepted` / `superseded` | decision lifecycle |
| `risk_category` | `risk` | `safety` / `security` / `technical` / `project` / `ai-workflow` | kind of risk |
| `severity` | `risk` | `low` / `medium` / `high` | impact |
| `likelihood` | `risk` | `low` / `medium` / `high` | probability |
| `risk_status` | `risk` | `open` / `mitigated` / `accepted` / `closed` | risk lifecycle |
| `review_due` | `dec`, `risk` | ISO date | trigger for the evaluation jobs |

Constraints (schemas in P3, both toolchains; SN-01: schema severities must not
break Sphinx `-W`, so choose severities that pass `-W` or document them):

- `risk_status = mitigated` → at least one `mitigated_by`;
- `risk_status = accepted` → a nested or linked `dec` that accepts it;
- `status = done` on `dec` → `decision_status` is `accepted` or `superseded`.

Keep the variant fields (`status` with `parse_variants`, `platform_note`,
`variants.json`) working; `REQ_AUTH` uses them, which makes PH-01 / PH-02
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

## 5. Workflow

### 5.1 Stages

| Stage | Produces | Depends on | Trace (up, link, direction, min) | Author skill | Review skill | Route |
|---|---|---|---|---|---|---|
| `user_stories` | `us` | — | — | `draft-us` (own) | `review-feat` | `docs/streams/{stream}/user_stories.rst` |
| `reqs` | `req` | `user_stories` | `us`, `satisfies`, both, 1 | `draft-requirement` | `review-requirement` | `…/requirements.rst` |
| `specs` | `spec` | `reqs` | `req`, `refines`, both, 1 | `draft-spec` (own) | `review-spec` (own) or `review-arch` | `…/specifications.rst` |
| `code` | `impl` | `specs` | `spec`, `implements`, both, 1 | `draft-impl` | — | `src` (global) |
| `test_specs` | `test_spec` | `specs` | `spec`, `verifies`, both, 1 | `draft-test-spec` (own) | `review-test-spec` (own) | `…/test_specifications.rst` |
| `test_results` | (STR) | `code`, `test_specs` | `test_spec`, `executes`, both, 1 — if PH-12 allows | — (pytest in CI) | — | `docs/verification/results.rst` |
| `decisions` | `dec` | — (global) | parents, `decides`, both, 1 | `record-dec` (own) | `review-decision` | nested in parent's document |
| `risks` | `risk` | — (global) | any, `affects`, outgoing, 1 | `record-risk` (own) | `review-risk` (own) | `docs/streams/_global/risks.rst` |

To check in P3 (record results in §9 and plan 999):

- **Nested decisions vs. routes.** Stage routes have `granularity`
  `single` / `per-root` / `global`. A route "into the parent's document" may
  not exist; options: (a) route = the stream file of the parent stage and the
  skill nests the `dec` in the parent directive there, (b) per-root route,
  (c) a 999 entry + workaround.
- **"Every need has decisions".** `direction = "both", min = 1` on the
  `decisions` trace turns every parent without a `dec` into a gap. Decide
  which types must carry one (`us`/`req`/`spec`? all?) and whether CI 1 keeps
  them as ratchet debt.
- **Lifecycle** `open` / `done`: the key that declares the states /
  transitions for `config-validate`; `release_disallow_status = ["open"]`.
- **Fingerprint.** A nested `dec` changes the parent's content → parent
  verdict `outdated` → re-review. Accept (it is intended: the decision is part
  of the parent) and document; check grandchildren (PH-03).

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
`chosen`, `consequences`, `rationale`, `decides[]`, `decision_status`,
`review_due`, `safety_relevant`, `security_relevant`.
Risk payload: `title`, `description`, `affects[]`, `risk_category`,
`severity`, `likelihood`, `mitigation` (text), `mitigated_by[]`,
`risk_status`, `review_due`.

### 5.3 Skills

Source in `.agents/skills/<name>/SKILL.md`, mirrored to
`.claude/skills/<name>/SKILL.md` and `.github/agents/<name>.agent.md` (same
layout as the installed ones; a small `scripts/mirror-skills.sh` keeps them in
sync, CI 1 checks they are identical).

| Skill | Kind | Content |
|---|---|---|
| `draft-us`, `draft-spec`, `draft-test-spec` | stage author | incoming needs (what to read, via `ubc agent context`), outgoing needs (type, template, route, links), **decision and risk triggers** for this stage (when to call `record-dec` / `record-risk`, how to fill the payload) |
| `review-spec`, `review-test-spec`, `review-risk` | review | generic "score the criteria of your briefing" (as the installed `review-*`), only if the installed ones cannot be reused |
| `record-dec` | recording ("stupid") | takes the decision payload, renders `dec.rst` nested into `target_need`, nothing else: no research, no own judgment |
| `record-risk` | recording ("stupid") | takes the risk payload, renders `risk.rst` at the route |
| `evaluate-decisions`, `evaluate-risks` | evaluation | only if P5 picks the agent-skill option |

Installed skills reused as-is: `draft-requirement`, `draft-impl`,
`review-feat`, `review-requirement`, `review-decision`, `drive-workflow`,
`ubc-agent-next`, `change-request`. `record-decision` is **not** used (it
routes and asks itself; we want a stupid recorder) — document why in the
model docs.

### 5.4 Quality packs

Own packs in `docs/quality/` (installed packs stay untouched):

- `us.toml` — based on `feat.toml` + axis `no_overlap` (no other `us`
  covers the same topic; the reviewer gets the list of existing `us` via
  `ubc agent context` / the brief);
- `spec.toml`, `test_spec.toml`, `risk.toml`;
- `dec.toml` — based on `decision.toml` (`context_present` required);
- every parent pack gets axis `decisions_documented` (the need carries the
  nested `dec` for its relevant choices, or states that none were needed).

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

1. `docs/ubproject.toml`: types (§2), fields (§3), links (§4).
2. Migrate `docs/specifications.rst` (`:implements:` → `:refines:`),
   `docs/verification.rst` (`test` → `test_spec`, `:tests:` → `:verifies:`,
   only to specs). Add one `us` per existing req (US for auth, logging),
   `satisfies` links.
3. Restructure into `docs/streams/<stream>/` if the routes of §5.1 require it
   (keep `index.rst` toctree working).
4. `docs/engineering_model/index.rst` first version: type diagram (check the
   renderer works in both toolchains — graphviz / mermaid / needflow), tables
   of types, fields, links.
5. `ubc script ci` + `ubc script sphinx` green.
6. **Gate G1 (model docs page):** user reviews the rendered page.

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
   `release_disallow_status = ["open"]`, lifecycle states.
2. `[quality]` + own packs (§5.4).
3. Schemas for the constraints of §3 (check SN-01, SN-05 in both toolchains).
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
| A CI report | `needtable` / `needlist` filters (`risk_status == "open"`, `review_due < today`, no `mitigated_by`, `decision_status == "proposed"`) + `ubc report` / Jinja | cheap, visible, non-blocking; "today" in filters? |
| B CI gate | script on `needs.json` (or schemas) failing CI 2 on unresolved risks / proposed decisions | strict; fits CI 2 only |
| C Agent skill | `evaluate-risks` / `evaluate-decisions`: read the open items, check whether the linked needs changed / mitigations exist, propose status updates for human approval | judgment, catches stale decisions; costs tokens |
| D Scheduled | weekly GitHub Action running A (+ C via `ubc agent run`) and opening an issue | catches `review_due` without a push |

**Gate G5:** user picks the option(s); P6 / P7 implement them.

### P6 Reports + engineering-model docs

1. `docs/reports/decisions.rst`, `docs/reports/risks.rst`: tables (open,
   overdue, by category / stage), pies, needflow of risks → affected needs;
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
  `ubc agent release-check` against `.pharaoh/release-baseline` (ratchet: new
  gaps fail), verdict gate **failing / malformed only** (`verdict-check` exits
  non-zero on `missing` too — filter its JSON with `jq`), skill mirror check.
  `open` needs allowed — verify that `release-check` without
  `--with-verdicts` does not apply `release_disallow_status`; otherwise run
  `gaps` + a baseline diff instead.
- `ci-release.yml` — on `pull_request` / `push` to `release/*` and `push`
  of tags `v*`: everything of CI 1, plus `ubc agent gaps` (zero gaps, no
  baseline), `ubc agent verdict-check` (nothing missing / failing / outdated),
  no need with `status = open` (from `release_disallow_status` or a
  `needs.json` check), plus the P5 result if it is a gate.
- Both upload the HTML site; ubc pinned via `UBC_VERSION` (keep in sync with
  plan 998), tools of the Sphinx build pinned.
- **Gate G7:** user sees a green CI 1 run on the PR and a CI 2 run on a test
  `release/*` branch.

### P8 Pilot chain

Using `ubc agent next` / `prompt` (propose-first, user approves each
artefact): one new feature end to end, e.g. "password reset":
`us` → `req` → `spec` (with a nested `dec`, e.g. token lifetime) → `impl`
→ `test_spec` → pytest result, plus one `risk` (e.g. token brute force,
`mitigated_by` the spec) and one `ai-workflow` risk. Reviews via the review
skills + `verdict-submit`. Then set everything to `done` and run CI 2
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

`docs/ubproject.toml`, `docs/conf.py`, `docs/*.rst` (migration),
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
| L5 | plan review | how CI gets the ubc license | ask open vs. closed repo; key only for closed repos, stored by the user as CI secrets | §1 `{REPO_VISIBILITY}`, `{UBC_LICENSE}`, §5 |
