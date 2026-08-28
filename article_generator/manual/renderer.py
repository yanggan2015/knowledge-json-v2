# -*- coding: utf-8 -*-
"""将 ModuleKnowledge + 章节类型渲染为完整 Markdown 教程"""

from typing import Optional

from article_generator.patterns import TYPE_LABELS, detect_pattern_type
from article_generator.sanitize import defensive_note, sanitize_text

from .content_types import ModuleKnowledge, DomainOverview, Concept, Pitfall
from .diagrams_manual import pick_module_diagram


PATTERN_INTROS = {
    "fundamentals": "本章建立 **{module}** 的概念模型与工作原理，是后续专题章节的基础。",
    "internals": "本章聚焦 **{module}** 的内部实现路径与关键数据结构，帮助从 API 用法深入到机制层。",
    "key_techniques": "本章归纳 **{module}** 在生产环境中最常用、最易出错的关键技术点。",
    "source_analysis": "本章沿源码与调用链剖析 **{module}** 的实现，适合需要排障或二次开发的读者。",
    "configuration": "本章讲解 **{module}** 的配置项含义、环境差异与验证方法，强调可重复部署。",
    "troubleshooting": "本章围绕 **{module}** 的典型故障现象、根因定位与修复步骤组织内容。",
    "performance": "本章从度量指标、瓶颈定位与优化手段三方面讲解 **{module}** 的性能议题。",
    "best_practices": "本章总结 **{module}** 在团队工程化中的约定、检查项与落地方式。",
    "advanced": "本章介绍 **{module}** 在复杂场景下的扩展用法与架构组合。",
    "case_study": "本章以真实工程案例串联 **{module}** 的选型、实现与复盘要点。",
    "design_evolution": "本章回顾 **{module}** 的设计动机、版本演进与当前生态中的位置。",
    "deep_internals": "本章从底层原理出发拆解 **{module}** 与运行时、内核或协议栈的交互。",
    "debugging": "本章提供 **{module}** 的调试工具链、日志/trace 解读与最小复现方法。",
    "security": "本章说明 **{module}** 相关的威胁面、防护基线与合规注意点。",
    "comparison": "本章对比 **{module}** 与主流替代方案的边界、成本与迁移路径。",
}


def _render_concepts(k: ModuleKnowledge, pattern_type: str) -> str:
    lines = [k.intro, "", "### 核心知识"]
    concepts = list(k.concepts)
    # 非基础章节突出与类型相关的条目，避免十篇章节完全雷同
    if pattern_type != "fundamentals" and len(concepts) > 3:
        focus_idx = {
            "internals": 1,
            "key_techniques": 2,
            "source_analysis": 1,
            "configuration": 0,
            "troubleshooting": 0,
            "performance": 0,
            "best_practices": 0,
            "advanced": 2,
            "case_study": 3,
            "design_evolution": 1,
            "deep_internals": 1,
            "debugging": 0,
            "security": 0,
            "comparison": 2,
        }.get(pattern_type, 0)
        ordered = [concepts[min(focus_idx, len(concepts) - 1)]] + [
            c for i, c in enumerate(concepts) if i != min(focus_idx, len(concepts) - 1)
        ]
        concepts = ordered[:4]
    for i, c in enumerate(concepts, 1):
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


def _section_block(title: str, body: str) -> str:
    if not body or len(body.strip()) < 20:
        return ""
    return f"### {title}\n\n{body.strip()}"


