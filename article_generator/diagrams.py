# -*- coding: utf-8 -*-
"""Mermaid 图表生成"""

from typing import Optional


def architecture_diagram(domain: str, module: str, stack: dict) -> str:
  return f"""```mermaid
graph TB
    subgraph 应用层
        A[业务逻辑 / {module}]
    end
    subgraph 框架层
        B[{stack.get('framework', domain)}]
        C[{stack.get('ecosystem', '生态组件').split(',')[0]}]
    end
    subgraph 运行时
        D[{stack.get('lang', 'Runtime')}]
        E[操作系统 / 基础设施]
    end
    A --> B
    B --> C
    B --> D
    D --> E
```"""


def flow_diagram(module: str, pattern_type: str) -> str:
    flows = {
        "fundamentals": ["概念定义", "核心组件", "调用关系", "输出结果"],
        "internals": ["输入", "解析/校验", "核心处理", "状态更新", "输出"],
        "performance": ["基准测试", "瓶颈定位", "优化实施", "回归验证"],
        "security": ["威胁识别", "风险评估", "防护策略", "监控审计"],
        "case_study": ["需求分析", "方案设计", "实现部署", "效果评估"],
    }
    steps = flows.get(pattern_type, ["准备", "处理", "验证", "交付"])
    nodes = "\n".join(f"    S{i}[{s}]" for i, s in enumerate(steps))
    arrows = "\n".join(f"    S{i} --> S{i+1}" for i in range(len(steps) - 1))
    return f"""```mermaid
flowchart LR
{nodes}
{arrows}
```"""


def sequence_diagram(domain: str, module: str) -> str:
    return f"""```mermaid
sequenceDiagram
    participant Client as 客户端
    participant App as {domain}应用
    participant Core as {module}核心
    participant Store as 数据/状态层

    Client->>App: 发起请求/交互
    App->>Core: 调用{module}逻辑
    Core->>Store: 读/写数据
    Store-->>Core: 返回结果
    Core-->>App: 处理完成
    App-->>Client: 响应/更新UI
```"""


def component_diagram(module: str, concepts: list) -> str:
    items = concepts[:4] if concepts else ["输入", "处理", "输出", "配置"]
    subgraph_items = "\n".join(f"        C{i}[{c}]" for i, c in enumerate(items))
    return f"""```mermaid
graph LR
    subgraph {module}
{subgraph_items}
    end
```"""


def learning_path_diagram(modules: list, max_items: int = 8) -> str:
    items = modules[:max_items]
    nodes = "\n".join(f"    M{i}[{m}]" for i, m in enumerate(items))
    arrows = "\n".join(f"    M{i} --> M{i+1}" for i in range(len(items) - 1))
    return f"""```mermaid
flowchart TD
{nodes}
{arrows}
```"""


def module_map_diagram(modules: list) -> str:
    """模块关系图"""
    lines = []
    for i, m in enumerate(modules[:12]):
        lines.append(f"    subgraph 模块{i+1}")
        lines.append(f"        N{i}[{m}]")
        lines.append("    end")
    return f"""```mermaid
graph TB
{chr(10).join(lines)}
```"""


def pick_diagram(domain: str, module: str, pattern_type: str, stack: dict, concepts: list) -> str:
    """根据章节类型选择合适图表"""
    if pattern_type in ("fundamentals", "advanced", "design_evolution"):
        return architecture_diagram(domain, module, stack)
    if pattern_type in ("internals", "source_analysis", "deep_internals"):
        return sequence_diagram(domain, module)
    if pattern_type in ("performance", "security", "case_study", "troubleshooting", "debugging"):
        return flow_diagram(module, pattern_type)
    if pattern_type == "comparison":
        return component_diagram(module, concepts)
    return architecture_diagram(domain, module, stack)
