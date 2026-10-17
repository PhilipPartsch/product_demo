# Plan 998: Re-check the tool bugs of plan 999 on new tool versions

Triggered re-run plan (not part of a numbered execution order). useblocks
releases new versions of its tools regularly. On each release, this plan
re-tests the entries of [999-tool-bugs.md](999-tool-bugs.md) on the new
version, records per entry whether it is still open, fixed or changed, and
lists the places in this repository that a fix affects.

Plan 999 was imported from the origin repository `PhilipPartsch/variant_demo`
(plan 999 header); all its entries are marked **external** and their markers
point there. The origin repository already re-tested them on 2026-10-17 (its
plan 998 run 1, Status lines in plan 999). This repository (`product_demo`)
is a small ubCode docs project in `docs/`. This plan therefore re-checks:

- entries marked **applies** or **latent** in plan 999 §2 — on this
  repository (its `docs/` project, or a scratch copy of it with the entry's
  input added);
- entries marked **n/a** — only when the origin repository is available (see
  §2), otherwise they keep their last status.

Its **first run here** re-tests every applies / latent entry on the
versions used today (ubc / ubCode 0.37.0, Sphinx-Needs as resolved by `uv`
for `sphinx-needs>=8.2`), so that each of them gets a Status line made in
this repository next to the external one.

Referenced: [999-tool-bugs.md](999-tool-bugs.md) (the record)

Rules that apply here:

- **ubc and Sphinx give the same result.** This repository builds with both
  (`ubc script ci`, `ubc script sphinx`, README "Build it"). Many entries are
  parity breaks; "fixed" means both toolchains agree again.
- **Tool bugs go into plan 999.** Plan 999 stays the only record of the
  entries. This plan records only its run log (§7); new findings of a run
  become new plan 999 entries in the same session, with markers of this
  repository.
- **The re-check does not touch the repository.** Work only in a shadow clone
  in the session scratchpad and delete it at the end (§4.6). Raising a
  version or changing the project is a follow-up (§5), never part of the run.
- Plan changes (998, 999) stay uncommitted until the user asks.

## 0. Goal

After each run:

- every re-checked entry in plan 999 has a **Status** line naming the version
  it was last checked on and the result (§3);
- every entry marked "applies?" or "Not verified yet" in plan 999 (UB-01,
  UB-05) is confirmed or corrected, and its **Here** column updated;
- every fixed entry names the version that fixed it, and the follow-up in this
  repository is listed (§5);
- every new problem found on the way is a new plan 999 entry.

## 1. Triggers

Run §4 when any of these happens:

| # | Trigger | How to notice | Entries to re-check (§6) |
|---|---|---|---|
| T1 | New ubCode extension / ubc release | `ls ~/.vscode/extensions/ \| grep useblocks.ubcode`; `"$UBC" --version`; ubCode changelog | §6.1, §6.2 |
| T2 | New Sphinx-Needs release | `curl -s https://pypi.org/pypi/sphinx-needs/json \| jq -r .info.version` | §6.3, and the parity entries of §6.1 (UB-06, UB-12, UB-15, UB-19) |
| T3 | Pharaoh profile update (`ubc agent` reinstalls skills, `profile_version` in `docs/.pharaoh/agent/install-manifest` changes) | `git diff` of the manifest and the skill copies | PH-09, PH-10, PH-11 |
| T4 | Release of a tool not used here (Sphinx-Codelinks, sphinx-mounts, Sphinx-Test-Reports, ubc-action) | as T2 for the package; `gh api repos/useblocks/ubc-action/commits/main --jq .sha` | n/a entries of that tool — only with the origin repository (§2) |
| T5 | useblocks reports a fix (release notes, issue replies) | release notes | the named entries |
| T6 | This repository adopts a feature that turns a **latent** entry into **applies** (e.g. a `[workflow]`, schemas, `id_regex`, external needs) | the change itself | the entries plan 999 §2 names for that feature |

