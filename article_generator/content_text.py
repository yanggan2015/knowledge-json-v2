# -*- coding: utf-8 -*-
"""高质量正文内容生成 — 以文字叙述为主"""

from typing import List

from .knowledge import (
    get_stack, get_module_hint, get_domain_intro, get_module_deep,
    CONCEPT_EXPLAINERS, PITFALL_ADVICE,
)
from .patterns import TYPE_LABELS


def expand_concepts(
    domain: str, module: str, concepts: List[str], pattern_type: str, chapter_id: str = ""
) -> str:
    stack = get_stack(domain)
    domain_intro = get_domain_intro(domain)
    module_deep = get_module_deep(module)
    hint = get_module_hint(module)

    lines = [
        domain_intro,
        "",
        f"在 **{domain}** 体系中，**{module}** 与上下游模块形成协作。"
        f"技术栈以 **{stack['framework']}** 为核心（{stack['lang']}），"
        f"生态包括 {stack['ecosystem']}。",
        "",
    ]
    if module_deep:
        lines.extend([module_deep, ""])
    elif hint:
        lines.extend([hint, ""])

    if concepts:
        lines.append("### 概念精讲")
        lines.append("")
        for i, c in enumerate(concepts[:5]):
            explainer = CONCEPT_EXPLAINERS[(i + int(chapter_id or 0)) % len(CONCEPT_EXPLAINERS)]
            lines.append(f"**{c}**")
            lines.append("")
            lines.append(f"{explainer} 在 {module} 语境下，这一点直接影响设计决策与故障排查思路。")
            lines.append("")

    return "\n".join(lines)


def _pitfall_advice(text: str) -> str:
    for keyword, advice in PITFALL_ADVICE.items():
        if keyword in text:
            return advice
    return PITFALL_ADVICE["默认"]


def expand_pitfalls(pitfalls: List[str], domain: str, module: str) -> str:
    lines = ["### 常见误区与应对", ""]
    if not pitfalls:
        lines.extend([
            f"- **只记用法不理解原理**：回到 {module} 的设计动机，画数据流图再动手改代码。",
            f"- **忽视性能与资源边界**：小规模验证通过后，用生产级数据量压测 {module}。",
            "- **环境配置不一致**：维护配置清单，部署前后自动 diff 校验。",
            "- **缺乏可观测性**：为关键路径补充日志、指标与告警，问题主动发现。",
            "",
        ])
        return "\n".join(lines)

    for p in pitfalls[:5]:
        advice = _pitfall_advice(p)
        lines.append(f"**误区：{p}**")
        lines.append("")
        lines.append(f"**应对**：{advice}")
        lines.append("")

    return "\n".join(lines)


def expand_practices(practices: List[str], domain: str, module: str) -> str:
    practice_actions = [
        "写入团队 Wiki 并纳入 Code Review 检查项",
        "配置静态检查或 CI 规则自动拦截违规写法",
        "在新人 onboarding 中作为必修内容讲解",
        "每季度回顾一次，对照社区最佳实践更新",
        "用真实项目案例演示正确与错误对比",
    ]
    lines = ["### 最佳实践", ""]
    if not practices:
        lines.extend([
            f"1. 遵循 {domain} 官方文档与社区公认规范。",
            f"2. {module} 相关变更小步提交，每次可回滚。",
            "3. 建立监控、日志、文档三位一体的可观测体系。",
            "4. 定期技术债务清理，避免临时方案固化。",
            "",
        ])
        return "\n".join(lines)

    for i, p in enumerate(practices[:5]):
        action = practice_actions[i % len(practice_actions)]
        lines.append(f"{i+1}. **{p}** — 落地方式：{action}。")
        lines.append("")

    return "\n".join(lines)


# --- 深度讲解各类型（保留原有 writers，略作润色）---

