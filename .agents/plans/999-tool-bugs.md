# Plan 999: Bugs and gaps in the useblocks tools

Record of bugs and gaps in the **useblocks tools**, imported on 2026-10-17
from the repository `github.com/PhilipPartsch/variant_demo` (the "origin
repository", where they were collected while building the CV platform).
Sphinx, kconfiglib, CMake / CMake Tools and libclang are out of scope. Kept up
to date by every later plan of this repository — add new entries at the end
of the tool's section.

Each entry: summary, **marker** (`branch@commit` + file:line where it can be
reproduced), input, wrong output (and what was expected), the workaround used,
and two alternative solutions.

**Markers.** Markers of the imported entries (`main@…`, `content/cv-platform@…`,
`ci/pages@…`, `feat/choose@…`, "scratch copy based on …") and the plan numbers
they cite (plans 1–7, 20, 110, M-04, M-12, …) refer to the **origin
repository**, not to this one; its files (`tools/*`, `third_party/`,
`Kconfig`, `src/`, …) do not exist here. Where an entry can also be reproduced
in this repository, it has an extra line **Marker here:** with a pushed
commit of this repository (`main@<commit>`). New entries found here use
markers of this repository only.

**Origin.** Every entry imported from the origin repository is marked
**external** (column **Origin** in §2, and a line `- **Origin:** external …`
under its heading). Entries found in this repository get `- **Origin:**
product_demo` and `product_demo` in the column. Status lines of external
entries come from the origin repository's plan 998 runs; a Status line made
here names `product_demo` (plan 998 §3).

## 0. This repository

`product_demo` is a small ubCode docs project (`docs/`) with an
engineering model built by plan 001: types `us` / `req` / `spec` / `impl`
(Sphinx-Codelinks markers in `src/`) / `test_spec` / test results
(Sphinx-Test-Reports from pytest) / `dec` / `risk`, one link per edge,
`schemas.json`, `id_regex`, derived fields (`fp`, `parent`), conditional
(hash) links on risks, sphinx-mounts (`src/`, `tests/`), variant data
(`docs/variants.json`, `<{ var.* }>` in `platform_note`), a `[workflow]`
with own skills, `[quality]` packs and a headless runner (Pharaoh, profile
`vmodel` 21, unused profile skills removed). It builds with ubc (`ubc script
ci`) and with Sphinx + Sphinx-Needs (`ubc script sphinx`, via `uv`); CI in
`.github/workflows/ci-main.yml` / `ci-release.yml` (setup:
`.github/actions/setup/action.yml`). Not used here: external needs,
`needimport`, ubc-action.

Column **Here** in §2:

- **applies** — the affected feature is used here; the bug can show in this repository today.
- **latent** — not triggered by the current content, but it will be as soon as the named feature is adopted (e.g. a `[workflow]` for Pharaoh, a parity check of the two `needs.json`).
- **n/a** — the affected tool or feature is not used here; kept for the record and for the re-check (plan 998).
- **avoided by design** / **not triggered** — the feature is used, but this repository's setup does not hit the bug (the reason is named); re-check when the setup changes.
- **workaround found** — applies, and a workaround is in place (named in the entry).

## 1. useblocks tools

Checked on [useblocks.com](https://useblocks.com) and the
[useblocks reference list](https://x-as-code.useblocks.com/reference/index.html), 2026-10-09.
The findings were made in the origin repository with older versions (column
"Findings made with"). The origin repository re-tested all entries on
2026-10-17 (its plan 998 run 1: ubc 0.37.0, Sphinx-Needs 9.0.0,
Sphinx-Codelinks 2.0.0, sphinx-mounts 0.3.0, Sphinx-Test-Reports 3.0.0 /
1.1.0); each entry has a **Status** line with that result. In this repository
no entry is re-tested yet; re-tests follow
[998-tool-bug-recheck.md](998-tool-bug-recheck.md).

| Tool | Kind | Version here | Findings made with | Used here | Section |
|---|---|---|---|---|---|
| ubCode (VS Code extension) + `ubc` CLI | commercial | 0.37.0 (`UBC_VERSION` in `.github/workflows/ci-main.yml` / `ci-release.yml`; extension 0.37.0) | 0.35.0; re-tested 0.37.0 (origin) | yes | §3 |
| Pharaoh (agentic engineering, `ubc agent`, `.pharaoh/`) | commercial | in ubc 0.37.0, profile `vmodel` 21 (`docs/.pharaoh/agent/install-manifest`) | 0.35.0; re-tested 0.37.0 (origin) | yes (`[workflow]`, `[quality]`, runner; plan 001) | §4 |
| Sphinx-Needs | open source | **unpinned** `>=9.0` (script `sphinx` in `docs/ubproject.toml`; derived fields need 9.0); resolved 9.0.0 | 8.5.0; re-tested 9.0.0 (origin); 9.0.0 (product_demo) | yes | §5 |
| Sphinx-Codelinks ("Codelinks") | open source | 2.0.0 (as resolved by `uv`) | 1.4.0; re-tested 2.0.0 (origin) | yes (`impl` markers, plan 001 P2) | §6 |
| sphinx-mounts (`github.com/useblocks/sphinx-mounts`) | open source | 0.3.0 (as resolved by `uv`) | 0.2.0; re-tested 0.3.0 (origin) | yes (`src/`, `tests/` docs, plan 001 P2) | §7 |
| useblocks/ubc-action | GitHub Action | — (CI downloads `ubc` directly) | `393f60b` | no | §8 |
| Sphinx-Data-Viewer | open source | as resolved by `uv` | 0.1.5 | indirectly (sphinx-needs dependency) | no findings |
| ubTrace, ubConnect | commercial | — | — | no | — |
| Sphinx-Test-Reports (`sphinx-test-reports` + `ub-test-reports`) | open source | 3.0.0 (as resolved by `uv`) | 2.0.0, 3.0.0 / 1.1.0 | yes (pytest JUnit, plan 001 P2; converter not used) | §9 |
| Sphinx-Modeling, Sphinx-Collections, Sphinx-Preview, Sphinx-SimplePDF, Sphinx-EMF, Bazel-Drives-Sphinx, libpdf | open source | — | — | no | — |

## 2. Overview

Severity: **high** = wrong result without notice or blocks a use case;
**medium** = wrong or inconsistent, workaround exists; **low** = cosmetic,
documentation, convenience.

| ID | Tool | Severity | Origin | Here | Summary |
|---|---|---|---|---|---|
| UB-01 | ubc | medium | external | applies (`ubc build needs`: no `docname` on any need since plan 001 P2; codelinks `local-url` avoided with `set_local_url = false`) | export has no `docname`, but absolute local paths (`__source__`, codelinks `local-url`) |
| UB-02 | ubc | high | external | n/a (no external needs) | one `null` in a declared non-nullable field drops the whole external-needs source |
| UB-03 | ubc | medium | external | latent (variant keys) | Python keyword in a `var.*` key accepted; Sphinx cannot evaluate it |
| UB-04 | ubc | medium | external | latent (uses `[needs] variant_data_file`; `[variants]` works since 0.37.0) | `[variants] data_file` is silently ignored — **fixed in 0.37.0** (with Sphinx-Needs 9.0.0) |
| UB-05 | ubc | medium | external | applies (confirmed 2026-10-17, plan 001 P1: `ubc check -c 'needs.fields.status.schema = …'` made `platform_note` unknown) | `-c` override of a nested table replaces the whole table |
| UB-06 | ubc | low | external | latent (parity check) | empty link lists omitted from `needs.json` (Sphinx writes `[]`) |
| UB-07 | ubc | medium | external | n/a | backlinks on external needs not filled (`allocated_from`) — HTML not reproducible on 0.37.0; JSON part = UB-15 |
| UB-08 | ubc | low | external | n/a | `needs.builder_filter` ignored |
| UB-09 | ubc | medium | external | latent (`:variant:` role) | `:variant:` role text stays unresolved in the exported `content` |
| UB-10 | ubc | low | external | n/a (no `variant_sources`) | info `variant_sources_sphinx_unsupported` is outdated / misleading |
| UB-12 | ubc + Sphinx-Needs | medium | external | latent (named variants, `if`) | `if` does not resolve named variants (`[needs.variants]`) |
| UB-13 | ubc + Sphinx-Needs | medium | external | n/a | imported needs of an undeclared type dropped, undeclared fields stripped, silently — not reproducible on 0.37.0 / 9.0.0 (diagnostics exist) |
| UB-14 | ubc | medium | external | applies (plan 001 P2: `code/implementations` shows the GitHub `remote-url` as plain text; local path avoided with `set_local_url = false`) | ubCode HTML: source links as plain text, absolute local path published |
| UB-15 | ubc | low | external | applies (plan 001 P5 / P6: ubc `needs.json` has no `decides_back`, Sphinx does; parity checks compare forward links only) | `ubc build needs` exports no backlinks (`<link>_back`); Sphinx does |
| UB-16 | ubc | medium | external | n/a | external source dropped when its `needs_schema` has `default: null` for a field declared non-nullable |
| UB-17 | ubc + Sphinx-Needs | low | external | n/a | `needimport` ignored `id_regex` in ubc only — **resolved** with Sphinx-Needs 9.0.0 (neither checks imports) |
| UB-18 | ubc | high | external | n/a | Sphinx-Test-Reports directives unknown — **fixed in 0.37.0** |
| UB-19 | ubc + Sphinx-Needs | low | external | applies (`id_regex` since plan 001 P1) | local need with an id outside `id_regex`: ubc warns and keeps it, Sphinx drops it |
| UB-20 | ubc | low | product_demo | applies (`docs/schemas.json`) | schema: a missing required link is reported twice (local `required` + network `local_fail`); Sphinx reports it once |
| UB-21 | ubc + Sphinx-Needs | medium | product_demo | applies (`docs/schemas.json`) | schema keyword outside the supported subset (e.g. `not`): ubc warns and applies **no** rule of the file; Sphinx aborts the build |
| UB-22 | ubc + Sphinx-Test-Reports | medium | product_demo | applies (`tests/test_results.rst`, `[test_reports] rootdir`) | `test-file` `:file:` resolved against `rootdir` for reading but against `confdir` for the mount check; a file inside `rootdir = ".."` is "outside the root" |
| UB-23 | ubc | low | product_demo | applies (found in plan 001 P2) | unknown keys in `[parse.parsers.*]` are accepted without a warning |
| UB-24 | ubc + Sphinx-Needs | medium | product_demo | latent (conditional links used on risks with the full 64-hex `fp`; bracketed conditions avoided) | link condition with an inner `[`: single brackets `ID[fp[:12]=="…"]` drop the condition silently in both tools; double brackets `ID[[fp[:12]=="…"]]` are `link_condition_invalid` in ubc but valid (and checked) in Sphinx |
| UB-25 | ubc + Sphinx-Needs | medium | product_demo | applies (plan 001 P6: `dec-nested` uses the derived field `parent` instead) | schema rules cannot see the core field `parent_need` in ubc: `required: ["parent_need"]` fails for every nested need (Sphinx: only for non-nested ones) |
| UB-26 | ubc (docs / schema) | low | product_demo | applies (`[[source.mounts]]`, plan 001 P2) | the `ubproject.schema.json` description of `[[source.mounts]]` says `ubc check` does not read mounts — it does (diagnostics point into mounted files) |
| PH-01 | Pharaoh | **high** | external | latent (`[workflow]` since plan 001 P3; no variant alternatives sharing one id) | verdicts stored per need id only: alternatives with one id overwrite each other |
| PH-02 | Pharaoh | **high** | external | applies (plan 001 P8: `REQ_AUTH` reviewed while `platform_note` resolves per variant) | review fingerprint ignores resolved field values and link variants |
| PH-03 | Pharaoh | medium | external | applies — relied on (plan 001 P5 / P8: decisions flip via `outgoing` trace edges; parent edits re-review direct children only) | fingerprint follows parents one level only (children / decisions flip, grandchildren not) |
| PH-04 | Pharaoh | medium | external | avoided by design (plan 001: one link name per edge) | backward trace of two stages with the same link + target is attributed to one stage |
| PH-05 | Pharaoh | medium | external | avoided by design (plan 001: one link name per edge; decisions stage edges are `outgoing`) | workflow traces apply per need type; no per-stage filter |
| PH-06 | Pharaoh | medium | external | n/a (no imports) | `agent status` / `next` count imported (`exempt_status`) needs as stage output |
| PH-07 | Pharaoh | low | external | n/a (no imports) | `review-brief` lists imported (`exempt_status`) needs as review targets |
| PH-08 | Pharaoh | low | external | latent (`ubc agent audit` used by the skills; missing fields not observed yet) | `agent audit` omits `value`, `tags` and `refines` / `allocates` in `trace` |
| PH-09 | Pharaoh | low | external | applies (plan 001 P4: 8 own skills; drift not detected) | `doctor` checks only the `.claude` copy of project skills |
| PH-10 | Pharaoh | low | external | applies (installed `review-feat` / `-requirement` / `-decision` and the own copies `review-spec` / `-test-spec` / `-risk`) | brief / skills: `submit_command` without `-p`, `stale` bucket undocumented |
| PH-11 | Pharaoh | low | external | applies (installed `review-*` and their own copies document `--ids <ID,...>`) | skills document `review-brief --ids <ID,...>`, the CLI rejects the comma list; TYPE + `--ids` is refused |
| PH-12 | Pharaoh | medium | external | applies (plan 001 P3: stage `produces = "testcase"` → `undeclared_type`; no `test_results` stage, schema rules instead) | `config-validate` / `doctor`: a type declared by `[test_reports]` counts as undeclared |
| PH-13 | Pharaoh | medium | external | n/a | outgoing trace obligation (`min = 1`) met by any link, e.g. STR's generic `links` |
| PH-14 | Pharaoh | medium | product_demo | applies (plan 001 P3: `[workflow.lifecycle]` left out) | `[workflow.lifecycle] states` gate applies to every need: needs of types without a lifecycle (no `status`) are all `status_undeclared`; no per-type scope |
| PH-15 | Pharaoh | medium | product_demo | applies (all stages) | author prompt orders `:status: draft` (no lifecycle) or the first lifecycle state for every type, and declares it authoritative over the skill |
| PH-16 | Pharaoh | medium | product_demo | applies (decisions / risks stages) | cross-cutting stage (global scope): prompt demands one element linking **all** needs of the `up` type; routes cannot point into a need, so nested decisions cannot be routed |
| PH-17 | Pharaoh | low | product_demo | applies (single-file routes) | author prompt says "CREATE THE FILE at `<path>`" for an existing single-file route (e.g. `requirements.rst`); a headless runner may overwrite it |
| PH-18 | Pharaoh | medium | product_demo | applies (plan 001 P4 follow-up: 11 skills removed, 2 replaced) | no way to opt out of preset assets: `ubc agent update` re-adds removed skills to the manifest and restores them on the next run; a replaced skill is a conflict on every run (`ok: false`); `doctor` errors on an edited installed skill |
| PH-19 | Pharaoh | medium | product_demo | workaround found (plan 001 P5: `outgoing` trace edges on the decisions / risks stages) | verdict fingerprints ignore cross-cutting links: a `dec` / `risk` stays fresh when what it decides / affects / is mitigated by changes; `impact` does not reach nested decisions; a parent's fingerprint includes its nested decisions' text |
| PH-20 | Pharaoh | medium | product_demo | applies (plan 001 P7: CI 1 uses `scripts/ci_gates.py` instead) | `release-check` baseline unusable for a two-tier CI: help says "a JSON gap-key list", the tool wants a map of an undocumented key to a count; `--update-baseline` only writes on a passing run; missing reviews and open / proposed statuses count as gaps, no category filter |
| PH-21 | Pharaoh | **high** | product_demo | applies (fixed in `[agent.runner]`, plan 001 P8) | `ubc agent run`: a runner that is not allowed to run `ubc` asks for approval, nobody answers headless, and every stage is reported `no change` with `ok: true` |
| PH-22 | Pharaoh | medium | product_demo | applies (plan 001 P8 cascade) | `change-request` cascade: the code stage reports `no change` although `src/` was changed; decisions nested in the edited anchor (and risks) are not part of the cascade |
| SN-01 | Sphinx-Needs | medium | external | applies (plan 001 P3: `info` suppressed via `suppress_warnings`, violations are errors on purpose, CI 2 reads `schema_violations.json`) | every schema severity is a Sphinx warning; `-W` fails on `warning` rules |
| SN-02 | Sphinx-Needs | medium | external | n/a | `needs_from_toml` overrides `needs_external_needs` from `conf.py` |
| SN-03 | Sphinx-Needs | low | external | n/a | `needs.json` drops external needs by default (`builder_filter`), unlike ubc |
| SN-04 | — | — | — | — | moved to CL-06 |
| SN-05 | Sphinx-Needs | low | external | not triggered (plan 001: `network_back` `contains` on link fields works in both toolchains) | schema `contains` on a list field rejected without `items` (ubc accepts) |
| SN-06 | Sphinx-Needs | medium | external | n/a | `id_prefix` rewrites ids inside the text of imported needs (plain `str.replace`): literals changed (in this repo), ids corrupted (`BMS_SWBMS_…`, synthetic) — **changed** in 9.0.0: corruption fixed, literals still prefixed |
| SN-07 | ubc + Sphinx-Needs | low | external | n/a | imported needs: `style` kept by ubc, dropped by Sphinx-Needs (intent undocumented) |
| SN-08 | Sphinx-Needs | low | product_demo | applies (`docs/schemas.json`) | schema network failure: console line names the link **target** (`Need 'SPEC_HASH' has schema violations`), `schema_violations.json` names the source |
| SN-09 | Sphinx-Needs | medium | product_demo | applies (fixed here with `flow_engine = "graphviz"`, plan 001 P6) | `needflow` with the default PlantUML engine but no PlantUML: the page shows "PlantUML is not available!", no warning — `sphinx-build -W` passes |
| CL-01 | Sphinx-Codelinks | medium | external | n/a | fails in a git worktree (`.git` must be a directory) — **fixed in 2.0.0** |
| CL-02 | Sphinx-Codelinks | medium | external | n/a | `.c` file without compile-database entry silently skipped |
| CL-03 | Sphinx-Codelinks + ubc | low | external | n/a (`set_local_url = false`; `remote-url` identical in both exports, plan 001 P2) | `remote-url` / `local-url` mean different things in the two exports (path vs URL, local path) — **changed** in 2.0.0: `remote-url` same, `local-url` differs |
| CL-04 | Sphinx-Codelinks | low | external | n/a (`set_local_url = false`: no source pages, no Codelinks CSS, plan 001 P9) | source pages reference `_static/_static/…` (CSS 404): wrong `add_css_file` path |
| CL-05 | Sphinx-Codelinks | medium | external | n/a | branch ref only in `packed-refs` (after `git gc`): source links to `blob/None`, warnings — **fixed in 2.0.0** |
| CL-06 | Sphinx-Codelinks | medium | external | n/a | duplicate need id in code aborts the build (uncaught `InvalidNeedException`) — **fixed in 2.0.0** |
| CL-07 | Sphinx-Codelinks | low | external | n/a (origin is `github.com`; no warning, plan 001 P2) | `Unsupported Git host` warning for every marker when `origin` is not a known host, although `remote_url_pattern` is set |
| SM-01 | sphinx-mounts + ubc | medium | external | n/a | bare boolean condition: sphinx-mounts aborts the build, ubc warns and drops the rule — **changed** in 0.3.0: same message, severity differs |
| UA-01 | ubc-action | low | external | n/a | Linux runners only |
| UA-02 | ubc-action | medium | external | n/a (the direct download in CI has no checksum either, see §8) | uses `actions/cache@v4` by tag: blocked in repositories that require SHA-pinned actions; downloads into the workspace, no checksum |
| STR-01 | Sphinx-Test-Reports | medium | external | n/a | CTest `status="disabled"` reported as `passed` |
| STR-02 | Sphinx-Test-Reports | medium | external | n/a | converter ignores the configured case prefix; lower-case hash IDs fail a strict `id_regex` |
| STR-03 | Sphinx-Test-Reports | high | external | avoided by design (plan 001: test-result types not in `[[needs.types]]`) | type declared in `[[needs.types]]` and `[test_reports.case]` aborts the Sphinx build |
| STR-04 | Sphinx-Test-Reports + ubc | low | external | n/a | `test-results` summary `Errors: -1` in Sphinx, `0` in ubc, when the JUnit file has no `errors` attribute |
| STR-05 | Sphinx-Test-Reports + ubc | low | external | n/a | renamed case directive (`[test_reports.case] directive`): ubc ignores the rename, Sphinx accepts it |
| STR-06 | Sphinx-Test-Reports (docs) | low | product_demo | applies (`docs/schemas.json` `type-test-case`) | docs name the need types `test-file` / `test-suite` / `test-case`; both toolchains create `testfile` / `testsuite` / `testcase` — a schema `select` on `test-case` matches nothing, silently |
| STR-07 | Sphinx-Test-Reports | medium | product_demo | applies (worked around with `sphinx-build -E`) | the JUnit file of a `test-file` is not a build dependency: an incremental Sphinx build keeps the old test results (new cases missing) |

## 3. ubc / ubCode

### UB-01 Export without `docname`, with absolute local paths

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`ubc build needs --source-maps`)
- **Marker:** `main@e744d72` `tools/pin_bms.py:54-61` (workaround); input
  from `rollout-demo-bms@38c9f30` (`docs/`).
- **Marker here:** `main@318328f` `docs/ubproject.toml:19` (`ubc script needs` → `docs/needs.json`, by this entry with absolute `__source__.path`; the file is not committed, `needs*.json` is in `.gitignore`). Not verified yet here.
- **Summary:** the needs export has no `docname`; instead every need carries a
  `__source__` block and codelinks needs a `local-url`, both with absolute
  paths of the exporting machine.
- **Input:** `cd rollout-demo-bms/docs && ubc build needs --source-maps -o nmc.json`;
  also **without** `--source-maps`: `ubc build needs -o build/x.json` in this repo
  (`main@1cb05e9`, any product) writes `__source__.path` with the absolute path
  for every local need (checked 2026-10-10, plan 6 site assembly).
- **Wrong output:**
  ```json
  "REQ_CELL_VOLTAGE_LIMITS": { "__source__": {"path": "/Users/<user>/…/docs/specs/cell-protection/requirements.rst", …} }
  "IMPL_CHARGE_INTEGRATION": { "local-url": "file:///Users/<user>/…/src/state_estimation/coulomb_counter.py#L30" }
  ```
  Expected: `"docname": "specs/cell-protection/requirements"` (as sphinx-needs
  writes it); no local paths in an artifact meant to be shared. Consumers using
  `needs_external_needs` link to `__error__.html` without `docname`.
- **Workaround:** `tools/pin_bms.py` derives `docname`, drops `__source__`, clears `local-url`.
- **Solution A:** write `docname` (and relative `lineno`) like sphinx-needs; keep
  `__source__` only with an explicit `--source-maps`, with paths relative to the project root.
- **Solution B:** an export option `--portable` (default for `ubc build needs`)
  that strips machine-specific fields and makes paths relative.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `ubc build needs` with and without `--source-maps` still writes no `docname` and absolute `__source__.path` / `local-url` (rollout-demo-bms@38c9f30; on `main@36f44a4` all 269 needs); no portable option in `--help`.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 001 P2, product_demo): `ubc build needs` in `docs/` exports 14 needs, none with `docname`; Sphinx `needs.json` has it (e.g. `code/implementations`). No absolute paths here because `set_local_url = false`.

### UB-02 One `null` value drops the whole external-needs source

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `main@e744d72` `ubproject.toml:312` (`[needs.fields.code_url]`,
  workaround) with `third_party/bms/0.1.0/nmc.needs.json`.
- **Summary:** a declared field with `nullable = false` and an imported need
  whose value is `null` makes ubc reject **all** needs of the source.
- **Input:**
  ```toml
  [needs.fields.code_url]
  default = ""
  nullable = false
  ```
  plus `[[needs.external_needs]] json_path = "build/active/bms.needs.json"` (205 needs, `needs_schema` with `code_url.default = null`).
- **Wrong output:**
  `warning[needs.external] root['versions']['0.1.0']['needs_schema']['properties']['code_url']['default'] could not be read: Value cannot be converted to string: null; the source contributed no needs` → 0 of 205 needs.
  Expected: per-need diagnostic, value replaced by the default (or the one need skipped); the other needs imported.
- **Workaround:** `code_url` declared without `nullable = false`.
- **Solution A:** coerce `null` to the field default for external needs and report one `info` per field.
- **Solution B:** validate per need: skip / report only the offending need, never the whole source.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `nullable = false` on `code_url` (`main@36f44a4`) gives the same `needs.external … could not be read: … null; the source contributed no needs`; 64 needs, 0 BMS.

### UB-03 Python keyword in a `var.*` key accepted

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (vs Sphinx-Needs 8.5.0)
- **Marker:** `main@0c27fc5` `Kconfig:50` (`choice HV__CLASS` → `var.hv.class`, renamed in
  `07806d7`); use `var.hv.class` in any field variant, e.g. in
  `content/cv-platform@25b77bd` `docs/vehicle/requirements.rst:65`.
- **Summary:** ubc evaluates `var.hv.class`; sphinx-needs evaluates conditions as
  Python, where `class` is a keyword → syntax error. The two tools disagree silently.
- **Input:** `:value: <<[var.hv.class == "v800"]: 800, 400>>` with `{"hv": {"class": "v800"}}`
- **Wrong output:** ubc: `800` (no warning). Sphinx: `WARNING: Error while resolving dynamic values for field 'value' … invalid syntax [needs.dynamic_function]`.
  Expected: the same result in both, or the same diagnostic.
- **Workaround:** symbol renamed (`HV__VOLTAGE`, fix `07806d7`); the generator rejects keywords.
- **Solution A:** ubc warns on Python keywords (and other non-identifiers) in `var.*` paths, matching the Sphinx grammar.
- **Solution B:** both tools accept item access (`var.hv["class"]`) and document it as the escape for such keys.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `var.hv.class` on `main@36f44a4` resolves in ubc (`800`) without a diagnostic; Sphinx `invalid syntax … [needs.dynamic_function]`, value empty.

### UB-04 `[variants] data_file` silently ignored

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (also the ubCode extension and Sphinx-Needs)
- **Marker:** `main@e744d72` `ubproject.toml:37` — replace `[needs] variant_data_file` by the `[variants]` form below.
- **Summary:** a `[variants]` table with `data_file` (seen in docs/examples) is
  read by none of the tools; all `if` / `:variant:` / `variant_sources` rules lose their data without a config error.
- **Input:**
  ```toml
  [variants]
  data_file = "build/active/variants.json"
  ```
- **Wrong output:** no config diagnostic; `'variant' role used but no variant data is available: 'meta.product'`; `if` blocks evaluate as unknown.
  Expected: either the key works, or `unknown key [variants]` / "use `[needs] variant_data_file`".
- **Workaround:** `[needs] variant_data_file` only.
- **Solution A:** report unknown top-level / table keys of `ubproject.toml` against the published schema.
- **Solution B:** accept `[variants] data_file` as an alias of `[needs] variant_data_file` in all three tools.
- **Status:** **fixed in ubc 0.37.0 / Sphinx-Needs 9.0.0** (2026-10-17, plan 998 run 1): `[variants] data_file` replacing `[needs] variant_data_file` on `main@36f44a4` gives exports identical to the baseline in both tools (ubc 0.35.0 / 0.36.0 still ignore it). Unknown `[variants]` keys are now reported by both (`variants.datafile` / `needs.variants_unknown_key`); Sphinx-Needs 9.0.0 calls the `[needs]` keys the legacy location and warns `variant_data_location` if both are set. The workaround is removed on `fix/tool-workarounds`: `ubproject.toml` uses `[variants] data_file`.

### UB-05 `-c` override replaces the whole nested table

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `main@e744d72` `ubproject.toml:326` (`[codelinks.projects.vcu]`).
- **Marker here:** `main@318328f` `README.md:44` — `ubc build needs -c 'needs.variant_data.platform = "windows"'`; by this entry (origin Status: the whole parent table is replaced) it may drop `edition = "pro"` of `[needs.variant_data]` (`docs/ubproject.toml:66-67`). Not verified yet here.
- **Summary:** overriding one nested key with `-c` replaces the complete table,
  so all sibling keys of the project disappear.
- **Input:** `ubc check -c "codelinks.projects.vcu.analyse.preprocessor.compile_commands = 'build/cmake/truck_diesel_eu/compile_commands.json'"`
- **Wrong output:** the `vcu` project loses `source_discover`, `oneline_comment_style`, … → no code needs.
  Expected: deep merge — only `compile_commands` changes.
- **Workaround:** gates run after configuring the product (active copies), no `-c` for codelinks.
- **Solution A:** deep-merge dotted-key overrides into the loaded config.
- **Solution B:** a separate `--set key=value` (merge) next to `-c <toml>` (replace), clearly documented.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `-c "codelinks.projects.vcu.analyse.preprocessor.compile_commands = '…'"` on `main@36f44a4` replaces the whole `codelinks.projects` table, not only `vcu`: `Unknown codelinks project: "chg"` (also `chg_tests`, `vcu_tests`), 255 needs, `IMPL_VCU_*` gone.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 001 P1, product_demo): `ubc check -c 'needs.fields.status.schema = { type = "string", enum = [...] }'` in `docs/` → `Unknown need directive option "platform_note"`: the override replaced the whole `[needs.fields]` table.
- **Status (2):** also for `[workflow]` (plan 001 P3): `ubc agent prompt --stage risks -c 'workflow.lifecycle.states = [...]'` → "no stage with that id is declared": the override replaced the whole `[workflow]` table.

