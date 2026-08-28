# -*- coding: utf-8 -*-
"""文章引擎 — 仅使用手工内容库，不读取 JSON 正文模板"""

from .patterns import detect_pattern_type, TYPE_LABELS, safe_filename
from .sanitize import sanitize_text, defensive_note
from .manual.registry import get_module_knowledge, get_domain_overview
from .manual.renderer import render_chapter, render_overview


def generate_chapter_article(chapter: dict, domain_data: dict) -> str:
    domain = domain_data["domain"]
    module = chapter["module"]
    title = chapter.get("title", module)
    difficulty = chapter.get("difficulty", "进阶")
    chapter_id = chapter.get("id", "")
    category = domain_data.get("category", "")

    knowledge = get_module_knowledge(domain, module, category)
    pattern_type = detect_pattern_type(title, module)

    related = [
        c.get("title", "") for c in domain_data.get("chapters", [])
        if c.get("module") == module and c.get("id") != chapter_id
    ][:5]

    return render_chapter(
        knowledge,
        title=title,
        difficulty=difficulty,
        chapter_id=chapter_id,
        pattern_type=pattern_type,
        related=related,
    )


def generate_overview_article(domain_data: dict) -> str:
    domain = domain_data["domain"]
    category = domain_data.get("category", "")
    prerequisites = domain_data.get("prerequisites", [])
    learning_path = domain_data.get("learning_path", [])
    modules = domain_data.get("modules", [])
    chapters = domain_data.get("chapters", [])
    total = domain_data.get("total_chapters", len(chapters))

    overview = get_domain_overview(domain, category, prerequisites, learning_path)

    diff_count: dict[str, int] = {}
    for c in chapters:
        d = c.get("difficulty", "进阶")
        diff_count[d] = diff_count.get(d, 0) + 1

    diff_table = "\n".join(
        f"| {d} | {n} | {n * 100 // max(total, 1)}% |"
        for d, n in sorted(diff_count.items())
    )

    chapters_by_module: dict[str, list] = {}
    for c in chapters:
        chapters_by_module.setdefault(c["module"], []).append(c)

    return render_overview(
        overview, modules, chapters_by_module, learning_path, diff_table
    )
