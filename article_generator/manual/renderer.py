# -*- coding: utf-8 -*-
"""将 ModuleKnowledge + 章节类型渲染为完整 Markdown 教程"""

from typing import Optional

from article_generator.patterns import TYPE_LABELS, detect_pattern_type
from article_generator.sanitize import defensive_note, sanitize_text

from .content_types import ModuleKnowledge, DomainOverview, Concept, Pitfall
from .diagrams_manual import pick_module_diagram


def _render_concepts(k: ModuleKnowledge) -> str:
    lines = [k.intro, "", "### 核心知识"]
    for i, c in enumerate(k.concepts, 1):
        lines.append(f"\n**{i}. {c.title}**\n\n{c.body}")
    return "\n".join(lines)


def _render_pitfalls(k: ModuleKnowledge) -> str:
    if not k.pitfalls:
        return ""
    lines = ["### 常见误区与纠正", ""]
    for p in k.pitfalls:
        lines.append(f"**{p.title}**\n\n{p.body}\n")
    return "\n".join(lines)


def _render_practices(k: ModuleKnowledge) -> str:
    if not k.practices:
        return ""
    lines = ["### 最佳实践", ""]
    for i, p in enumerate(k.practices, 1):
        lines.append(f"{i}. {p}")
    return "\n".join(lines)


def _render_references(k: ModuleKnowledge) -> str:
    if not k.references:
        return ""
    lines = ["### 延伸阅读", ""]
    for r in k.references:
        lines.append(f"- {r}")
    return "\n".join(lines)


def _section_deep(k: ModuleKnowledge, pattern_type: str, difficulty: str) -> str:
    """按章节类型选取最相关的深度段落"""
    mapping = {
        "fundamentals": ("基础理解", k.intro + "\n\n" + k.workflow if k.workflow else k.intro),
        "internals": ("实现机制", k.mechanism or k.internals),
        "key_techniques": ("关键技术", k.workflow or k.mechanism),
        "source_analysis": ("源码与实现", k.internals or k.mechanism),
        "configuration": ("配置实践", k.configuration or k.workflow),
        "troubleshooting": ("问题排查", k.debugging or k.mechanism),
        "performance": ("性能优化", k.performance),
        "best_practices": ("工程实践", "\n".join(k.practices) if k.practices else k.workflow),
        "advanced": ("高级应用", k.case_study or k.mechanism),
        "case_study": ("实战案例", k.case_study or k.workflow),
        "design_evolution": ("设计演进", k.internals or k.intro),
        "deep_internals": ("底层原理", k.internals or k.mechanism),
        "debugging": ("调试排错", k.debugging or k.mechanism),
        "security": ("安全实践", k.security),
        "comparison": ("对比选型", k.comparison),
    }
    title, body = mapping.get(pattern_type, ("深度讲解", k.mechanism or k.intro))
    if not body or len(body.strip()) < 80:
        body = k.mechanism or k.workflow or k.intro
    return f"### {title}\n\n{body.strip()}"


def render_chapter(
    k: ModuleKnowledge,
    title: str,
    difficulty: str,
    chapter_id: str,
    pattern_type: Optional[str] = None,
    related: Optional[list] = None,
) -> str:
    domain = k.domain
    module = k.module
    if pattern_type is None:
        pattern_type = detect_pattern_type(title, module)
    type_label = TYPE_LABELS.get(pattern_type, "专题")

    title = sanitize_text(title, domain)
    diagram = pick_module_diagram(domain, module, k)

    parts = [
        f"# {title}",
        "",
        f"> **领域**：{domain} ｜ **模块**：{module} ｜ **难度**：{difficulty} ｜ **类型**：{type_label}",
        "",
        defensive_note(domain),
        "## 导读",
        "",
        f"本章系统讲解 **{domain}** 中 **{module}** 的相关知识（{type_label}）。"
        f"内容基于主流框架与工程实践撰写，不依赖过时概念堆砌。",
        "",
        "## 核心知识",
        "",
        _render_concepts(k),
        "",
        "## 架构与流程",
        "",
        diagram,
        "",
        "## 技术详解",
        "",
        _section_deep(k, pattern_type, difficulty),
        "",
    ]

    pitfalls = _render_pitfalls(k)
    if pitfalls:
        parts.extend([pitfalls, ""])

    practices = _render_practices(k)
    if practices:
        parts.extend([practices, ""])

    parts.extend([
        "### 本章小结",
        "",
        f"学完本章，你应能独立说明 **{module}** 在 {domain} 中的角色，"
        f"理解其核心机制，规避常见误区，并在项目中正确运用。",
        "",
    ])

    if related:
        parts.extend([
            "## 延伸学习",
            "",
            "\n".join(f"- {sanitize_text(r, domain)}" for r in related[:5]),
            "",
        ])

    refs = _render_references(k)
    if refs:
        parts.extend([refs, ""])

    parts.append(f"---\n*章节 ID: {chapter_id} ｜ 领域: {domain}*")
    return "\n".join(parts)


def render_overview(o: DomainOverview, modules: list, chapters_by_module: dict, learning_path: list, diff_table: str) -> str:
    from article_generator.diagrams import learning_path_diagram

    domain = o.domain
    diagram = learning_path_diagram(learning_path or modules[:8])

    index_lines = []
    for mod in modules:
        chs = chapters_by_module.get(mod, [])
        if not chs:
            continue
        index_lines.append(f"### {mod}")
        index_lines.append("")
        for c in chs:
            cid = c.get("id", "")
            ctitle = sanitize_text(c.get("title", ""), domain)
            diff = c.get("difficulty", "")
            from article_generator.patterns import safe_filename
            fname = f"chapters/{cid}-{safe_filename(ctitle, 50)}.md"
            index_lines.append(f"- [{ctitle}]({fname}) ｜ {diff}")
        index_lines.append("")

    outcomes = "\n".join(f"- {x}" for x in o.outcomes)
    prereq = "\n".join(f"- {p}" for p in o.prerequisites)

    return "\n".join([
        f"# {domain} 学习指南",
        "",
        f"> **分类**：{o.category} ｜ **技术生态**：{o.ecosystem}",
        "",
        defensive_note(domain),
        "## 领域定位",
        "",
        o.intro,
        "",
        o.positioning,
        "",
        "## 学习目标",
        "",
        outcomes,
        "",
        "## 前置知识",
        "",
        prereq,
        "",
        "## 学习路径",
        "",
        diagram,
        "",
        "\n".join(f"{i+1}. **{s}**" for i, s in enumerate(learning_path or modules[:8])),
        "",
        "## 模块体系",
        "",
        "\n".join(f"- **{m}**" for m in modules),
        "",
        "## 难度分布",
        "",
        diff_table,
        "",
        "## 章节索引",
        "",
        "\n".join(index_lines),
        "",
        "---",
        f"*领域: {domain}*",
    ])
