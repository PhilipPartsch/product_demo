---
name: record-risk
description: Render ONE risk hand-over payload into a risk need appended to docs/risks.rst. Renders only — no research, no judgment.
---

# Record a risk (renderer)

You receive ONE risk payload (JSON, schema
`.agents/templates/handover/risk.json`) from the stage skill that found the
risk. You render it with `.agents/templates/risk.rst` and append it to
`docs/risks.rst`. You add nothing, change nothing and decide nothing: the
content was already approved by the user in the stage skill's outline.

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

1. **Check the payload.** Every field `risk.json` requires is present,
   `affects` has at least one id, the enums hold (`risk_category`,
   `severity`, `likelihood`, `status`), `mitigated_by` is non-empty when
   `status` is `mitigated`, `id` matches `^RISK_[A-Z][A-Z0-9_]*$` and is not
   used yet (`ubc agent audit --id <id>` must fail). An `accepted` risk needs
   an accepted decision that decides it — if the payload does not name one in
   `mitigation`, STOP. On any problem, STOP and report exactly which fields —
   do not fill gaps yourself.
2. **Check the links.** `ubc agent audit --id <ID>` for every id in
   `affects` and `mitigated_by`; each must exist, and `mitigated_by` names
   only `req` / `spec` / `test_spec` / `dec` needs.
3. **Render** `.agents/templates/risk.rst` with plain ids in `:affects:` /
   `:mitigated_by:` (comma-separated). Leave out the `:mitigated_by:` line
   when the list is empty. Bold labels Cause, Effect, Mitigation; never
   an RST section underline inside the body.
4. **Append** to the end of `docs/risks.rst`, one blank line before it. Never
   rewrite the file (plan 999 PH-17).
5. **Sign off the links:** run `python3 scripts/refresh_risk_links.py <id>`
   (from the repository root). It turns every target into
   `TARGET[fp=="<its current fingerprint>"]`, so a later change of an
   affected or mitigating need fails the condition
   (`needs.link_condition_failed`) and marks the risk stale.
6. **Confirm** with `ubc check <project path>`: no warning or error may
   name the new risk.

## Status

Write the payload's `status` (a new risk is `open`), never `draft` or any
status a generic instruction names (plan 999 PH-15).

## Not your job

No outline, no questions about the content, no review, no verdict. If the
content looks wrong to you, still render it and say so in your report — the
review step judges it.

## Confirm

Report the risk id and the needs it affects. Leave the change uncommitted.
