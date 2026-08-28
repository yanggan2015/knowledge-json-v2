# -*- coding: utf-8 -*-
"""标题模式识别与章节类型映射"""

import re
from typing import Optional

PATTERN_TYPES = {
    "fundamentals": "核心概念与原理",
    "internals": "的实现机制详解",
    "key_techniques": "的关键技术点",
    "source_analysis": "的源码级分析",
    "configuration": "的配置与使用",
    "troubleshooting": "的常见问题与解决方案",
    "performance": "的性能优化技巧",
    "best_practices": "的最佳实践指南",
    "advanced": "的高级应用场景",
    "case_study": "的实战案例分析",
    "design_evolution": "的设计思想与演进",
    "deep_internals": "的底层原理剖析",
    "debugging": "的调试与排错",
    "security": "的安全注意事项",
    "comparison": "的对比与选型",
}

# 扩展模式（超出15个模板后的标题）
EXTENDED_PATTERNS = [
    "深入理解", "实战指南", "原理剖析", "性能调优", "源码解读",
    "架构设计", "最佳实践", "常见陷阱", "高级技巧", "应用案例",
    "配置详解", "故障排查", "安全加固", "迁移指南", "对比分析",
]

EXTENDED_TO_TYPE = {
    "深入理解": "fundamentals",
    "实战指南": "case_study",
    "原理剖析": "deep_internals",
    "性能调优": "performance",
    "源码解读": "source_analysis",
    "架构设计": "advanced",
    "最佳实践": "best_practices",
    "常见陷阱": "troubleshooting",
    "高级技巧": "advanced",
    "应用案例": "case_study",
    "配置详解": "configuration",
    "故障排查": "debugging",
    "安全加固": "security",
    "迁移指南": "comparison",
    "对比分析": "comparison",
}


def detect_pattern_type(title: str, module: str) -> str:
    """从标题识别章节类型"""
    for ptype, suffix in PATTERN_TYPES.items():
        if title.endswith(suffix) or suffix in title:
            return ptype
    for prefix, ptype in EXTENDED_TO_TYPE.items():
        if title.startswith(prefix):
            return ptype
    # 按模块名回退
    if "安全" in title or "安全" in module:
        return "security"
    if "性能" in title or "优化" in title:
        return "performance"
    if "实战" in title or "案例" in title:
        return "case_study"
    if "源码" in title:
        return "source_analysis"
    return "fundamentals"


def safe_filename(title: str, max_len: int = 60) -> str:
    """生成安全的文件名"""
    name = re.sub(r'[<>:"/\\|?*]', '', title)
    name = re.sub(r'\s+', '-', name.strip())
    name = re.sub(r'-+', '-', name)
    if len(name) > max_len:
        name = name[:max_len].rstrip('-')
    return name or "chapter"


TYPE_LABELS = {
    "fundamentals": "基础概念",
    "internals": "实现机制",
    "key_techniques": "关键技术",
    "source_analysis": "源码分析",
    "configuration": "配置实践",
    "troubleshooting": "问题排查",
    "performance": "性能优化",
    "best_practices": "最佳实践",
    "advanced": "高级应用",
    "case_study": "实战案例",
    "design_evolution": "设计演进",
    "deep_internals": "底层原理",
    "debugging": "调试排错",
    "security": "安全实践",
    "comparison": "对比选型",
}