### UB-06 Empty link lists omitted from `needs.json`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (vs Sphinx-Needs 8.5.0)
- **Marker:** `content/cv-platform@25b77bd` `docs/subsystems/vcu/architecture.rst:21` (`ARCH_VCU_POWER_MGMT`), product `truck_diesel_eu`.
- **Summary:** a link field without targets (also after a link variant resolved to nothing) is missing in ubc's export; Sphinx writes `[]`.
- **Input:** `:allocates: <<bev: BMS_REQ_POWER_DERATING>>` in a diesel product.
- **Wrong output:** ubc: key `allocates` absent; Sphinx: `"allocates": []`. Same for `refines: []` etc.
- **Workaround:** comparisons treat absent = `[]` (`tools/eval_expect.py`).
- **Solution A:** ubc writes every declared link with `[]` (as Sphinx).
- **Solution B:** both tools honour one `needs_json_remove_defaults`-style switch and document the format.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `truck_diesel_eu` on `main@36f44a4`: `ARCH_VCU_POWER_MGMT.allocates` absent in ubc, `[]` in Sphinx; 447 empty list fields differ. Same class: 77 imported BMS needs without `content` (52 test, 25 impl) have no `content` key in ubc, `""` in Sphinx.

### UB-07 Backlinks on external needs not filled

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (Sphinx-Needs fills them)
- **Marker:** `content/cv-platform@25b77bd` `docs/subsystems/bms/integration.rst` (column `allocated_from`), any BEV product.
- **Summary:** CV needs `allocates` imported `BMS_REQ_*` needs; Sphinx shows the incoming `allocated_from` on the external need, ubc leaves it empty.
- **Input:** `BB_POWER_LIMITS` with `:allocates: BMS_REQ_POWER_DERATING`; needtable column `allocated_from`.
- **Wrong output:** ubCode HTML / ubc `needs.json`: `BMS_REQ_POWER_DERATING.allocated_from` empty. Sphinx: `['BB_POWER_LIMITS', 'ARCH_VCU_POWER_MGMT']`.
- **Workaround:** the BMS usage report relies on the Sphinx output.
- **Solution A:** compute backlinks for external needs like for local ones.
- **Solution B:** if intentional, document it and offer a filter (`allocated_from` via a query function) usable in needtables.
- **Status:** not reproducible (HTML part) on ubc 0.37.0 and 0.35.0 (2026-10-17, plan 998 run 1): `ubc build html` `subsystems/bms/integration.html` shows `allocated_from` of `BMS_REQ_POWER_DERATING` (`ARCH_VCU_POWER_MGMT ; BB_POWER_LIMITS`) at `25b77bd` and `main@36f44a4`, as Sphinx. The input is in doubt. Still open: ubc's `needs.json` has no back key for it (Sphinx `allocates_back`) — that is UB-15.