def _section_deep(k: ModuleKnowledge, pattern_type: str, difficulty: str) -> str:
    mapping = {
        "fundamentals": ("基础理解", k.intro + ("\n\n" + k.workflow if k.workflow else "")),
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


def _render_supplementary(k: ModuleKnowledge, pattern_type: str) -> list[str]:
    """补充章节：拉长篇幅并增加教学维度"""
    parts: list[str] = []

    mechanism_block = _section_block("工作机制", k.mechanism)
    internals_block = _section_block("内部实现", k.internals)
    if mechanism_block or internals_block:
        parts.extend(["## 原理与实现", "", mechanism_block or internals_block, ""])
        if mechanism_block and internals_block:
            parts.extend([internals_block, ""])

    workflow_block = _section_block("操作流程", k.workflow)
    config_block = _section_block("配置要点", k.configuration)
    if workflow_block or config_block:
        parts.extend(["## 操作流程与实践", "", workflow_block or config_block, ""])
        if workflow_block and config_block:
            parts.extend([config_block, ""])

    perf = _section_block("性能优化", k.performance)
    sec = _section_block("安全注意", k.security)
    dbg = _section_block("调试排错", k.debugging)
    extras = [x for x in [perf, sec, dbg] if x]
    if extras:
        parts.extend(["## 性能、安全与排查", "", "\n\n".join(extras), ""])

    case_block = _section_block("案例复盘", k.case_study)
    cmp_block = _section_block("方案对比", k.comparison)
    if case_block or cmp_block:
        parts.extend(["## 案例与选型", "", case_block or cmp_block, ""])
        if case_block and cmp_block:
            parts.extend([cmp_block, ""])

    # 按章节类型追加一段聚焦说明，减少同模块多章完全重复
    focus_notes = {
        "internals": (
            f"阅读 **{k.module}** 实现时，建议对照调用栈画出数据流："
            "入口 API → 核心数据结构 → 系统调用或 I/O 边界，标注锁与共享状态位置。"
        ),
        "key_techniques": (
            f"**{k.module}** 的关键技术往往集中在默认配置与边界行为；"
            "生产问题多源于「以为懂了」的细节，应用 checklist 逐项验证。"
        ),
        "source_analysis": (
            f"源码阅读 **{k.module}** 宜采用「由外向内」："
            "先跟一次主路径请求，再展开分支与错误处理，避免陷入细节迷失主线。"
        ),
        "performance": (
            f"针对 **{k.module}**，性能工作应「先度量后优化」："
            "明确 P50/P95/P99 与资源占用基线，用 profiler/trace 定位热点，"
            "优先处理 I/O、锁竞争与算法复杂度问题，避免无数据支撑的微调。"
        ),
        "troubleshooting": (
            f"排障 **{k.module}** 时建议固定顺序：复现 → 收集日志/metrics/trace → "
            "对比最近变更与配置 diff → 最小化隔离实验 → 记录根因与回归用例。"
        ),
        "security": (
            f"**{k.module}** 的安全基线包括：最小权限、输入校验、敏感数据保护、"
            "审计日志与依赖漏洞跟踪；变更前做威胁建模，避免在日志中泄露密钥或 PII。"
        ),
        "configuration": (
            f"**{k.module}** 配置应外部化并分环境管理；"
            "关键项在文档中注明默认值、取值范围与生产推荐值，纳入 Code Review。"
        ),
    }
    if pattern_type in focus_notes:
        parts.extend([
            "## 本章聚焦",
            "",
            focus_notes[pattern_type],
            "",
        ])

    return parts


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
    intro_line = PATTERN_INTROS.get(pattern_type, PATTERN_INTROS["fundamentals"]).format(
        module=module
    )

    parts = [
        f"# {title}",
        "",
        f"> **领域**：{domain} ｜ **模块**：{module} ｜ **难度**：{difficulty} ｜ **类型**：{type_label}",
        "",
        defensive_note(domain),
        "## 导读",
        "",
        f"本章系统讲解 **{domain}** 中 **{module}** 的相关知识（{type_label}）。"
        f"{intro_line}"
        "内容基于主流框架与工程实践撰写，不依赖过时概念堆砌。",
        "",
        "## 核心知识",
        "",
        _render_concepts(k, pattern_type),
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

    supplementary = _render_supplementary(k, pattern_type)
    if supplementary:
        parts.extend(supplementary)

    pitfalls = _render_pitfalls(k)
    if pitfalls:
        parts.extend([pitfalls, ""])

    practices = _render_practices(k)
    if practices:
        parts.extend([practices, ""])

    parts.extend([
        "## 巩固建议",
        "",
        f"建议结合 **{domain}** 官方文档与小型实验，亲手验证 **{module}** 的默认行为与边界条件；"
        "将本章要点整理为检查清单或 ADR，便于评审与团队 onboarding。",
        "",
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
    prereq = "\n".join(f"- {p}" for p in o.prerequisites) if o.prerequisites else "- 无硬性前置，按章节难度循序渐进即可"

    ecosystem_line = (
        f"本领域常用技术栈与工具包括：{o.ecosystem}。"
        if o.ecosystem
        else "建议结合官方文档与社区主流工具链同步学习。"
    )

    return "\n".join([
        f"# {domain} 学习指南",
        "",
        f"> **分类**：{o.category} ｜ **技术生态**：{o.ecosystem or '见正文'}",
        "",
        defensive_note(domain),
        "## 领域定位",
        "",
        o.intro,
        "",
        o.positioning,
        "",
        ecosystem_line,
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
