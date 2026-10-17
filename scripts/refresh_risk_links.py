"""Refresh the hash conditions of risk links (sign-off after an evaluation).

Risks link to the needs they affect and to the needs that mitigate them with
a condition on the target's derived fingerprint `fp` (docs/ubproject.toml):

    :affects: SPEC_HASH[fp=="<fp of SPEC_HASH when the risk was evaluated>"]

When a target changes, its `fp` changes and the build reports
`needs.link_condition_failed`: the risk is stale and must be re-evaluated.
After the evaluation (the risk still holds, or was updated), this script
writes the targets' current `fp` into the risk's `affects` / `mitigated_by`
conditions in docs/risks.rst. Targets without a condition get one.

Usage:
  python3 scripts/refresh_risk_links.py RISK_ID [RISK_ID ...]
  python3 scripts/refresh_risk_links.py --all
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
RISKS = DOCS / "risks.rst"
LINKS = ("affects", "mitigated_by")
# One target: an id, optionally followed by a bracketed condition.
TARGET = re.compile(r"([A-Za-z0-9_]+)(\[[^\]]*\])?")


def fingerprints() -> dict[str, str]:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "needs.json"
        subprocess.run(
            ["ubc", "build", "needs", str(DOCS), "-o", str(out)],
            check=True,
            capture_output=True,
        )
        data = json.loads(out.read_text())
    needs = data["versions"][next(reversed(data["versions"]))]["needs"]
    return {nid: need.get("fp") for nid, need in needs.items()}


def refresh_value(value: str, fp: dict[str, str]) -> str:
    targets = []
    for match in TARGET.finditer(value):
        nid = match.group(1)
        if nid not in fp or not fp[nid]:
            raise SystemExit(f"unknown target or no fp: {nid}")
        targets.append(f'{nid}[fp=="{fp[nid]}"]')
    return ", ".join(targets)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    fp = fingerprints()
    lines = RISKS.read_text().split("\n")
    current = None
    wanted = None if args == ["--all"] else set(args)
    changed = set()
    for i, line in enumerate(lines):
        if line.startswith(".. "):
            current = None
        m = re.match(r"^   :id: (\S+)\s*$", line)
        if m:
            current = m.group(1)
        m = re.match(r"^(   :(" + "|".join(LINKS) + r"): )(.*)$", line)
        if m and current and (wanted is None or current in wanted):
            new = m.group(1) + refresh_value(m.group(3), fp)
            if new != line:
                lines[i] = new
                changed.add(current)
    missing = (wanted or set()) - {
        m.group(1) for line in lines if (m := re.match(r"^   :id: (\S+)", line))
    }
    if missing:
        raise SystemExit(f"not in {RISKS.relative_to(ROOT)}: {', '.join(sorted(missing))}")
    RISKS.write_text("\n".join(lines))
    print(f"refreshed: {', '.join(sorted(changed)) or 'nothing (already current)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
