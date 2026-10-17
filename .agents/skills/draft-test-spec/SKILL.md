---
name: draft-test-spec
description: Draft test specifications that verify specifications, write the pytest test that executes each one, and hand their decisions and risks to record-dec / record-risk.
---

# Draft a test specification

The produced need is one test specification (`test_spec`): how one
specification is verified — preconditions, inputs and steps, observable pass
criteria. You also write the pytest test that executes it, so the test result
links back to it.

Pass `-p <project path>` on every `ubc agent` command. `<project path>` is the
directory that holds the target `ubproject.toml` (here `docs/`). Resolve it once
from the briefing you were handed and reuse it on every call.

When these instructions say `ubc`, run the exact version-matched `ubc` the
harness named in the task, not a bare `ubc` from your PATH, and never one
you install yourself. With no path given, use the `ubc` on your PATH.

## Use the briefing and the tools — do NOT spelunk the filesystem

The briefing in your prompt already contains the anchor need, the upstream
needs and the resolved route. For one need's full detail run
`ubc agent audit --id <ID> -p <project path>`; for its linked needs run
`ubc agent context --id <ID> --no-code -p <project path>`. Prefer these over
reading `.rst` files.

## Incoming and outgoing needs

- **Incoming:** the specification(s) in your briefing (`spec`). Read each
  with `ubc agent audit --id <SPEC_ID>`; the `implements_back` links name the
  code (`impl`) under test.
- **Outgoing:**
  - `test_spec` needs in `docs/verification.rst`, template
    `.agents/templates/test_spec.rst`; link `:verifies:` to the specification
    (only `spec` ids — schema rule `link-tspec-spec`); fields `test_level`
    (`unit` / `integration` / `system`), `safety_relevant`,
    `security_relevant` (all required);
  - one pytest test per test specification in `tests/`, template
    `.agents/templates/test.py`, with
    `record_property("executes", "<TSPEC_ID>")` — it becomes the `executes`
    link of the test result (schema rules `link-result-tspec`,
    `cov-tspec-result`).
- **Coverage:** every specification in the briefing is verified by at least
  one test specification (trace gate `verifies`, schema rule
  `cov-spec-test`), including the error cases it implies (review axis
  `spec_coverage`).

## Propose before you author

Do NOT write anything yet. First present a short, scannable outline and ask
the user to approve or adjust it:

- per test specification: id (`TSPEC_` prefix), title, `test_level`, the
  specification it verifies, the pass criteria in one line each,
  `safety_relevant` / `security_relevant`,
- the pytest test name and file for each,
- the decisions (title, chosen option, rejected alternatives) and risks
  (title, category, severity, likelihood) you will hand over.

Wait for the user to confirm; then author exactly what was agreed, call the
recording skills, and leave the independent review to the review step.

## Output shape

Copy `.agents/templates/test_spec.rst` and `.agents/templates/test.py` and
replace every `{{…}}` placeholder.

## Status

Only decisions (`dec`) and risks (`risk`) carry `:status:`. A test specification has none: write no `:status:` line. The
generic instruction line "`:status: draft`" (or any other status the engine
names) does NOT apply to this type — `schemas.json` rule `status-none` rejects
it (plan 999 PH-15).

## Edit, never rewrite

The route file already exists. Append the new directive at the end of it (or
edit the one directive you are changing). Never rewrite or reorder the rest
of the file, even when the instruction says "CREATE THE FILE" (plan 999
PH-17).

## Decisions and risks of this stage

Every test specification documents its decisions, and every risk you notice is
recorded. You do not write these needs yourself: you fill a complete payload
and hand it to the simple recording skill, which only renders it.

**Record a decision** (`record-dec`) whenever the test specification depends on a
choice between plausible options, for example the test level, mocking versus a real dependency, test data, or which error cases are covered. Each
test specification needs at least one decision (`schemas.json` rule
`dec-present`); if no real alternative existed, record the scoping decision
(what is in, what is deliberately left out, and why).

**Record a risk** (`record-risk`) for anything that can make the
test specification or the product fail its purpose, for example a case that cannot be tested automatically, a flaky or environment-dependent test, or a pass criterion that only proxies the real obligation.
Use `risk_category = "ai-workflow"` for risks of the authoring itself (an
assumption you could not verify, missing information, a guess you had to
make).

**Hand-over.** The payloads are defined by
`.agents/templates/handover/decision.json` and
`.agents/templates/handover/risk.json`. Fill EVERY required field from your
own work — the recording skills add nothing, research nothing and decide
nothing. A new decision has `status = "proposed"`, a new risk
`status = "open"`. `target_need` / `decides` / `affects` name the
test specification you just authored (its id), plus further needs if they are
affected too. Hand the payload over as one JSON object when you invoke the
recording skill.

**Order.** Author the test specification first (the recording skills nest into or
link to it), then call `record-dec` / `record-risk` once per payload.

## Rules

- **If you cannot decide or lack the context to author this faithfully, do NOT
  guess or fabricate.** Write `[NEEDS CLARIFICATION: <exactly what you need to
  know>]` in the body and stop; also record an `ai-workflow` risk for it.
- Pass criteria are observable; no "works correctly".
- Every test specification has exactly one pytest test that records its id
  as `executes`.
- The `:id:` uses the `TSPEC_` prefix and matches `^[A-Z]+_[A-Z][A-Z0-9_]*$`.

## Confirm

Run `ubc check <project path>` and `ubc script --path <project path> tests` (the new test must pass): it must report no warning or error
(`info` findings for still missing coverage are allowed on `main`). Leave all
changes uncommitted for human review.
