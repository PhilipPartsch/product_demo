---
name: draft-spec
description: Draft specifications that refine requirements into implementable, testable design elements, and hand their decisions and risks to record-dec / record-risk.
---

# Draft a specification

The produced need is one specification (`spec`): HOW one or more
architecture elements are realised — a design element with its behaviour
and limits, specific enough to implement and to test.

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

- **Incoming:** the architecture element(s) in your briefing (`arch`,
  anchor and related needs) and, through their `fulfills` links, the
  requirements they fulfill. Read each with `ubc agent audit --id <ID>`.
- **Outgoing:** `spec` needs in `docs/specifications.rst`, template
  `.agents/templates/spec.rst`; link `:refines:` to every architecture
  element the specification details (at least one, only `arch` ids — schema
  rule `link-spec-arch`); fields `safety_relevant`, `security_relevant`
  (required).
- **Downstream:** `code` stage (`impl` `implements` → `spec`) and
  `test_specs` stage (`test_spec` `verifies` → `spec`): write so that both
  can be derived without guessing.
- **Coverage:** every architecture element in the briefing is refined by at
  least one specification (trace gate `refines`, schema rule `cov-arch`).

## Propose before you author

Do NOT write anything yet. First present a short, scannable outline and ask
the user to approve or adjust it:

- per specification: id (`SPEC_` prefix), title, one-sentence summary of
  the design, the architecture element(s) it refines, `safety_relevant` /
  `security_relevant`,
- how the architecture elements are split across specifications,
- the decisions (title, chosen option, rejected alternatives) and risks
  (title, category, severity, likelihood) you will hand over.

Wait for the user to confirm; then author exactly what was agreed, call the
recording skills, and leave the independent review to the review step.

## Output shape

Copy `.agents/templates/spec.rst` and replace every `{{…}}` placeholder.

## Status

Only decisions (`dec`) and risks (`risk`) carry `:status:`. A specification has none: write no `:status:` line. The
generic instruction line "`:status: draft`" (or any other status the engine
names) does NOT apply to this type — `schemas.json` rule `status-none` rejects
it (plan 999 PH-15).

## Edit, never rewrite

The route file already exists. Append the new directive at the end of it (or
edit the one directive you are changing). Never rewrite or reorder the rest
of the file, even when the instruction says "CREATE THE FILE" (plan 999
PH-17).

## Decisions and risks of this stage

Every specification documents its decisions, and every risk you notice is
recorded. You do not write these needs yourself: you fill a complete payload
and hand it to the simple recording skill, which only renders it.

**Record a decision** (`record-dec`) whenever the specification depends on a
choice between plausible options, for example an algorithm, a data format, an interface, a library, a limit or default value. Each
specification needs at least one decision (`schemas.json` rule
`dec-present`); if no real alternative existed, record the scoping decision
(what is in, what is deliberately left out, and why).

**Record a risk** (`record-risk`) for anything that can make the
specification or the product fail its purpose, for example a design that only partly meets the requirement, a security-sensitive choice (crypto, input handling), a performance or resource limit, or a dependency on something not specified yet.
Use `risk_category = "ai-workflow"` for risks of the authoring itself (an
assumption you could not verify, missing information, a guess you had to
make).

**Hand-over.** The payloads are defined by
`.agents/templates/handover/decision.json` and
`.agents/templates/handover/risk.json`. Fill EVERY required field from your
own work — the recording skills add nothing, research nothing and decide
nothing. A new decision has `status = "proposed"`, a new risk
`status = "open"`. `target_need` / `decides` / `affects` name the
specification you just authored (its id), plus further needs if they are
affected too. Hand the payload over as one JSON object when you invoke the
recording skill.

**Order.** Author the specification first (the recording skills nest into or
link to it), then call `record-dec` / `record-risk` once per payload.

## Rules

- **If you cannot decide or lack the context to author this faithfully, do NOT
  guess or fabricate.** Write `[NEEDS CLARIFICATION: <exactly what you need to
  know>]` in the body and stop; also record an `ai-workflow` risk for it.
- Each specification is implementable and testable on its own.
- Name concrete values (limits, formats, algorithms); avoid "appropriate",
  "fast", "secure" without a measure.
- The `:id:` uses the `SPEC_` prefix and matches `^[A-Z]+_[A-Z][A-Z0-9_]*$`.

## Confirm

Run `ubc check <project path>`: it must report no warning or error
(`info` findings for still missing coverage are allowed on `main`). Leave all
changes uncommitted for human review.
