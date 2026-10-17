"""CI gates on top of `ubc agent` (plan 001 P7).

The two CI tiers differ in what they allow (docs/engineering_model/ci.rst):

  main     (CI 1, PR / push to main): open topics allowed — missing reviews,
           open risks, proposed decisions; blocks new structural gaps
           (ratchet against docs/.pharaoh/gaps-baseline.json) and failing
           or malformed review verdicts.
  release  (CI 2, release/* and tags v*): nothing open — no gap at all,
           every verdict present, fresh and passing, no schema finding.

`ubc agent release-check` is not used for the main tier: it counts missing
reviews and open / proposed statuses as gaps, has no category filter, and
its baseline cannot be captured from a failing state (plan 999 PH-20).

Usage (from the repository root):
  python3 scripts/ci_gates.py gaps --tier main|release [--update-baseline]
  python3 scripts/ci_gates.py verdicts --tier main|release
  python3 scripts/ci_gates.py schema-json <sphinx outdir>/schema_violations.json
  python3 scripts/ci_gates.py stale-risks      # report, never fails
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BASELINE = DOCS / ".pharaoh" / "gaps-baseline.json"
# Allowed on main: work not done yet, not a broken structure.
OPEN_ON_MAIN = {"review", "status_disallowed"}


def agent(*args: str) -> dict:
    out = subprocess.run(
        ["ubc", "agent", *args, "-p", str(DOCS)], capture_output=True, text=True
    )
    return json.loads(out.stdout)


def key(gap: dict) -> str:
    return f"{gap['category']}:{gap['id']}:{gap['link']}"


def annotate(level: str, text: str) -> None:
    # GitHub Actions annotation; plain text elsewhere.
    print(f"::{level}::{text}")


def gaps(tier: str, update: bool) -> int:
    found = agent("gaps")["gaps"]
    if tier == "release":
        for gap in found:
            annotate("error", f"gap {key(gap)}")
        print(f"{len(found)} gap(s); a release needs none")
        return 1 if found else 0
    structural = {key(g) for g in found if g["category"] not in OPEN_ON_MAIN}
    accepted = set(json.loads(BASELINE.read_text())) if BASELINE.exists() else set()
    new = sorted(structural - accepted)
    for k in new:
        annotate("error", f"new structural gap {k}")
    for k in sorted(structural & accepted):
        annotate("warning", f"accepted debt {k}")
    open_items = [g for g in found if g["category"] in OPEN_ON_MAIN]
    print(
        f"{len(new)} new structural gap(s), {len(structural & accepted)} accepted, "
        f"{len(open_items)} open item(s) allowed on main"
    )
    if new:
        return 1
    if update:
        # Ratchet down: a fixed gap can never come back as accepted debt.
        BASELINE.parent.mkdir(parents=True, exist_ok=True)
        BASELINE.write_text(json.dumps(sorted(structural & accepted), indent=2) + "\n")
    return 0


def verdicts(tier: str) -> int:
    result = agent("verdict-check")
    blocking = ["failing", "malformed"]
    if tier == "release":
        blocking += ["missing", "outdated", "unverifiable"]
    problems = 0
    # `malformed` is a count (unreadable files have no need id), the others
    # are lists of need ids.
    malformed = result.get("malformed", 0)
    if malformed:
        annotate("error", f"{malformed} malformed verdict file(s) in docs/.pharaoh/verdicts")
        problems += 1
    for bucket in ["missing", "failing", "outdated", "unverifiable"]:
        for item in result.get(bucket, []):
            nid = item if isinstance(item, str) else item.get("need") or item.get("id")
            level = "error" if bucket in blocking else "notice"
            annotate(level, f"verdict {bucket}: {nid}")
            problems += bucket in blocking
    print(f"{problems} blocking verdict problem(s) for tier {tier}")
    return 1 if problems else 0


def schema_json(path: str) -> int:
    data = json.loads(Path(path).read_text())
    findings = data.get("validation_warnings") or {}
    for nid, items in sorted(findings.items()):
        for item in items:
            rule = item["details"].get("schema_path", "").split(" ")[0]
            annotate("error", f"schema {item['log_lvl']} {nid} {rule}")
    print(f"{sum(len(v) for v in findings.values())} schema finding(s) in {path}")
    return 1 if findings else 0


def stale_risks() -> int:
    out = subprocess.run(
        ["ubc", "check", str(DOCS)], capture_output=True, text=True
    ).stdout.splitlines()
    stale = 0
    for i, line in enumerate(out):
        if "needs.link_condition_failed" in line:
            where = next((l.strip() for l in out[i + 1 : i + 4] if ".rst:" in l), "")
            annotate("warning", f"stale risk link (re-evaluate, then refresh_risk_links.py): {where}")
            stale += 1
    print(f"{stale} stale risk link(s)")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    command = args[0]
    tier = args[args.index("--tier") + 1] if "--tier" in args else "main"
    if command == "gaps":
        return gaps(tier, "--update-baseline" in args)
    if command == "verdicts":
        return verdicts(tier)
    if command == "schema-json":
        return schema_json(args[1])
    if command == "stale-risks":
        return stale_risks()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
