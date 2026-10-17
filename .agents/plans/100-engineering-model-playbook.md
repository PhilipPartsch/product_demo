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
- The project's tool-bug record, if it has one (`{TOOL_BUGS}`)

## 0. Outputs of a run

Always:

1. `ubproject.toml` with the types, fields, links, `[workflow]` and
   `[quality]` of the brief (plus `[codelinks]`, `[test_reports]`, schemas
   when the brief uses them).
2. Templates and own skills (`{SKILL_HOME}`, mirrored to `{HARNESSES}`).
3. Documentation of the model and the engineering process.
4. CI as decided (Q-CI…).
5. Project plan with learning log; this playbook updated.

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
regulatory, none); fields given by the user or suggested. A suggestion
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

**e. Overviews** — which reports, in which format (RST pages, `ubc report`
templates, …).

**f. Expected results** — config, documentation, CI, anything else.

**g. Process constraints** — bootstrap tool, how the user wants to evaluate
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
| Q-XCUT | Placement of each cross-cutting type | brief has cross-cutting types | nested in parent + link; file per stream; central log | 001: decisions nested, risks global |
| Q-LANG | Code / test language, framework | brief has code-marker or test-result types, `{CODE}` unclear | from the repository | 001: Python + pytest |
| Q-MOUNT | sphinx-mounts usage | Sphinx in `{TOOLCHAINS}` and sources outside `{DOCS}` | mount sources; mount templates; none | 001: src + tests |
| Q-LINKS | Rename existing links / migrate needs? | `{EXISTING}` conflicts with the model | rename + migrate; keep | 001: rename |
| Q-LIFE | Lifecycle states | always | minimal; draft→review→approved; extended | 001: open / done |
| Q-EVAL | How the user evaluates the configuration | always | model docs page; gate per phase; validator output; pilot chain; extra questions in pilot | 001: docs page, gates, pilot questions |
| Q-JOBS | Evaluation jobs for cross-cutting needs | brief asks for evaluation | CI report; CI gate; agent skill; scheduled; spike first | 001: spike |
| Q-CI | CI tiers | always | one pipeline; integration + release tiers; more | 001: two tiers |
| Q-REL | What marks a release | release tier exists | release branch PR (name pattern?); tag (pattern?); both | 001: both (`release/*`, `v*`) |
| Q-CI1 | What the integration tier blocks on | per tier | build / lint; new gaps (ratchet); failing verdicts; tests; open status | 001: all but open status |
| Q-CI2 | What the release tier requires | release tier exists | all needs final; zero gaps; verdicts clean; cross-cutting needs resolved | 001: first three |
| Q-PILOT | Pilot chain: which feature | Q-EVAL includes a pilot | from the domain | 001: "password reset" (proposed) |
| Q-PLANS | Plan files | always | project plan + playbook update; project plan only | 001: both |

## 3. Steps

### A. Inventory

- Fill §1 from the repository.
- Tool versions; CI version pin = local version.
- `{MANIFEST}`: install-owned skills / packs (never edit; own assets get own
  names).
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

### C. Brief, discussion, project plan

1. Collect the brief (§2.1); propose what the user asked to be suggested.
2. Present the resulting model compactly, then the questions of §2.2.
3. Write the project plan in `{PLAN_DIR}` from context + brief + answers
   (structure example: plan 001).

### D. Phases (each ends with a user gate; include only what applies)

| Phase | Content | Include when | Done when | Gate shows |
|---|---|---|---|---|
| P0 | branch, versions, references | always | references saved | proposal vs. references |
| P1 | types, fields, links, migration, model docs page | always | all `{TOOLCHAINS}` green | rendered model page |
| P2 | code / tests / codelinks / test reports / mounts | brief has code-marker or test-result types | those needs in all builds | builds |
| P3 | `[workflow]`, `[quality]`, schemas | always | `config-validate` + `doctor` ok | validator / status / gaps output |
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
- **Schemas**: pick severities that do not break Sphinx `-W` (SN-01) — if
  Sphinx is in `{TOOLCHAINS}`.
- **Variants + verdicts** (if `{VARIANTS}`): verdicts are per id and ignore
  resolved variant values (PH-01, PH-02) — keep reviewed needs variant-free or
  document it.
- **Install-owned assets** (`{MANIFEST}`) stay untouched, or `ubc agent
  update` reports conflicts.

From the playbook's method (apply unless the brief says otherwise):

- **Stage skills own the context.** Each stage skill lists incoming needs,
  outgoing needs, template, route, links, and when to raise a cross-cutting
  need; it fills the hand-over payload, the recording skill only renders it.
- **Every produced type has a template** in `{SKILL_HOME}`; every recording
  skill has a payload definition.
- **A quality pack per reviewed type**, own packs next to installed ones.
- **All `{TOOLCHAINS}` after every phase**; differences → `{TOOL_BUGS}`.

## 5. CI blueprint

Fill per tier from Q-CI, Q-REL, Q-CI1, Q-CI2 on `{CI}`:

| Check | Command | Typical tier |
|---|---|---|
| lint / build | `ubc script check`, `ubc build html`, other `{TOOLCHAINS}` (e.g. Sphinx `-W`) | all |
| tests | `{CODE}` test command → report file, **before** the docs build | all, if P2 |
| agent config | `ubc agent config-validate`, `ubc agent doctor` | all |
| new gaps | `ubc agent release-check` vs. committed baseline (ratchet) | integration |
| zero gaps | `ubc agent gaps` | release |
| failing verdicts | `ubc agent verdict-check` filtered to `failing` / `malformed` (`jq`) | integration |
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
- A playbook drifts into one project's answers: run 001 first hard-wired its
  basic model and its context (paths, CI, language, tiers) — keep them in the
  parameters / brief, examples only in "seen in runs".

## 7. Updating this playbook

At the end of each run (phase P9):

1. Move every learning-log entry of the project plan into §1 (parameter),
   §2 (brief field or question), §3 (step), §4 (rule), §5 (CI) or §6
   (pitfall). Run-specific answers go only into "seen in runs" columns.
2. Re-check §4 / §6 against the tool versions of the run.
3. Add the run below.

| Run | Plan | Date | Project | Notes |
|---|---|---|---|---|
| 1 | [001](001-engineering-model.md) | 2026-10-17 | product_demo `docs/` | first run, pilot |
