---
name: draft-architecture
description: Allocate requirements to architecture elements (components, interfaces) that fulfill them, keep the component diagram current, and hand risks and design decisions to record-risk / record-dec.
---

# Draft an architecture element

The produced need is one architecture element (`arch`): a component or
interface with its responsibility, its interfaces and — where relevant — the
trust boundary it sits on. It fulfills the requirement(s) it is responsible
for; specifications refine it.

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

- **Incoming:** the requirement(s) in your briefing (`req`). Read each with
  `ubc agent audit --id <REQ_ID>`; list the existing elements with
  `ubc build needs <project path> -o <temp file outside the repo>` (type
  `arch`) — extend an existing element instead of adding an overlapping one.
- **Outgoing:**
  - `arch` needs in `docs/architecture.rst`, template
    `.agents/templates/arch.rst`; link `:fulfills:` to every requirement the
    element is responsible for (only `req` ids — schema rule
    `link-arch-req`); fields `trust_boundary`, `safety_relevant`,
    `security_relevant` (all required);
  - the **component diagram** at the top of `docs/architecture.rst`
    (`.. mermaid::`, `flowchart TD`, one node per element, arrows for
    "uses"): create it below the page intro if it is missing, then add or
    change the nodes of the elements you author.
- **Downstream:** `specs` stage (`spec` `refines` → `arch`).
- **Coverage:** every requirement in the briefing is fulfilled by at least
  one element (trace gate `fulfills`, schema rule `cov-req`).

## Propose before you author

Do NOT write anything yet. First present a short, scannable outline and ask
the user to approve or adjust it:

- per element: id (`ARCH_` prefix), title, responsibility in one sentence,
  the requirement(s) it fulfills, `trust_boundary`, `safety_relevant` /
  `security_relevant`,
- the change to the component diagram,
- the decisions (title, chosen option, rejected alternatives) and risks
  (title, category, severity, likelihood) you will hand over.

Wait for the user to confirm; then author exactly what was agreed, call the
recording skills, and leave the independent review to the review step.

## Output shape

Copy `.agents/templates/arch.rst` and replace every `{{…}}` placeholder.

## Status

Only decisions (`dec`) and risks (`risk`) carry `:status:`. An architecture element has none: write no `:status:` line. The
generic instruction line "`:status: draft`" (or any other status the engine
names) does NOT apply to this type — `schemas.json` rule `status-none` rejects
it (plan 999 PH-15).

## Edit, never rewrite

The route file already exists. Append the new directive at the end of it (or
edit the one directive you are changing). Never rewrite or reorder the rest
of the file, even when the instruction says "CREATE THE FILE" (plan 999
PH-17).

## Decisions and risks of this stage

You do not write these needs yourself: you fill a complete payload and hand
it to the simple recording skill, which only renders it.

**Record a decision** (`record-dec`) when the architecture depends on a
choice between plausible options, for example how responsibilities are
split into components, a technology, or an interface style. Decisions on
architecture elements are **optional** (no `dec-present` rule) — record the
real choices, not a placeholder.

**Record a risk** (`record-risk`) for anything that can make the
architecture fail its requirements, for example a trust boundary without
input validation, a single point of failure, or an interface without a clear
owner. Use `risk_category = "ai-workflow"` for risks of the authoring itself.

**Hand-over.** The payloads are defined by
`.agents/templates/handover/decision.json` and
`.agents/templates/handover/risk.json`. Fill EVERY required field from your
own work — the recording skills add nothing, research nothing and decide
nothing. A new decision has `status = "proposed"`, a new risk
`status = "open"`. `target_need` / `decides` / `affects` name the element you
just authored.

**Order.** Author the architecture element first, then call `record-dec` /
`record-risk` once per payload.

## Rules

- **If you cannot decide or lack the context to author this faithfully, do NOT
  guess or fabricate.** Write `[NEEDS CLARIFICATION: <exactly what you need to
  know>]` in the body and stop; also record an `ai-workflow` risk for it.
- **Ground every element in what exists.** Responsibilities and interfaces
  come from the requirements in your briefing and from the existing code
  (`src/`, via the `impl` needs); do not invent features, protocols or
  interfaces they do not have (plan 002: an invented HTTP / session design
  cascaded into new specifications). A gap you see is a risk
  (`record-risk`), not new design.
- One responsibility per element; a requirement may be fulfilled by several
  elements, an element may fulfill several requirements.
- `trust_boundary: true` for every element that takes input from outside the
  product or changes privileges; its **Boundary** section says what crosses
  and how it is guarded (review axis `trust_boundary_addressed`).
- The `:id:` uses the `ARCH_` prefix and matches `^[A-Z]+_[A-Z][A-Z0-9_]*$`.

## Confirm

Run `ubc check <project path>`: it must report no warning or error
(`info` findings for still missing coverage are allowed on `main`). Leave all
changes uncommitted for human review.