### UB-08 `needs.builder_filter` ignored

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `main@e744d72` `ubproject.toml` (`builder_filter = ""` in `[needs]`).
- **Summary:** ubc always exports all needs including external ones; the sphinx-needs option `builder_filter` has no effect.
- **Input:** `ubc build needs -c 'needs.builder_filter = "is_external==False"'`
- **Wrong output:** 205 needs (all external) exported. Expected: 0 (as Sphinx).
- **Workaround:** `builder_filter = ""` so that Sphinx matches ubc (SN-03).
- **Solution A:** honour `builder_filter` in `ubc build needs`.
- **Solution B:** report it as unsupported (`info`) so the difference is visible.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `-c 'needs.builder_filter = "is_external==False"'` and removing `builder_filter = ""` both export 269 needs, 205 BMS, no diagnostic.

### UB-09 `:variant:` role text unresolved in the exported `content`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`ubc build needs`, also `agent audit` bodies)
- **Marker:** `main@e744d72` `third_party/bms/0.1.0/nmc.needs.json` (`REQ_CELL_VOLTAGE_LIMITS.content`).
- **Summary:** text using the `:variant:` role is exported raw; only fields are resolved. A consumer of the export cannot see the per-variant values.
- **Input:** BMS `REQ_CELL_VOLTAGE_LIMITS`: ``… below :variant:`pack.cell_v_min` …`` exported for `variants/nmc.json`.
- **Wrong output:** `"content": "… below :variant:`pack.cell_v_min` …"`. Expected: the value of `pack.cell_v_min` from `variants/nmc.json` (resolved for the exported variant), or a separate resolved field.
- **Workaround:** none; values must be exposed as fields by the producing project.
- **Solution A:** resolve roles in `content` when exporting a concrete variant (option `--resolve-variants`).
- **Solution B:** export `content` raw plus `content_resolved`.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `REQ_CELL_VOLTAGE_LIMITS.content` still contains `:variant:\`pack.cell_v_min\``; no option to resolve it.

### UB-10 Outdated info `variant_sources_sphinx_unsupported`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `main@e744d72`, any `ubc check`.
- **Summary:** every check prints that Sphinx does not honour `variant_sources` and that `sphinx-build -W` should not be run — sphinx-mounts 0.2.0 does honour them, and `-W` passes.
- **Input:** `[[source.variant_sources]]` rules, `sources_from_toml` in `conf.py`.
- **Wrong output:** `info[config.variant_sources_sphinx_unsupported] … do not run sphinx-build -W on this project`.
- **Workaround:** ignored.
- **Solution A:** detect `sphinx_mounts` (version) in `conf.py` and drop the info.
- **Solution B:** word it as "requires sphinx-mounts ≥ 0.2.0" and show it once (`ubc check --explain`), not on every run.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): every `ubc check` on `main@36f44a4` prints the same `info[config.variant_sources_sphinx_unsupported] … do not run sphinx-build -W`, although sphinx-mounts 0.3.0 and `-W` pass.

### UB-12 `if` does not resolve named variants

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 and Sphinx-Needs 8.5.0
- **Marker:** `content/cv-platform@25b77bd` `ubproject.toml` (`[needs.variants]` with `mcs`), `docs/vehicle/requirements.rst` (`.. if::` blocks).
- **Summary:** named variants work in `<<mcs: a, b>>` but not in `.. if:: mcs`; the same name means two things.
- **Input:** `[needs.variants] mcs = "var.charging.mcs == True"` and `.. if:: mcs`
- **Wrong output:** `warning[if.invalid_expression] 'if' directive expression could not be evaluated: 'mcs' — Unknown variant key: var.mcs`. Expected: the named condition.
- **Workaround:** spelled-out conditions in every `if`.
- **Solution A:** resolve bare names in `if` (and `variant_sources` / mount `if`) against `[needs.variants]` first.
- **Solution B:** explicit syntax, e.g. `.. if:: variant('mcs')`, in both tools.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `.. if:: mcs` (`docs/vehicle/requirements.rst:82`, `main@36f44a4`): ubc `if.invalid_expression … Unknown variant key: var.mcs`, Sphinx `name 'mcs' is not defined [needs.if]`; `REQ_MCS_CHARGING` missing in both.

### UB-13 Imported needs of undeclared types / fields silently lost

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 and Sphinx-Needs 8.5.0
- **Marker:** `main@e744d72` `ubproject.toml:132` — remove the `test_result` type.
- **Summary:** external needs whose type is not declared are dropped, undeclared fields stripped, without a diagnostic.
- **Input:** BMS export with 52 `test_result` needs; CV without `[[needs.types]] directive = "test_result"`.
- **Wrong output:** 153 of 205 needs; `chemistry` missing when undeclared; no warning. Expected: one warning per dropped type / stripped field.
- **Workaround:** the CV metamodel declares the full BMS vocabulary.
- **Solution A:** warn per external source with counts of dropped needs / stripped fields.
- **Solution B:** keep unknown types / fields read-only (as "external type") instead of dropping them.
- **Status:** not reproducible on ubc 0.37.0 / Sphinx-Needs 9.0.0, and also not on ubc 0.35.0 / Sphinx-Needs 8.5.0 (2026-10-17, plan 998 run 1): at `main@e744d72` and `main@36f44a4`, removing type `test_result` gives one diagnostic per need in both tools (ubc `needs.external Invalid need type: test_result`, Sphinx `[needs.load_external_need]`), removing field `chemistry` one per source (ubc `unknown keys … dropped`, Sphinx `[needs.unknown_external_keys]`). The needs are still lost, but not silently; the original input is in doubt. Workaround stays (the needs are wanted).

### UB-14 ubCode HTML: source links as plain text, with the local path

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`ubc build html`)
- **Marker:** `content/cv-platform@25b77bd`, `tools/build_product.sh truck_bev_nmc_eu`,
  page `build/site/truck_bev_nmc_eu/ubcode/subsystems/vcu/code_trace.html`. Checked 2026-10-09.
- **Summary:** the code needs' `remote-url` and `local-url` are rendered as plain
  table text, not as links; the `local-url` is the absolute `file://` path of the
  build machine and ends up in the published HTML (on GitHub Pages it would show
  the CI runner's path). Sphinx renders both as links (GitHub with commit, and
  a generated source page).
- **Input:** code needs from `src/vcu/energy_display.c` with `set_local_url` / `set_remote_url`.
- **Wrong output:**
  ```html
  <td>file:///Users/<user>/…/variant_demo/src/vcu/energy_display.c#L8
  <td>https://github.com/PhilipPartsch/variant_demo/blob/b0a203be10f1…/src/vcu/energy_display.c#L8
  ```
  Expected: clickable links; no local machine path in published pages (a link
  to a generated source page, or to the remote URL only).
- **Workaround:** none yet; to be handled before publishing (plan 6, e.g. `set_local_url = false` for the CI build).
- **Solution A:** render URL fields (`remote-url`, `local-url`, fields with `needs_string_links`) as links, and map `local-url` to a generated source page as Sphinx does.
- **Solution B:** an option for `ubc build html` to drop / rewrite machine-specific fields (`local-url`) for published builds.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `ubcode/subsystems/vcu/code_trace.html` (`main@36f44a4`) shows `local-url` (`file:///…`) and `remote-url` as plain text in `<td>`; also in `chg`.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 001 P2, product_demo): `docs/_build/html/code/implementations.html` shows `https://github.com/PhilipPartsch/product_demo/blob/…` as text (0 `href`s), Sphinx renders 2 links.

### UB-15 `ubc build needs` exports no backlinks

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (Sphinx-Needs 8.5.0 for comparison)
- **Marker:** `main@1a480bf`, any product, e.g. `truck_bev_nmc_eu`: need `REQ_MAX_CHARGE_POWER`. Found in plan 7 phase 1 (`model/system`).
- **Summary:** the Sphinx `needs.json` carries every incoming link as `<link>_back` (`satisfies_back`, `part_of_back`, `covers_back`, …); the ubc export carries none, although ubc knows them (tables with an incoming-link column, e.g. `has_part`, `covered_by`, `allocated_from`, render the same in both HTML outputs).
- **Input:** `tools/build_product.sh truck_bev_nmc_eu`, then compare `REQ_MAX_CHARGE_POWER` in `build/site/truck_bev_nmc_eu/{ubc,sphinx}.needs.json`.
- **Wrong output:** ubc: no `*_back` key. Sphinx: `"satisfies_back": ["ARCH_CHG_INLET", "BB_CHARGE_LIMITS"]`. Expected: the same backlinks in both exports (or the configured `incoming` names).
- **Workaround:** the tests compute backlinks from the outgoing links (`tools/tests/system_model.py`, `has_part` from `part_of`); the parity check compares ids only.
- **Solution A:** export backlinks like Sphinx-Needs (`<link>_back`).
- **Solution B:** an option of `ubc build needs` to include backlinks, documented as a known difference otherwise.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `REQ_MAX_CHARGE_POWER` (`main@36f44a4`, truck_bev_nmc_eu): no `*_back` keys in ubc; Sphinx `satisfies_back`, `covers_back`.

### UB-16 External source dropped: `needs_schema` `default: null` vs non-nullable field

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0, still in 0.37.0 (Sphinx-Needs 8.5.0 / 9.0.0 for comparison)
- **Marker:** scratch copy based on `main@54e862c` (plan 110 E9): input is the
  `test-reports build needs` output of a `build/site/<p>/junit.xml`
  (`tools/build_product.sh:32`), fields declared like `ubproject.toml:267-287`.
- **Summary:** the converter writes a `needs_schema` block with `"default": null`
  for its fields. When those fields are declared in `[needs.fields]` with
  `default = ""` / `nullable = false` (the style of this repository), ubc drops
  the whole external source. The needs themselves contain no `null`. Related to
  UB-02, but triggered by the schema block alone.
- **Input:** `[[needs.external_needs]] json_path = "active/tr.json"`, fields
  `case`, `result`, `time`, … declared with `default = ""`, `nullable = false`.
- **Wrong output:** `warning[needs.external] root['versions']['1.0']['needs_schema']['properties']['case']['default'] could not be read: Value cannot be converted to string: null; the source contributed no needs` (one per field); 0 of 3 needs. Sphinx imports all 3.
- **Workaround:** declare the imported fields with `nullable = true` and no
  default (both tools import everything, ubc warning-free), or strip `needs_schema`.
- **Solution A:** read `default: null` as "no default"; the declared field wins.
- **Solution B:** on a schema mismatch keep the needs, ignore the block, and warn once.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 with sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 (2026-10-17, plan 998 run 1): converter output as external source with 13 fields `nullable = false`: 13 × `needs.external … default could not be read: … null; the source contributed no needs`, 0 needs in ubc, 3 in Sphinx. Workaround still works.

### UB-17 `needimport`: `id_regex` checked by Sphinx only (resolved)

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 with Sphinx-Needs 8.5.0. **Resolved** on 2026-10-14 by
  Sphinx-Needs 9.0.0, which skips `id_regex` for imported and external needs by
  design (`sphinx_needs/api/need.py`, `from_outside`); ubc 0.37.0 behaves the same.
- **Marker:** scratch copy based on `main@9546209` / `main@54e862c` (plan 110 E8).
- **Summary:** with 0.35.0 / 8.5.0, ubc imported needs whose ids fail `id_regex`
  and Sphinx refused them, a silent parity break. Now both import them; no tool
  checks imported ids any more.
- **Input:** `.. needimport:: tr.json` with `:id_prefix: TRES_` (ids
  `TRES_test_result__…`), `id_regex = "^[A-Z]+_[A-Z][A-Z0-9_]*$"`.
- **Wrong output (old):** ubc 3 needs, "No errors found"; Sphinx 0 needs (`does not match configured regex`).
- **Workaround:** none needed now; a schema rule on the id can replace the regex if wanted.
- **Solution A:** (resolved.) If an id check for imports is wanted again: an opt-in option in both tools.
- **Solution B:** a schema rule on `id` that selects imported needs.
- **Re-check:** still resolved on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `needimport` with `:id_prefix: TRES_` and a strict `id_regex`: 6 needs in both tools.

### UB-18 Sphinx-Test-Reports directives unknown to ubc (fixed in 0.37.0)

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 / ubCode. **Fixed in 0.37.0** (checked 2026-10-14, plan 110 E7).
- **Marker:** scratch copy based on `main@9546209` (plan 110 E7).
- **Summary:** ubc did not know `test-file` / `test-suite` / `test-case`; no test
  needs in ubc, the IDE or the ubCode HTML. 0.37.0 reads `[test_reports]` and
  creates the same needs as Sphinx.
- **Input:** `.. test-file::` in an rst file.
- **Wrong output (old):** `warning[block.directive_unknown] Unknown directive: 'test-file'`.
- **Workaround:** keep `tools/import_test_results.py`.
- **Solution A:** ubc supports the STR directives (done in 0.37.0).
- **Solution B:** ubc runs the STR conversion for an external source that is a JUnit file.
- **Re-check:** still fixed on ubc 0.37.0 (2026-10-17, plan 998 run 1): `test-file` / `test-results` without `block.directive_unknown`; the same 8 needs in ubc and Sphinx.

### UB-19 Local need outside `id_regex`: ubc keeps it, Sphinx drops it

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.37.0, Sphinx-Needs 9.0.0
- **Marker:** scratch copy based on `main@54e862c` (plan 110, E8 control);
  `id_regex` as in `ubproject.toml:32`.
- **Summary:** both tools report the bad id, but ubc still creates the need and
  Sphinx does not, so the two `needs.json` differ by that need.
- **Input:** `.. test:: Bad id` with `:id: TEST_bad`, `id_regex = "^[A-Z]+_[A-Z][A-Z0-9_]*$"`.
- **Wrong output:** ubc `warning[needs.id_regex]`, 7 needs; Sphinx `WARNING: Need could not be created: Given ID 'TEST_bad' does not match configured regex` [needs.create_need], 6 needs.
- **Workaround:** none needed; the parity check and `-W` / `--deny warning` catch it.
- **Solution A:** ubc drops the need too, like Sphinx.
- **Solution B:** document the difference; same diagnostic in both.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `TEST_bad` on `main@36f44a4`: ubc `needs.id_regex` warning and 270 needs, Sphinx `[needs.create_need]` and 269 needs.

### UB-20 Missing required link reported twice

- **Origin:** product_demo
- **Tool:** ubc 0.37.0
- **Marker:** scratch copy of `docs/` on branch `feat/engineering-model` (plan 001 P1,
  uncommitted) with `docs/schemas.json` and an added `bad.rst` holding one
  broken need per rule.
- **Summary:** a rule with `local.required: ["satisfies"]` and a
  `network.satisfies.items` check reports a need without the link twice.
- **Input:** rule `link-req-us` (`docs/schemas.json`), `.. req::` without `:satisfies:`.
- **Wrong output:** `error[needs.schema_definition_violation] REQ_BAD_NOLINK:link-req-us: "satisfies" is a required property` **and** `error[needs.schema_network_violation] REQ_BAD_NOLINK:local_fail: "satisfies" is a required property`. Sphinx-Needs 9.0.0: one `local_fail` entry. Expected: one finding.
- **Workaround:** none needed (both block); counts of ubc and Sphinx findings differ by these duplicates in parity checks.
- **Solution A:** skip the network pass for a link field that failed `required`.
- **Solution B:** de-duplicate findings with the same need, rule and message.

### UB-21 Unsupported schema keyword disables the whole `schemas.json` in ubc

- **Origin:** product_demo
- **Tool:** ubc 0.37.0, Sphinx-Needs 9.0.0
- **Marker:** scratch copy of `docs/` on branch `feat/engineering-model` (plan 001 P1,
  uncommitted) with `docs/schemas.json` and an added `bad.rst` holding one
  broken need per rule.
- **Summary:** ubc supports only `allOf`, `properties`, `required`, `type`,
  `unevaluatedProperties` in `select` / `local`. Any other keyword (here
  `not`) makes ubc warn and apply no rule of the file at all; Sphinx-Needs
  aborts the build with `NeedsConfigException`. The keyword subset is not
  stated in the Sphinx-Needs schema docs.
