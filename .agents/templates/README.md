# Need templates

One template per need type of the engineering model (plan 001 §5.2). Skills
copy the matching template and replace every `{{…}}` placeholder; nothing
else changes. Field values and links follow `docs/ubproject.toml` and
`docs/schemas.json`.

| Template | Type | Written by | Where |
|---|---|---|---|
| `us.rst` | `us` | `draft-us` | `docs/user_stories.rst` |
| `req.rst` | `req` | `draft-requirement` | `docs/requirements.rst` |
| `arch.rst` | `arch` | `draft-architecture` | `docs/architecture.rst` |
| `spec.rst` | `spec` | `draft-spec` | `docs/specifications.rst` |
| `test_spec.rst` | `test_spec` | `draft-test-spec` | `docs/verification.rst` |
| `dec.rst` | `dec` | `record-dec` | nested inside the need it decides |
| `risk.rst` | `risk` | `record-risk` | `docs/risks.rst` |
| `impl.py` | `impl` | `draft-impl` | `src/` (one-line marker) |
| `test.py` | test result | `draft-test-spec` | `tests/` (pytest, `executes` property) |
| `handover/decision.json` | — | stage skills → `record-dec` | payload schema |
| `handover/risk.json` | — | stage skills → `record-risk` | payload schema |

Links:

- `dec.rst` has no `:decides:` line: a nested decision decides its parent
  automatically (`predicates` on the `decides` link). Only a decision that
  decides further needs writes `:decides:` — with all targets, parent first.
- `risk.rst` is rendered with plain ids; `scripts/refresh_risk_links.py
  <RISK_ID>` then adds the hash conditions `TARGET[fp=="…"]` (the sign-off).
  A failed condition (`needs.link_condition_failed`) means the risk is stale:
  re-evaluate it, then run the script again.

Status: only `dec` (`proposed` / `accepted` / `superseded`) and `risk`
(`open` / `mitigated` / `accepted` / `closed`) carry `:status:`. No other
template has one, whatever a generic prompt says (`status-none` in
`schemas.json`).
