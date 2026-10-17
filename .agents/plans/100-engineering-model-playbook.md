# Plan 100: Playbook — set up an engineering model with ubCode / Sphinx-Needs

Reusable recipe for setting up a need-type model, an agentic workflow
(Pharaoh, `ubc agent`), cross-cutting needs (e.g. decisions, risks), reports,
model documentation and CI in a ubCode / Sphinx-Needs project. Every new
setup is a **run** of this playbook with its own project plan (first run:
[001-engineering-model.md](001-engineering-model.md)). Each run ends by
folding its learning log back into this file (§7).

**Nothing project-specific is fixed here.** Everything the user decides is a
parameter (§1) or comes from the input brief (§2.1). Earlier runs appear only
as examples ("seen in runs"), never as defaults. What *is* fixed here is tool
behaviour (§4 rules from tool facts, §6 pitfalls) — and that, too, is
re-checked against the current tool versions on every run.

Sources (check for changes at the start of every run):

- Sphinx-Needs <https://sphinx-needs.readthedocs.io/en/stable/>
- Sphinx-Codelinks <https://codelinks.useblocks.com/en/stable/>
- Sphinx-Test-Reports <https://sphinx-test-reports.readthedocs.io/en/latest/>
- sphinx-mounts <https://sphinx-mounts.useblocks.com/en/stable/>
- ubCode <https://ubcode.useblocks.com/index.html>, agentic engineering
  <https://ubcode.useblocks.com/usage/agentic_engineer/index.html>,
  CI/CD <https://ubcode.useblocks.com/usage/ubc_ci_cd.html>
- Config schema <https://ubcode.useblocks.com/ubproject.schema.json>
- Sphinx-Needs schema validation (`schemas.json`)
  <https://sphinx-needs.readthedocs.io/en/stable/schema/index.html>
- The project's tool-bug record, if it has one (`{TOOL_BUGS}`)

## 0. Outputs of a run

Always:

1. `ubproject.toml` with the types, fields (`schema.type` / `schema.enum`),
   links, `[workflow]` and `[quality]` of the brief (plus `[codelinks]`,
   `[test_reports]` when the brief uses them).
2. `schemas.json` validating the elements and links of the model
   (`schema_definitions_from_json`), with severities mapped to the CI tiers.
3. Templates and own skills (`{SKILL_HOME}`, mirrored to `{HARNESSES}`).
4. Documentation of the model and the engineering process.
5. CI as decided (Q-CI…).
6. Project plan with learning log; this playbook updated.

When the brief asks for it: code / test layout with markers and test results,
cross-cutting needs with hand-over payloads and evaluation jobs, reports, a
pilot chain.

## 1. Project context (parameters)

Collect first, mostly from the repository (ask only what cannot be read off
it, confirm the rest). Every later section uses these names.