- **Input:** `"items": { "local": { "not": { "$ref": "#/$defs/type-dec" } } }` in rule `link-dec`.
- **Wrong output:** ubc `warning[config.schema_unknown_key] … unknown key 'not' … no rule from this file is applied`; Sphinx `NeedsConfigException: Schemas entry 'link-dec[11]' is not valid`. Expected: the same reaction in both, and only the broken rule skipped (or both fail hard).
- **Workaround:** allow-lists instead of `not` (`$defs/type-decidable`); `ubc check --deny warning` in CI turns the warning into a failure.
- **Solution A:** ubc fails as hard as Sphinx (error, not warning).
- **Solution B:** both skip only the invalid rule and report it; the docs list the supported keyword subset.

### UB-22 `test-file` path: read against `rootdir`, mount-checked against `confdir`

- **Origin:** product_demo
- **Tool:** ubc 0.37.0, Sphinx-Test-Reports 3.0.0
- **Marker:** branch `feat/engineering-model` (plan 001 P2, uncommitted): `docs/ubproject.toml`
  `[test_reports]`, `tests/test_results.rst`.
- **Summary:** project `docs/` (confdir), JUnit file `tests/_results/junit.xml`
  at the repository root, `test-file` page mounted from `tests/`. ubc reads
  `:file:` relative to `[test_reports] rootdir`, but its mount check
  (`build.mount_path_escape`) resolves the same path relative to `docs/`; the
  Sphinx-Test-Reports docs say `:file:` is relative to the `conf.py` folder.
  So only paths that resolve to the same file under both bases work.
- **Input / output** (`ubc check` in `docs/`):
  - `rootdir = ".."`, `:file: ../tests/_results/junit.xml` → `needs.test_report_path_outside_root … it was not read` (the file **is** inside the repository root);
  - `rootdir = ".."`, `:file: tests/_results/junit.xml` → `test_report_missing` + `mount_path_escape` (`../docs/tests/_results/junit.xml`);
  - `rootdir = "../tests"`, `:file: ../tests/_results/junit.xml` → clean (both bases give `tests/_results/junit.xml`).
- **Expected:** one documented base for `:file:` (confdir, as the STR docs say) used by reading, the root check and the mount check alike.
- **Workaround:** `rootdir = "../tests"` with `:file: ../tests/_results/junit.xml`.
- **Solution A:** resolve `:file:` against confdir everywhere, check it lies under `rootdir`.
- **Solution B:** resolve against `rootdir` everywhere (also in the mount check) and document it in both tools.

### UB-23 Unknown keys in `[parse.parsers.*]` accepted silently

- **Origin:** product_demo
- **Tool:** ubc 0.37.0
- **Marker:** branch `feat/engineering-model` (plan 001 P2, uncommitted): `docs/ubproject.toml`
  `[test_reports]`, `tests/test_results.rst` — found when a script edit put `rootdir = "../tests"` under `[parse.parsers.md]` by mistake.
- **Input:** `ubc check -c 'parse.parsers.md.bogus_key = "x"'` in `docs/`.
- **Wrong output:** `No errors found.` Expected: `config.unknown_key` warning, as for other tables (e.g. `config.schema_unknown_key`).
- **Workaround:** review toml diffs; the misplaced key had no effect, which hid the mistake.
- **Solution A:** warn on unknown keys in parser tables.
- **Solution B:** `additionalProperties: false` for the parser tables in `ubproject.schema.json`, so the IDE flags them.

### UB-24 Link conditions with inner brackets: silently dropped / parity break

- **Origin:** product_demo
- **Tool:** ubc 0.37.0, Sphinx-Needs 9.0.0
- **Marker:** scratch copy of branch `feat/engineering-model` (plan 001 P5): field `fp` with `derive = { kind = "fingerprint" }`, `RISK_SCRYPT_PARAMS` `:mitigated_by: TSPEC_HASH[…]`.
- **Summary:** conditional links (Sphinx-Needs 8.0) take a filter string in
  brackets; a condition that itself contains `[` must use as many opening as
  closing brackets (`ID[[…]]`).
- **Input / output:**
  - `TSPEC_HASH[fp[:12]=="a84103146b3c"]` (single) → no warning in either tool, `needs.json` link `['TSPEC_HASH']`: the condition is gone, a later change of `TSPEC_HASH` is never reported. Expected: `link_condition_invalid`.
  - `TSPEC_HASH[[fp[:12]=="a84103146b3c"]]` (double) → ubc `warning[needs.link_condition_invalid]` (4×, also unchanged targets); Sphinx valid, and `link_condition_failed` after `TSPEC_HASH` changes. Expected: the same in both (ubc supports slicing, or both reject it).
- **Workaround:** compare the full value (`ID[fp=="<64 hex>"]`), which works in both.
- **Solution A:** reject unbalanced / unparsable conditions in both tools (`link_condition_invalid`).
- **Solution B:** ubc supports the Python subset Sphinx evaluates (slicing), or the docs list the supported filter grammar.

### UB-25 `parent_need` invisible to schema rules in ubc

- **Origin:** product_demo
- **Tool:** ubc 0.37.0, Sphinx-Needs 9.0.0
- **Marker:** scratch copy of branch `feat/engineering-model` (plan 001 P5): `DEC_HASH_ALGO` / `DEC_AUDIT_STORE` nested in `SPEC_HASH` / `SPEC_AUDIT`, `DEC_OUTSIDE` written outside any need.
- **Summary:** a rule "a decision is nested in a need" needs the core field
  `parent_need`. Sphinx-Needs validates it; ubc does not resolve it as a
  schema property and treats it as absent on every need.
- **Input:** `{"id": "dec-nested", "select": {"$ref": "#/$defs/type-dec"}, "validate": {"local": {"required": ["parent_need"], "properties": {"parent_need": {"minLength": 1}}}}}`.
- **Wrong output:** ubc `warning[needs.schema_config] … property 'parent_need' not found in field resolver, using schema-inferred type`, `… failed to parse schema for property 'parent_need'`, and `error[needs.schema_definition_violation] DEC_HASH_ALGO:dec-nested: "parent_need" is a required property` (also `DEC_AUDIT_STORE`, both nested). Sphinx: only `DEC_OUTSIDE` (`local_fail`, `"parent_need" is a required property`). `needs.json` of both tools carries `parent_need` (`DEC_HASH_ALGO` → `SPEC_HASH`).
- **Expected:** the core fields of `needs.json` (`parent_need`, `parent_needs`, …) usable in schema rules in both tools.
- **Workaround:** a derived copy, `[needs.fields.parent] schema.type = "string"`, `derive = { kind = "copy", field = "parent_need" }`, and the rule on `parent` — identical in both tools (`DEC_OUTSIDE` only).
- **Solution A:** ubc's field resolver knows the core fields `parent_need` / `parent_needs`.
- **Solution B:** document which core fields schema rules may reference; warn (not fail every need) when a rule names an unknown one.

### UB-26 Schema docs: "`ubc check` does not read mounts" — it does

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`ubproject.schema.json`)
- **Marker:** `docs/ubproject.toml` `[[source.mounts]]` (`../src` at `code/`, `../tests` at `tests/`), plan 001 P2.
- **Summary:** the schema description of `[source] mounts` says: "Mounts
  apply to the project build. `ubc check` and `ubc format` discover files by
  walking for the nearest configuration file, and do not read mounts." In
  this project `ubc check` reports diagnostics located in the mounted files,
  e.g. `warning[needs.test_report_path_outside_root] --> …/tests/test_results.rst:12:11`
  and `warning[needs.src_trace] --> …/src/implementations.rst:10:4`, and
  `Processing 8 files` includes them. Plan 001 first planned CI around the
  documented behaviour (mounted docs unlinted) before it was checked.
- **Expected:** the description matches the behaviour (or `ubc format` /
  `ubc check` differ and the text says which).
- **Workaround:** none needed (the behaviour is the useful one); CI relies on `ubc check` covering mounted files.
- **Solution A:** correct the schema description.
- **Solution B:** state explicitly which commands read mounts (`check` yes, `format` ?).

## 4. Pharaoh (`ubc agent`)

### PH-01 Verdicts stored per need id only

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`agent verdict-submit`, `verdict-check`)
- **Marker:** `content/cv-platform@25b77bd` `docs/vehicle/requirements.rst:16` and `:27`
  (`REQ_ENERGY_SOURCE`, two complementary `if` blocks), `.pharaoh/verdicts/REQ_ENERGY_SOURCE.json`.
- **Summary:** `.pharaoh/verdicts/<ID>.json` holds one verdict; alternatives with
  the same id (one per product) overwrite each other, so `verdict-check` can
  never be green in all products.
- **Input:** review `REQ_ENERGY_SOURCE` under `truck_bev_nmc_eu` (state of
  charge), then under `truck_diesel_eu` (fuel level).
- **Wrong output:** after both submits: diesel `ok: true`; every BEV product `outdated: [REQ_ENERGY_SOURCE]`, `ok: false`. Re-reviewing BEV flips diesel. Now 8 outdated in N / B, 2 in A.
  Expected: both variants keep their verdict.
- **Workaround:** none; gaps imported honestly (`docs/_global/gaps.rst`).
- **Solution A:** key verdicts by id + reviewed fingerprint (several verdicts per file, `verdict-check` picks the one matching the current fingerprint).
- **Solution B:** key by id + variant (e.g. hash of the active variant data or `meta.product`), `<ID>@<variant>.json`.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `verdict-submit REQ_ENERGY_SOURCE` under truck_bev_nmc_eu then truck_diesel_eu (`25b77bd`): one `REQ_ENERGY_SOURCE.json`, the other product is `outdated` again.

### PH-02 Review fingerprint ignores resolved values and link variants

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `content/cv-platform@25b77bd` `docs/vehicle/requirements.rst:65`
  (`:value: <<mcs: 1000 kW, 350 kW>>`), `docs/subsystems/vcu/architecture.rst:21`
  (`:allocates: <<bev: BMS_REQ_POWER_DERATING>>`).
- **Summary:** the fingerprint covers the raw source, not the per-product
  resolved `value` or links — a verdict judged on 1000 kW counts as fresh for 350 kW.
- **Input:** review `REQ_MAX_CHARGE_POWER` under `truck_bev_nmc_eu` (1000 kW), brief under `bus_bev_lfp_eu` (350 kW).
- **Wrong output:** bus brief lists it in `fresh_skipped` (same fingerprint `e70c…`). Same for `ARCH_VCU_POWER_MGMT` (link gone in diesel) and `BB_*` (allocated BMS content differs NMC / LFP).
  Expected: re-review when the reviewed content differs.
- **Workaround:** none.
- **Solution A:** fingerprint the resolved need (fields after variant functions, links after link variants) — together with PH-01 A.
- **Solution B:** fingerprint raw source + the values of all `var.*` keys the need references.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `REQ_MAX_CHARGE_POWER` has fingerprint `f2b2b642` in truck_bev_nmc_eu and bus_bev_lfp_eu (value 1000 kW / 350 kW); ubc 0.35.0 gives the same hash today, so the changed hash comes from the content.

### PH-03 Fingerprint follows parents only one level

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `content/cv-platform@25b77bd` `docs/subsystems/vcu/architecture.rst`
  (`ARCH_VCU_ENERGY_DISPLAY`), `docs/_global/decisions.rst:34` (`:affects: ARCH_CHG_INLET`),
  `docs/subsystems/vcu/software_requirements.rst` (`SWREQ_VCU_ENERGY_DISPLAY`).
- **Summary:** a need's fingerprint includes its direct parent, so a
  single-definition child of an alternative flips between products; one level
  further down it does not. Inconsistent and amplifies PH-01.
- **Input:** `ARCH_VCU_ENERGY_DISPLAY` (one definition) satisfies `REQ_ENERGY_SOURCE` (alternative).
- **Wrong output:** `ARCH_VCU_ENERGY_DISPLAY` fingerprint `f4db…` (BEV) vs `517e…` (diesel) → outdated after each product; `DEC_CHARGING_INLET_PRIORITY` flips with `ARCH_CHG_INLET`; `SWREQ_VCU_ENERGY_DISPLAY` (grandchild) does not.
  Expected: a documented, consistent rule.
- **Workaround:** none.
- **Solution A:** fingerprint only the need itself; signal parent changes separately (`parent_changed`).
- **Solution B:** include the full upstream chain, consistently, and combine with PH-01 so variants do not collide.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `ARCH_VCU_ENERGY_DISPLAY` and `DEC_CHARGING_INLET_PRIORITY` flip per product, the grandchild `SWREQ_VCU_ENERGY_DISPLAY` stays `20b5c8b7` in all three.

### PH-04 Backward trace attributed to one of two stages

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`agent gaps`)
- **Marker:** `main@c10bbd7` `ubproject.toml` (stage `bms_allocation`, `satisfies` trace `direction = "both"`, fixed in `9abdd2c`) with the content of `content/cv-platform@25b77bd`.
- **Summary:** stages `archs` (`arch` satisfies `req`, both) and `bms_allocation`
  (`bms_block` satisfies `req`, both) share link + target; the backward
  obligation of every req is attributed to `bms_allocation` only.
- **Input:** `REQ_DOOR_DRIVE_INTERLOCK` satisfied by `ARCH_VCU_DOOR_INTERLOCK` (arch), no `bms_block`.
- **Wrong output:** `{'id': 'REQ_DOOR_DRIVE_INTERLOCK', 'link': 'satisfies', 'have': 0, 'need': 1, 'category': 'trace_backward'}` — the arch link is not counted. Expected: `have: 1` (arch stage satisfied), or one obligation per stage reported separately.
- **Workaround:** `bms_allocation` trace `direction = "outgoing"`.
- **Solution A:** evaluate backward obligations per stage (count only the producing type of that stage) and report the stage in the gap.
- **Solution B:** `config-validate` warns when two stages declare the same (link, up, direction both).
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `satisfies` trace `direction = "both"` in `bms_allocation` (`25b77bd`, bus_bev_lfp_eu): `agent gaps` reports `REQ_DOOR_DRIVE_INTERLOCK … trace_backward`.

### PH-05 Workflow traces apply per need type

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `main@37257e1` `ubproject.toml` (stage `bms_allocation`
  `produces = "arch"`, route `docs/subsystems/bms/architecture.rst`; stage
  `swreqs` with `refines` up `arch`, `direction = "both"`), product
  `truck_bev_nmc_eu`. Reproduced 2026-10-09 with the snippets below.
- **Summary:** `[[workflow.stages.trace]]` has only `link`, `up`, `direction`,
  `min`, and a stage owns every need of the type it `produces` — the route
  does not decide. A stage producing a type shared with another stage cannot
  opt out of the other stage's downstream obligations, so the BMS black boxes
  (realised by the BMS via `allocates`, never refined by a CV swreq) carry a
  gap that can never be closed. `config-validate` accepts two stages with the
  same `produces` without a warning.
- **Input** (append to the three files on `main@37257e1`, then
  `cmake -S . -B build/cmake/truck_bev_nmc_eu -G Ninja -DVARIANT=truck_bev_nmc_eu`,
  `cp build/cmake/truck_bev_nmc_eu/compile_commands.json build/`,
  `ubc agent gaps -p .` and `ubc agent status -p .`):

  `docs/vehicle/user_stories.rst`
  ```rst
  .. user_story:: Probe story
     :id: US_PROBE
     :status: draft

     As a driver, I see the probe.
  ```
  `docs/vehicle/requirements.rst`
  ```rst
  .. req:: Probe requirement
     :id: REQ_PROBE
     :status: draft
     :traces_to: US_PROBE

     The vehicle shall show the probe.
  ```
  `docs/subsystems/bms/architecture.rst` (route of stage `bms_allocation`)
  ```rst
  .. arch:: BMS power limits (black box)
     :id: ARCH_BMS_PROBE
     :status: draft
     :satisfies: REQ_PROBE
     :allocates: BMS_REQ_POWER_DERATING

     The BMS publishes the permitted discharge power.
  ```
- **Wrong output:**
  ```
  agent gaps:   {'id': 'ARCH_BMS_PROBE', 'type': 'arch', 'link': 'refines', 'have': 0, 'need': 1, 'category': 'trace_backward'}
  agent status: archs blocked 16 / bms_allocation blocked 16
  ```
  Expected: no `refines` obligation for the needs of stage `bms_allocation`;
  `bms_allocation` counts only the needs on its route (1), `archs` only its
  own. (The 16 include the 15 imported `BMS_ARCH_*`, see PH-06.)
