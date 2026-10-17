---
name: draft-impl
description: Implement specifications in src/ as one-line codelinks markers above real code, each implementing its specification, and hand risks and implementation decisions to record-risk / record-dec.
---

<!-- Project skill (plan 001 P4 follow-up): replaces the installed vmodel
     `draft-impl` with this project's pattern; removed from the install
     manifest, so `ubc agent update` must only run in a shadow clone
     (plan 998 T3). -->

# Draft an implementation

The produced need is one implementation (`impl`): a one-line codelinks
marker in the production source, directly above the code that realises one
specification. The marker materialises the need; the code beneath it is the
implementation.

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
  with `ubc agent audit --id <SPEC_ID>`; its `verifies_back` links name the
  test specifications the code has to pass.
- **Outgoing:** a marker + code in a Python module under `src/product_demo/`
  (template `.agents/templates/impl.py`), exactly this shape (all six fields
  required, positional):

  ```python
  # @<title>, IMPL_<NAME>, impl, [<SPEC_ID>], <safety_relevant>, <security_relevant>
  ```

  `<safety_relevant>` / `<security_relevant>` are `true` / `false`; the
  bracketed list names only `spec` ids (schema rule `link-impl-spec`).
- **Already in place — do not author:** the `src-trace` directive lives in
  `src/implementations.rst` and covers all of `src/`. Do NOT create
  `code_trace.rst` or any second `src-trace` for project `code`: every `impl`
  need would then exist twice.
- **Coverage:** every specification in the briefing is implemented by at
  least one marker (trace gate `implements`, schema rule `cov-spec-impl`).

## Propose before you author

Do NOT write any code or marker yet. First present a short, scannable outline
and ask the user to approve or adjust it:

- per implementation: id (`IMPL_` prefix), title, the specification it
  implements, the module and function / class, `safety_relevant` /
  `security_relevant`,
- the decisions (title, chosen option, rejected alternatives) and risks
  (title, category, severity, likelihood) you will hand over.

Wait for the user to confirm; then author exactly what was agreed, call the
recording skills, and leave the review to the tests and the review step.

## Status

Markers have no status field; write none anywhere (plan 999 PH-15).

## Edit, never rewrite

Add markers and code to existing modules or create a new module; never
rewrite unrelated code. Keep the code minimal and idiomatic.

## Decisions and risks of this stage

Implementations need no decision of their own, but record every real
implementation choice and every risk you notice. You do not write these
needs yourself: you fill a complete payload and hand it to the simple
recording skill, which only renders it.

**Record a decision** (`record-dec`) when the code depends on a choice the
specification left open, for example a library, a data structure, a
parameter value or an error-handling strategy. The marker is a comment and
cannot hold a nested need, so nest the decision in the **specification** you
implement: `target_need = <SPEC_ID>`, `decides = [<SPEC_ID>, <IMPL_ID>]`.

**Record a risk** (`record-risk`) for anything that can make the code fail
its specification, for example an unvalidated input, a security-sensitive
primitive, a platform dependency or missing error handling. Use
`risk_category = "ai-workflow"` for risks of the authoring itself (an
assumption you could not verify, a guess you had to make).

**Hand-over.** Payload schemas: `.agents/templates/handover/decision.json`,
`.agents/templates/handover/risk.json`. Fill EVERY required field from your
own work; the recording skills add nothing. A new decision has
`status = "proposed"`, a new risk `status = "open"`. Write the marker and
code first, then call `record-dec` / `record-risk` once per payload.

## Rules

- **If you cannot decide which specification an implementation realises, or
  lack the context, do NOT guess or fabricate.** Leave the marker out, say
  what is missing, and record an `ai-workflow` risk.
- One marker per implementation element; one specification per coherent unit
  (split distinct responsibilities).
- The `:id:` uses the `IMPL_` prefix and matches `^[A-Z]+_[A-Z][A-Z0-9_]*$`.
- No URL fields, no `@need-ids:` back-attach — this project uses one-line
  needs only.

## Confirm

Run `ubc script --path <project path> tests` (the tests of the verifying test
specifications must pass) and `ubc check <project path>` (no warning or
error). Leave all changes uncommitted for human review.
