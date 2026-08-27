# -*- coding: utf-8 -*-
"""文章正文生成引擎 — 以高质量文字叙述为主"""

from .patterns import detect_pattern_type, TYPE_LABELS
from .knowledge import get_stack
from .diagrams import pick_diagram, learning_path_diagram
from .sanitize import sanitize_text, defensive_note
from .content_text import (
    expand_concepts,
    generate_body,
    expand_pitfalls,
    expand_practices,
    write_summary_section,
)


def generate_chapter_article(chapter: dict, domain_data: dict) -> str:
    """生成单章 Markdown 文章（纯文字为主）"""
    domain = domain_data["domain"]
    module = chapter["module"]
    title = sanitize_text(chapter.get("title", ""), domain)
    difficulty = chapter.get("difficulty", "进阶")
    pattern_type = detect_pattern_type(title, module)

    stack = get_stack(domain)
    concepts = [sanitize_text(c, domain) for c in chapter.get("core_concepts", [])]
    key_points = [sanitize_text(p, domain) for p in chapter.get("key_points", [])]
    references = [sanitize_text(r, domain) for r in chapter.get("references", [])]
    related = [sanitize_text(r, domain) for r in chapter.get("related_topics", [])]

    diagram = pick_diagram(domain, module, pattern_type, stack, concepts)
    concepts_text = expand_concepts(domain, module, concepts, pattern_type, chapter.get("id", ""))
    body = generate_body(domain, module, pattern_type, difficulty)
    pitfalls_text = expand_pitfalls(chapter.get("common_pitfalls", []), domain, module)
    practices_text = expand_practices(chapter.get("best_practices", []), domain, module)
    summary_text = write_summary_section(domain, module, title, pattern_type)

    # 实现要点段落
    key_points_section = ""
    if key_points:
        kp_actions = [
            "能向同事解释其原理与适用边界",
            "能在项目中正确配置并验证行为",
            "能阅读关键路径的实现或调用链",
            "能识别性能瓶颈并制定优化方案",
            "能设计错误处理与降级策略",
            "能编写测试用例覆盖主要场景",
        ]
        kp_lines = "\n".join(
            f"- **{p}** — 验收标准：{kp_actions[i % len(kp_actions)]}。"
            for i, p in enumerate(key_points[:6])
        )
        key_points_section = f"### 掌握标准\n\n{kp_lines}\n"

    parts = [
        f"# {title}",
        "",
        f"> **领域**：{domain} ｜ **模块**：{module} ｜ **难度**：{difficulty} ｜ **类型**：{TYPE_LABELS.get(pattern_type, '专题')}",
        "",
        defensive_note(domain),
        "## 导读",
        "",
        f"本章属于 **{domain}** 教程的 **{module}** 模块，难度为 **{difficulty}**。"
        f"阅读重点在于建立清晰的概念模型与工程判断能力，而非死记细节。",
        "",
        "## 核心概念",
        "",
        concepts_text,
        "",
        "## 架构与流程",
        "",
        "以下框图帮助你在宏观层面把握模块协作关系与处理流向：",
        "",
        diagram,
        "",
        "## 深度讲解",
        "",
        body,
        "",
    ]

    if key_points_section:
        parts.extend([key_points_section, ""])

    parts.extend([
        pitfalls_text,
        "",
        practices_text,
        "",
        summary_text,
        "",
    ])

    if related:
        parts.extend([
            "## 延伸学习",
            "",
            "建议结合以下同模块章节继续阅读，构建完整知识链：",
            "",
            "\n".join(f"- {r}" for r in related[:6]),
            "",
        ])

    if references:
        parts.extend([
            "### 参考资料",
            "",
            "\n".join(f"- {r}" for r in references[:5]),
            "",
        ])

    parts.extend([
        "---",
        f"*章节 ID: {chapter.get('id', '')} ｜ 领域: {domain} ｜ 版本: {domain_data.get('version', '2.0')}*",
    ])

    return "\n".join(parts)