- **Workaround:** dedicated type `bms_block` (`e744d72`) — costs an extra type,
  duplicated schema rules (`alloc-*` for `arch` and `bms_block`), and the CV
  metamodel diverges from the BMS metamodel.
- **Solution A:** a `select` / filter per stage (e.g. by route path, docname
  or a field) deciding which needs of the type belong to it; traces apply to
  that set only.
- **Solution B:** attribute needs to the stage whose route they live in;
  traces apply per stage, not per type. Supplement for both: `config-validate`
  warns when two stages declare the same `produces`.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): the snippets on `main@37257e1` give `ARCH_BMS_PROBE … refines … trace_backward`; `config-validate` still accepts two stages producing `arch` without a warning.

### PH-06 Stage counts include imported needs

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`agent status`, `agent next`)
- **Marker:** `main@e744d72`, product `truck_bev_nmc_eu` configured (no CV content).
- **Summary:** needs with a status in `exempt_status` (`imported`) are excluded
  from gaps but counted as stage output.
- **Input:** `[workflow] exempt_status = ["imported"]`, 205 imported `BMS_*` needs, no CV needs.
- **Wrong output:** `user_stories=done/5 reqs=done/20 …`; `agent next` → stage `bms_allocation` (or `done`). Expected: `user_stories=ready/0`, next `user_stories` (as in the diesel product).
- **Workaround:** check with `-c 'needs.external_needs = []'` or in the diesel product.
- **Solution A:** apply `exempt_status` to stage counts and `next`.
- **Solution B:** exclude `is_external` needs from all workflow counts by default.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `main@e744d72`, truck_bev_nmc_eu: `agent status` `user_stories=done/5 …`, `agent next` → `bms_allocation`; with `-c 'needs.external_needs = []'` → `user_stories`.

### PH-07 `review-brief` lists exempt needs

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `content/cv-platform@25b77bd`, `ubc agent review-brief arch -p .` under `truck_bev_nmc_eu`.
- **Summary:** `review_needs` contains the 15 imported `BMS_ARCH_*` needs; `verdict-check` correctly ignores them.
- **Wrong output:** `"review_needs": ["BMS_ARCH_…", …, "ARCH_VCU_…"]`. Expected: only non-exempt, local needs.
- **Workaround:** reviewer instruction "skip `BMS_*`".
- **Solution A:** apply `exempt_status` in `review-brief`.
- **Solution B:** list them separately as `exempt` for transparency.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `review-brief arch` (`25b77bd`, truck_bev_nmc_eu) lists 18 needs, 15 of them `BMS_ARCH_*`.

### PH-08 `agent audit` omits fields and links

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0
- **Marker:** `content/cv-platform@25b77bd`, `ubc agent audit --id SWREQ_CHG_SESSION_START -p .` / `--id REQ_MAX_CHARGE_POWER`.
- **Summary:** `audit` shows neither the (resolved) `value` nor `tags`; `trace.outgoing` lacks `refines` and `allocates`, `trace.incoming` lacks `refines_back` (they appear only under `links`).
- **Wrong output:** reviewers had to use `ubc query filter … --field value` and read `build/active/bms.needs.json`.
- **Solution A:** include all declared fields (resolved) and all links in `trace`.
- **Solution B:** `--fields all` / `--links all` options, documented in the review skills.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `agent audit --id SWREQ_CHG_SESSION_START` has `trace.outgoing: {}` (`refines` only under `links`); `--id REQ_MAX_CHARGE_POWER` has no `value` / `tags`.

### PH-09 `doctor` checks only the `.claude` copy of project skills

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 (`agent doctor`)
- **Marker:** `main@e744d72` `.claude/skills/draft-allocation/SKILL.md` — delete or change `.agents/skills/draft-allocation/SKILL.md`.
- **Summary:** for skills outside the install manifest, `doctor` requires `.claude/skills/<n>/SKILL.md` but does not check the `.agents/skills/` and `.github/agents/` copies or their drift.
- **Wrong output:** `doctor ok` with a missing / different `.agents` copy.
- **Workaround:** `tools/check_skill_mirrors.py`.
- **Solution A:** mirror check for every skill found in any host location.
- **Solution B:** `ubc agent skill add <path>` registering project skills in the manifest (then the existing mirror check applies).
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): changing or deleting the `.agents` copy of `draft-allocation` → `doctor` `ok: true`; only deleting the `.claude` copy is an error.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 001 P4, product_demo): own skill `draft-us` with a changed `.agents` copy and `draft-spec` without `.github/agents` copy → `doctor` `ok: true` (25 checks). Workaround here: `scripts/mirror_skills.py --check` in CI.

### PH-05 addendum: membership links (plan 7)

The same per-type rule appears with `part_of` (arch / bms_block → subsystem):
a `direction = "both"` trace in stage `archs` makes `SUB_BMS` owe an `arch`
part (`{'id': 'SUB_BMS', 'link': 'part_of', 'have': 0, 'need': 1, 'category':
'trace_backward'}` on `model/system`, truck_bev_nmc_eu) although its parts
are `bms_block`s of stage `bms_allocation`. Workaround: `direction =
"outgoing"` in both stages, "every subsystem has a part" as the schema rule
`coverage-subsystem-part_of-back` (counts both types).

- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): marker now `main@36f44a4` `ubproject.toml:606` (`model/system` is merged): `part_of` trace `both` gives `SUB_BMS … part_of … trace_backward`.

### PH-10 Brief and skill documentation gaps

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 + installed `review-*` skills (vmodel v9)
- **Marker:** `content/cv-platform@25b77bd`, any `review-brief`.
- **Summary:** `submit_command` omits `-p <project>` although the skills require it; `verdict-check` returns a `stale` bucket (verdict of a need absent in the product) not described in the skills; exit code 1 whenever `ok` is false.
- **Solution A:** include `-p` in `submit_command`; document `stale` (useful for product lines).
- **Solution B:** `verdict-check --variant-aware` treating `stale` explicitly as "not applicable".
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `submit_command` still without `-p`; `stale` documented only in the CLI `--help`, not in the review skills of preset v21.

### PH-11 `review-brief --ids` comma list rejected

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 + installed `review-*` skills
- **Marker:** `main@1a480bf`, `.claude/skills/review-arch/SKILL.md` step 1 (`--ids <ID,...>`). Found in plan 7 phase 1.
- **Marker here:** `main@318328f` `.claude/skills/review-arch/SKILL.md:49` (profile `vmodel` 21, as in the origin Status; same text in `review-requirement`, `review-feat`, `review-decision`, and the `.agents/skills/` and `.github/agents/` copies).
- **Summary:** the skills tell the reviewer to call `ubc agent review-brief <TYPE> … (or --ids <ID,...>)`; the CLI takes space-separated ids only and refuses a type together with `--ids`.
- **Input:** `ubc agent review-brief --ids ARCH_VCU_POWER_MGMT,ARCH_ENG_FUEL_LEVEL -p .`; `ubc agent review-brief arch --ids ARCH_VCU_POWER_MGMT -p .`
- **Wrong output:** `{"ok": false, "error": "unknown_need", "id": "ARCH_VCU_POWER_MGMT,ARCH_ENG_FUEL_LEVEL"}`; `{"ok": false, "error": "ambiguous_selection"}`. Expected: the documented comma list works (or the skills document the space-separated form).
- **Workaround:** space-separated ids without a type.
- **Solution A:** accept comma-separated ids (and a type as a filter together with `--ids`).
- **Solution B:** correct the skills (`--ids <ID> <ID> …`, no type).
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `--ids A,B` → `unknown_need` with the joined id; `arch --ids A` → `ambiguous_selection`; the v21 `review-arch/SKILL.md:49` still documents `--ids <ID,...>`.

### PH-12 `config-validate`: a type declared by `[test_reports]` counts as undeclared

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.37.0 (`ubc agent config-validate`, `ubc agent doctor`) with Sphinx-Test-Reports 3.0.0
- **Marker:** scratch copy based on `main@54e862c` (plan 110 E7b / E16); stage
  `test_results` as in `ubproject.toml:686-697`.
- **Summary:** STR registers the case type from `[test_reports.case]`, and ubc
  builds those needs. Because of STR-03 the type may not also be in
  `[[needs.types]]`, but `config-validate` only accepts `[[needs.types]]`, so
  every project that uses the STR directives fails `doctor`.
- **Input:** `[test_reports.case] type = "test_result"` (all six keys), no
  `[[needs.types]]` entry, `[[workflow.stages]] produces = "test_result"`.
- **Wrong output:** `{"kind": "undeclared_type", "subject": "test_result", "message": "type 'test_result' referenced by stage 'test_results' is not a declared [[needs.types]] directive"}`; `doctor` `ok: false`. `status` / `gaps` work on the same config.
- **Workaround:** give only the `doctor` / `config-validate` run the full type list:
  `ubc agent doctor -p . -c 'needs.types = [{directive = "…", title = "…", prefix = "…"}, …, {directive = "test_result", …}]'`.
  The override replaces the whole list (as in UB-05), so every type must be repeated. Checked 2026-10-14 on a scratch
  copy of `../test-reports-example` (its README documents it) with a `[workflow]` stage producing `testcase`:
  plain `doctor` `ok: false` (`undeclared_type`), with the override `ok: true`; `status` unchanged. Declaring the type
  twice is no workaround: it aborts Sphinx (STR-03).
- **Solution A:** `config-validate` accepts the types `[test_reports]` declares (file, suite, case), as ubc's build does.
- **Solution B:** fix STR-03, so the type can stay in `[[needs.types]]`.
- **Status:** open on ubc 0.37.0 with sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 (2026-10-17, plan 998 run 1): `config-validate` exits 1 with `undeclared_type … test_result`; `doctor` `config-validity` error. Workaround (`-c 'needs.types = […]'`) still works.

### PH-13 Outgoing trace obligation met by any link

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.37.0 (`ubc agent gaps`, `ubc agent status`)
- **Marker:** scratch copy based on `main@54e862c` (plan 110 E16); stage
  `test_results` with `[[workflow.stages.trace]] link = "results_for"`,
  `direction = "outgoing"`, `min = 1` (`ubproject.toml:693-697`).
- **Summary:** a `test_result` without `results_for` is only reported (as
  `orphan`) when it has no link at all. Any other link, e.g. the generic `links`
  STR sets from each case to its file and suite need, hides the gap, and the
  stage reads `done`.
- **Input:** `.. test_result::` `:id: TRES_MANUAL` `:links: TRES_P2` (no
  `results_for`); the same for every STR case of a JUnit file without `cmake_labels`.
- **Wrong output:** `gaps` lists only the `TEST_*` orphans; `status`: `test_results done`, `failing_gates: []`, although `results_for` is missing. Without `:links:` the same need is an `orphan` and the stage fails the `trace` gate. Expected: a gap on the declared link `results_for`.
- **Workaround:** the schema rule `trace-test_result-results_for` (min 1) catches it in `ubc check` and Sphinx.
- **Solution A:** check the declared trace link per need of the produced type, not "has any link".
- **Solution B:** report `trace_forward` gaps for needs that lack the declared outgoing link.
- **Status:** open on ubc 0.37.0 (2026-10-17, plan 998 run 1): `TRES_MANUAL` with only `:links:` meets the `results_for` obligation: `agent gaps` `[]`, stage `test_results` done; without `:links:` it is an orphan.

### PH-14 Lifecycle gate applies to every need, also types without a status

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent gaps`, `agent status`)
- **Marker:** branch `feat/engineering-model` (plan 001 P3, uncommitted), `docs/ubproject.toml` `[workflow]`, with `[workflow.lifecycle] states = ["proposed", "accepted", "superseded", "open", "mitigated", "closed"]` added.
- **Summary:** only `dec` / `risk` carry a `status` in this model. With a
  lifecycle declared, every other need (us, req, spec, impl, test_spec, test
  results) is a `status_undeclared` gap and every stage shows
  `failing_gates: ["lifecycle"]`. There is no per-type or per-stage scope for
  the states.
- **Wrong output:** `by_category: {'status_undeclared': 14, 'review': 8}`, e.g. `{'id': 'US_LOGIN', 'type': 'us', 'link': 'status', 'have': 0, 'need': 1, 'category': 'status_undeclared'}`. Expected: needs without a status, or of types no lifecycle covers, are not judged.
- **Workaround:** no `[workflow.lifecycle]`; status values per type in `schemas.json` (`status-dec`, `status-risk`, `status-none`).
- **Solution A:** `[workflow.lifecycle] types = [...]` (or states per type).
- **Solution B:** judge only needs that set a status; an absent status is not "undeclared".

### PH-15 Author prompt hard-codes the new need's status for every type

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent prompt`, `agent run`)
- **Marker:** branch `feat/engineering-model` (plan 001 P3, uncommitted), `docs/ubproject.toml` `[workflow]`; `ubc agent prompt --stage risks --id SPEC_HASH`.
- **Summary:** the INSTRUCTION orders "a valid sphinx-needs RST directive with
  a unique id, `:status: draft`" when no lifecycle is declared, and the first
  lifecycle state otherwise — the same value for every stage / type. It adds
  "If the SKILL block's worked example … shows a different `:status:` value,
  this INSTRUCTION is authoritative". Here `draft` is no valid status at all,
  `us` / `req` / … must have none, `dec` starts `proposed`, `risk` `open`.
- **Wrong output:** `:status: draft` (no lifecycle); `:status: open` for every stage with `states = ["open", …]` (scratch copy). Expected: the status from the produced type's own rule, or none.
- **Workaround:** each stage's `authoring` text states the status rule and says it overrides the generic line; `schemas.json` rejects a wrong value as a violation.
- **Solution A:** a per-stage `initial_status` (empty = write none).
- **Solution B:** derive it from the schema / field config of the produced type; drop the "authoritative" sentence for status.

### PH-16 Cross-cutting stages: one element for all upstream needs, no route into a need

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent prompt`)
- **Marker:** branch `feat/engineering-model` (plan 001 P3, uncommitted), `docs/ubproject.toml` `[workflow]`; scratch variant with stages `decisions_req` / `decisions_spec` (`produces = "dec"`, route `single` to the parent's file, trace `up = "req"`, `link = "decides"`, `direction = "outgoing"`).
- **Summary:** decisions here are nested in the one need they decide. A
  global-scope stage lists all needs of its `up` type and orders "set
  `:decides: REQ_AUTH, REQ_LOG` … Author or extend the `decisions_req` so EVERY
  listed upstream need is satisfied by at least one element", even with
  `direction = "outgoing"` (not gated). Routes name files (`single`,
  `per-root`, `per-need` → `{id}` = a new file per need), never a position
  inside an existing need.
- **Expected:** a cross-cutting stage anchored on ONE need (`--id`), linking only that need, and a route kind "nested in the anchor need".
- **Also regular stages (plan 001 P4):** with `route.scope = "global"` the `reqs` prompt anchored on `US_LOGIN` ordered `:satisfies: US_AUDIT, US_LOGIN`, `specs` `:refines: REQ_AUTH, REQ_LOG`, `code` `:implements: SPEC_AUDIT, SPEC_HASH`. With `scope = "stream"` (same single file) they order only the anchor's parent (`:satisfies: US_LOGIN`). The docs do not say that `scope` decides how many parents a new need must link.
- **Workaround:** regular stages use `scope = "stream"`; decisions / risks are created by the stage skills through simple recording skills (payload hand-over); the `decisions` / `risks` stages carry no trace and exist for review / verdicts only; completeness via `schemas.json`.
- **Solution A:** `route.granularity = "nested"` (inside the anchor need's directive) and anchor-only linking for optional stages.
- **Solution B:** document that cross-cutting stages cover the whole upstream set, and offer a per-anchor mode.

### PH-17 "CREATE THE FILE" for an existing single-file route

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent prompt`)
- **Marker:** branch `feat/engineering-model` (plan 001 P3, uncommitted), `docs/ubproject.toml` `[workflow]`; scratch stage `decisions_req` with route `single` → `requirements.rst` (exists, holds `REQ_AUTH`, `REQ_LOG`).
- **Wrong output:** "CREATE THE FILE at `requirements.rst` using your file-writing tool — actually write the file to disk". Expected: "append to / edit the existing file `requirements.rst`" when it exists.
- **Workaround:** skills say "append, never rewrite the file"; changes stay uncommitted for review.
- **Solution A:** word the order by file existence (create vs. append).
- **Solution B:** route option `mode = "append"`.