**Sphinx-Needs is unpinned here** (`sphinx-needs>=8.2` in the `sphinx`
script, `docs/ubproject.toml:25`): every `ubc script sphinx` run picks up the
newest release, so T2 happens without notice. Check the resolved version on
each run (§4.2).

One-shot version check:

```bash
UBC="$(ls -d ~/.vscode/extensions/useblocks.ubcode-*/server/cli/ubc | sort -V | tail -1)"
"$UBC" --version
grep UBC_VERSION .github/workflows/docs.yml
for p in sphinx-needs sphinx-codelinks sphinx-mounts sphinx-test-reports ub-test-reports; do
  printf '%-22s %s\n' "$p" "$(curl -s "https://pypi.org/pypi/$p/json" | jq -r .info.version)"
done
```

Always call `"$UBC"`, never a bare `ubc`: the `ubc` on `PATH` can be an older
release (extensions 0.35.0, 0.36.0 and 0.37.0 are installed side by side). The
`[scripts]` in `docs/ubproject.toml` call a bare `ubc`, so put the tested
`ubc` first on `PATH` before `"$UBC" script …` (§4.2). Before a T1 run, also
search the ubCode docs (ubcode MCP `search_docs`) for the keywords of the
entries in scope: a documented fix or design decision changes the expected
result.

## 2. Scope

- **Re-checked here:** every applies / latent entry of the triggered tool(s)
  that is not marked fixed or resolved (§6).
- **Regression check (cheap):** applies / latent entries marked fixed (UB-04)
  are re-run only when the fix's area changed in the release notes, or when
  this repository starts to rely on the fix.
- **Origin-repository entries (n/a here):** re-checked only if a clone of
  `github.com/PhilipPartsch/variant_demo` is available (e.g. `../variant_demo`)
  and the user asks for it; then follow the markers of plan 999 in a shadow
  clone of that repository. Otherwise they keep their status, and the run log
  says "n/a entries not re-checked".
- **Full build:** on every run, `docs/` builds once with ubc and Sphinx on the
  new version and the two `needs.json` are compared (§4.4). This finds new
  problems and is the go / no-go input for a version raise.
- **Out of scope:** Sphinx itself, MyST-Parser, `uv`; changing the
  repository.

## 3. Status vocabulary

Each re-checked entry in plan 999 gets (or updates) one line, the same form
CL-06 already uses:

```
- **Status:** <result> on <tool> <version> (<date>, plan 998 run <n>, product_demo): <one sentence of evidence>.
```

The Status lines already in plan 999 come from the origin repository (they
name no `product_demo`). Keep them; add the line made here below them. For an
entry found in this repository, set `- **Origin:** product_demo` and the
**Origin** column of plan 999 §2 to `product_demo`.

| Result | Meaning | Overview table in plan 999 §2 |
|---|---|---|
| **open** | reproduced with the same wrong output | unchanged |
| **changed** | still wrong, but the output differs; update "Wrong output" | summary updated |
| **fixed in X** | the expected output from the entry is produced | append `— **fixed in X**` |
| **resolved** | the tool changed its design so the entry no longer applies (as UB-17) | append `— **resolved** with X` |
| **not reproducible** | the wrong output is gone, but no release note explains it; re-check the input before calling it fixed | append `— not reproducible on X` |
| **regression** | an entry marked fixed is wrong again | severity raised one level, append `— **regression in X**` |

Also update plan 999 §1: the "Version here" column, and the sentence about
which entries are re-tested (`re-tested on <versions>, <date>, plan 998`).
When a run confirms that an entry applies here, replace "applies?" /
"Not verified yet" in plan 999 by the result.

## 4. Run procedure

### 4.1 Shadow clone

```bash
S="<session scratchpad>/shadow998"      # never inside the repository
git clone --no-local "$PWD" "$S/repo"
git -C "$S/repo" remote set-url origin "$(git remote get-url origin)"
```

