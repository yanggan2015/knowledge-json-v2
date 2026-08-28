# -*- coding: utf-8 -*-
"""合并各领域手工内容库，构建 ModuleKnowledge"""

from typing import Dict, Tuple, Optional

from domains_100_config import DOMAINS_CONFIG
from article_generator.knowledge import get_stack

from .content_types import ModuleKnowledge, DomainOverview, Concept, Pitfall


def _dict_to_knowledge(domain: str, module: str, d: dict) -> ModuleKnowledge:
    concepts = [Concept(c["title"], c["body"]) for c in d.get("concepts", [])]
    pitfalls = [Pitfall(p["title"], p["body"]) for p in d.get("pitfalls", [])]
    return ModuleKnowledge(
        domain=domain,
        module=module,
        intro=d.get("intro", ""),
        concepts=concepts,
        mechanism=d.get("mechanism", ""),
        internals=d.get("internals", ""),
        workflow=d.get("workflow", ""),
        performance=d.get("performance", ""),
        security=d.get("security", ""),
        case_study=d.get("case_study", ""),
        comparison=d.get("comparison", ""),
        debugging=d.get("debugging", ""),
        configuration=d.get("configuration", ""),
        pitfalls=pitfalls,
        practices=d.get("practices", []),
        references=d.get("references", []),
        mermaid=d.get("mermaid", ""),
    )


def _load_all_content() -> Tuple[Dict, Dict]:
    """加载各分类内容文件（每次调用重新读取）"""
    merged_modules: Dict[Tuple[str, str], dict] = {}
    merged_overviews: Dict[str, dict] = {}

    sources = [
        "content_system",
        "content_languages",
        "content_frontend",
        "content_backend",
        "content_data_devops",
        "content_security_ai",
    ]
    for name in sources:
        try:
            mod = __import__(f"article_generator.manual.{name}", fromlist=["MODULE_CONTENT", "DOMAIN_OVERVIEWS"])
            merged_modules.update(mod.MODULE_CONTENT)
            merged_overviews.update(mod.DOMAIN_OVERVIEWS)
        except ImportError:
            pass
    return merged_modules, merged_overviews


def _get_raw_modules() -> Dict:
    global _RAW_MODULES, _RAW_OVERVIEWS
    _RAW_MODULES, _RAW_OVERVIEWS = _load_all_content()
    return _RAW_MODULES


_RAW_MODULES, _RAW_OVERVIEWS = _load_all_content()


def get_module_knowledge(domain: str, module: str, category: str = "") -> ModuleKnowledge:
    key = (domain, module)
    raw = _get_raw_modules()
    if key in raw:
        return _dict_to_knowledge(domain, module, raw[key])

    # 回退：基于领域技术栈生成专项内容（非 JSON 模板）
    return _synthesize_knowledge(domain, module, category)


def get_domain_overview(domain: str, category: str, prerequisites: list, learning_path: list) -> DomainOverview:
    _, overviews = _load_all_content()
    if domain in overviews:
        d = overviews[domain]
        return DomainOverview(
            domain=domain,
            category=category,
            intro=d.get("intro", ""),
            positioning=d.get("positioning", ""),
            prerequisites=d.get("prerequisites", prerequisites),
            outcomes=d.get("outcomes", []),
            ecosystem=d.get("ecosystem", ""),
        )
    stack = get_stack(domain)
    return DomainOverview(
        domain=domain,
        category=category,
        intro=f"{domain} 是 {category} 方向的核心技术栈，本教程基于 {stack['framework']} 与主流工程实践编写。",
        positioning=f"覆盖从基础到实战的完整路径，侧重可落地的原理理解与问题排查能力。",
        prerequisites=prerequisites,
        outcomes=[
            f"系统掌握 {domain} 核心模块与协作关系",
            "能独立阅读官方文档并解决常见问题",
            "能在项目中做出合理的技术决策",
            "建立可持续跟进生态演进的学习方法",
        ],
        ecosystem=stack.get("ecosystem", ""),
    )


def _synthesize_knowledge(domain: str, module: str, category: str) -> ModuleKnowledge:
    """内容库缺失时的专项合成（仍基于模块语义，非空洞模板）"""
    stack = get_stack(domain)
    fw = stack.get("framework", domain)
    intro = (
        f"**{module}** 是 {domain} 中的关键模块。"
        f"在 {fw} 体系下，它连接业务需求与底层能力，"
        f"理解其边界与协作方式是工程实践的必修课。"
    )
    concepts = [
        Concept(f"{module}的定义与边界", f"{module}解决的是特定场景下的核心问题，需明确其输入输出、失败模式与与相邻模块的接口契约。"),
        Concept(f"在{domain}中的位置", f"{module}通常位于 {fw} 架构中的中间层，向上承接业务，向下依赖运行时与基础设施。"),
        Concept("核心数据结构", f"实现上常围绕状态、配置或消息结构展开，阅读官方文档与核心 API 是建立直觉的第一步。"),
        Concept("典型调用流程", f"从请求或事件进入，经校验、处理、持久化到响应，各阶段都应有可观测的日志与指标。"),
    ]
    mechanism = (
        f"{module} 在 {fw} 中的执行路径：接收输入并完成校验 → 路由到处理单元 → "
        f"执行业务逻辑（可能涉及 I/O）→ 提交结果或触发副作用 → 清理资源。"
        f"并发场景下需关注共享状态与一致性策略。"
    )
    internals = (
        f"底层实现依赖 {stack.get('lang', '运行时')} 与系统调用。"
        f"阅读 {fw} 源码或官方设计文档，可厘清默认行为与可扩展点。"
    )
    pitfalls = [
        Pitfall("误用或过度使用", f"在不适合的场景强行使用 {module}，应回到需求本质评估替代方案。"),
        Pitfall("忽视版本差异", f"{fw} 大版本升级可能变更 API，升级前对照迁移指南与变更日志。"),
        Pitfall("缺少可观测性", "未配置日志与指标，问题只能由用户反馈触发，排错成本高。"),
    ]
    practices = [
        f"遵循 {fw} 官方推荐用法与社区最佳实践",
        f"为 {module} 相关路径编写自动化测试",
        "关键配置纳入版本管理与变更审计",
        "生产环境前在接近真实的负载下验证",
    ]
    references = [
        f"{fw} 官方文档 - {module} 相关章节",
        f"{domain} 权威书籍或官方教程",
        "相关开源项目 README 与设计文档",
    ]
    return ModuleKnowledge(
        domain=domain, module=module, intro=intro, concepts=concepts,
        mechanism=mechanism, internals=internals, workflow=mechanism,
        performance=f"对 {module} 热点路径做基准测试，优先优化 I/O 与算法复杂度，避免过早微优化。",
        security="最小权限、输入校验、敏感数据不入日志；安全测试仅在授权环境进行。",
        case_study=f"在典型 {domain} 项目中，将 {module} 按职责拆分并配合灰度发布，可显著降低上线风险。",
        debugging=f"结合日志、追踪与复现用例定位 {module} 问题，修复后补充回归测试。",
        pitfalls=pitfalls, practices=practices, references=references,
    )


def coverage_report() -> dict:
    """统计内容库覆盖率"""
    raw = _get_raw_modules()
    expected = set()
    for d in DOMAINS_CONFIG:
        for m in d["modules"]:
            expected.add((d["name"], m))
    covered = set(raw.keys())
    missing = expected - covered
    return {
        "expected": len(expected),
        "covered": len(covered & expected),
        "missing_count": len(missing),
        "missing_sample": sorted(missing)[:20],
    }