### PH-18 No opt-out from preset skills: `update` restores what the project removed

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent update`, `agent doctor`), profile `vmodel` 21
- **Marker:** branch `feat/engineering-model` (plan 001 P4 follow-up, uncommitted): `docs/.pharaoh/agent/install-manifest` with 21 entries; scratch copies of the repository for the runs below.
- **Summary:** a project that does not want some preset skills (here 11
  unused ones: `draft-arch`, `review-arch`, `draft-test`, `record-decision`,
  the recovery skills) and replaces others with its own pattern
  (`draft-requirement`, `draft-impl`) cannot tell the engine so.
- **Input / output:**
  - files deleted, manifest unchanged → `doctor` ok; `update` restores the files;
  - installed skill edited, manifest unchanged → `doctor` **error** `skill-integrity:draft-requirement` (+ 2 mirror errors); `update` `ok: false`, `conflicts` = its 3 copies;
  - files deleted **and** manifest entries removed → `doctor` ok; first `update`: exit 0, files still gone, but the manifest is back to all 60 entries; second `update`: files restored;
  - edited skill with manifest entries removed → `doctor` ok ("hand-authored or custom-named skill"); every `update`: `ok: false`, conflict on its 3 copies (content preserved).
- **Expected:** a way to exclude preset assets (removed, or replaced by a project skill of the same name) that `update` and `doctor` respect.
- **Workaround:** never run `ubc agent update` in the repository; run it in a shadow clone and port changes by hand (plan 998 §4.7).
- **Solution A:** `[agent] exclude_assets = ["draft-arch", …]` / `override_assets = ["draft-requirement", …]`, honoured by `install`, `update` and `doctor`.
- **Solution B:** `ubc agent update --only-owned` that never re-adds entries the project removed from the manifest.

### PH-19 Decisions and risks never go stale in the review gate

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent verdict-check`, `agent impact`, `agent context`)
- **Marker:** scratch copy of branch `feat/engineering-model` (plan 001 P5): `DEC_HASH_ALGO` (accepted) nested in `SPEC_HASH` with `:decides: SPEC_HASH`; `RISK_SCRYPT_PARAMS` (mitigated) `:affects: SPEC_HASH`, `:mitigated_by: DEC_HASH_ALGO, TSPEC_HASH`; verdicts submitted for the three needs.
- **Summary:**
  1. Changing `SPEC_HASH`'s body → `verdict-check` `outdated: ['SPEC_HASH']` only; the decision that decides it and the risk that affects it stay fresh. Changing the mitigating `TSPEC_HASH` → nothing outdated. The one-hop fingerprint (PH-03) follows trace links, not `decides` / `affects` / `mitigated_by`.
  2. `ubc agent impact --id SPEC_HASH` reaches `TSPEC_HASH`, `IMPL_HASH`, `RISK_SCRYPT_PARAMS` — not the nested `DEC_HASH_ALGO`.
  3. The parent's fingerprint (`agent context`) includes the raw text of its nested decisions: editing only the decision changes `SPEC_HASH`'s fingerprint and outdates its verdict.
- **Expected:** cross-cutting links count for staleness (a decision / risk is outdated when a need it links to changes); nested needs are excluded from the parent's fingerprint (they have their own).
- **Workaround (found later in P5):** give the `decisions` / `risks` stages trace edges with `direction = "outgoing"`, one per target type (`decides` → us / req / spec / test_spec; `affects` → …; `mitigated_by` → req / spec / test_spec / dec). The one-hop fingerprint then follows those links: a changed parent outdates the decision and the risk, a changed mitigation outdates the risk; no trace gaps (outgoing edges are not gated), several edges per stage accepted by `config-validate`. Item 3 (nested text in the parent's fingerprint) remains and is accepted: editing a decision re-reviews its parent. Earlier fallback: own ledger script (option B+).
- **Solution A:** a per-type list of links that feed the fingerprint (`[workflow] fingerprint_links`).
- **Solution B:** fingerprint nested needs separately and exclude them from the parent's content hash.

### PH-20 `release-check` baseline: undocumented format, cannot capture debt, no category filter

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent release-check`)
- **Marker:** scratch copy of branch `feat/engineering-model` (plan 001 P5 sample data: an open risk, a proposed decision, no verdicts).
- **Summary:** plan 001's CI 1 should block *new* structural gaps but allow
  missing reviews and open risks / proposed decisions on `main`.
  `release-check --baseline` cannot express that:
  1. `--help`: "a JSON gap-key list"; `[]` → `failed to parse baseline JSON … invalid type: sequence, expected a map`; the `ubc agent gaps` output → `… expected usize at line 2 column 10`. So the file is a map *key → count*; 11 plausible key spellings (`DEC_AUDIT_STORE`, `…:status`, `…|status|status_disallowed`, `status_disallowed:…`, …) all gave `baselined_debt: 0`. The key format is not documented.
  2. `--update-baseline` "on a passing run" only — existing debt cannot be captured from today's (failing) state.
  3. `review` (missing verdict) and `status_disallowed` (`release_disallow_status`) gaps are part of the gate, with no way to exclude categories, and a `-c` override of `workflow.release_disallow_status` replaces the whole `[workflow]` table (UB-05).
- **Expected:** a documented baseline format (and `--write-baseline` from the current state); category selection (`--categories trace,orphan,…`) or a tier mode.
- **Workaround:** `scripts/ci_gates.py gaps --tier main`: reads `ubc agent gaps`, ratchets structural gaps against its own `docs/.pharaoh/gaps-baseline.json` (`category:id:link` list), allows `review` / `status_disallowed`.
- **Solution A:** document the key; add `release-check --write-baseline`.
- **Solution B:** `release-check --allow <category>` per tier.

### PH-21 Runner without tool permission: every stage "no change", `ok: true`

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent run`), Claude Code 2.1.224 as runner
- **Marker:** branch `feat/engineering-model` (plan 001 P8, uncommitted) and a scratch clone with the lockout chain committed; `[agent.runner] command = "claude -p --permission-mode acceptEdits --output-format stream-json --verbose"` (as the `vmodel` profile's example suggests).
- **Summary:** `ubc agent run --skill change-request --id REQ_LOCKOUT` after
  changing "15" to "10 minutes": the runner's first step is
  `/Users/…/ubc agent impact …`; `acceptEdits` does not allow Bash, so the
  headless runner replies "I'm being blocked from running the `ubc` CLI
  pending your approval" and stops. The engine reports
  `specs(no change), code(no change), test_specs(no change)`, `ok: true`.
- **Expected:** a runner that ends without doing its task (permission
  denial, question to the user) is a failed run (`ok: false`, non-zero exit),
  not "no change".
- **Workaround:** `--allowedTools "Bash(*/ubc *)" "Bash(ubc *)" "Bash(python3 scripts/*)"` in the runner command (`Bash(*/ubc:*)` does not match an absolute path; `Bash(*/ubc *)` does). Then the cascade changes spec, code and test spec.
- **Solution A:** detect permission denials / unanswered questions in the runner's stream and fail the stage.
- **Solution B:** the profile's runner example includes the needed `--allowedTools`; `doctor` checks that the runner may run `ubc`.

### PH-22 `change-request` cascade: misreported code stage, nested decisions not reconciled

- **Origin:** product_demo
- **Tool:** ubc 0.37.0 (`agent run --skill change-request`)
- **Marker:** branch `feat/engineering-model` (plan 001 P8, uncommitted) and a scratch clone with the lockout chain committed; runner with the PH-21 workaround.
- **Summary:**
  1. Result `specs(modified SPEC_LOCKOUT), code(no change), test_specs(modified TSPEC_LOCKOUT)`, but `src/product_demo/lockout.py` was changed (`LOCK_SECONDS = 900` → `600`): the code stage is judged by its needs (the marker did not change), not by the source.
  2. `DEC_REQ_LOCKOUT_LIMITS`, nested in the edited `REQ_LOCKOUT`, still says "15 minutes … 480 per day": the cascade runs the stages below the anchor's stage only, not the decisions inside the anchor (and `impact` does not list them, PH-19). Decisions nested in downstream needs were updated (`DEC_TSPEC_LOCKOUT_CLOCK`). Risks with "15 minutes" in their text are not reconciled either.
  3. The code stage is not reliable: in a repeat of the same cascade (same edit, same config) the runner changed spec and test spec but **not** `lockout.py`, so spec (600 s) and code (900 s) disagreed — and the tests stayed green because they used the code's constant.
- **Expected:** a code stage reports a changed source file; the cascade (or at least its report) covers the anchor's nested decisions and the cross-cutting needs linked to the changed needs.
- **Workaround:** the review gate flags the decision (`outdated` through the `decides` trace edges, option F) and the hash conditions flag the risks (`needs.link_condition_failed`); both are re-evaluated by review. Tests use the specified values literally (`tests/test_lockout.py`), so a code stage that missed the change fails the tests.
- **Solution A:** count changed files under a code stage's route as a modification.
- **Solution B:** add a pass for the anchor's nested needs and for `decides` / `affects` / `mitigated_by` neighbours.

## 5. Sphinx-Needs

### SN-01 Every schema severity is a Sphinx warning

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Needs 8.5.0
- **Marker:** `content/cv-platform@25b77bd` `docs/conf.py:24` (workaround).
- **Summary:** `warning` and `info` schema results become Sphinx warnings, so `sphinx-build -W` fails on rules meant as non-blocking (backward coverage while a stream is in progress).
- **Input:** schema rule `coverage-req-satisfies-back` with `"severity": "warning"`, a req without arch yet.
- **Wrong output:** `WARNING: Need 'REQ_…' has schema warnings … [sn_schema_warning.network_contains_too_few]` → build failed with `-W`.
- **Workaround:** `suppress_warnings = ["sn_schema_warning.network_contains_too_few"]` (as the BMS).
- **Solution A:** map severities: `violation` → warning (fails `-W`), `warning` / `info` → log only; configurable `needs_schema_warn_level`.
- **Solution B:** a per-rule `fail_build` flag.
- **Status:** open on Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): without `suppress_warnings` and with a req lacking an arch (`25b77bd`), `-W` fails on `[sn_schema_warning.network_contains_too_few]`. `warning` and `info` are still logged as Sphinx warnings; `violation` is now an error.

### SN-02 `needs_from_toml` overrides `needs_external_needs` in `conf.py`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Needs 8.5.0
- **Marker:** `main@e744d72` `ubproject.toml:48-50` and `docs/conf.py`.
- **Summary:** a `needs_external_needs` computed in `conf.py` (e.g. per-chemistry `base_url`) is replaced by the TOML value.
- **Input:** `conf.py`: `needs_external_needs = [{"json_path": …, "base_url": f".../{chemistry}"}]` with `needs_from_toml = "../ubproject.toml"`.
- **Wrong output:** the TOML `base_url` is used. Expected: `conf.py` wins (or merge), as for other Sphinx options.
- **Workaround:** one `base_url` per BMS version.
- **Solution A:** let `conf.py` override TOML (documented precedence).
- **Solution B:** variant functions in `base_url` (`<<[var.bms.chemistry == 'lfp']: …/lfp, …/nmc>>`), supported by ubc as well.
- **Status:** open on Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): a `needs_external_needs` `base_url` in `conf.py` (`main@e744d72`) is never used; `external_url` comes from the TOML.

### SN-03 `needs.json` drops external needs by default

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Needs 8.5.0
- **Marker:** `main@e744d72` `ubproject.toml` (`builder_filter = ""` is the workaround).
- **Summary:** default `builder_filter = "is_external==False"`; ubc exports external needs → per-product exports differ (0 vs 205).
- **Workaround:** `builder_filter = ""`.
- **Solution A:** align the default with ubc (or ubc with Sphinx) and document it.
- **Solution B:** see UB-08 — both tools honour the same option.
- **Status:** open on Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): without `builder_filter = ""` (`main@e744d72`) Sphinx `needs.json` has 0 BMS needs, ubc 205; the default is still `is_external==False`.

### SN-04 Moved to CL-06

Re-checked 2026-10-09: Sphinx-Needs handles a duplicate id correctly (located
warning); the abort comes from Sphinx-Codelinks — see CL-06.

### SN-05 Schema `contains` without `items` rejected

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Needs 8.5.0 (ubc accepts)
- **Marker:** `main@e744d72` `metamodel/schemas.json:979` (`alloc-target-interface`) — remove `"items": {"type": "string"}`.
- **Input:** `"tags": {"type": "array", "contains": {"type": "string", "const": "interface"}}`
- **Wrong output:** sphinx-needs rejects the schema; ubc validates it. Expected: same acceptance (valid JSON Schema).
- **Solution A:** accept `contains` without `items`.
- **Solution B:** ubc applies the same restriction and reports it.
- **Status:** open on Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): without `items` in `alloc-target-interface` (`main@e744d72`): `NeedsConfigException … not valid under any of the schemas listed in the 'anyOf' keyword`; `ubc check` accepts it.

### SN-06 `id_prefix` rewrites ids inside the text of imported needs

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Needs 8.5.0 (`needs_external_needs` with `id_prefix`); ubc 0.35.0 keeps the text
- **Summary:** `utils.py` `import_prefix_link_edit()` prefixes not only the
  links but also every occurrence of every imported id in `content` /
  `description`, with a plain `str.replace` (code comment: `# ToDo: Use regex
  for better matches.`). This rewrites ids inside code literals (case 1) and
  corrupts an id that contains another imported id (case 2). Found 2026-10-10
  by test DOC-10 (plan 5).
- **Case 1 — literal rewritten (reproducible in this repo):**
  - **Marker:** `content/cv-platform@25b77bd`, `tools/build_product.sh truck_bev_nmc_eu`,
    need `BMS_GAP_REQ_CELL_BALANCING_WINDOW_NO_SATISFIES_BACK` in
    `build/site/truck_bev_nmc_eu/{ubc,sphinx}.needs.json`.
  - **Input** (`third_party/bms/0.1.0/nmc.needs.json`, `id_prefix = "BMS_"`):
    ``Resolve it with ``ubc agent next --id REQ_CELL_BALANCING_WINDOW``, …``
  - **Wrong output (Sphinx):** ``Resolve it with ``ubc agent next --id BMS_REQ_CELL_BALANCING_WINDOW``, …``
    — a command for the BMS project, now with the CV prefix. ubc: text unchanged.
- **Case 2 — id corrupted (synthetic; the BMS has 13 ids contained in other
  ids, e.g. `REQ_FAULT_RECORD` in `SWREQ_FAULT_RECORD_WRITE`, but their texts do
  not mention each other):**
  - **Marker:** none in this repo — reproduce with the two files below
    (reproduced 2026-10-10 with Sphinx 8.2.3, Sphinx-Needs 8.5.0).
  - **Input:** `ext.json`
    ```json
    {"current_version": "1.0", "project": "x", "versions": {"1.0": {"needs": {
     "REQ_FAULT_RECORD": {"id": "REQ_FAULT_RECORD", "type": "req", "title": "Fault record",
       "content": "Refined by SWREQ_FAULT_RECORD_WRITE; run `ubc agent next --id REQ_FAULT_RECORD`."},
     "SWREQ_FAULT_RECORD_WRITE": {"id": "SWREQ_FAULT_RECORD_WRITE", "type": "req", "title": "Write",
       "content": "Refines REQ_FAULT_RECORD."}}}}}
    ```
    `docs/conf.py` (plus an `index.rst` with a title), then `sphinx-build -b html docs build`:
    ```python
    extensions = ["sphinx_needs"]
    needs_types = [{"directive": "req", "title": "Req", "prefix": "", "color": "#fff", "style": "node"}]
    needs_external_needs = [{"json_path": "../ext.json", "base_url": "https://x.invalid", "id_prefix": "BMS_"}]
    needs_build_json = True
    needs_builder_filter = ""
    ```
  - **Wrong output (`build/needs.json`):**
    ```
    BMS_REQ_FAULT_RECORD | Refined by BMS_SWBMS_REQ_FAULT_RECORD_WRITE; run `ubc agent next --id BMS_REQ_FAULT_RECORD`.
    ```
