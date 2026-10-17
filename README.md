# ubCode engineering-model starter

An **empty, ready-to-use engineering model** in ubCode / Sphinx-Needs
(`docs/`): need types, links, schema, workflow stages, AI skills, templates,
quality packs, reports and a two-tier CI — no content yet. Put the product
code in `src/` and its tests in `tests/`, then author the needs stage by stage
with `ubc agent` (or by hand from the templates). It builds with both the
`ubc` CLI and an upstream Sphinx + Sphinx-Needs build.

The model was built and tried out with a demo product (login, lockout, audit
log) that was removed again (plan 003); `.agents/plans/` documents how it was
built and how to repeat it.

## What this project shows

- **A traced V-model.** User stories → requirements → architecture
  elements → specifications →
  implementations (one-line codelinks markers in `src/`) and test
  specifications → test results (pytest JUnit XML via Sphinx-Test-Reports).
  One link name per edge: `satisfies`, `fulfills`, `refines`, `implements`,
  `verifies`, `executes`.
- **Decisions and risks.** Decisions are nested inside the need they decide;
  risks link the needs they affect and the needs that mitigate them, with
  hash conditions that flag a risk as stale when a target changes.
- **Schema validation.** `docs/schemas.json` checks elements and links in
  both toolchains: violations always block, completeness findings (`info`)
  block only a release.
- **An agentic workflow.** `[workflow]` stages with author and review skills
  (`.agents/skills/`, mirrored for Claude Code and GitHub Copilot), templates
  (`.agents/templates/`) and quality packs (`docs/quality/`).
- **Build variants ("150% model").** `variants.json` plus inline
  `[needs.variant_data]` feed `<{ var.* }>` references.
- **Reports.** Decision and risk overviews (`docs/reports/`) and a starter
  Jinja2 report.

The model, the workflow, decisions / risks and the CI gates are documented in
`docs/engineering_model/`. The plans that built it are in `.agents/plans/`.

## Build it

Run the configured scripts from `docs/` with `ubc script <name>`:

```bash
ubc script tests       # pytest (no tests yet is fine); writes the JUnit XML the test-result needs come from
ubc script ci          # tests, then lint (ubc check), then the HTML site
ubc script sphinx      # build HTML with Sphinx + Sphinx-Needs (needs uv)
ubc script needs       # write needs.json
ubc script report      # render reports/needs_overview.html.j2
```

Run `ubc script tests` before any other build: without the JUnit XML the
test-result needs are missing.

## Work with the agents

```bash
cd docs
ubc agent status       # state of every workflow stage
ubc agent next         # the next action
ubc agent prompt       # that action as an instruction
ubc agent run          # execute it with the headless runner ([agent.runner])
```

After a risk was re-evaluated, sign off its links:
`python3 scripts/refresh_risk_links.py <RISK_ID>`. After editing a skill in
`.agents/skills/`, copy it to the other harnesses:
`python3 scripts/mirror_skills.py`. Never run `ubc agent update` in the
repository (see `.agents/plans/998-tool-bug-recheck.md` §4.7).

## Explore further

```bash
# Query needs with a filter expression (requires an active license):
ubc query filter "type == 'risk' and status == 'open'"

# Compare two build variants (note: `-c` replaces the whole nested table,
# plan 999 UB-05):
ubc build needs -o needs.linux.json
ubc build needs -c 'needs.variant_data = { edition = "pro", platform = "windows" }' -o needs.windows.json
ubc diff --needs needs.linux.json --needs needs.windows.json
```
