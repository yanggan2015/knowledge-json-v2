# -*- coding: utf-8 -*-
"""手工教程内容数据结构"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Concept:
    title: str
    body: str


@dataclass
class Pitfall:
    title: str
    body: str


@dataclass
class ModuleKnowledge:
    """单个模块的完整教程素材（与 JSON 无关）"""
    domain: str
    module: str
    intro: str
    concepts: List[Concept] = field(default_factory=list)
    mechanism: str = ""          # 实现机制 / 工作原理
    internals: str = ""          # 底层 / 源码视角
    workflow: str = ""             # 使用流程 / 操作步骤
    performance: str = ""          # 性能要点
    security: str = ""             # 安全要点（防御视角）
    case_study: str = ""           # 实战案例
    comparison: str = ""           # 对比选型
    debugging: str = ""            # 调试排错
    configuration: str = ""        # 配置实践
    pitfalls: List[Pitfall] = field(default_factory=list)
    practices: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    mermaid: str = ""              # 本模块专属 Mermaid


@dataclass
class DomainOverview:
    """领域概述素材"""
    domain: str
    category: str
    intro: str
    positioning: str
    prerequisites: List[str]
    outcomes: List[str]
    ecosystem: str