- **Expected:** ids replaced only as whole words and not inside literals — or
  the text left alone (the links are already prefixed); the same rule in both tools.
- **Workaround:** none; parity test DOC-10 ignores `content` of imported needs.
- **Solution A:** replace with a word-boundary regex over all ids at once
  (longest match first) and skip literals / roles; same rule in ubc.
- **Solution B:** leave `content` untouched and rewrite only `:need:` references
  (and links); document the behaviour of both tools.
- **Status:** changed in Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): the corruption is fixed — `import_prefix_link_edit()` now replaces whole ids, longest first, in one pass (synthetic case: `BMS_SWBMS_…` no longer produced). Still open: ids inside literals are prefixed (``ubc agent next --id BMS_REQ_CELL_BALANCING_WINDOW`` at `25b77bd` and `main@36f44a4`); ubc keeps the text. DOC-10 keeps ignoring `content`.

### SN-07 Imported needs: `style` kept by ubc, dropped by Sphinx-Needs

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** ubc 0.35.0 + Sphinx-Needs 8.5.0 (difference between the toolchains)
- **Marker:** `content/cv-platform@25b77bd`, `tools/build_product.sh truck_bev_nmc_eu`,
  `BMS_GAP_REQ_CELL_BALANCING_WINDOW_NO_SATISFIES_BACK` (`style = "red_bar"` in
  `third_party/bms/0.1.0/nmc.needs.json`). Found 2026-10-10 by DOC-10 (plan 5).
- **Summary:** Sphinx-Needs (`external_needs.py`) removes the core fields marked
  `exclude_external` — including `style` — from imported needs, apparently on
  purpose; ubc imports them. The same need therefore renders differently in the
  two outputs. Which behaviour is intended is not documented.
- **Input:** an external need with `"style": "red_bar"`.
- **Wrong output:** different results in the two toolchains: ubc `style = "red_bar"`,
  Sphinx `style = None`. Expected: the same result in both, documented.
- **Workaround:** DOC-10 ignores `style` of imported needs.
- **Solution A:** align both tools (import `style` in Sphinx-Needs, or drop it
  in ubc too) and document the list of fields that are not imported.
- **Solution B:** a per-source option in `[[needs.external_needs]]` (e.g.
  `keep_fields = ["style"]`), honoured by both tools.
- **Status:** open on ubc 0.37.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `BMS_GAP_REQ_CELL_BALANCING_WINDOW_NO_SATISFIES_BACK` `style` `red_bar` in ubc, `None` in Sphinx (`main@36f44a4`).

### SN-08 Schema network failure: console names the link target

- **Origin:** product_demo
- **Tool:** Sphinx-Needs 9.0.0
- **Marker:** scratch copy of `docs/` on branch `feat/engineering-model` (plan 001 P1,
  uncommitted) with `docs/schemas.json` and an added `bad.rst` holding one
  broken need per rule.
- **Summary:** for a `validate.network` failure the console line names the
  linked need, not the need that carries the bad link; `schema_violations.json`
  is correct (`need_path: "REQ_BAD_TARGET > satisfies > SPEC_HASH"`).
- **Input:** `.. req::` `REQ_BAD_TARGET` with `:satisfies: SPEC_HASH` (a spec), rule `link-req-us`.
- **Wrong output:** `ERROR: Need 'SPEC_HASH' has schema violations:`. Expected: `Need 'REQ_BAD_TARGET' …` (as ubc: `REQ_BAD_TARGET:satisfies/SPEC_HASH: "us" was expected`).
- **Workaround:** read `schema_violations.json` (CI does) instead of the console.
- **Solution A:** log under the source need of the `need_path`.
- **Solution B:** print the full `need_path` in the console line.

### SN-09 `needflow` without PlantUML: error text in the page, no warning

- **Origin:** product_demo
- **Tool:** Sphinx-Needs 9.0.0 (Sphinx 9.1.0)
- **Marker:** branch `feat/engineering-model` before the fix (plan 001 P6): `docs/engineering_model/index.rst` `.. needflow::`, no `flow_engine` set, no `sphinxcontrib.plantuml`.
- **Summary:** the default `needs_flow_engine` is `plantuml`. Without the
  PlantUML extension the diagram is replaced by the text "PlantUML is not
  available!" in the HTML, and no warning is logged, so `sphinx-build -W`
  succeeds. Seen by the user in the published page, not by CI.
- **Expected:** a warning (e.g. `needs.flow_engine_unavailable`) so `-W` fails.
- **Workaround:** `[needs] flow_engine = "graphviz"` + `sphinx.ext.graphviz` in `conf.py` (needs `dot`; CI installs graphviz). ubc draws `needflow` with mermaid either way.
- **Solution A:** warn when the configured flow engine's extension is missing.
- **Solution B:** fall back to graphviz (or mermaid) with an info message.

## 6. Sphinx-Codelinks

### CL-01 Fails in a git worktree

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0 (`set_remote_url = true`); ubc 0.35.0 is not affected
- **Marker:** any commit, e.g. `main@9929c6d`:
  `git worktree add ../wt main && cd ../wt && tools/build_product.sh truck_diesel_eu`
  (seen 2026-10-09 in plan 3 with the fix worktree of `07806d7`).
- **Summary:** `analyse/utils.py` `locate_git_root()` accepts a git root only if
  `.git` is a **directory** (`(parent / ".git").is_dir()`). In a linked worktree
  (by the same logic also in submodules — not tested) `.git` is a **file** (`gitdir: …`), so no root is found and
  every codelinks project warns; with `-W` the build fails. ubc builds the same
  worktree without a warning.
- **Input:** a worktree whose `.git` is the file `gitdir: <repo>/.git/worktrees/wt`.
- **Wrong output:** `…/wt/src/eng.rst: WARNING: git root is not found in the parent of …/wt` (one per codelinks project, ×4) → `build finished with problems … (with warnings treated as errors)`; no `remote-url`.
  Expected: root found, remote URL with the commit of the worktree.
- **Workaround:** build in the main checkout.
- **Solution A:** ask git (`git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git remote get-url origin`) instead of reading `.git` by hand — covers worktrees, submodules, packed refs (CL-05).
- **Solution B:** accept a `.git` file and follow its `gitdir:` (plus `commondir` for config and refs); offer config options for repository root / commit / remote URL (useful in CI without `.git`).
- **Status:** **fixed in Sphinx-Codelinks 2.0.0** (2026-10-17, plan 998 run 1): `git worktree add --detach` and `tools/build_product.sh truck_diesel_eu` on `main@36f44a4`: all steps ok, 0 warnings, links `blob/36f44a4…`; also on a worktree branch with its own commit. `analyse/utils.py` follows the `.git` file to `gitdir` / `commondir`.

### CL-02 `.c` file without compile-database entry skipped silently

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0 and ubc 0.35.0 (preprocessor with explicit `compile_commands`)
- **Marker:** `main@36f44a4` `tests/CMakeLists.txt` — `foreach(component IN ITEMS vcu chg eng)` → `IN ITEMS chg eng` (old marker `main@e744d72` no longer reproduces, plan 998 run 1).
- **Wrong output:** markers of `tests/vcu/test_vcu.c` disappear without a message. Expected: a warning "file not in compile database".
- **Workaround:** every traced `.c` file is built by CMake.
- **Solution A:** warn per skipped file.
- **Solution B:** fall back to `includes` / `defines` (as for headers) with an info.
- **Status:** open on Sphinx-Codelinks 2.0.0 / ubc 0.37.0 (2026-10-17, plan 998 run 1): the marker `main@e744d72` no longer reproduces (its `tests/vcu/test_vcu.c` has no markers). New marker `main@36f44a4` `tests/CMakeLists.txt`: `foreach(component IN ITEMS vcu chg eng)` → `IN ITEMS chg eng`; all `TEST_VCU_*` disappear in both tools without a message about `test_vcu.c`.

### CL-03 `remote-url` / `local-url`: different meaning in the two exports

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0 and ubc 0.35.0
- **Marker:** `content/cv-platform@25b77bd`, product `truck_bev_nmc_eu`,
  `IMPL_VCU_ENERGY_DISPLAY` in `build/site/truck_bev_nmc_eu/{ubc,sphinx}.needs.json`
  (after `tools/build_product.sh truck_bev_nmc_eu`). Checked 2026-10-09.
- **Summary:** both tools fill the same two fields with different kinds of
  values. Sphinx-Codelinks stores only `path#Lline` and builds the URL at
  render time (`directives/src_trace.py`: `needs_string_links` with
  `remote_url_pattern.format(commit=…)`), so its HTML links are correct but its
  `needs.json` carries no URL. ubc stores the finished URLs, including an
  absolute path of the build machine. A consumer of `needs.json` (ubTrace,
  reports, diffs between the toolchains) cannot use one rule for both.
- **Input:** `[codelinks] set_local_url = true`, `set_remote_url = true`,
  `remote_url_pattern = "https://github.com/PhilipPartsch/variant_demo/blob/{commit}/{path}#L{line}"`.
- **Wrong output:**
  ```
  ubc    remote-url = https://github.com/PhilipPartsch/variant_demo/blob/b0a203be10f1…/src/vcu/energy_display.c#L8
         local-url  = file:///Users/<user>/…/variant_demo/src/vcu/energy_display.c#L8
  Sphinx remote-url = src/vcu/energy_display.c#L8
         local-url  = ../../vcu/energy_display.c#L8   (→ generated page vcu/energy_display.html#L-8)
  ```
  Expected: one documented meaning per field in both exports — e.g.
  `remote-url` = finished URL, `local-url` = path relative to the project root —
  and no machine-specific paths in `needs.json`.
- **Workaround:** comparisons ignore both fields (`tools/eval_expect.py`, parity check by id).
- **Solution A:** both tools export the resolved `remote-url` and a
  project-relative `local-url`; the HTML builders derive their links from these.
- **Solution B:** keep the raw `path#Lline` in one field (`source_path`) and the
  resolved URL in another (`remote-url`), in both tools; never export `file://` paths.
- **Status:** changed in Sphinx-Codelinks 2.0.0 (2026-10-17, plan 998 run 1): `remote-url` is now the same full GitHub URL in both exports (`blob/<commit>/src/vcu/energy_display.c#L8`). Still open: `local-url` is `file:///<absolute path>` in ubc and `../../vcu/energy_display.c#L8` in Sphinx. DOC-10 compares `remote-url` now (`fix/tool-workarounds`, `PARITY` in `tools/tests/test_l3_docs.py`); `local-url` stays ignored.

### CL-04 Broken CSS path on generated source pages

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0
- **Marker:** `content/cv-platform@25b77bd`, `tools/build_product.sh truck_bev_nmc_eu`,
  page `build/site/truck_bev_nmc_eu/sphinx/vcu/energy_display.html`. Checked 2026-10-09
  (first seen in plan 1, E-R F-7).
- **Summary:** `sphinx_extension/source_tracing.py:141` calls
  `app.add_css_file("_static/source_tracing/ub_sct.css")`. Sphinx expects a path
  relative to the static directory and prepends `_static/` itself, so every
  generated source page links `_static/_static/…` (404). The file is copied
  correctly (`builder_inited`) to `_static/source_tracing/ub_sct.css`. The CSS
  positions the "back" links of the source view (`.viewcode-back`
  `position: absolute; right: 0`), so without it they sit inline — cosmetic.
- **Input:** any `src-trace` directive; codelinks generates one HTML source page per traced file.
- **Wrong output:**
  ```html
  <link rel="stylesheet" type="text/css" href="../_static/_static/source_tracing/ub_sct.css" />
  ```
  on all 8 source pages of `truck_bev_nmc_eu` (`vcu/*.html`, `chg/*.html`);
  expected `../_static/source_tracing/ub_sct.css`.
- **Workaround:** none (cosmetic).
- **Solution A:** `app.add_css_file("source_tracing/ub_sct.css")` (one-line fix).
- **Solution B:** register the CSS once in `setup()` / `builder_inited` for all
  pages (it is tiny) instead of per page in `html-page-context`.
- **Status:** open on Sphinx-Codelinks 2.0.0 (2026-10-17, plan 998 run 1): all 8 source pages reference `../_static/_static/source_tracing/ub_sct.css` (`source_tracing.py:171`).

### CL-05 Packed refs: warnings and links to `blob/None`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0 (`set_remote_url = true`)
- **Marker:** `content/cv-platform@25b77bd`: fresh clone, configure
  `truck_bev_nmc_eu`, `git pack-refs --all`, `sphinx-build -b html docs build/s`.
  Reproduced 2026-10-09 (same clone without `pack-refs` as the control).
