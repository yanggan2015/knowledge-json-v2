# -*- coding: utf-8 -*-
"""Rich module content builder for security/AI/other domains."""

from __future__ import annotations

SECURITY_NOTE = (
    "本教程内容仅供合法授权的安全测试、防御加固与学术研究使用。"
    "未经授权对他人系统进行扫描、入侵或破坏属于违法行为。"
)

DEFENSIVE_DOMAINS = frozenset({
    "网络安全", "Web安全", "密码学", "渗透测试", "逆向工程", "漏洞挖掘", "移动安全", "云安全",
})


def _concepts(*items: tuple[str, str]) -> list[dict]:
    return [{"title": t, "body": b} for t, b in items]


def _pitfalls(*items: tuple[str, str]) -> list[dict]:
    return [{"title": t, "body": b} for t, b in items]


MODULE_KB: dict[str, dict] = {}


def _merge_kb() -> None:
    from article_generator.manual._kb_expand_web import EXPANDED_KB_WEB
    from article_generator.manual._kb_expand_web import EXPANDED_KB_WEB
    from article_generator.manual._kb_expand_part1 import EXPANDED_KB
    from article_generator.manual._kb_expand_part2 import EXPANDED_KB_P2
    from article_generator.manual._kb_expand_part3 import EXPANDED_KB_P3

    MODULE_KB.update(EXPANDED_KB)
    MODULE_KB.update(EXPANDED_KB_WEB)
    MODULE_KB.update(EXPANDED_KB_WEB)
    MODULE_KB.update(EXPANDED_KB_P2)
    MODULE_KB.update(EXPANDED_KB_P3)


_merge_kb()


def build_from_kb(domain: str, module: str, category: str) -> dict | None:
    """Build content from MODULE_KB if available."""
    kb = MODULE_KB.get(module)
    if not kb:
        return None

    focus = kb.get("focus", module)
    intro = f"**{module}** 是 {domain} 领域的核心主题。{focus}。本模块从原理与工程实践出发，帮助读者建立系统理解。"

    if domain in DEFENSIVE_DOMAINS:
        intro += " " + SECURITY_NOTE

    concepts = []
    for key in ("c1", "c2", "c3", "c4"):
        if key in kb:
            concepts.append({"title": kb[key][0], "body": kb[key][1]})

    result = {
        "intro": intro,
        "concepts": concepts,
        "mechanism": kb.get("mech", f"{module} 的工作流程：输入 → 处理 → 输出，各阶段需关注正确性与安全性。"),
        "internals": kb.get("internals", f"{module} 的底层实现依赖 {domain} 生态中的标准组件与协议，建议阅读官方规范文档。"),
        "workflow": kb.get("workflow", f"1. 理解 {module} 概念 → 2. 学习标准用法 → 3. 动手实验 → 4. 分析案例 → 5. 总结最佳实践。"),
        "performance": kb.get("perf", f"评估 {module} 性能时建立基准测试，关注时间/空间复杂度或系统吞吐延迟指标。"),
        "security": kb.get("sec", SECURITY_NOTE if domain in DEFENSIVE_DOMAINS else f"在 {domain} 场景下注意输入校验、权限控制与敏感数据保护。"),
        "case_study": kb.get("case", f"在典型 {domain} 项目中，正确应用 {module} 可显著提升系统质量与可维护性。"),
        "comparison": kb.get("cmp", f"选择 {module} 方案时需对比多种替代方案的适用场景、性能与生态支持。"),
        "debugging": kb.get("debug", f"排查 {module} 问题时，结合日志、监控与最小复现用例逐步定位根因。"),
        "configuration": kb.get("config", f"配置 {module} 时遵循官方推荐默认值，仅在理解影响后调整参数。"),
        "pitfalls": _pitfalls(
            ("概念理解偏差", f"对 {module} 理解不全面导致误用，应回到官方文档重新梳理。"),
            ("忽视边界条件", f"{module} 在极端输入或高并发下行为可能不同，需充分测试。"),
            ("缺少监控", f"未对 {module} 关键指标监控，问题只能被动发现。"),
        ),
        "practices": kb.get("practices", [
            f"遵循 {domain} 领域 {module} 的官方推荐实践",
            f"为 {module} 相关功能编写自动化测试",
            "关键配置纳入版本管理与变更审计",
            "生产部署前在接近真实环境验证",
        ]),
        "references": kb.get("refs", [
            f"{domain} 官方文档 - {module}",
            "OWASP / NIST 相关指南（如适用）",
            "权威书籍与 RFC 标准文档",
        ]),
    }
    return result


