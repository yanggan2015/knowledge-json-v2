#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_system.py — 系统底层 12 领域完整教程内容。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from domains_100_config import DOMAINS_CONFIG
from _system_module_specs import MODULE_SNIPPETS, _fill_defaults
from _system_domain_overviews import DOMAIN_OVERVIEWS

# Populate all module snippets
import _populate_system_specs  # noqa: F401 — Linux内核
import _populate_system_specs_rest  # noqa: F401
import _populate_system_specs_rest2  # noqa: F401
import _populate_system_specs_rest3  # noqa: F401
import _populate_system_specs_rest4  # noqa: F401

OUTPUT = ROOT / "content_system.py"
SYSTEM_DOMAINS = [
    "Linux内核", "Linux系统编程", "操作系统原理", "计算机网络", "编译原理",
    "计算机组成原理", "汇编语言", "嵌入式系统", "驱动开发", "虚拟化技术",
    "容器技术", "实时系统",
]


def build_module_content() -> dict:
    content = {}
    for cfg in DOMAINS_CONFIG:
        if cfg["name"] not in SYSTEM_DOMAINS:
            continue
        domain = cfg["name"]
        for module in cfg["modules"]:
            key = (domain, module)
            raw = MODULE_SNIPPETS.get(key, {})
            content[key] = _fill_defaults(dict(raw), domain, module)
    return content


def serialize(content: dict, overviews: dict) -> str:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""系统底层领域手工教程内容库',
        "",
        "涵盖 Linux内核、Linux系统编程、操作系统原理、计算机网络、编译原理、",
        "计算机组成原理、汇编语言、嵌入式系统、驱动开发、虚拟化技术、容器技术、实时系统。",
        '"""',
        "",
        "from typing import Dict, Tuple",
        "",
        "MODULE_CONTENT: Dict[Tuple[str, str], dict] = {",
    ]
    for (domain, module), d in sorted(content.items()):
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        indented = "\n".join("    " + line if line else line for line in blob.split("\n"))
        lines.append(f"    ({domain!r}, {module!r}): {indented},")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("DOMAIN_OVERVIEWS: Dict[str, dict] = {")
    for name in SYSTEM_DOMAINS:
        d = overviews[name]
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        indented = "\n".join("    " + line if line else line for line in blob.split("\n"))
        lines.append(f"    {name!r}: {indented},")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def main():
    content = build_module_content()
    expected = sum(
        len(c["modules"]) for c in DOMAINS_CONFIG if c["name"] in SYSTEM_DOMAINS
    )
    if len(content) != expected:
        missing = []
        for cfg in DOMAINS_CONFIG:
            if cfg["name"] not in SYSTEM_DOMAINS:
                continue
            for m in cfg["modules"]:
                if (cfg["name"], m) not in content:
                    missing.append((cfg["name"], m))
        raise SystemExit(f"Expected {expected} modules, got {len(content)}. Missing: {missing[:10]}")
    OUTPUT.write_text(serialize(content, DOMAIN_OVERVIEWS), encoding="utf-8")
    print(f"Wrote {OUTPUT} — {len(content)} modules, {len(DOMAIN_OVERVIEWS)} overviews")


if __name__ == "__main__":
    main()