Use a clone, not `git worktree`, so nothing is written to the repository's
`.git`. Do not run `ubc script …` in the repository itself: it writes
`docs/_build/`, `docs/needs*.json` and `docs/.ub_cache/`; in the clone it is
fine.

### 4.2 Environment

```bash
export UBC="<path of the ubc to test>"              # T1; else the current one
export PATH="$(dirname "$UBC"):$PATH"               # the [scripts] call a bare `ubc`
"$UBC" --version
SN="<sphinx-needs version to test>"                 # T2; else the newest (what `>=8.2` resolves to)
UVRUN=(uv run --no-project --with "sphinx,sphinx-needs==$SN,myst-parser")
SPHINX=("${UVRUN[@]}" sphinx-build)
"${UVRUN[@]}" python -c 'import sphinx_needs, sphinx; print(sphinx_needs.__version__, sphinx.__version__)'
```

Run Sphinx with the explicit pin above instead of `ubc script sphinx`, so the
tested version is known; the script itself resolves `>=8.2` to the newest
release. For an older ubc to compare against, use the previous extension
folder in `~/.vscode/extensions/`. Record every version in the run log (§7).

Change one tool at a time where possible. If ubc and Sphinx-Needs change
together, first raise both, then for every entry that is now fixed or changed,
find out which of the two did it by reverting one.

### 4.3 Re-check the entries

For each entry in scope (§6 lists how to reproduce each one):

1. Start from `docs/` of the clone (`main` HEAD). For a **Marker here** entry
   use that marker; otherwise build the scratch project §6 describes: a copy
   of `docs/` under `$S/mini/<id>` with the entry's input added (e.g. a
   `[workflow]` stage, a schema rule, an `id_regex`).
2. Run the command the entry names, with the new version.
3. Compare with **Wrong output** and **Expected** of plan 999; pick the result
   from §3.
4. If the input of a latent entry cannot be expressed in this project without
   larger changes, write "not re-checked (latent, needs <feature>)" in the run
   log instead of a Status line.
5. A new marker in this repository must point to a pushed commit; if the
   reproduction needs content that is not committed, describe it as a scratch
   project in the entry.

### 4.4 Full build on the new version

```bash
cd "$S/repo/docs"
ubc script ci                                     # check --deny warning, then html
ubc build needs -o "$S/logs/ubc.needs.json"
"${SPHINX[@]}" -W -b html . _build                # what `ubc script sphinx` does
"${SPHINX[@]}" -b needs -D needs_build_json=1 . "$S/logs/sphinx"   # Sphinx needs.json
```

Compare the two exports by need id and by the fields used here (`status`,
`platform_note`, `implements`, `tests`), with absent = `[]` for links (UB-06)
and without `*_back` (UB-15) until those are fixed. Also build the variant of
the README (`-c 'needs.variant_data.platform = "windows"'`, and for Sphinx
`-D` or an edited `variants.json`) and check that `REQ_AUTH.status` resolves
to `win_auth` and that `edition` is kept (UB-05).

Run the same on the current versions first and keep both logs under
`$S/logs/`. Every new warning, failure or parity difference caused by the tool
is a candidate entry for plan 999. Reproduce it on a pushed commit (or as a
scratch project) before writing the entry.

### 4.5 Record

1. Plan 999: Status lines, overview table (columns **Origin** and **Here**),
   version table (§3); new entries at the end of their tool's section, with
   `- **Origin:** product_demo`.
2. This plan: one row per run in §7 and the per-entry results in §6 (column
   "Last check").
3. Report to the user: versions, fixed / changed / new entries, follow-ups
   (§5). Plan changes stay uncommitted.

### 4.6 Cleanup (mandatory)

```bash
rm -rf "$S"; test ! -e "$S" && echo removed
git status --short      # only the plan files 998 / 999 changed (other agents' files excepted)
```

## 5. Outcome → follow-up