- **Summary:** `analyse/utils.py` `get_current_rev()` reads `.git/HEAD` and then
  the loose ref file `.git/<ref>`. After `git gc` / `git pack-refs` (also run by
  git's automatic `gc --auto`) the branch ref exists only in `.git/packed-refs`,
  so no revision is found. `directives/src_trace.py` then formats
  `remote_url_pattern` with `commit=None`: every source link in the HTML points
  to `…/blob/None/…`. A detached HEAD (CI checkouts) is handled; the next commit
  on the branch writes a loose ref again, so the state comes and goes.
- **Input:** `.git/HEAD` = `ref: refs/heads/content/cv-platform`; that ref only in `.git/packed-refs`;
  `remote_url_pattern = "https://github.com/PhilipPartsch/variant_demo/blob/{commit}/{path}#L{line}"`.
- **Wrong output:**
  ```
  WARNING: …/.git/refs/heads/content/cv-platform does not exist          (×4, one per codelinks project → -W fails)
  HTML: https://github.com/PhilipPartsch/variant_demo/blob/None/src/vcu/energy_display.c#L8
  ```
  Expected (control, loose ref): `…/blob/25b77bd78ac9185b00a8a8fce6c21152e620edc7/src/vcu/energy_display.c#L8`, no warning.
  Without `-W` the build succeeds with broken links.
- **Workaround:** none needed so far (a fresh clone keeps the checked-out
  branch as a loose ref; CI uses a detached HEAD); before a release build check
  that no link contains `blob/None`.
- **Solution A:** as CL-01 A — let git resolve the revision (`git rev-parse HEAD`).
- **Solution B:** fall back to `.git/packed-refs` when the loose ref is missing,
  and never format the pattern with `None` (omit the remote link and warn once).
- **Status:** **fixed in Sphinx-Codelinks 2.0.0** (2026-10-17, plan 998 run 1): with the branch only in `packed-refs` (`git pack-refs --all` at `25b77bd`, `git gc` on `main@36f44a4`) `sphinx-build -W` passes, links `blob/<commit>`; `get_current_rev()` falls back to `_packed_ref()`. The `blob/None` note of WEB-03 is removed (`fix/tool-workarounds`).

### CL-06 Duplicate need id in code aborts the build

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 1.4.0 (with Sphinx-Needs 8.5.0); ubc 0.35.0 is not affected
- **Marker:** `content/cv-platform@25b77bd` `src/vcu/energy_display.c:7,16,25` —
  remove `#if` / `#else` / `#endif` (and rename the second function), configure
  `truck_bev_nmc_eu`, `sphinx-build -b html docs build/a`. Reproduced 2026-10-09
  (formerly SN-04; first seen in plan 3, V12b probe).
- **Summary:** `directives/src_trace.py:320` calls `sphinx_needs.api.add_need()`
  without catching `InvalidNeedException`. The Sphinx-Needs directive does catch
  it (`directives/need.py:207`) and warns with a location. A duplicate id from a
  code marker therefore crashes the whole build instead of producing a warning
  that points to the C file and line.
- **Input:** two active markers with the same id:
  ```c
  // @need: Show remaining energy (state of charge), IMPL_VCU_ENERGY_DISPLAY, [SWREQ_VCU_ENERGY_DISPLAY]
  …
  // @need: Show remaining energy (fuel level), IMPL_VCU_ENERGY_DISPLAY, [SWREQ_VCU_ENERGY_DISPLAY]
  ```
- **Wrong output:**
  ```
  File "sphinx_needs/api/need.py", line 717, in add_need
      raise InvalidNeedException("duplicate_id", message)
  sphinx_needs.exceptions.InvalidNeedException: A need with ID 'IMPL_VCU_ENERGY_DISPLAY' already exists. [duplicate_id]
  → exit code 2, no HTML
  ```
  Expected (as for the same duplicate in RST, control in the same clone):
  `src/vcu/energy_display.c:17: WARNING: Need could not be created: A need with ID 'IMPL_VCU_ENERGY_DISPLAY' already exists.`
  and the build continues (fails only with `-W`). ubc reports `warning[needs.duplicate]` with the location.
- **Workaround:** none needed — alternatives in code always use `#if` / `#else` (C§5 rule 6).
- **Solution A:** wrap `add_need()` in `src_trace.py` with `try / except InvalidNeedException` and log a warning with the marker's file and line.
- **Solution B:** check marker ids for duplicates in the analysis step (before `add_need`) and report all duplicates of a project at once.
- **Status:** fixed in Sphinx-Codelinks 2.0.0 (2026-10-14, Solution A): `src/vcu/energy_display.c:15: WARNING: one-line need 'IMPL_VCU_ENERGY_DISPLAY' is already defined in document 'subsystems/vcu/code_trace': not created again … [codelinks.duplicate_need]`, the build continues (fails only with `-W`). Test NEG-16, `feat/choose@f9a2deb`.
- **Re-check:** still fixed on Sphinx-Codelinks 2.0.0 (2026-10-17, plan 998 run 1): NEG-16 (`tools/tests/test_l5_negative.py:134`) passes in the full run.

### CL-07 `Unsupported Git host` warning although `remote_url_pattern` is set

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** Sphinx-Codelinks 2.0.0 (same code in 1.4.0, not run); ubc 0.37.0 is not affected
- **Marker:** `main@36f44a4`, any product with code markers, e.g. `truck_bev_nmc_eu`;
  `git remote set-url origin <local path>` (as after `git clone --no-local`, or with
  a self-hosted host). Found 2026-10-17 in plan 998 run 1 (full build in a shadow clone).
- **Summary:** `analyse/utils.py` `form_https_url()` parses the host of `origin`
  for every marker, also when the project sets `remote_url_pattern`. An unknown
  host gives a warning per marker without a location; the links themselves are
  correct, because the configured pattern is used.
- **Input:** `git remote set-url origin /path/to/variant_demo`, then
  `tools/build_product.sh truck_bev_nmc_eu` (Sphinx with `-W`).
- **Wrong output:** 14 × `WARNING: Unsupported Git host: None [codelinks.git_host]`
  (50 over four products), `build finished with problems … (with warnings treated as errors)`;
  `remote-url` is `https://github.com/PhilipPartsch/variant_demo/blob/36f44a4…/src/vcu/energy_display.c#L8`
  anyway. ubc gives no warning and the same URL. Expected: no warning when
  `remote_url_pattern` is set.
- **Workaround:** keep `origin` on the GitHub URL (plan 998 §4.1 sets it in the shadow clone).
- **Solution A:** skip the host lookup when `remote_url_pattern` is set.
- **Solution B:** warn once per project, with the configuration as location.

## 7. sphinx-mounts

### SM-01 Bare boolean condition: abort vs warning

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-mounts 0.2.0 (vs ubc 0.35.0)
- **Marker:** `main@e744d72` `ubproject.toml:62` — change a rule to `if = "var.charging.mcs"`.
- **Wrong output:** sphinx-mounts aborts the build; ubc warns and excludes the rule. Expected: the same behaviour (and both accept `var.charging.mcs`, or both reject it with the same message).
- **Workaround:** always `== True` (enforced by `tools/check_variants.py`).
- **Solution A:** accept bare booleans in both.
- **Solution B:** same diagnostic code and severity in both (error), pointing to `== True`.
- **Status:** changed in sphinx-mounts 0.3.0 / ubc 0.37.0 (2026-10-17, plan 998 run 1): both tools now give the same message (`var.charging.mcs` is used as a condition on its own … compare it, e.g. `== True`), but sphinx-mounts still aborts (`VariantRuleError`, exit 2) while ubc warns `config.variant_source_invalid_condition` and excludes the rule. `tools/check_variants.py` stays.

## 8. useblocks/ubc-action

### UA-01 Linux runners only

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** useblocks/ubc-action
- **Marker:** — (plan 6, A§2.2; not used yet).
- **Summary:** the action installs ubc only on Linux runners; macOS / Windows jobs cannot run `ubc`.
- **Solution A:** support macOS / Windows (the extension already ships ubc for them).
- **Solution B:** document a manual install route (download URL per platform, checksum).
- **Status:** open (2026-10-17, plan 998 run 1): `useblocks/ubc-action` main is still `393f60b` (tag 0.1); `action.yml` fails on non-Linux runners.

### UA-02 Unpinned nested action, binary in the workspace

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** useblocks/ubc-action @ `393f60bb24e9988cd62f2044e4e200ad253395a7` (main, 2026-03-25)
- **Marker:** `ci/pages@0400fa4` `.github/actions/setup/action.yml` (step `ubc`
  with `uses: useblocks/ubc-action@393f60b…`), run
  https://github.com/PhilipPartsch/variant_demo/actions/runs/38045904775 (2026-10-10).
- **Summary:** the composite action calls `actions/cache@v4` by tag. A repository
  that requires all actions to be pinned to a full-length commit SHA (GitHub
  setting "Require actions to be pinned to a full-length commit SHA", B§3.4 R7)
  rejects the whole action, although the caller pins `ubc-action` itself. The
  action also downloads `ubc` into the working directory (an untracked file in
  the checkout) and verifies no checksum.
- **Input:** `uses: useblocks/ubc-action@393f60bb24e9988cd62f2044e4e200ad253395a7` with `version: "0.35.0"`.
- **Wrong output:** `##[error]The action actions/cache@v4 is not allowed in PhilipPartsch/variant_demo because all actions must be from a repository owned by PhilipPartsch, created by GitHub, or match one of the patterns: astral-sh/setup-uv@*, useblocks/ubc-action@*. All actions must also be pinned to a full-length commit SHA.` — every job using the action fails in setup.
- **Workaround:** download `ubc` directly from the same URL into `$RUNNER_TEMP`, check a pinned SHA-256 (`ci/pages`, `.github/actions/setup/action.yml`).
- **Solution A:** pin `actions/cache` (and every nested action) to a commit SHA inside ubc-action.
- **Solution B:** publish checksums next to the binaries and let the action verify them and install outside the workspace (`$RUNNER_TOOL_CACHE`).
- **Status:** open (2026-10-17, plan 998 run 1): unchanged `393f60b`; `actions/cache@v4` by tag, download into the workspace, no checksum.

**This repository:** `.github/workflows/ci-main.yml` / `ci-release.yml` (setup: `.github/actions/setup/action.yml`) do not use the action; it
downloads `ubc` directly into `$RUNNER_TEMP` (the UA-02 workaround), but
without the SHA-256 check, and uses `actions/checkout@v4` /
`actions/upload-artifact@v4` by tag. Not a tool bug; a hardening follow-up
(plan 998 §5).

## 9. Sphinx-Test-Reports

Evaluated in plan 110 (`sphinx-test-reports` 2.0.0 on 2026-10-12; 3.0.0 with
`ub-test-reports` 1.1.0 on 2026-10-14). Not used in the repository yet, so the
markers point to a scratch copy based on `main@54e862c` with the repository
inputs named.

### STR-01 CTest `status="disabled"` reported as passed

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-test-reports 2.0.0; `ub-test-reports` 1.1.0 (`ub_test_reports/junitparser.py:247-256`), used by the converter and the 3.0.0 directives
- **Marker:** scratch copy based on `main@54e862c`; CTest as in `tests/CMakeLists.txt` with one case `DISABLED TRUE`.
- **Summary:** a CTest case without a result child is read as passed unless it is googletest's `status="notrun"` / `result="suppressed"`.
- **Input:** CTest `--output-junit` with `set_tests_properties(T PROPERTIES DISABLED TRUE)` → `<testcase … status="disabled">` without a result child.
- **Wrong output:** `result: passed` (converter and `test-file` directive). Expected `disabled` / `skipped`.
- **Workaround:** none needed yet (no disabled tests).
- **Solution A:** treat every `status` other than `run` (`disabled`, `notrun`) as not passed.
- **Solution B:** a CTest dialect (as for googletest), detected by `cmake_labels` / `<testsuite name="(empty)">`.
- **Status:** open on sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 / ubc 0.37.0 (2026-10-17, plan 998 run 1): CTest `status="disabled"` → `passed` in the converter and in the `test-file` directive (ubc and Sphinx); `junitparser.py` unchanged.

### STR-02 Converter ignores the configured prefix; IDs fail a strict `id_regex`

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-test-reports 2.0.0; `ub-test-reports` 1.1.0 (`needs_export.py:227`, `identity.py:71-93`)
- **Marker:** scratch copy based on `main@54e862c`; `id_regex` as in `ubproject.toml:32`.
- **Summary:** `test-reports build needs` builds case ids as `<need_type>__<class>__<name>_<hash5>` with a lower-case hash; `[test_reports.case] prefix` is not used.
- **Input:** `[test_reports] deterministic_case_ids = true`, `[test_reports.case] prefix = "TRES_"` (all six keys), `[test_reports.build.needs] need_type = "test_result"`, `test-reports build needs -o out.json cm.xml`.
- **Wrong output:** `test_result__TEST_A__TEST_A_isagy`. Expected `TRES_…` and an id that can match `^[A-Z]+_[A-Z][A-Z0-9_]*$`. (The 3.0.0 directives build upper-case ids from the `test-file` id instead, see plan 110 E13.)
- **Workaround:** `[[needs.external_needs]] id_prefix`; neither tool checks imported ids (UB-17).
- **Solution A:** the converter uses `[test_reports.case].prefix` and the directives' id scheme.
- **Solution B:** an id template option (e.g. `{prefix}{name}`) for cases whose name is already unique.
- **Status:** open on sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 (2026-10-17, plan 998 run 1): with `[test_reports.case] prefix = "TRES_"` the converter writes `test_result__TEST_A__TEST_A_isagy`.

### STR-03 Type declared in `[[needs.types]]` and `[test_reports.case]` aborts Sphinx

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-test-reports 2.0.0 and 3.0.0 with sphinx-needs 8.5.0 / 9.0.0 `needs_from_toml`
- **Marker:** scratch copy based on `main@54e862c`; type `test_result` as in `ubproject.toml` (`[[needs.types]] directive = "test_result"`).
- **Summary:** STR registers the case type with `add_need_type`, which fails when the type already comes from `[[needs.types]]`. ubc accepts both declarations; Pharaoh needs the `[[needs.types]]` one (PH-12).
- **Input:** one `ubproject.toml` with `[[needs.types]] directive = "test_result"` and `[test_reports.case] type = "test_result"`.
- **Wrong output:** `NeedsApiConfigException: test_result already exists as need type`; the build aborts. Expected: reuse the declared type, or a typed `test_reports.*` warning.
- **Workaround:** declare the type only in `[test_reports.case]` (costs PH-12).
- **Solution A:** skip `add_need_type` when the type already exists with compatible settings.
- **Solution B:** `[test_reports.case]` references an existing `[[needs.types]]` entry.
- **Status:** open on sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 / Sphinx-Needs 9.0.0 (2026-10-17, plan 998 run 1): `test_result` in `[[needs.types]]` and `[test_reports.case]`: `NeedsApiConfigException: test_result already exists as need type`, exit 2; ubc accepts it.

### STR-04 `test-results` summary: `Errors: -1` in Sphinx, `0` in ubc

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-test-reports 3.0.0 (directive `test-results`), ubc 0.37.0
- **Marker:** scratch copy based on `main@54e862c`; any CTest `junit.xml` (`tools/build_product.sh:32`).
- **Summary:** CTest writes no `errors` attribute on `<testsuite>`. Sphinx shows the parser's "unknown" value, ubc shows 0.
- **Input:** `.. test-results:: p1/junit.xml` on a CTest file.
- **Wrong output:** Sphinx HTML `Tests: 3, Failures: 1, Errors: -1, Skips: 0`; ubc HTML `… Errors: 0 …`. Expected the same value, and `0` (or "n/a") rather than `-1`. Also `Skips: 0` although the file has `disabled="1"` (STR-01).
- **Workaround:** use a `needtable` instead of `test-results`.
- **Solution A:** count `<error>` children when the attribute is missing (as ubc does).
- **Solution B:** show "n/a" for a missing attribute in both tools.
- **Status:** open on sphinx-test-reports 3.0.0 / ub-test-reports 1.1.0 / ubc 0.37.0 (2026-10-17, plan 998 run 1): `test-results` shows `Errors: -1` in Sphinx, `Errors: 0` in ubc; `Skips: 0` in both although the file has `disabled="1"` (STR-01).


### STR-05 Renamed case directive: ubc ignores the rename, Sphinx accepts it

- **Origin:** external (`PhilipPartsch/variant_demo`); markers point there.
- **Tool:** sphinx-test-reports 3.0.0 with Sphinx-Needs 9.0.0, ubc 0.37.0
- **Marker:** scratch copy based on `main@36f44a4` (plan 110 §4.3 `dir` project).
  Found 2026-10-17 in plan 998 run 1.
- **Summary:** `[test_reports.case] directive` renames the case directive in
  Sphinx; ubc keeps `test-case` and does not know the new name, so needs written
  with the new directive exist only in Sphinx. ubc warns, so it is a declared
  limitation, but it breaks parity silently on the Sphinx side.
- **Input:** `[test_reports.case] directive = "tcase"` (other keys as in `dir`), and
  `.. tcase:: Case A by hand` with `:id: TRES_HAND`, `:file: p1/junit.xml`, `:case: TEST_A`.
- **Wrong output:** ubc `warning[config.test_reports_rename_unsupported] … the directive
  keeps its name 'test-case'` and `warning[block.directive_unknown] … 'tcase'`, 8 needs;
  Sphinx no warning, 9 needs (with `TRES_HAND`). Expected: both accept the rename,
  or both reject it. Pitfall nearby: `directive = "test_result"` (the type name)
  makes Sphinx warn `directive 'test_result' is already registered`.
- **Workaround:** keep the default directive name `test-case`.
- **Solution A:** ubc supports the rename.
- **Solution B:** STR warns that the rename is not supported by ubc (same code as ubc).

### STR-06 Docs name the need types `test-case`, the tools create `testcase`

- **Origin:** product_demo
- **Tool:** Sphinx-Test-Reports 3.0.0 (docs), ubc 0.37.0
- **Marker:** branch `feat/engineering-model` (plan 001 P2, uncommitted): `docs/ubproject.toml`
  `[test_reports]`, `tests/test_results.rst`, `docs/schemas.json` `$defs/type-test-case`.
- **Summary:** the configuration docs list the default need types as
  `test-file` / `test-suite` / `test-case`; both ubc and Sphinx create
  `testfile` / `testsuite` / `testcase` (`needs.json` `type`). A schema rule
  with `select` `type == "test-case"` silently validates nothing.
- **Workaround:** `"const": "testcase"`; negative test (wrong `executes` target) confirms the rule fires in both toolchains.
- **Solution A:** fix the docs table (directive `test-case`, type `testcase`).
- **Solution B:** warn when a schema `select` names a type that no need type declares.

### STR-07 JUnit file not a build dependency: stale results in incremental builds

- **Origin:** product_demo
- **Tool:** Sphinx-Test-Reports 3.0.0 (Sphinx 9.1.0)
- **Marker:** branch `feat/engineering-model` (plan 001 P8, uncommitted) and a scratch clone with the lockout chain committed: `tests/test_lockout.py` added, `ubc script tests` rewrote `tests/_results/junit.xml`, then `sphinx-build -W -b html . _build` (incremental).
- **Summary:** the `test-file` page kept the previous results — the two new
  cases (`TSPEC_LOCKOUT`) were missing, so the schema rule
  `cov-tspec-result` reported `TSPEC_LOCKOUT` as not executed; `ubc` showed
  them. A clean build (`sphinx:clean`) showed both.
- **Expected:** the JUnit file is registered as a dependency of the document (`env.note_dependency`), so a changed file rebuilds the page.
- **Workaround:** the `sphinx` script builds with `-E` (fresh environment).
- **Solution A:** `note_dependency` for every `:file:` of `test-file` / `test-results`.
- **Solution B:** document that test reports need a fresh build.

