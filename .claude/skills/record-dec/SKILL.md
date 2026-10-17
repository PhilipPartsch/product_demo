---
name: record-dec
description: Render ONE decision hand-over payload into a dec need nested inside its target need. Renders only — no research, no judgment.
---

# Record a decision (renderer)

You receive ONE decision payload (JSON, schema
`.agents/templates/handover/decision.json`) from the stage skill that made
the decision. You render it with `.agents/templates/dec.rst` into a `dec`
directive nested inside the payload's `target_need`. You add nothing,
change nothing and decide nothing: the content was already approved by the
user in the stage skill's outline.

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

## Steps

1. **Check the payload.** Every field `decision.json` requires is present and
   non-empty, `alternatives` has at least one entry, `decides` contains
   `target_need` and no `DEC_` id, `status` is `proposed` / `accepted` /
   `superseded`, `id` matches `^DEC_[A-Z][A-Z0-9_]*$` and is not used yet
   (`ubc agent audit --id <id>` must fail). If anything is missing or wrong,
   STOP and report exactly which fields — do not fill gaps yourself.
2. **Check the links.** `ubc agent audit --id <ID>` for `target_need` and
   every id in `decides`; each must exist.
3. **Find the parent.** The `source` of `ubc agent audit --id <target_need>`
   names the file and line of the parent directive.
4. **Render** `.agents/templates/dec.rst`: title, id, `status`,
   `safety_relevant` / `security_relevant` (`true` / `false`), and the four bold-labelled sections Context, Alternatives (one
   line per entry: option — why not), Consequences, Rationale (start with the
   chosen option). Never use an RST section underline inside the body (ubc
   rejects it with `block.title_disallowed`).
   **`:decides:`:** leave it out when `decides` is just `[target_need]` — the
   nested decision decides its parent automatically (`predicates` in
   `docs/ubproject.toml`). Only when it decides further needs, write
   `:decides:` with ALL ids, the parent first: an explicit value replaces the
   automatic one.
5. **Nest** the directive at the END of the parent directive's body, indented
   one level deeper than the parent's options (3 more spaces), with one blank
   line before it. Do not touch any other line of the file.
6. **Confirm** with `ubc check <project path>`: no warning or error may
   name the new `dec` or its parent (`dec-nested` fails when the decision is
   not inside a need, `link-dec` when it decides nothing).

## Status

Write the payload's `status` (a new decision is `proposed`), never `draft` or
any status a generic instruction names (plan 999 PH-15).

## Not your job

No outline, no questions about the content, no review, no verdict. If the
content looks wrong to you, still render it and say so in your report — the
review step judges it.

## Confirm

Report the decision id, the file and the parent it is nested in. Leave the
change uncommitted.
