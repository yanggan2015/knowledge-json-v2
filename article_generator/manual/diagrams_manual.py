# -*- coding: utf-8 -*-
"""模块级专属 Mermaid 图生成"""

from .content_types import ModuleKnowledge


def default_architecture(domain: str, module: str, framework: str, lang: str) -> str:
    return f"""```mermaid
graph TB
    subgraph 业务层
        A[{module}]
    end
    subgraph {framework}
        B[核心运行时]
        C[生态组件]
    end
    subgraph 基础设施
        D[{lang}]
        E[OS / 网络 / 存储]
    end
    A --> B
    B --> C
    B --> D
    D --> E
```"""


def react_fiber_render() -> str:
    return """```mermaid
flowchart LR
    A[调度器 Scheduler] --> B[协调 reconcile]
    B --> C[提交 commit]
    C --> D[DOM 更新]
    B --> E[Fiber 链表遍历]
    E --> B
```"""


def react_jsx_compile() -> str:
    return """```mermaid
flowchart LR
    A[JSX 源码] --> B[Babel / SWC]
    B --> C[React.createElement]
    C --> D[虚拟 DOM 对象]
    D --> E[React 渲染]
```"""


def react_use_state() -> str:
    return """```mermaid
sequenceDiagram
    participant C as 组件
    participant H as Hooks 链表
    participant S as 调度器
  participant D as DOM
    C->>H: useState 读取 state
    C->>H: setState 入队更新
    H->>S: 标记 Fiber 待更新
    S->>C: 重新渲染
    C->>D: commit 阶段更新 UI
```"""


def flask_request_cycle() -> str:
    return """```mermaid
sequenceDiagram
    participant W as Werkzeug
    participant F as Flask
    participant V as 视图函数
    participant T as 模板
    W->>F: WSGI 请求
    F->>F: 路由匹配
    F->>V: dispatch
    V->>T: render_template
    T-->>V: HTML
    V-->>F: Response
    F-->>W: WSGI 响应
```"""


def k8s_pod_service() -> str:
    return """```mermaid
graph LR
    Ingress --> Service
    Service --> Pod1
    Service --> Pod2
    Pod1 --> Container
    Pod2 --> Container
```"""


def pick_module_diagram(domain: str, module: str, knowledge: ModuleKnowledge) -> str:
    if knowledge.mermaid:
        return knowledge.mermaid

    key = (domain, module)
    presets = {
        ("React", "React基础"): react_fiber_render(),
        ("React", "JSX"): react_jsx_compile(),
        ("React", "useState"): react_use_state(),
        ("Flask", "Flask基础"): flask_request_cycle(),
        ("Flask", "请求响应"): flask_request_cycle(),
        ("Kubernetes", "Pod"): k8s_pod_service(),
        ("Kubernetes", "Service"): k8s_pod_service(),
    }
    if key in presets:
        return presets[key]

    from article_generator.knowledge import get_stack
    stack = get_stack(domain)
    return default_architecture(domain, module, stack.get("framework", domain), stack.get("lang", ""))
