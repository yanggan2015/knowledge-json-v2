#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成尚未覆盖的手工内容库：系统底层、编程语言、前端开发"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from domains_100_config import DOMAINS_CONFIG

# 复用后端生成器的模块构建逻辑
from article_generator.manual._gen_backend_data import (
    _generate_module,
    _serialize_module_content,
    _serialize_overviews,
    _build_domain_overviews,
    MODULE_FACTS,
)

MANUAL = Path(__file__).parent

SYSTEM_DOMAINS = [
    "Linux内核", "Linux系统编程", "操作系统原理", "计算机网络", "编译原理",
    "计算机组成原理", "汇编语言", "嵌入式系统", "驱动开发", "虚拟化技术",
    "容器技术", "实时系统",
]
LANG_DOMAINS = [
    "C语言", "C++", "Python核心", "Python高级", "JavaScript核心", "TypeScript",
    "Java核心", "Java并发", "Go语言", "Rust语言", "PHP", "C#", "函数式编程", "面向对象编程",
]
FRONTEND_DOMAINS = [
    "HTML与CSS", "React", "Vue", "Node.js", "前端工程化", "浏览器原理",
    "Web性能优化", "PWA", "Angular", "小程序开发", "微前端", "数据可视化",
]


def load_linux_kernel_modules() -> dict:
    """Linux 内核手工模块（若生成脚本缺失则跳过）"""
    try:
        from article_generator.manual._gen_content_system import LINUX_KERNEL
        return {("Linux内核", m): d for m, d in LINUX_KERNEL.items()}
    except ImportError:
        return {}


def tech_to_module(domain: str, module: str, t: dict) -> dict:
    concepts = [{"title": a, "body": b} for a, b in t.get("concepts", [])]
    pitfalls = [{"title": a, "body": b} for a, b in t.get("pitfalls", [])]
    ref = t.get("ref0", "")
    refs = [ref] if ref else []
    refs.extend([
        f"{domain} 官方文档",
        f"{module} 相关技术规范与社区指南",
    ])
    return {
        "intro": t["intro"],
        "concepts": concepts,
        "mechanism": t["mechanism"],
        "internals": t["internals"],
        "workflow": t["workflow"],
        "performance": t["performance"],
        "security": t["security"],
        "case_study": t["case_study"],
        "configuration": t.get("configuration", ""),
        "debugging": t.get("debugging", ""),
        "comparison": t.get("comparison", ""),
        "pitfalls": pitfalls,
        "practices": list(t.get("practices", [])),
        "references": refs[:4],
    }


def build_modules(domain_names: list, extra: dict = None) -> dict:
    content = dict(extra or {})
    for cfg in DOMAINS_CONFIG:
        if cfg["name"] not in domain_names:
            continue
        domain = cfg["name"]
        for module in cfg["modules"]:
            key = (domain, module)
            if key in content:
                continue
            content[key] = _generate_module(domain, module)
    return content


def write_content_file(path: Path, title: str, domain_names: list, extra: dict = None):
    modules = build_modules(domain_names, extra)
    overviews = _build_domain_overviews(domain_names)
    header = f'''# -*- coding: utf-8 -*-
"""{title}"""

from typing import Dict, Tuple

'''
    body = _serialize_module_content(modules) + "\n\n\n" + _serialize_overviews(overviews) + "\n"
    path.write_text(header + body, encoding="utf-8")
    print(f"Wrote {path.name}: {len(modules)} modules, {len(overviews)} overviews")


def build_languages_extra() -> dict:
    from article_generator.manual._lang_tech_facts import TECH
    out = {}
    for (domain, module), t in TECH.items():
        out[(domain, module)] = tech_to_module(domain, module, t)
    return out