def write_fundamentals(domain: str, module: str, difficulty: str) -> str:
    stack = get_stack(domain)
    return (
        f"### 为什么需要 {module}\n\n"
        f"工程实践中，{module} 解决的是「在 {stack['framework']} 约束下，"
        f"如何可靠、可维护地完成特定职责」的问题。"
        f"初学者常只记 API 而不理解动机——场景变化时便无法判断该不该用、怎么用。\n\n"
        f"### 核心原理\n\n"
        f"{module} 的设计遵循：**职责单一**、**接口稳定**、**可观测**。"
        f"在 **{difficulty}** 阶段，重点是把这三条映射到具体概念与操作上。\n\n"
        f"### 与周边模块的关系\n\n"
        f"向上为业务层提供能力；向下依赖运行时与基础设施。"
        f"横向通过清晰的数据流或事件流衔接，避免循环依赖。"
    )


def write_internals(domain: str, module: str) -> str:
    stack = get_stack(domain)
    return (
        f"### 调用链路\n\n"
        f"典型 {module} 调用五阶段：**接入**（校验与上下文）→ **路由**（分发）→ "
        f"**执行**（{stack['framework']} 核心逻辑）→ **提交**（写存储/回调）→ "
        f"**收尾**（释放资源、记日志、返回响应）。\n\n"
        f"### 状态与生命周期\n\n"
        f"许多「偶发异常」源于状态转换时机错误——资源未就绪即操作，或清理前重复触发。"
        f"建议对照生命周期图与日志时间线分析。\n\n"
        f"### 并发与一致性\n\n"
        f"多调用并发时需明确：共享可变状态、锁粒度、重试对一致性的影响。"
        f"设计应预设最坏情况，而非假设「不会同时发生」。"
    )


def write_source_analysis(domain: str, module: str) -> str:
    stack = get_stack(domain)
    return (
        f"### 源码阅读路径\n\n"
        f"分析 {stack['framework']} 中 {module} 相关实现：\n\n"
        f"1. 从公开 API 入口定位首次调用函数。\n"
        f"2. 阅读核心数据结构，字段含义揭示设计意图。\n"
        f"3. 梳理正常路径与异常路径，注意错误传播。\n"
        f"4. 识别扩展点（钩子、插件），理解内核如何保持稳定。\n\n"
        f"### 文档与实现差异\n\n"
        f"记录文档未覆盖的边界行为，形成团队「已知行为清单」，"
        f"避免把实现细节误当作公开契约。\n\n"
        f"### 工程决策\n\n"
        f"读懂实现后，能更准确评估定制代价、升级风险与性能瓶颈位置。"
    )


def write_performance(domain: str, module: str) -> str:
    return (
        f"### 性能指标体系\n\n"
        f"优化前先定义目标：降 P99、提吞吐还是减资源？"
        f"同时关注 **延迟、吞吐、错误率、资源利用率**。\n\n"
        f"### 常见瓶颈\n\n"
        f"- I/O 等待（网络、磁盘、数据库）\n"
        f"- 锁竞争与排队\n"
        f"- 内存压力引发 GC 或缓存失效\n"
        f"- 算法复杂度在规模增长后成为硬伤\n\n"
        f"### 优化循环\n\n"
        f"度量 → 定位 → 改动 → 验证。每次只改一处，保留对比数据。"
        f"优先缓存、批处理、索引、连接池、异步化；避免过早微优化。\n\n"
        f"### 防回归\n\n"
        f"将 {module} 关键路径基线纳入 CI 或定期压测。"
    )


def write_security(domain: str, module: str) -> str:
    return (
        f"### 威胁建模\n\n"
        f"梳理 {module} 攻击面：接收哪些输入、输出到哪里、谁有权调用、失败暴露什么信息？\n\n"
        f"### 防护原则\n\n"
        f"- **最小权限**：账号与令牌仅授予必要范围。\n"
        f"- **输入校验**：白名单校验，拒绝可疑内容。\n"
        f"- **机密隔离**：密钥不入库、不进日志。\n"
        f"- **默认拒绝**：未授权操作拒绝并记审计日志。\n\n"
        f"### 合规要求\n\n"
        f"安全学习与实践须在合法授权范围内，使用隔离环境，禁止对未授权目标操作。\n\n"
        f"### 持续改进\n\n"
        f"定期回顾配置与依赖版本，关注安全公告，建立响应流程。"
    )


