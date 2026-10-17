---
name: draft-requirement
description: Draft requirements from a user story, each a single shall-clause that satisfies it, and hand their decisions and risks to record-dec / record-risk.
---

<!-- Project skill (plan 001 P4 follow-up): replaces the installed vmodel
     `draft-requirement` with this project's pattern; removed from the install
     manifest, so `ubc agent update` must only run in a shadow clone
     (plan 998 T3). -->

# Draft a requirement

The produced need is one requirement (`req`): ONE obligation stated as a
single shall-clause, grounded in observable behaviour, satisfying the user
story it decomposes.

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

- **Incoming:** the user story in your briefing (`us`, the anchor). Read it
  with `ubc agent audit --id <US_ID>`.
- **Outgoing:** `req` needs in `docs/requirements.rst`, template
  `.agents/templates/req.rst`; link `:satisfies:` to the user story (only
  `us` ids — schema rule `link-req-us`); fields `safety_relevant`,
  `security_relevant` (required).
- **Downstream:** `specs` stage (`spec` `refines` → `req`): state WHAT, leave
  HOW to the specification.
- **Coverage:** the user story is satisfied by at least one requirement
  (trace gate `satisfies`, schema rule `cov-us`); decompose it completely —
  happy path, error and edge cases, relevant non-functional constraints.

## Propose before you author

Do NOT write anything yet. First present a short, scannable outline and ask
the user to approve or adjust it:

- per requirement: id (`REQ_` prefix), title, the shall-clause, the user
  story it satisfies, `safety_relevant` / `security_relevant`,
- how you split compound obligations and what you leave to a later stage,
- the decisions (title, chosen option, rejected alternatives) and risks
  (title, category, severity, likelihood) you will hand over.

Wait for the user to confirm; then author exactly what was agreed, call the
recording skills, and leave the independent review to the review step.

## Output shape

Copy `.agents/templates/req.rst` and replace every `{{…}}` placeholder.
The title is a few words saying what the requirement is about (not a
sentence, not a repeat of the body); the shall-clause is the body, written
once.

## Status

Only decisions (`dec`) and risks (`risk`) carry `:status:`. A requirement has none: write no `:status:` line. The
generic instruction line "`:status: draft`" (or any other status the engine
names) does NOT apply to this type — `schemas.json` rule `status-none` rejects
it (plan 999 PH-15).

## Edit, never rewrite

The route file already exists. Append the new directive at the end of it (or
edit the one directive you are changing). Never rewrite or reorder the rest
of the file, even when the instruction says "CREATE THE FILE" (plan 999
PH-17).

## Decisions and risks of this stage

Every requirement documents its decisions, and every risk you notice is
recorded. You do not write these needs yourself: you fill a complete payload
and hand it to the simple recording skill, which only renders it.

**Record a decision** (`record-dec`) whenever the requirement depends on a
choice between plausible options, for example how a compound wish is split, which quality level (a limit, a rate, a time) is required, or what is deliberately out of scope. Each
requirement needs at least one decision (`schemas.json` rule
`dec-present`); if no real alternative existed, record the scoping decision
(what is in, what is deliberately left out, and why).

**Record a risk** (`record-risk`) for anything that can make the
requirement or the product fail its purpose, for example an obligation that cannot be verified, a conflict with another requirement, a safety- or security-relevant obligation that is missing, or a user story that is too vague to decompose.
Use `risk_category = "ai-workflow"` for risks of the authoring itself (an
assumption you could not verify, missing information, a guess you had to
make).

**Hand-over.** The payloads are defined by
`.agents/templates/handover/decision.json` and
`.agents/templates/handover/risk.json`. Fill EVERY required field from your
own work — the recording skills add nothing, research nothing and decide
nothing. A new decision has `status = "proposed"`, a new risk
`status = "open"`. `target_need` / `decides` / `affects` name the
requirement you just authored (its id), plus further needs if they are
affected too. Hand the payload over as one JSON object when you invoke the
recording skill.

**Order.** Author the requirement first (the recording skills nest into or
link to it), then call `record-dec` / `record-risk` once per payload.

## Rules

- **If you cannot decide or lack the context to author this faithfully, do NOT
  guess or fabricate.** Write `[NEEDS CLARIFICATION: <exactly what you need to
  know>]` in the body and stop; also record an `ai-workflow` risk for it.
- One obligation per directive; no compound "and / or".
- Write `shall`, not `should` or `must`.
- No design detail in the body; that belongs to the specification.
- The `:id:` uses the `REQ_` prefix and matches `^[A-Z]+_[A-Z][A-Z0-9_]*$`.

## Confirm

Run `ubc check <project path>`: it must report no warning or error (`info`
findings for still missing coverage are allowed on `main`). Leave all changes
uncommitted for human review.