| Outcome | Follow-up (never done inside the run) |
|---|---|
| Full build (§4.4) green on a new ubc | Propose a version raise on a feature branch: `UBC_VERSION` in `.github/workflows/docs.yml`, the local ubCode extension, and the versions named in `README.md` |
| Full build green on a new Sphinx-Needs | Update the comment "verified against sphinx-needs …" in `docs/ubproject.toml:24` (and `README.md:6` if the minimum changes); propose pinning an upper bound if a release broke the build before |
| Full build red because of a tool problem | New plan 999 entry; no version raise until there is a workaround. For Sphinx-Needs, propose an upper bound (`sphinx-needs>=8.2,<X`) in the `sphinx` script right away, since it is unpinned |
| UB-05 confirmed | Fix the README example (`README.md:44`, e.g. repeat `edition`, or use a second variants file) |
| PH-10 / PH-11 fixed by a new Pharaoh profile | Reinstall the skills (T3); the three copies (`.claude/skills`, `.agents/skills`, `.github/agents`) must stay identical to the manifest |
| Entry **fixed** and it is **latent** here | Nothing beyond the record; note it in plan 999 so the feature can be adopted without the workaround |
| Entry **changed** or **open** | Nothing beyond the record |
| CI hardening (plan 999 §8 note, not a tool bug) | Add a SHA-256 check for the `ubc` download and pin `actions/checkout` / `actions/upload-artifact` to commit SHAs in `.github/workflows/docs.yml` |

## 6. Entry checklist

How to reproduce each applies / latent entry in this repository, and what to
do when it is fixed. "scratch" means a copy of `docs/` under `$S/mini/<id>`
with the named input. Entries marked n/a in plan 999 §2 are not listed; they
follow their origin-repository markers (§2). Last check: the version the
result in plan 999 was made on (update after every run; "origin" = only the
external result from the origin repository's run 1 exists, nothing checked
here yet).

### 6.1 ubc / ubCode (T1, parity entries also T2)

| ID | Here | Reproduce | Fixed when | On fix | Last check |
|---|---|---|---|---|---|
| UB-01 | applies | `docs/`: `ubc build needs -o x.json`; look for `__source__`, `docname` | `docname` present, no absolute paths | — | origin: open 0.37.0 |
| UB-03 | latent | scratch: key `class` in `variants.json`, field `<<[var.class == "x"]: a, b>>` | ubc reports the keyword | — | origin: open 0.37.0 / SN 9.0.0 |
| UB-04 | latent | regression check only (§2): scratch, replace `variant_data_file` (`docs/ubproject.toml:55`) by `[variants] data_file` | variants loaded, or a diagnostic | the `[variants]` form may be used (fixed in the origin run) | origin: **fixed** 0.37.0 / SN 9.0.0 |
| UB-05 | applies? | `docs/`: the README override (`README.md:44`); check `edition` in the result | keys merged | README example stays as is | origin: open 0.37.0 (whole parent table replaced) |
| UB-06 | latent | `docs/`: §4.4 parity, `REQ_LOG` (no outgoing links) | `[]` written by ubc | parity compare without absent = `[]` | origin: open 0.37.0 / SN 9.0.0 |
| UB-09 | latent | scratch: ``:variant:`platform` `` in the body of `REQ_LOG`, `ubc build needs` | role text resolved | — | origin: open 0.37.0 |
| UB-12 | latent | scratch: `[needs.variants] win = "var.platform == 'windows'"`, `.. if:: win` | resolved in **both** tools | named variants may be used in `if` | origin: open 0.37.0 / SN 9.0.0 |
| UB-15 | latent | `docs/`: §4.4 parity, `REQ_AUTH` (`implements_back`, `tests_back`) | `<link>_back` exported | parity compare may include backlinks | origin: open 0.37.0 / SN 9.0.0 |
| UB-19 | latent | scratch: `id_regex = "^[A-Z]+_[A-Z][A-Z0-9_]*$"`, a need `:id: TEST_bad` | same need set in both tools | — | origin: open 0.37.0 / SN 9.0.0 |

