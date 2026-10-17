# Plan 003: Remove the test data — leave an empty starter

The needs, code and tests built by plans 001 and 002 are test data
(user, 2026-10-17: "finally the repo shall not have test data inside the
repo"; the git history does not matter). This plan removes them from the
current state and keeps everything that makes the engineering model work,
so the repository becomes an **empty starter**: a configured model, workflow,
skills, templates, scripts, CI and documentation, ready for real content.

Referenced: [001-engineering-model.md](001-engineering-model.md),
[002-add-arch-level.md](002-add-arch-level.md),
[100-engineering-model-playbook.md](100-engineering-model-playbook.md).

Rules: as plan 001 (ubc and Sphinx agree; CI 1 and CI 2 stay green); branch
`feat/remove-test-data` off `main` after PR #3 (the user merged plan 002
**with** its content first, after CI 1 and CI 2 passed on GitHub); one PR.

## 1. What is test data

| Removed | What |
|---|---|
| need directives in `docs/user_stories.rst`, `requirements.rst`, `architecture.rst` (incl. the component diagram), `specifications.rst`, `verification.rst`, `risks.rst` | 3 `us`, 3 `req`, 3 `arch`, 3 `spec`, 3 `test_spec`, 15 nested `dec`, 8 `risk` |
| `src/product_demo/` | the demo package (hashing, audit log, lockout guard) with its `impl` markers |
| `tests/test_*.py` | the pytest tests (they produced the test-result needs) |
| `docs/.pharaoh/verdicts/*.json` | 38 review verdicts |

Kept: every page (with its intro), `src/implementations.rst` (`src-trace`),
`tests/test_results.rst` (`test-file`), `pyproject.toml`, configuration,
schema, quality packs, templates, skills, scripts, CI, reports, model docs,
plans, `docs/.pharaoh/gaps-baseline.json` (`[]`), variant data
(`variants.json`, `[needs.variant_data]`).

## 2. What depends on the content (checked in a scratch copy first)

| Depends | Empty state | Change |
|---|---|---|
| pytest | no tests → exit code 5, `ubc script tests` / CI fail; `junit.xml` is still written | `scripts/run_tests.py`: exit 5 ("no tests collected") counts as success |
| `test-file` page | empty JUnit file | none needed (builds in both toolchains) |
| `src-trace` | no markers | none needed |
| reports, model page `needflow` | empty tables / diagram | none needed (both builds `-W` clean) |
| `ubc agent` | `config-validate`, `doctor`, `trace`, `status` ok | none |
| CI gates | gaps 0, no verdicts, `schema_violations.json` empty | none |
| examples in docs | `SPEC_HASH`, `IMPL_HASH`, `RISK_SCRYPT_PARAMS` in the model / decisions-risks pages and the refresh script | generic placeholders |
| `draft-architecture` | edits the component diagram "at the top" of the page | creates the diagram when it is missing |
| README | describes the demo product | describes the empty starter |

## 3. Steps

1. Remove the test data (§1).
2. `scripts/run_tests.py` + `tests` script; examples, skill, README (§2).
3. Checks: CI 1 and CI 2 steps locally, both builds, `ubc agent next`
   briefs the first stage on the empty graph.
4. Plans: 001 / 002 notes ("content removed by plan 003"), playbook (the
   empty starter as a starting point), run log below.
5. Push the branch, PR, CI (CI 1 on the PR; CI 2 on a temporary
   `release/*` branch, deleted afterwards); the user merges.

## 4. Run log

### Run (2026-10-17, branch `feat/remove-test-data`)

- Removed: all need directives of the six content pages (incl. the
  component diagram), `src/product_demo/` (4 files), `tests/test_*.py` (3),
  `docs/.pharaoh/verdicts/*.json` (38).
- `scripts/run_tests.py` (pytest; exit 5 = no tests → 0; a failing test
  still exits 1 — checked); `tests` script uses it.
- Examples made generic (`SPEC_X`, `RISK_X`, `IMPL_LOGIN` / `SPEC_LOGIN`) in
  the model page, the decisions / risks page and `refresh_risk_links.py`;
  `draft-architecture` creates the component diagram when it is missing;
  README describes the empty starter.
- Found: with the `test-file` directive active, the empty JUnit file yields
  two test-result needs, and `ubc agent prompt` then refuses to brief the
  first stage (PH-24) → the directive stays in `tests/test_results.rst` as an
  RST comment; `draft-test-spec` activates it with the first test. Now 0
  needs; `ubc agent prompt` briefs "the FIRST artefact" with `draft-us`.
- Checks: CI 1 and CI 2 steps locally all green (also `--deny info`, empty
  `schema_violations.json`, `trace`).
- Findings → plan 999: PH-24 (998 §6.4 row).