def generate_overview_article(domain_data: dict) -> str:
    """生成领域概述文章"""
    domain = domain_data["domain"]
    category = domain_data.get("category", "")
    description = sanitize_text(domain_data.get("description", ""), domain)
    prerequisites = domain_data.get("prerequisites", [])
    learning_path = domain_data.get("learning_path", [])
    modules = domain_data.get("modules", [])
    chapters = domain_data.get("chapters", [])
    total = domain_data.get("total_chapters", len(chapters))
    stack = get_stack(domain)

    diff_count: dict[str, int] = {}
    for c in chapters:
        d = c.get("difficulty", "进阶")
        diff_count[d] = diff_count.get(d, 0) + 1

    diff_table = "\n".join(
        f"| {d} | {n} | {n * 100 // max(total, 1)}% |"
        for d, n in sorted(diff_count.items())
    )

    module_chapters: dict[str, list] = {}
    for c in chapters:
        m = c["module"]
        module_chapters.setdefault(m, []).append(c)

    index_lines = []
    for mod in modules:
        if mod not in module_chapters:
            continue
        index_lines.append(f"### {mod}")
        index_lines.append("")
        for c in module_chapters[mod]:
            cid = c.get("id", "")
            ctitle = sanitize_text(c.get("title", ""), domain)
            diff = c.get("difficulty", "")
            from .patterns import safe_filename
            fname = f"chapters/{cid}-{safe_filename(ctitle, 50)}.md"
            index_lines.append(f"- [{ctitle}]({fname}) ｜ {diff}")
        index_lines.append("")

    learning_diagram = learning_path_diagram(learning_path or modules[:8])

    intro_extra = (
        f"\n\n## 你将学到什么\n\n"
        f"完成本系列后，你将能够：\n\n"
        f"- 系统理解 **{domain}** 的核心概念与模块划分。\n"
        f"- 按难度递进掌握从入门到实战的完整知识路径。\n"
        f"- 在工程实践中做出合理的技术判断与问题排查。\n"
        f"- 通过章节索引快速定位所需知识点。\n"
    )

    parts = [
        f"# {domain} 学习指南",
        "",
        f"> **分类**：{category} ｜ **章节总数**：{total} ｜ **技术栈**：{stack['framework']}",
        "",
        defensive_note(domain),
        "## 领域概述",
        "",
        description,
        "",
        f"本教程基于 **{stack['lang']}** 与 **{stack['framework']}** 生态编写，"
        f"涵盖 {stack['ecosystem']} 等主流工具与框架。"
        f"每章独立成篇，文字精炼、逻辑清晰，适合系统学习与按需查阅。",
        intro_extra,
        "## 前置知识",
        "",
        "\n".join(f"- {p}" for p in prerequisites),
        "",
        "## 推荐学习路径",
        "",
        learning_diagram,
        "",
        "\n".join(f"{i+1}. **{step}**" for i, step in enumerate(learning_path or modules[:8])),
        "",
        "## 模块体系",
        "",
        "本领域按以下模块组织，难度由浅入深：",
        "",
        "\n".join(f"- **{m}**" for m in modules),
        "",
        "## 难度分布",
        "",
        "| 难度 | 章节数 | 占比 |",
        "|------|--------|------|",
        diff_table,
        "",
        "## 章节索引",
        "",
        "点击章节标题进入对应教程：",
        "",
        "\n".join(index_lines),
        "",
        "## 学习方法建议",
        "",
        "1. **先读概述再读章节**：用本指南建立全局地图，避免迷失在细节中。",
        "2. **按模块递进**：同一模块内章节有前后关联，顺序阅读效果更好。",
        "3. **主动复述**：每章读完后，用三五句话概括「是什么、为什么、怎么用」。",
        "4. **关联阅读**：利用章节底部的「延伸学习」在同模块内构建知识网络。",
        "5. **对照官方文档**：本教程提供结构化视角，细节以官方文档为准。",
        "",
        "---",
        f"*领域: {domain} ｜ 版本: {domain_data.get('version', '2.0')} ｜ 共 {total} 章*",
    ]

    return "\n".join(parts)