def write_case_study(domain: str, module: str) -> str:
    return (
        f"### 场景背景\n\n"
        f"中型产品需在三个月内完成 {module} 能力建设。团队约 8 人，兼顾交付与可维护性。\n\n"
        f"### 方案设计\n\n"
        f"1. 按核心/扩展/运维路径拆分需求。\n"
        f"2. 在 {domain} 生态内选成熟组件，避免自研基础设施。\n"
        f"3. 提前定义接口契约与错误码，并行开发。\n"
        f"4. 小流量灰度 → 放量 → 全量，每阶段有回滚预案。\n\n"
        f"### 实施与复盘\n\n"
        f"开发期覆盖核心路径测试；联调期用真实量级压测；"
        f"上线 72 小时内加强监控。成功共性：边界清晰、度量先行、文档与实现同步。"
    )


def write_best_practices(domain: str, module: str) -> str:
    return (
        f"### 编码规范\n\n"
        f"遵循 {domain} 风格指南；{module} 逻辑集中存放；公开接口文档化，契约变更版本化。\n\n"
        f"### 测试策略\n\n"
        f"- 单元测试：核心逻辑与边界（空值、超限、并发）。\n"
        f"- 集成测试：{module} 与依赖的真实协作。\n"
        f"- 回归测试：每次发布前自动运行。\n\n"
        f"### 可观测性\n\n"
        f"结构化日志、关键指标、告警阈值与 Runbook。日志带追踪 ID，便于跨服务串联。\n\n"
        f"### 团队协作\n\n"
        f"复杂模块设 Owner；重大变更经设计评审；小步迭代。"
    )


def write_comparison(domain: str, module: str) -> str:
    return (
        f"### 六维选型表\n\n"
        f"| 维度 | 关注点 |\n|------|--------|\n"
        f"| 功能匹配 | 当前与未来 12 个月需求 |\n"
        f"| 性能 | 预期负载下延迟与吞吐 |\n"
        f"| 运维成本 | 部署、升级、排错复杂度 |\n"
        f"| 学习曲线 | 团队上手时间 |\n"
        f"| 生态成熟度 | 文档、社区、集成 |\n"
        f"| 合规 | 许可证与数据主权 |\n\n"
        f"### 决策记录\n\n"
        f"将结论与否决理由写入 ADR，避免日后无人记得选型原因。"
    )


def write_troubleshooting(domain: str, module: str) -> str:
    return (
        f"### 五步排错法\n\n"
        f"现象 → 范围 → 根因 → 修复 → 验证。\n\n"
        f"1. 复现：记录错误、时间、范围、触发条件。\n"
        f"2. 缩小：配置、依赖、数据还是逻辑？\n"
        f"3. 证据：日志、指标、追踪、变更记录。\n"
        f"4. 验证假设：一次只改一个变量。\n"
        f"5. 归档：postmortem，更新监控与文档。\n\n"
        f"### 高频问题\n\n"
        f"配置未生效、版本不兼容、资源耗尽、时序竞态、数据异常（脏数据、编码、空值）。"
    )


def write_debugging(domain: str, module: str) -> str:
    return (
        f"### 工具链\n\n"
        f"日志（结构化+上下文 ID）、断点调试、分布式追踪、Profiler/火焰图。\n\n"
        f"### 调试纪律\n\n"
        f"先明确预期行为，再查差异。保留最小复现用例作回归。\n\n"
        f"### 与监控联动\n\n"
        f"调试发现的盲点应反哺告警规则，让同类问题下次主动暴露。"
    )


def write_configuration(domain: str, module: str) -> str:
    stack = get_stack(domain)
    return (
        f"### 配置三层\n\n"
        f"- **默认值**：框架内置，开箱可用。\n"
        f"- **环境配置**：开发/测试/生产差异化注入。\n"
        f"- **运行时覆盖**：紧急开关、限流阈值。\n\n"
        f"### 原则\n\n"
        f"敏感项由密钥服务注入；变更可追溯；启动时校验，失败快速退出。\n\n"
        f"### 版本注意\n\n"
        f"{stack['framework']} 配置项可能随大版本更名，升级前对照迁移指南。"
    )