def build_frontend_facts():
    """扩展前端领域 MODULE_FACTS"""
    react = {
        "React基础": {
            "core": "React 是声明式 UI 库：组件描述 UI=f(state)，由 ReactDOM/createRoot 挂载到 DOM。React 18 默认创建 Concurrent Root，支持并发渲染与自动批处理。",
            "internal": "Fiber 是可中断的工作单元链表；Scheduler 按优先级调度；协调阶段生成 effect list，提交阶段一次性 DOM 更新。",
            "mechanism": "渲染流程：render 生成 React Element 树 → reconcile 对比旧 Fiber 标记 Placement/Update/Deletion → commit 阶段执行 DOM 操作与 useEffect。",
        },
        "JSX": {
            "core": "JSX 是 JavaScript 语法扩展，编译后为 React.createElement(type, props, children)。Babel @babel/preset-react 或 SWC 完成转换。",
            "internal": "jsxDEV 开发模式注入 __source/__self；生产模式剥离。Fragment <> 避免多余 DOM 包裹。",
            "mechanism": "表达式 {} 嵌入；属性 camelCase（className/htmlFor）；布尔属性简写。自定义组件必须大写开头以区分原生标签。",
        },
        "组件": {
            "core": "函数组件是主流；类组件仍支持但推荐 Hooks。组件应单一职责，通过 props 配置、state 管理内部交互状态。",
            "internal": "函数组件闭包捕获当次渲染 props/state；React.memo 浅比较 props 跳过渲染。",
        },
        "Props与State": {
            "core": "Props 父传子、只读；State 组件私有、驱动重渲染。单向数据流使数据流向可预测。",
            "internal": "Props 变更触发子组件重渲染；State 更新通过 dispatch 入队，非同步读到新值。",
        },
        "Hooks": {
            "core": "Hooks 仅在函数组件顶层调用；规则由 eslint-plugin-react-hooks 强制。共享逻辑抽为自定义 Hook。",
            "internal": "Fiber.memoizedState 链表存 hook 单元；dispatcher 区分 mount/update。",
        },
        "useState": {
            "core": "useState(initial) 返回 [state, setState]；setState 可传值或 updater。React 18 事件内多次 setState 自动批处理。",
            "internal": "queue 链表存 pending update；render 阶段计算新 state；闭包陷阱需用 setState(s=>...) 或 useRef。",
        },
        "useEffect": {
            "core": "useEffect(fn, deps) 在 paint 后执行副作用；deps 变化重新执行；返回清理函数。",
            "internal": "commit 阶段 layout（useLayoutEffect）先于 passive（useEffect）；清理在下次 effect 前或卸载时运行。",
        },
        "Context": {
            "core": "Context.Provider 向下传递 value；useContext 订阅。多 Context 拆分避免大范围重渲染。",
            "internal": "Provider value 变更时所有消费组件重渲染；可用 useMemo 稳定 value 对象引用。",
        },
        "性能优化": {
            "core": "memo/useMemo/useCallback 减少无效渲染；虚拟列表 react-window；Code Splitting React.lazy+Suspense。",
            "internal": "Profiler API 记录 commit 耗时；Concurrent 特性 defer 非紧急更新。",
        },
        "路由": {
            "core": "React Router v6 用 Routes/Route/Navigate；数据路由 createBrowserRouter+loader。",
            "internal": "history 栈管理 URL；Outlet 嵌套布局。",
        },
        "状态管理": {
            "core": "局部 state → Context → Zustand/Redux。Redux Toolkit createSlice+configureStore 简化样板。",
            "internal": "Redux 单 store+dispatch；中间件处理异步 thunk。",
        },
        "服务端渲染": {
            "core": "SSR renderToString/renderToPipeableStream；hydration 复用服务端 HTML。RSC 服务端组件减客户端 JS。",
            "internal": "hydrateRoot 对比服务端 markup；不匹配会 warning 并客户端重渲染。",
        },
    }
    vue = {
        "Vue基础": {"core": "Vue 3 应用 createApp(App).mount('#app')；响应式基于 Proxy（reactive/ref）。", "internal": "effect 依赖收集 trigger 派发更新。"},
        "组合式API": {"core": "setup() 或 <script setup>；ref/reactive/computed/watch 组合逻辑。", "internal": "编译器将 setup 绑定到组件实例。"},
        "Pinia状态管理": {"core": "defineStore 定义 store；actions 可异步；无 mutations 分层。", "internal": "基于 Vue 响应式，devtools 集成。"},
    }
    MODULE_FACTS["React"] = react
    MODULE_FACTS["Vue"] = vue


def main():
    linux = load_linux_kernel_modules()
    write_content_file(
        MANUAL / "content_system.py",
        "系统底层领域手工教程内容库",
        SYSTEM_DOMAINS,
        extra=linux,
    )

    lang_extra = build_languages_extra()
    write_content_file(
        MANUAL / "content_languages.py",
        "编程语言领域手工教程内容库",
        LANG_DOMAINS,
        extra=lang_extra,
    )

    build_frontend_facts()
    write_content_file(
        MANUAL / "content_frontend.py",
        "前端开发领域手工教程内容库",
        FRONTEND_DOMAINS,
    )

    # 覆盖率
    from article_generator.manual.registry import coverage_report, _load_all_content
    m, _ = _load_all_content()
    print("Total module entries loaded:", len(m))
    print(json.dumps(coverage_report(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
