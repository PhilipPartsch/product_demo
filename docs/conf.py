import tomllib
from pathlib import Path

extensions = [
   "myst_parser",
   "sphinx_needs",
   ]

needs_from_toml = "ubproject.toml"

# Share the source excludes with ubCode: read `[source] extend_exclude` from
# ubproject.toml so both builds skip the same files (e.g. README.md).
with open(Path(__file__).parent / needs_from_toml, "rb") as f:
    _ubproject = tomllib.load(f)

exclude_patterns = [ *_ubproject.get("source", {}).get("extend_exclude", [])]