def write_advanced(domain: str, module: str) -> str:
    return (
        f"### 进阶场景\n\n"
        f"高并发、多租户、跨区域、强合规或极端资源约束下，"
        f"{module} 的默认配置往往不够，需深入理解底层。\n\n"
        f"### 架构模式\n\n"
        f"分层解耦、异步削峰、缓存分层、多活容灾（定义 RTO/RPO 与 failover）。\n\n"
        f"### 演进路径\n\n"
        f"先正确性与可观测，再性能与成本；每步保留回滚能力。"
    )


def write_design_evolution(domain: str, module: str) -> str:
    return (
        f"### 设计动机\n\n"
        f"{module} 解决特定历史阶段的技术痛点。理解「当初为何这样设计」比死记用法更重要。\n\n"
        f"### 演进脉络\n\n"
        f"功能优先 → 模块化与自动化 → 云原生与全链路可观测。\n\n"
        f"### 关注方向\n\n"
        f"跟踪 {domain} 社区技术雷达，生产选型以稳定为先。"
    )


def write_deep_internals(domain: str, module: str) -> str:
    stack = get_stack(domain)
    return (
        f"### 底层视角\n\n"
        f"{module} 最终转化为内存读写、系统调用、网络 I/O、线程调度。"
        f"页大小、锁粒度、网络 RTT 等约束依然存在。\n\n"
        f"### 内存与资源\n\n"
        f"关注分配模式、对象池、临时对象风暴、大对象存储。资源泄漏缓慢累积，看趋势而非瞬时值。\n\n"
        f"### 硬件协同\n\n"
        f"缓存友好性、NUMA、顺序读 vs 随机读，影响极限负载表现。"
    )


def write_key_techniques(domain: str, module: str) -> str:
    return (
        f"### 技能链\n\n"
        f"1. 概念建模 — 准确术语描述问题与方案。\n"
        f"2. 接口运用 — API 能力边界与副作用。\n"
        f"3. 错误处理 — 分类与恢复策略。\n"
        f"4. 测试验证 — 可重复用例。\n"
        f"5. 集成协作 — 数据契约。\n\n"
        f"### 深化路径\n\n"
        f"每完成项目里程碑，复盘 {module} 相关决策，结构化反思比单纯阅读更有效。"
    )


WRITERS = {
    "fundamentals": write_fundamentals,
    "internals": write_internals,
    "source_analysis": write_source_analysis,
    "key_techniques": write_key_techniques,
    "configuration": write_configuration,
    "troubleshooting": write_troubleshooting,
    "performance": write_performance,
    "best_practices": write_best_practices,
    "advanced": write_advanced,
    "case_study": write_case_study,
    "design_evolution": write_design_evolution,
    "deep_internals": write_deep_internals,
    "debugging": write_debugging,
    "security": write_security,
    "comparison": write_comparison,
}


def generate_body(domain: str, module: str, pattern_type: str, difficulty: str) -> str:
    writer = WRITERS.get(pattern_type, write_fundamentals)
    if pattern_type == "fundamentals":
        return writer(domain, module, difficulty)
    return writer(domain, module)


def write_summary_section(domain: str, module: str, title: str, pattern_type: str) -> str:
    type_label = TYPE_LABELS.get(pattern_type, "专题")
    return (
        f"### 本章小结\n\n"
        f"学完本章，你应能：\n\n"
        f"- 说清 **{title}** 在 {domain}/{module} 中的定位。\n"
        f"- 描述核心流程与关键概念，能用自己的话复述。\n"
        f"- 识别常见误区并采取预防与排查手段。\n"
        f"- 在项目中做出与场景匹配的工程决策。\n\n"
        f"类型：**{type_label}**。建议完成小练习或复盘笔记，将阅读转化为能力。"
    )