### 6.2 Pharaoh (`ubc agent`, T1 / T3)

The latent entries need a `[workflow]` in the scratch copy, e.g. stages
`reqs` (`req`), `specs` (`spec`, trace `implements` up `req`), `tests`
(`test`, trace `tests` up `req` / `spec`), with `[quality.type_configs]`
pointing to `docs/quality/*.toml`. Use `ubc agent config-validate -p .` first;
a config that does not validate is part of the input, not a finding.

| ID | Here | Reproduce | Fixed when | On fix | Last check |
|---|---|---|---|---|---|
| PH-01 | latent | scratch + workflow: review `REQ_AUTH` with `platform = linux`, then `windows` (`:status:` differs) | both verdicts kept | — | origin: open 0.37.0 |
| PH-02 | latent | scratch + workflow: review `REQ_AUTH` under `linux`, brief under `windows` | fingerprint changes with the resolved `status` / `platform_note` | — | origin: open 0.37.0 |
| PH-03 | latent | scratch + workflow: change `REQ_AUTH`, compare fingerprints of `SPEC_HASH` and `TEST_AUTH` | consistent rule | — | origin: open 0.37.0 |
| PH-04 | latent | scratch + workflow: two stages with the same link + target, `direction = "both"` | trace attributed to both stages | — | origin: open 0.37.0 |
| PH-05 | latent | scratch + workflow: two stages producing `spec` on different routes | per-stage filter | — | origin: open 0.37.0 |
| PH-08 | latent | scratch + workflow: `ubc agent audit --id REQ_AUTH -p .` | fields (resolved) and all links shown | — | origin: open 0.37.0 |
| PH-09 | latent | scratch: add a project skill outside the manifest, change its `.agents` copy, `ubc agent doctor -p .` | `doctor` reports it | — | origin: open 0.37.0 |
| PH-10 | applies | any `review-brief` (scratch + workflow); read `submit_command` and the skills' text | `-p` in `submit_command`, `stale` documented | reinstall skills (T3) | origin: open 0.37.0 (skills v21) |
| PH-11 | applies | `.claude/skills/review-arch/SKILL.md:49`; scratch + workflow: `review-brief --ids A,B -p .` | comma list accepted, or skills corrected | reinstall skills (T3) | origin: open 0.37.0 (skills v21) |

### 6.3 Sphinx-Needs (T2)

| ID | Here | Reproduce | Fixed when | On fix | Last check |
|---|---|---|---|---|---|
| SN-01 | latent | scratch: a schema rule with `"severity": "warning"` that fails, `sphinx-build -W` | `warning` / `info` not a Sphinx warning | schemas may be adopted without `suppress_warnings` | origin: open 9.0.0 (`violation` now an error) |
| SN-05 | latent | scratch: schema `contains` on a list field without `items` | accepted | — | origin: open 9.0.0 |

## 7. Run log

| Run | Date | Trigger | Versions tested | Open / changed / fixed / new | Notes |
|---|---|---|---|---|---|
| origin 1 | 2026-10-17 | (origin repository `variant_demo`, external) | ubc 0.37.0, SN 9.0.0, CL 2.0.0, mounts 0.3.0, STR 3.0.0 / 1.1.0, ubc-action `393f60b` | 48 entries: 40 open, 3 changed (SN-06, CL-03, SM-01), 3 fixed (UB-04, CL-01, CL-05), 2 not reproducible (UB-07 HTML, UB-13); new: CL-07, STR-05 | imported with plan 999; results are the Status lines of the external entries |
| 1 | — | first run in this repository (plan 999 imported 2026-10-17; UB-01 / UB-05 unverified here) | ubc 0.37.0, Sphinx-Needs as resolved by `>=8.2` | — | open; n/a entries not re-checked (origin repository not available) |
