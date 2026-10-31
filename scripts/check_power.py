#!/usr/bin/env python3
"""Check plugin.json and mcp.json: valid JSON, the fields the Kiro form asks for, the vendored skill.

Standard library only. The published schemas at agent-plugins.org are fetched when the network allows
and the required fields they name are checked too.
"""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def schema_required(url: str) -> list[str]:
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:  # noqa: S310
            return list(json.load(resp).get("required", []))
    except Exception as err:  # noqa: BLE001
        print(f"check_power: schema {url} not fetched ({err}), checking the local list only")
        return []


def main() -> int:
    problems: list[str] = []
    plugin = load("plugin.json")
    for field in ("$schema", "name", "version", "description", "author", "keywords", "license", "homepage", "repository"):
        if field not in plugin:
            problems.append(f"plugin.json: {field} is missing")
    for field in schema_required(plugin.get("$schema", "")):
        if field not in plugin:
            problems.append(f"plugin.json: {field} is required by its schema")
    if not plugin.get("author", {}).get("name"):
        problems.append("plugin.json: author.name is missing")
    if not plugin.get("keywords"):
        problems.append("plugin.json: keywords activate the power and must not be empty")
    mcp = load("mcp.json")
    for field in schema_required(mcp.get("$schema", "")):
        if field not in mcp:
            problems.append(f"mcp.json: {field} is required by its schema")
    server = mcp.get("mcpServers", {}).get("faxforagents", {})
    if server.get("command") != "npx" or server.get("args") != ["-y", "faxforagents-mcp"]:
        problems.append("mcp.json: the server must run npx -y faxforagents-mcp")
    if server.get("env", {}).get("FAXFORAGENTS_API_KEY") != "${FAXFORAGENTS_API_KEY}":
        problems.append("mcp.json: the key must come from ${FAXFORAGENTS_API_KEY}")
    skill = ROOT / "skills" / "fax-for-agents" / "SKILL.md"
    if not skill.is_file() or not skill.read_text(encoding="utf-8").startswith("---\nname: fax-for-agents\n"):
        problems.append("skills/fax-for-agents/SKILL.md is missing or its frontmatter does not start with the name")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for needle in ("https://faxforagents.com/privacy", "hello@faxforagents.com"):
        if needle not in readme:
            problems.append(f"README.md must carry {needle} (the Kiro form asks for a privacy policy and support contact)")
    for problem in problems:
        print(f"check_power: FAIL: {problem}", file=sys.stderr)
    if not problems:
        print("check_power: OK")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