| Parameter | Meaning | How to find / ask | Seen in runs |
|---|---|---|---|
| `{DOCS}` | directory of the `ubproject.toml` (project root for `ubc -p`) | `find . -name ubproject.toml`; ask if several | 001: `docs/` |
| `{PLAN_DIR}` | where plans live, numbering scheme | ask; check existing plans | 001: `.agents/plans/`, `NNN-` |
| `{TOOL_BUGS}` | tool-bug record to append findings to (or none) | look for one; ask | 001: plan 999 (+ re-check plan 998) |
| `{MAIN}` | integration branch | `git symbolic-ref refs/remotes/origin/HEAD` | 001: `main` |
| `{BRANCH_POLICY}` | work branch, commit / PR policy | ask | 001: feature branch, uncommitted until asked |
| `{CI}` | CI platform | `.github/`, `.gitlab-ci.yml`, …; ask | 001: GitHub Actions |
| `{REPO_VISIBILITY}` | open (public) or closed (private) repository | `gh repo view --json visibility` (or the forge's equivalent); confirm with the user | 001: public |
| `{UBC_LICENSE}` | how CI gets the ubc license | open repo: no key needed; closed repo: ask for a key — the **user** stores it as CI secrets (`UBCODE_LICENSE_KEY`, `UBCODE_LICENSE_USER`, e.g. `gh secret set`); never paste the key into chat, plans or files | 001: none (public) |
| `{TOOLCHAINS}` | builders that must agree | `[scripts]`, `conf.py`; ask | 001: ubc + Sphinx (parity required) |
| `{HARNESSES}` | AI harnesses that need skill copies | install manifest, `.claude/`, `.github/agents/`, …; ask | 001: Claude Code, GitHub Copilot |
| `{SKILL_HOME}` | source of own skills / templates | ask | 001: `.agents/` + mirrors |
| `{MANIFEST}` | install-owned assets | `{DOCS}/.pharaoh/agent/install-manifest` | 001: `vmodel` profile 21 |
| `{VARIANTS}` | variant handling in use | `[variants]`, `variant_data*`, `parse_variants` | 001: yes |
| `{EXISTING}` | existing needs, types, links to keep / migrate | `ubc build needs`, config | 001: 2 req, 2 spec, 2 test |
| `{CODE}` | languages, source / test dirs, test framework, report format | repository; ask | 001: none yet → Python, pytest, JUnit |

## 2. Input brief and questions

Two steps before the project plan is written: collect the **basic model**
from the user (§2.1), then settle the open design decisions (§2.2). The basic
model of an earlier run is never taken as given.

### 2.1 Input brief (the user's basic model)

Ask the user for the brief below, as free text or by filling in this form.
Where the user asks for a suggestion, the agent proposes and the user
confirms. Copy the confirmed brief into the project plan.

**a. Types** — one row per type:

| Field | Ask | Example (run 001) |
|---|---|---|
| name / directive | what is it called, which directive | user story, `us` |
| prefix | id prefix | `US_` |
| purpose | what does one need of this type state | one user-visible goal |
| authored as | RST directive, code marker (codelinks), generated (e.g. test results), nested in another need | RST |
| up-link | which type(s) it links to, how many | `req` → `us` |
| special rules | uniqueness, mandatory children, coverage | no two `us` on the same topic |

Also ask: cross-cutting types (e.g. decisions, risks, assumptions, issues)?
How do they attach (nested, linked, global log)? Must every need carry one?

**b. Fields** — domain and applicable standards (safety, security,
regulatory, none); fields given by the user or suggested. Offer a
suggestion as a **pick list** (each field with its purpose), not as a
package — run 001 dropped 5 of 11 suggested fields. A suggestion
covers what the domain needs, e.g. lifecycle, integrity / relevance,
ownership, priority, verification method, test level, fields of the
cross-cutting types, review dates.

**c. Links** — the user's list or a suggestion: one link per type pair
(outgoing / incoming names), cross-cutting links, domain-specific links.

**d. Workflow principles** — stage shape (simple need-to-need or larger);
what each stage skill must state (incoming / outgoing needs, template,
route, links); templates per type; how cross-cutting needs are documented
per stage (e.g. a full hand-over payload to simple recording skills);
evaluation of cross-cutting needs (resolved, stale, overdue).

**e. Schema (elements and links)** — ask explicitly, also when the brief
does not mention it: which rules the model must enforce in `schemas.json`:

- elements: allowed values per type (e.g. per-type `status`), required
  fields per type;
- links: mandatory up-links (`minItems`), allowed target types
  (`validate.network` `items` / `contains`), conditional rules (e.g. "a
  mitigated risk has a mitigation link");
- completeness: coverage back-links (`network_back`), mandatory
  cross-cutting needs (e.g. decisions per type);
- propagation of attributes along links (e.g. safety relevance);
- which findings may stay open on the integration branch and which block a
  release (→ severities, Q-SEV).

**f. Overviews** — which reports, in which format (RST pages, `ubc report`
templates, …).

**g. Expected results** — config, documentation, CI, anything else.

**h. Process constraints** — is the existing / pilot content **real or test
data** (decides how much migration and review care later changes need; run 2:
test data, removed later); bootstrap tool, how the user wants to evaluate
the configuration, CI docs to follow, repeatability.

### 2.2 Decision questions

Ask with the interactive question tool, max 4 per round. The recommended
option (listed first) is derived **from this brief and context**, with a
reason — not copied from an earlier run. Skip a question the brief already
answers, or that does not apply (column "Ask when"). Ask follow-ups on free
text answers. Record everything in the project plan.

| ID | Question | Ask when | Options to consider | Seen in runs |
|---|---|---|---|---|
| Q-BOOT | Bootstrap approach | always | by hand + references (§3 B); `ubc agent install --detect` (graph already covers the model); `pharaoh-onboard` (brownfield) | 001: by hand |
| Q-TYPES | Gaps in the type list (e.g. architecture level missing?) | always | from the brief | 001: none |
| Q-DUP | How to prevent overlapping needs of a type | brief has a uniqueness rule | review axis; axis + check skill; check skill | 001: review axis |
| Q-INT | Integrity attributes | brief names safety / security | domain standard levels (e.g. ASIL, SIL, DAL, CAL, IEC 62304 class); generic bools + level; none | 001: generic |
| Q-XCUT | Placement of each cross-cutting type (suggestion for decisions / risks: §9.1) | brief has cross-cutting types | nested in parent + link; file per stream; central log — tell the user first: workflow stages cover a whole upstream type and author into files (PH-16), so nested / per-need elements are created by stage skills, not stages | 001: decisions nested, risks global; both via stage skills + recording skills |
| Q-LANG | Code / test language, framework | brief has code-marker or test-result types, `{CODE}` unclear | from the repository | 001: Python + pytest |
| Q-MOUNT | sphinx-mounts usage — tell the user first: mounts carry **documents** (`.rst` / `.md`), not code; code is read by Codelinks directly | Sphinx in `{TOOLCHAINS}` and sources outside `{DOCS}` | docs next to the code (`src-trace` / `test-file` pages in `src/`, `tests/`); mount templates; none | 001: src + tests |
| Q-LINKS | Rename existing links / migrate needs? | `{EXISTING}` conflicts with the model | rename + migrate; keep | 001: rename |
| Q-SCHEMA | Create a `schemas.json` for elements and links? | always (the user may not think of it) | yes, from the brief §2.1 e; later; no | 001: yes (asked late, at G0) |
| Q-SEV | Schema severities per CI tier | Q-SCHEMA = yes | `violation` always wrong + `info` completeness (open on integration, zero on release); all `violation`; three levels | 001: violation + info |
| Q-COV | Coverage rules: where | Q-SCHEMA = yes | schema + workflow traces; workflow only; schema only | 001: both |
| Q-PROP | Propagate attributes along links | integrity attributes exist | child must match parent; parent from child; both; none | 001: none |
| Q-XREQ | Which types must carry a cross-cutting need (e.g. a decision) | brief has a "every … has …" rule | per type | 001: decisions on us, req, spec, test_spec |
| Q-LIFE | **Which types** have a lifecycle (`status`), and which values / final values per type (suggestion: §9.1) | always — ask per type, not one answer for all | only cross-cutting types; all authored types; all types; draft→review→approved; own values per type on the one `status` field | 001: only `dec` / `risk` (first misapplied to all types, L20) |
| Q-EVAL | How the user evaluates the configuration | always | model docs page; gate per phase; validator output; pilot chain with per-artefact approvals; **autonomous pilot + HTML review** (agent authors and reviews, user reviews the rendered result); extra questions in pilot | 001: docs page, gates; the pilot ran autonomously with an HTML review (user's choice at P8) |
| Q-JOBS | How cross-cutting needs are kept current (unresolved / stale) (suggestion: §9.1) | brief asks for evaluation | unresolved: schema `info` rules + report pages; stale: review gate with `outgoing` trace edges on the stage (works for nested needs), hash-conditioned links `TARGET[fp=="…"]` with a derived `fingerprint` field (not for nested needs — the hash invalidates itself), own ledger script; judgment: review skills | 001: decisions → trace edges, risks → hash conditions, reports, no script |
| Q-CI | CI tiers | always | one pipeline; integration + release tiers; more | 001: two tiers |
| Q-REL | What marks a release | release tier exists | release branch PR (name pattern?); tag (pattern?); both | 001: both (`release/*`, `v*`) |
| Q-CI1 | What the integration tier blocks on | per tier | build / lint; new gaps (ratchet); failing verdicts; tests; open status | 001: all but open status |
| Q-CI2 | What the release tier requires | release tier exists | all needs final; zero gaps; verdicts clean; cross-cutting needs resolved | 001: first three |
| Q-PILOT | Pilot chain: which feature | Q-EVAL includes a pilot | from the domain | 001: "password reset" (proposed) |
| Q-PRESET | What happens to the installed profile skills (`ubc agent install`) | always, after reading the installed skills that the stages would use | keep all + own copies under new names; replace the used ones with the project pattern + remove the unused ones (then `update` only in a shadow clone, PH-18); keep all, only instruct agents (`AGENTS.md`) | 001: replace + remove |
| Q-RUNNER | Headless runner for `ubc agent run` | always | configure (`[agent.runner]`); interactive only | 001: configured (`claude -p`) |
| Q-PLANS | Plan files | always | project plan + playbook update; project plan only | 001: both |

## 3. Steps

### A. Inventory

- Fill §1 from the repository.
- Tool versions; CI version pin = local version.
- `{MANIFEST}`: install-owned skills / packs (see Q-PRESET before editing
  any). Its paths mix bases: harness copies are relative to the repository
  root, `quality/*.toml` to `{DOCS}`.
- `{EXISTING}`: check existing field values against the planned enums
  before migrating (run 001: a variant status `win_auth` violated the new
  status set).
- `{TOOL_BUGS}`: which entries turn from latent to applies with the planned
  features (`[workflow]`, codelinks, test reports, schemas, `id_regex`,
  mounts, variants).

### B. Reference configs (scratchpad only)

- `ubc agent install --detect --plan -p {DOCS}` (writes nothing): what the
  engine derives from the current graph.
- `ubc agent install` in an **empty** scratch dir (with `git init`): the
  blank profile (`vmodel` or the profile in use) with full `[workflow]`,
  `[codelinks]`, `[quality]` and comments — the reference shape for stages,
  routes, traces, markers. (In a dir that already has a `ubproject.toml` it
  writes no `[workflow]`.)
- Fetch the schema; check every planned key against it.
- **Diff the brief against the blank profile** (types, links, stages,
  routes, quality packs, `id_regex`, provenance fields) and ask the user
  about every deviation, one question each.
- Stage routes and codelinks `src_dir` are **relative to `{DOCS}`** (the
  directory of `ubproject.toml`), e.g. `user_stories.rst`, `../src` — not
  repository-relative.

### C. Brief, discussion, project plan

1. Collect the brief (§2.1); propose what the user asked to be suggested.
2. Present the resulting model compactly, then the questions of §2.2.
3. Write the project plan in `{PLAN_DIR}` from context + brief + answers
   (structure example: plan 001).

### D. Phases (each ends with a user gate; include only what applies)

| Phase | Content | Include when | Done when | Gate shows |
|---|---|---|---|---|
| P0 | branch, versions, references | always | references saved | proposal vs. references |
| P1 | types, fields, links, schema element + link rules, migration, model docs page | always | all `{TOOLCHAINS}` green, no schema `violation` | rendered model page incl. schema rules |
| P2 | code / tests / codelinks / test reports / mounts | brief has code-marker or test-result types | those needs in all builds | builds |
| P3 | `[workflow]`, `[quality]`, schema completeness rules | always | `config-validate` + `doctor` ok | validator / status / gaps output |
| P4 | templates, payloads, skills, mirrors | always | `ubc agent prompt --stage` per stage sensible | sample skills |
| P5 | spike evaluation jobs | Q-JOBS = spike | options compared | option table |
| P6 | reports, model docs section | always | builds green | docs section |
| P7 | CI per Q-CI… | always | every tier green on a test branch | CI runs |
| P8 | pilot chain via `ubc agent next` / `prompt` | Q-EVAL includes a pilot | chain passes the strictest tier | chain + CI |
| P9 | retro: this playbook, `{TOOL_BUGS}` | always | learning log folded | diff of this playbook |

## 4. Design rules

From tool facts (re-check on new versions):

- **One link name per edge.** Avoid one link for several type pairs
  (PH-04, PH-05); never rely on the generic `links` field for traces (PH-13).
- **Do not declare Sphinx-Test-Reports types** in `[[needs.types]]`
  (STR-03); `config-validate` may flag them (PH-12).
- **Schema severities vs. Sphinx**: `info` / `warning` are Sphinx warnings,
  `violation` a Sphinx error (SN-01). With `-W`, suppress the non-blocking
  level (`suppress_warnings = ["sn_schema_info"]`) and gate on
  `schema_violations.json` instead — if Sphinx is in `{TOOLCHAINS}`.
- **Core fields have fixed types** (`id`, `title`, `status`, `type`,
  `tags`): an enum on `status` may be refused; then put the allowed values
  into a global `schemas.json` rule. Shared fields: union of values in the
  toml, per-type values in `schemas.json`.
- **A field default applies to every type.** Never use it for a value that
  only some types should carry (run 001: `status` default `open` put a
  status on generated needs); require the field per type in `schemas.json`
  instead.
- **Conditional selects need `required`.** `properties.X.const` passes when
  `X` is absent; add `required: [X]` to every select fragment that tests a
  value.
- **Forbidding a field** on some types: `maxLength: 0` (string fields) works
  in ubc and Sphinx; `type: null` is refused for a typed field, `not` is
  unsupported in ubc (UB-21).
- **Lifecycle and prompt status are global in Pharaoh.** `[workflow.lifecycle]
  states` judges every need (PH-14) and the author prompt orders one status
  for every type (PH-15). If only some types have a status, leave the
  lifecycle out, check status per type in `schemas.json`, and state the
  status rule in every stage's `authoring` text.
- **Regular stages use `scope = "stream"`.** With `global`, the author
  prompt orders every new need to link ALL needs of its up type (PH-16).
  Dry-run every stage with `ubc agent prompt --stage <id> --id <anchor>`
  (in a scratch copy without review holds) before the pilot.
- **Tests use specified values literally** (limits, durations, formats),
  never the code's constants — otherwise a code change missed by a
  `change-request` cascade stays green (001 P8, PH-22).
- **Headless runner:** give it `--allowedTools` for `ubc` (`Bash(*/ubc *)` —
  prompts use the absolute path) and the project scripts; without them every
  stage is reported "no change" (PH-21). Test `change-request` in a clone
  with the chain committed.
- **Commands in skills:** only `ubc agent` takes `-p`; `ubc check` /
  `ubc build` take the project path as argument, `ubc script` takes
  `--path`. Run every command a skill names once.
- **Nested needs:** let the link to the parent be derived
  (`predicates = [["type == '<t>'", "[[copy('parent_need')]]"]]` — not
  `default`, which warns on every need without a parent); check nesting with a
  derived copy of `parent_need` (ubc cannot see `parent_need` in schemas,
  UB-25); remember the parent's fingerprint contains the nested text.
- **Diagrams:** ubc renders `mermaid` and draws `needflow` with mermaid;
  Sphinx-Needs draws `needflow` with **PlantUML by default** — without it the
  page says "PlantUML is not available!" and `-W` still passes (SN-09). Set
  `[needs] flow_engine = "graphviz"` + `sphinx.ext.graphviz` (CI: install
  graphviz), and look at every rendered diagram in both builds at the gates.
- **Derived fields** (`derive`) need Sphinx-Needs >= 9.0; pin it and silence
  `config.derive_sphinx_minimum` (an `info`, fatal under `--deny info`).
- **Schemas with allow-lists.** ubc supports only `allOf`, `properties`,
  `required`, `type`, `unevaluatedProperties` in `select` / `local`; express
  "not X" as an enum of the allowed types (UB-21). Negative-test every rule
  in a scratch copy, in both toolchains.
- **Type names from `needs.json`,** not from tool docs (Sphinx-Test-Reports
  creates `testcase`, its docs say `test-case`, STR-06); a `select` on a
  wrong name silently validates nothing.
- **Ground new elements in what exists.** Stage skills (especially
  architecture) must take responsibilities and interfaces from the
  requirements and the existing code, not invent features; a gap is a risk,
  not new design (run 2: an invented session design cascaded into specs).
- **Codelinks one-line fields are positional:** a required field after one
  with a default is refused; make all marker fields required (explicit
  links and safety / security values).
- **Own review skills** are copies of a generic installed review skill
  (only the stage name differs); the rubric comes from the quality pack.
- **Network validation** nests at most 4 levels; `contains` on a list field
  needs `items` in Sphinx (SN-05).
- **Variants + verdicts** (if `{VARIANTS}`): verdicts are per id and ignore
  resolved variant values (PH-01, PH-02) — keep reviewed needs variant-free or
  document it.
- **Installed profile skills** (`{MANIFEST}`): read every one a stage would
  use before wiring it — they follow the profile's model, not the project's
  (001: status line, `code_trace.rst`, no hand-over). Per Q-PRESET either
  leave them untouched (own copies under new names), or replace / remove them
  **and** remove their manifest entries: an edited installed skill is a
  `doctor` error, and `ubc agent update` re-adds removed entries and restores
  removed files (PH-18) — then run `update` only in a shadow clone and port
  changes by hand (plan 998 §4.7 of run 001).
- **Engine-invoked skills** (e.g. `change-request`) are run by name and
  cannot be swapped for a copy; test them in the pilot against the model's
  rules (nested needs, status, append-only).

From the playbook's method (apply unless the brief says otherwise):

- **Stage skills own the context.** Each stage skill lists incoming needs,
  outgoing needs, template, route, links, and when to raise a cross-cutting
  need; it fills the hand-over payload, the recording skill only renders it.
- **Every produced type has a template** in `{SKILL_HOME}`; every recording
  skill has a payload definition.
- **Schema and workflow describe the same edges.** Every link edge appears
  once in the links table, once as a workflow trace and once as a schema
  link rule; change all three together.
- **A quality pack per reviewed type**, own packs next to installed ones.
- **All `{TOOLCHAINS}` after every phase**; differences → `{TOOL_BUGS}`.

## 5. CI blueprint

Fill per tier from Q-CI, Q-REL, Q-CI1, Q-CI2 on `{CI}`:

| Check | Command | Typical tier |
|---|---|---|
| lint / build | `ubc script check`, `ubc build html`, other `{TOOLCHAINS}` (e.g. Sphinx `-W`) | all |
| tests | `{CODE}` test command → report file, **before** the docs build | all, if P2 |
| agent config | `ubc agent config-validate`, `ubc agent doctor` | all |
| schema `violation` | `ubc check`, Sphinx errors | all |
| schema completeness (`info`) | `ubc check --deny info` (ubc) + `schema_violations.json` empty (Sphinx, `info` suppressed on the console) | release |
| new gaps | own gate on `ubc agent gaps` with a committed baseline (ratchet), allowing `review` / `status_disallowed` — not `release-check` (PH-20) | integration |
| zero gaps | `ubc agent gaps` | release |
| failing verdicts | `ubc agent verdict-check` filtered to `failing` / `malformed` (`malformed` is a count, the rest are id lists) | integration |
| clean verdicts | `ubc agent verdict-check` | release |
| final status | no need in a non-final status (`release_disallow_status`) | release |
| evaluation jobs | per Q-JOBS | per Q-JOBS |
| skill mirrors | copies in `{HARNESSES}` identical to `{SKILL_HOME}` | all |

Install ubc in CI per the ubCode CI/CD docs with a pinned version and the
runner OS's binary; pin the other builders too. For a closed repository
(`{REPO_VISIBILITY}`), pass the license secrets as the `UBCODE_LICENSE_KEY` /
`UBCODE_LICENSE_USER` environment variables to every `ubc` step; for an open
one, set none. If the visibility changes later, the CI must change with it.

## 6. Pitfalls seen so far

- `--detect` drops types it cannot place in a chain (001: `test`) and never
  proposes types the graph does not have yet.
- `ubc agent install` writes no `[workflow]` into an existing
  `ubproject.toml`.
- `verdict-check` exits non-zero on `missing` as well — an integration tier
  that tolerates missing verdicts needs a filter.
- Editing install-owned skills makes `ubc agent update` report conflicts.
- One answer generalised to all types: a lifecycle chosen for some types got
  applied to all of them (run 001, L20) — confirm per type.
- The schema of elements and links is easy to forget: run 001 asked for it
  only at G0 — Q-SCHEMA is now asked always.
- A playbook drifts into one project's answers: run 001 first hard-wired its
  basic model and its context (paths, CI, language, tiers) — keep them in the
  parameters / brief, examples only in "seen in runs".

## 7. Updating this playbook

At the end of each run (phase P9):

1. Move every learning-log entry of the project plan into §1 (parameter),
   §2 (brief field or question), §3 (step), §4 (rule), §5 (CI) or §6
   (pitfall); a setup the user liked as a whole goes to §9 (suggested
   patterns). Run-specific answers go only into "seen in runs" columns.
2. Re-check §4 / §6 against the tool versions of the run.
3. Add the run below.

| Run | Plan | Date | Project | Notes |
|---|---|---|---|---|
| 1 | [001](001-engineering-model.md) | 2026-10-17 | product_demo `docs/` | first run; P0–P9; pilot "login lockout" autonomous with HTML review; CI 1 + CI 2 green; 20 new tool findings (UB-20…26, PH-14…22, SN-08/09, STR-06/07); decisions / risks setup became pattern §9.1 |
| 2 | [002](002-add-arch-level.md) | 2026-10-17 | product_demo `docs/` | model change: architecture level; autonomous; became §8 "Changing a model later"; finding PH-23 |

## 8. Changing a model later (proven in run 2, plan 002)

Inserting a level (or any type / link change) into a model that already has
content, reviews and CI:

1. **Re-check the plan against the current state** before asking anything
   (needs, verdicts, risks with hash conditions, CI tiers, every page /
   skill / template that names the changed edge).
2. **Order of changes:** links → schema (rules + type lists) → workflow
   (new stage, changed `depends_on` / traces, `decisions` edges) → quality
   pack → template → skills (new stage skill, parent / downstream text of
   the neighbours) → docs pages → migration → re-review → sign-off of risks.
3. **Migration:** new elements can be authored through the workflow
   (`ubc agent run --id <parent>`), but **re-linking existing needs to a new
   parent is manual** — `change-request` designs new needs instead (PH-23).
   Check every runner output against the skill (missing steps, invented
   scope).
4. **Expect re-reviews** where content or parents change, and stale risks
   where their targets change; `scripts/refresh_risk_links.py` after the
   re-evaluation.
5. **Land the change in one merge:** CI 1 ratchets structural gaps, so a
   half-migrated model must not reach `main`.

## 9. Suggested patterns

Proven setups to **propose** in §2 (the user decides; adapt names and
values to the brief). Each lists what to build, the reference files of the
run that proved it, and its limits.

### 9.1 Decisions and risks (proven in run 001)

Use when the brief asks for documented decisions and risks that stay
current while the model changes (§2.2 Q-XCUT, Q-LIFE, Q-JOBS).

**Model**

| | Decision (`dec`) | Risk (`risk`) |
|---|---|---|
| Where it lives | **nested inside** the need it decides | own page (`risks.rst`) |
| Links | `decides` → the parent, **filled automatically**; further targets explicit (parent first) | `affects` → any need; `mitigated_by` → req / spec / test_spec / dec; both with **hash conditions** `TARGET[fp=="…"]` |
| Status (built-in `status`, only these two types) | `proposed` → `accepted` / `superseded` | `open` → `mitigated` / `accepted` → `closed` |
| Fields | `safety_relevant`, `security_relevant` | + `risk_category` (safety / security / technical / project / ai-workflow), `severity`, `likelihood` |
| Body | Context / Alternatives / Consequences / Rationale (bold labels) | Cause / Effect / Mitigation |
| Required on | every `us` / `req` / `spec` / `test_spec` has ≥ 1 decision (adapt per brief) | — |
| Kept current by | the **review gate**: a changed parent outdates the decision's verdict | the **hash conditions**: a changed target fails the link (`needs.link_condition_failed`) |
| Re-evaluation | re-review (`review-decision`) | re-review (`review-risk`), then sign-off `scripts/refresh_risk_links.py <ID>` |

**Configuration** (`ubproject.toml`)

- `[needs.links.decides] predicates = [["type == 'dec'", "[[copy('parent_need')]]"]]`
  — not `default` (warns on every need without a parent).
- Derived fields (Sphinx-Needs ≥ 9.0, pin it; `[lint] ignore =
  ["config.derive_sphinx_minimum"]`):
  `fp` = `derive = { kind = "fingerprint" }`, `parent` =
  `derive = { kind = "copy", field = "parent_need" }`.
- `status`: `schema.enum` = union of the decision and risk values, **no
  default** (a default lands on every type).
- `[workflow]`: a `decisions` stage (`produces = "dec"`, `optional = true`,
  review skill) with `[[workflow.stages.trace]]` `link = "decides"`,
  `direction = "outgoing"`, `min = 1`, one edge per parent type — makes the
  fingerprint follow `decides`, creates no gaps; a `risks` stage
  (`optional = true`, review skill) **without** trace edges. Neither stage
  is authored through `ubc agent prompt` (it would ask for one element
  linking all upstream needs, PH-16); `release_disallow_status = ["open",
  "proposed"]`; no `[workflow.lifecycle]` (PH-14).

**Schema** (`schemas.json`, all negative-tested in both toolchains)

| Rule | Severity | Checks |
|---|---|---|
| `status-dec`, `status-risk` | violation | status required, own values |
| `status-none` | violation | other types carry no status (`maxLength: 0`) |
| `dec-nested` | violation | `parent` set (not `parent_need`, UB-25) |
| `link-dec` | violation | ≥ 1 `decides`, no decision as target |
| `link-risk-affects`, `link-risk-mitigation` | violation | ≥ 1 `affects`; mitigation targets req / spec / test_spec / dec |
| `risk-mitigated`, `risk-accepted` | violation | mitigated → `mitigated_by`; accepted → an accepted decision decides it (selects with `required: [status]`) |
| `dec-present` | info | required parents have a decision |
| `dec-proposed`, `risk-open` | info | unresolved items (block a release only) |

**Skills and templates**

- Stage skills record decisions / risks of their stage and hand a complete
  JSON payload to the recorders (`handover/decision.json`, `risk.json`);
  `draft-impl` nests implementation decisions in the spec it implements.
- `record-dec` (renders `dec.rst` nested at the end of the parent's body,
  `:decides:` only for further targets), `record-risk` (renders `risk.rst`
  with plain ids, appends, runs the refresh script) — validate the payload,
  stop on gaps, decide nothing.
- Quality packs `dec.toml` (context present required, alternatives,
  consequences, rationale), `risk.toml` (cause and effect, rating justified,
  affected complete, mitigation fit); parent packs get `decisions_documented`.

**CI and reports**

- CI 1: `proposed` / `open`, `dec-present` (info) and stale risks allowed
  (Sphinx `suppress_warnings += needs.link_condition_failed` via an env
  var, ubc `UBCODE_CONFIG_OVERRIDE` `lint.ignore`), reported; CI 2: none.
- Reports: proposed decisions, needs without a decision
  (`len(decides_back) == 0`), decision log; open risks, risks without a
  mitigation (`len(mitigated_by) == 0`), security / safety risks — same rows
  in ubc and Sphinx; hashes are not rendered.

**Reference files (run 001):** `docs/ubproject.toml`, `docs/schemas.json`,
`docs/quality/{dec,risk}.toml`, `.agents/templates/{dec,risk}.rst`,
`.agents/templates/handover/`, `.agents/skills/{record-dec,record-risk,review-risk}/`,
`scripts/refresh_risk_links.py`, `docs/reports/{decisions,risks}.rst`,
`docs/engineering_model/decisions_risks.rst`.

**Limits to tell the user**

- Editing a decision changes its parent's text → the parent (and its
  direct children) are re-reviewed too.
- Hash conditions do not work for nested needs (the hash would include
  itself) — that is why decisions use the review gate; only the full 64-hex
  value works (UB-24); the RST carries the hashes (pages do not).
- `change-request` does not reconcile the decisions nested in the edited
  need, nor risk texts (PH-22) — the review gate and the hash conditions
  flag them instead.
- `ubc agent impact` does not list nested decisions (PH-19).
- Alternatives evaluated in run 001 P5 and not chosen: own ledger script
  (works with nesting, extra code), hash conditions for decisions (fail with
  nesting), `evaluate-*` skills (the review skills do the job), scheduled job
  (optional).