def build_generic(domain: str, module: str, category: str, idx: int, total: int) -> dict:
    """Generate rich generic content for modules without specific KB entry."""
    phase = "基础" if idx < total * 0.25 else "核心" if idx < total * 0.6 else "高级" if idx < total * 0.85 else "实战"

    intro = (
        f"**{module}** 是 {domain}（{category}）中「{phase}」阶段的关键模块。"
        f"系统掌握 {module} 的原理、使用方法与常见陷阱，"
        f"是从入门到实战的必经之路。"
    )
    if domain in DEFENSIVE_DOMAINS:
        intro += " " + SECURITY_NOTE

    domain_angles = {
        "数据结构与算法": f"{module} 的时间/空间复杂度分析是算法选型的基础",
        "机器学习": f"{module} 在 ML 流水线中连接数据预处理与模型部署",
        "深度学习": f"{module} 是构建与训练神经网络的核心组件",
        "自然语言处理": f"{module} 处理文本数据的关键环节",
        "计算机视觉": f"{module} 处理图像/视频数据的核心技术",
        "强化学习": f"{module} 定义智能体与环境的交互方式",
        "数据挖掘": f"{module} 从数据中发现模式与知识",
        "知识图谱": f"{module} 构建与查询知识图谱的关键步骤",
        "大语言模型": f"{module} 是 LLM 训练、微调与应用的核心技术",
        "AIGC": f"{module} 是 AI 内容生成的关键技术",
        "区块链": f"{module} 是区块链系统的重要组成",
        "游戏开发": f"{module} 是游戏引擎与游戏逻辑的核心系统",
        "计算机图形学": f"{module} 是渲染管线的重要环节",
        "音视频处理": f"{module} 是音视频链路的关键处理步骤",
        "物联网": f"{module} 是 IoT 系统从设备到云端的关键环节",
        "低代码开发": f"{module} 是低代码平台的核心能力",
        "量子计算": f"{module} 是量子计算理论与实践的基础",
        "Rust系统编程": f"{module} 是 Rust 系统级编程的核心主题",
        "逆向工程": f"{module} 是二进制分析与恶意软件研究的分析方法",
        "漏洞挖掘": f"{module} 是发现与报告软件漏洞的系统方法",
        "移动安全": f"{module} 是移动应用安全防护的关键环节",
        "云安全": f"{module} 是云环境安全配置与合规的核心",
    }
    angle = domain_angles.get(domain, f"{module} 在 {domain} 工程实践中的应用")

    concepts = _concepts(
        (f"{module}的定义", f"{module} 解决 {domain} 中特定场景的核心问题。{angle}。"),
        (f"{module}的核心原理", f"理解 {module} 的底层机制是正确应用的前提，需结合 {domain} 典型架构学习。"),
        (f"在{domain}中的位置", f"{module} 与 {domain} 其他模块协作，形成完整的技术链路。"),
        (f"典型应用场景", f"在 {domain} 实际项目中，{module} 常用于解决性能、可靠性或功能扩展问题。"),
    )

    mechanism = (
        f"{module} 的执行流程：接收输入并完成校验 → "
        f"核心处理逻辑（{angle}）→ "
        f"输出结果并处理异常 → 记录日志与指标。"
        f"理解各阶段的数据流转是排查问题的基础。"
    )

    internals = (
        f"深入 {module} 需阅读 {domain} 官方文档与源码/规范。"
        f"关注默认行为、扩展点与性能特征。"
        f"对比不同版本/API 的变更以避免兼容问题。"
    )

    sec_text = SECURITY_NOTE if domain in DEFENSIVE_DOMAINS else f"注意 {module} 的输入校验与权限控制。"

    if domain == "漏洞挖掘" and module in ("漏洞利用", "Shellcode", "ROP"):
        sec_text = (
            "本模块仅讲解漏洞分类与防御原理，不提供武器化利用代码。"
            "发现漏洞应遵循负责任披露流程。"
        )
        mechanism = (
            f"从防御视角理解 {module} 的原理，帮助开发安全代码与配置防护规则。"
            f"安全研究人员在授权环境中验证漏洞存在性，不提供完整攻击链。"
        )

    if domain == "渗透测试":
        sec_text = SECURITY_NOTE + " 严格遵循 PTES 方法论与 SOW 授权范围。"

    return {
        "intro": intro,
        "concepts": concepts,
        "mechanism": mechanism,
        "internals": internals,
        "workflow": f"1. 学习 {module} 概念与 API → 2. 跟随官方教程动手实践 → 3. 在 {domain} 示例项目中应用 → 4. 分析常见问题 → 5. 总结最佳实践",
        "performance": f"对 {module} 热点路径做 profiling，优先优化算法复杂度与 I/O 瓶颈。",
        "security": sec_text,
        "case_study": f"某 {domain} 项目通过正确应用 {module}，解决了生产环境中的关键问题，显著提升了系统质量。",
        "comparison": f"对比 {module} 的不同实现/方案，从性能、易用性、生态支持角度选型。",
        "debugging": f"排查 {module} 问题：复现 → 日志分析 → 最小化测试 → 定位根因 → 修复验证。",
        "configuration": f"参考 {domain} 官方文档配置 {module}，关键参数变更需经过测试验证。",
        "pitfalls": _pitfalls(
            ("理解不深入", f"对 {module} 一知半解导致误用，应系统学习后再应用于生产。"),
            ("忽视版本差异", f"{domain} 生态版本更新可能变更 {module} API，升级前查阅变更日志。"),
            ("缺少测试", f"未对 {module} 编写测试，变更后无法快速发现回归。"),
        ),
        "practices": [
            f"遵循 {domain} 官方 {module} 推荐用法",
            f"为 {module} 关键路径编写单元/集成测试",
            "文档化配置与架构决策",
            "持续跟进社区最佳实践",
        ],
        "references": [
            f"{domain} 官方文档 - {module}",
            f"《{domain}权威指南》",
            "相关开源项目与 RFC/论文",
        ],
    }
