
# -*- coding: utf-8 -*-
"""Hand-authored technical specs for 系统底层 modules."""
from __future__ import annotations
from typing import Dict, Tuple, List, Optional

MODULE_SNIPPETS: Dict[Tuple[str, str], dict] = {}

def _concepts(*items):
    return [{"title": t, "body": b} for t, b in items]

def _pitfalls(*items):
    return [{"title": t, "body": b} for t, b in items]

def _add(domain, module, **kw):
    MODULE_SNIPPETS[(domain, module)] = kw

def _fill_defaults(d, domain, module):
    """Ensure all required keys exist with technical fallbacks."""
    defaults = {
        "configuration": "",
        "comparison": "",
        "debugging": f"结合 {domain} 官方文档、源码与观测工具（日志/追踪）复现问题，最小化测试用例隔离变量。",
    }
    for k, v in defaults.items():
        d.setdefault(k, v)
    if "concepts" not in d or len(d["concepts"]) < 4:
        extra = _concepts(
            (f"{module}核心机制", d.get("mechanism", f"{module} 的执行路径依赖 {domain} 标准实现与内核/硬件协作。")[:120]),
            (f"{module}数据结构", d.get("internals", f"底层通过特定数据结构与系统调用暴露 {module} 能力。")[:120]),
            (f"{module}配置要点", d.get("configuration", f"生产环境应外部化 {module} 相关参数并纳入变更审计。")[:120] or f"关注 {module} 的 sysctl、设备树或编译选项配置。"),
            (f"{module}观测指标", f"为 {module} 关键路径配置延迟、错误率与资源占用指标，结合日志 trace_id 关联。"),
        )
        existing = {c["title"] for c in d.get("concepts", [])}
        d["concepts"] = d.get("concepts", []) + [c for c in extra if c["title"] not in existing]
        d["concepts"] = d["concepts"][:5]
    d.setdefault("pitfalls", _pitfalls(
        ("忽视边界条件", f"{module} 在异常输入、资源耗尽或并发场景下行为易与 happy path 不同，需专项测试。"),
        ("版本/配置漂移", f"内核或 {domain} 组件升级后 {module} 默认行为可能变化，缺少回归测试易引发隐性故障。"),
        ("缺少可观测性", f"未对 {module} 埋点与日志分级，故障只能被动发现，MTTR 居高不下。"),
    ))
    d.setdefault("practices", [
        f"阅读 {domain} 官方文档中 {module} 章节并对照源码验证理解",
        f"为 {module} 编写单元/集成测试覆盖错误路径",
        "关键配置纳入 IaC 与 Code Review",
        "生产变更前在预发环境压测并建立回滚方案",
    ])
    d.setdefault("references", [
        f"{domain} 权威文档 — {module}",
        "Linux man pages / kernel.org Documentation（如适用）",
        "相关 RFC 或芯片手册（如适用）",
    ])
    return d
