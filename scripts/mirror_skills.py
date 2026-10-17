"""Mirror the project's own skills from .agents/skills to the other harnesses.

Own skills are the skills in .agents/skills/ that the Pharaoh install
manifest (docs/.pharaoh/agent/install-manifest) does not own; installed
skills are managed by `ubc agent update` and never touched here. Each own
skill .agents/skills/<name>/SKILL.md is copied byte for byte to

  .claude/skills/<name>/SKILL.md   (Claude Code)
  .github/agents/<name>.agent.md   (GitHub Copilot)

Usage:
  python3 scripts/mirror_skills.py          # write the copies
  python3 scripts/mirror_skills.py --check  # report drift, exit 1 if any (CI)
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / ".agents" / "skills"
MANIFEST = ROOT / "docs" / ".pharaoh" / "agent" / "install-manifest"


def installed_skills() -> set[str]:
    entries = json.loads(MANIFEST.read_text())["entries"]
    return {
        Path(e["path"]).parent.name
        for e in entries
        if e["path"].startswith(".agents/skills/")
    }


def targets(name: str) -> list[Path]:
    return [
        ROOT / ".claude" / "skills" / name / "SKILL.md",
        ROOT / ".github" / "agents" / f"{name}.agent.md",
    ]


def main() -> int:
    check = "--check" in sys.argv[1:]
    installed = installed_skills()
    own = sorted(
        d.name for d in SOURCE.iterdir() if d.is_dir() and d.name not in installed
    )
    drift = []
    for name in own:
        content = (SOURCE / name / "SKILL.md").read_bytes()
        for target in targets(name):
            if target.exists() and target.read_bytes() == content:
                continue
            if check:
                drift.append(target.relative_to(ROOT))
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
                print(f"wrote {target.relative_to(ROOT)}")
    if drift:
        print("Skill copies differ from .agents/skills (run scripts/mirror_skills.py):")
        for path in drift:
            print(f"  {path}")
        return 1
    print(f"{len(own)} own skill(s) in sync: {', '.join(own)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
