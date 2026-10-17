import os
import tomllib
from pathlib import Path

extensions = [
   "myst_parser",
   "sphinx_needs",
   "sphinxcontrib.mermaid",
   "sphinx_codelinks",
   "sphinx_test_reports",
   "sphinx_mounts",
   # needflow diagrams (needs.flow_engine = "graphviz"); requires `dot`.
   "sphinx.ext.graphviz",
   ]

needs_from_toml = "ubproject.toml"

# Share the source excludes with ubCode: read `[source] extend_exclude` from
# ubproject.toml so both builds skip the same files (e.g. README.md).
with open(Path(__file__).parent / needs_from_toml, "rb") as f:
    _ubproject = tomllib.load(f)

exclude_patterns = [ *_ubproject.get("source", {}).get("extend_exclude", [])]

# Schema `info` findings mark incomplete work (coverage, decisions present):
# allowed on main, blocking only for a release (CI 2 reads
# schema_violations.json). Sphinx logs them as warnings, which `-W` would turn
# into errors, so they are suppressed here; they are still recorded.
suppress_warnings = ["sn_schema_info"]

# A stale risk (a hash-conditioned link whose target changed) is allowed on
# main and blocks a release (plan 001 G5): CI 1 sets CI_TIER=main to report it
# without failing `-W`. Locally and in CI 2 it fails the build.
if os.environ.get("CI_TIER") == "main":
    suppress_warnings.append("needs.link_condition_failed")
