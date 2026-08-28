#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_languages.py — hand-authored programming language tutorial content."""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import importlib.util

def _load_specs():
    spec_path = Path(__file__).resolve().parent / "_content_specs_languages.py"
    spec = importlib.util.spec_from_file_location("_content_specs_languages", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LANG_SPECS, mod.LANG_DETAILED

_specs = _load_specs()
LANG_SPECS, LANG_DETAILED = _specs

from domains_100_config import DOMAINS_CONFIG

LANG_DOMAINS = [
    "C语言", "C++", "Python核心", "Python高级", "JavaScript核心", "TypeScript",
    "Java核心", "Java并发", "Go语言", "Rust语言", "PHP", "C#", "函数式编程", "面向对象编程",
]

OUTPUT = Path("/workspace/article_generator/manual/content_languages.py")

DOMAIN_OVERVIEWS = {
    "C语言": {
        "intro": "C 语言是 Unix 与现代系统软件的基石，直接映射硬件与操作系统 ABI，"
                 "在嵌入式、操作系统、编译器与高性能库中仍不可替代。",
        "positioning": "从语法与内存模型入手，建立对指针、编译链接与 UB 的严谨理解，"
                       "为阅读 Linux 内核、数据库引擎与 FFI 边界打基础。",
        "prerequisites": ["基本计算机组成与二进制表示", "命令行与 Makefile 基础", "算法与数据结构入门"],
        "outcomes": [
            "能编写符合 C17 标准、可移植且安全的模块级 C 代码",
            "理解指针、内存布局与链接模型，能排查段错误与内存泄漏",
            "能阅读 glibc/内核等 C 源码的关键路径",
            "掌握 Valgrind/ASan 等工具链进行质量保障",
        ],
        "ecosystem": "GCC/Clang、Make/CMake、gdb、Valgrind、glibc/musl、Linux man pages",
    },
    "C++": {
        "intro": "C++ 在 C 之上引入 RAII、泛型与零开销抽象，是游戏引擎、浏览器、"
                 "高频交易与系统中间件的主力语言。",
        "positioning": "覆盖 OOP、模板元编程、STL 与现代并发，强调值语义、移动语义与异常安全。",
        "prerequisites": ["C 语言基础与指针", "面向对象基本概念", "数据结构与算法"],
        "outcomes": [
            "熟练使用现代 C++（C++17/20）编写类型安全、可维护代码",
            "理解 RAII、智能指针与 STL 复杂度保证",
            "能设计异常安全接口并做性能剖析",
            "掌握多线程与内存模型基础",
        ],
        "ecosystem": "GCC/Clang/MSVC、CMake、Boost、STL、GoogleTest、perf、Compiler Explorer",
    },
    "Python核心": {
        "intro": "Python 以可读性与丰富生态著称，是数据科学、自动化运维与 Web 后端的默认选择之一。",
        "positioning": "系统掌握语法、对象模型、标准库与工程化实践，为高级主题与框架开发奠基。",
        "prerequisites": ["编程入门经验", "基本命令行操作", "文本编辑器或 IDE 使用"],
        "outcomes": [
            "熟练运用 Python 3 核心语法与标准库",
            "理解对象模型、迭代器协议与异常体系",
            "能组织模块、包与虚拟环境",
            "遵循 PEP 8 与类型提示最佳实践",
        ],
        "ecosystem": "CPython、pip/venv/poetry、PyPI、pytest、mypy、Black、官方 docs.python.org",
    },
    "Python高级": {
        "intro": "Python 高级主题涵盖解释器 internals、并发模型、元编程与性能优化，"
                 "面向需要突破 GIL 或构建框架的工程师。",
        "positioning": "深入 CPython 实现、asyncio、描述符与 C 扩展，连接语言特性与系统性能。",
        "prerequisites": ["Python 核心语法与 OOP", "基本网络与 IO 概念", "多线程基础知识"],
        "outcomes": [
            "理解 GIL、asyncio 事件循环与进程/线程选型",
            "能使用描述符、元类与 typing 构建可扩展 API",
            "掌握 cProfile、memory_profiler 与 Cython 优化路径",
            "能编写 C 扩展或 ctypes 绑定",
        ],
        "ecosystem": "asyncio、aiohttp、Cython、CFFI、multiprocessing、uvloop、py-spy",
    },
    "JavaScript核心": {
        "intro": "JavaScript 是唯一内置全平台浏览器引擎的语言，ES 规范持续演进，"
                 "Node.js 将其延伸至服务端与工具链。",
        "positioning": "从原型链、闭包到 ES Module 与 Promise，建立浏览器与 Node 通用的语言直觉。",
        "prerequisites": ["HTML/CSS 基础（浏览器场景）", "基本编程概念", "HTTP 基础"],
        "outcomes": [
            "精通 JS 类型系统、作用域与 this 绑定规则",
            "熟练使用 Promise/async-await 与模块化",
            "理解事件循环与微任务队列",
            "能在浏览器与 Node 环境调试与测试",
        ],
        "ecosystem": "V8/SpiderMonkey、Node.js、npm、Webpack/Vite、Jest、MDN、TC39 提案",
    },
    "TypeScript": {
        "intro": "TypeScript 为 JavaScript 添加结构化类型系统，在大型前端与全栈项目中"
                 "提供编译期约束与 IDE 智能提示。",
        "positioning": "掌握类型推断、泛型、条件类型与工程配置，使类型服务于可维护性而非阻碍表达。",
        "prerequisites": ["JavaScript ES6+ 语法", "npm 与模块系统", "基本面向对象概念"],
        "outcomes": [
            "能设计清晰的 interface/type 层次",
            "配置 tsconfig 并集成构建工具",
            "使用类型守卫与泛型编写复用组件",
            "理解声明合并、模块解析与 JS 互操作",
        ],
        "ecosystem": "tsc、ts-node、ESLint typescript-eslint、Vite、React/Vue 类型定义、DefinitelyTyped",
    },
    "Java核心": {
        "intro": "Java 通过 JVM 实现「一次编写，到处运行」，在企业后端、Android 与大数据"
                 "生态中拥有成熟工具链与人才储备。",
        "positioning": "覆盖 OOP、集合、IO/NIO、反射与 JVM 内存/GC/类加载，建立平台级思维。",
        "prerequisites": ["面向对象基础", "基本算法与数据结构", "命令行与 IDE 使用"],
        "outcomes": [
            "熟练使用 Java 8+ 特性与集合框架",
            "理解 JVM 堆栈、GC 与类加载机制",
            "能使用 NIO、注解与反射构建可扩展组件",
            "遵循 Effective Java 与模块化最佳实践",
        ],
        "ecosystem": "OpenJDK、Maven/Gradle、IntelliJ IDEA、JUnit、Spring（进阶）、JFR/async-profiler",
    },
    "Java并发": {
        "intro": "Java 并发包（java.util.concurrent）提供从锁到无锁、从线程池到 CompletableFuture"
                 "的完整工具集，是高性能服务端必修课。",
        "positioning": "以 JMM、AQS 与 j.u.c 源码为纲，理解可见性、有序性与 happens-before 规则。",
        "prerequisites": ["Java 核心语法与 OOP", "基本操作系统进程线程概念", "集合与异常处理"],
        "outcomes": [
            "正确使用 synchronized、Lock 与原子类",
            "能配置与调优 ThreadPoolExecutor",
            "理解 AQS 与常见同步器实现原理",
            "能诊断死锁、活锁与线程饥饿",
        ],
        "ecosystem": "j.u.c、JMH、JVisualVM、async-profiler、Doug Lea JSR-166、Java Concurrency in Practice",
    },
    "Go语言": {
        "intro": "Go 由 Google 设计，以简洁语法、快速编译与内置并发（goroutine/channel）"
                 "著称，是云原生与基础设施的热门选择。",
        "positioning": "从 goroutine M:N 调度到 interface 隐式实现，强调简单、显式错误处理与可观测性。",
        "prerequisites": ["至少一门命令式语言经验", "HTTP 与网络基础", "基本命令行操作"],
        "outcomes": [
            "熟练使用 goroutine、channel 与 context 构建并发服务",
            "理解 GMP 调度与 GC 对延迟的影响",
            "能编写 table-driven 测试与 benchmark",
            "掌握 go mod 与标准库 idiomatic 用法",
        ],
        "ecosystem": "go toolchain、pprof、Delve、Kubernetes/Docker（生态）、Prometheus、Effective Go",
    },
    "Rust语言": {
        "intro": "Rust 通过所有权、借用与生命周期在编译期保证内存与线程安全，"
                 "无需 GC 即可实现系统级性能。",
        "positioning": "从所有权模型到 trait 泛型与 async，理解零成本抽象与安全边界。",
        "prerequisites": ["C/C++ 或系统编程基础更佳", "指针与内存概念", "基本算法能力"],
        "outcomes": [
            "能通过编译器反馈理解并修复借用检查错误",
            "使用 Result/Option 与模式匹配处理错误",
            "编写并发安全代码与 async/await 程序",
            "使用 cargo 管理依赖与测试",
        ],
        "ecosystem": "rustc/cargo、crates.io、clippy、miri、Tokio、The Rust Book、Rustonomicon",
    },
    "PHP": {
        "intro": "PHP 是 Web 动态页面历史上最广泛部署的语言之一，PHP 7+ 性能大幅提升，"
                 "Laravel/Symfony 提供现代 MVC 开发体验。",
        "positioning": "从语言基础到 Composer 生态与 Laravel 入门，关注 Web 安全与请求生命周期。",
        "prerequisites": ["HTML 与 HTTP 基础", "基本 SQL", "命令行与 Web 服务器概念"],
        "outcomes": [
            "编写符合 PSR 标准的现代 PHP 代码",
            "理解 PHP-FPM 请求模型与 OPcache",
            "使用 PDO 安全访问数据库",
            "掌握 Composer 依赖管理与自动加载",
        ],
        "ecosystem": "PHP-FPM、Nginx/Apache、Composer、Laravel、PHPUnit、PHPStan、php.net 文档",
    },
    "C#": {
        "intro": "C# 是 .NET 平台主力语言，融合 OOP、LINQ、async/await 与跨平台运行时，"
                 "适用于 Web、桌面、游戏（Unity）与云原生。",
        "positioning": "覆盖类型系统、委托事件、LINQ 与 ASP.NET 基础，理解 CLR 与 GC 行为。",
        "prerequisites": ["面向对象基础", "基本 HTTP 与数据库概念", "IDE（VS/ Rider）使用"],
        "outcomes": [
            "熟练使用 C# 10+ 语法与 .NET 基础类库",
            "理解值类型/引用类型、装箱与 async 状态机",
            "使用 LINQ 与依赖注入构建可测试代码",
            "能部署 ASP.NET Core 应用",
        ],
        "ecosystem": ".NET SDK、NuGet、Visual Studio/Rider、xUnit、ASP.NET Core、Entity Framework",
    },
    "函数式编程": {
        "intro": "函数式编程强调不可变数据、纯函数与声明式组合，"
                 "影响 Haskell、Scala、Clojure 及现代 JS/Python 风格。",
        "positioning": "从 λ 演算直觉到 Monad 与代数数据类型，建立与命令式思维互补的抽象工具箱。",
        "prerequisites": ["至少一门编程语言经验", "基本集合与映射概念", "递归初步理解"],
        "outcomes": [
            "能识别并应用纯函数、高阶函数与不可变性",
            "理解 Functor/Applicative/Monad 的动机与限制",
            "使用模式匹配与 ADT 建模领域",
            "在混合范式语言中平衡 FP 与实用主义",
        ],
        "ecosystem": "Haskell、Scala、Clojure、F#、Ramda/lodash-fp、Category Theory for Programmers",
    },
    "面向对象编程": {
        "intro": "面向对象编程通过封装、继承、多态与抽象管理复杂性，"
                 "是 Java/C++/C# 等语言的核心范式，也与设计模式、DDD 紧密相关。",
        "positioning": "从 UML 到 SOLID 与设计模式，强调职责划分、可测试性与演进式重构。",
        "prerequisites": ["基本编程语法", "数据结构与算法入门", "阅读类图与序列图的意愿"],
        "outcomes": [
            "能设计内聚的类与接口并避免继承滥用",
            "应用 SOLID 原则评估架构",
            "识别并重构常见坏味道",
            "使用 UML 与领域模型沟通设计",
        ],
        "ecosystem": "UML 工具、Design Patterns（GoF）、Refactoring（Fowler）、DDD、各语言 OOP 文档",
    },
}


def _facts(domain: str, module: str) -> dict:
    return LANG_SPECS.get(domain, {}).get(module, {})


def _generate_module(domain: str, module: str) -> dict:
    key = (domain, module)
    if key in LANG_DETAILED:
        return LANG_DETAILED[key]

    f = _facts(domain, module)
    if not f:
        raise ValueError(f"Missing LANG_SPECS for ({domain!r}, {module!r})")

    intro = f.get("intro", f["core"])
    concepts_raw = f.get("concepts")
    if concepts_raw:
        concepts = [{"title": t, "body": b} for t, b in concepts_raw]
    else:
        concepts = [
            {"title": f.get("c1_title", f"{module}核心原理"), "body": f["core"]},
            {"title": f.get("c2_title", "底层实现"), "body": f["internal"]},
            {"title": f.get("c3_title", "工作机制"), "body": f.get("mechanism", f["core"])},
            {"title": f.get("c4_title", "工程应用"), "body": f.get("case_study", f.get("workflow", f["core"]))},
        ]
        if f.get("c5_title") or f.get("c5_body"):
            concepts.append({"title": f.get("c5_title", "对比与选型"), "body": f.get("c5_body", f.get("comparison", f["internal"]))})

    pitfalls_raw = f.get("pitfalls")
    if pitfalls_raw:
        pitfalls = [{"title": t, "body": b} for t, b in pitfalls_raw]
    else:
        pitfalls = [
            {"title": p["title"], "body": p["body"]}
            for p in f.get("pitfall_list", [
                {"title": f.get("p1_title", "误用场景"), "body": f.get("p1", f"在不适合的场景过度使用 {module}，应回到问题本质评估替代方案。")},
                {"title": f.get("p2_title", "版本与兼容性"), "body": f.get("p2", f"{domain} 版本升级可能改变 {module} 语义，升级前对照变更日志与迁移指南。")},
                {"title": f.get("p3_title", "可观测性不足"), "body": f.get("p3", f"未对 {module} 关键路径配置日志与指标，生产故障难以快速定位。")},
            ])
        ]

    practices = f.get("practices", [
        f"遵循 {domain} 官方关于 {module} 的推荐用法",
        f"为 {module} 编写单元测试覆盖边界与错误路径",
        "关键配置纳入版本管理与 Code Review",
        "生产变更前在预发环境压测验证",
    ])

    references = f.get("references", [
        f"{domain} 官方文档 — {module}",
        f.get("ref2", f"《{domain}权威教程》相关章节"),
        f.get("ref3", "相关开源项目源码与设计文档"),
    ])

    def _g(key: str, default: str) -> str:
        v = f.get(key)
        return v if v else default

    return {
        "intro": intro,
        "concepts": concepts[:5],
        "mechanism": _g("mechanism", f["core"]),
        "internals": f["internal"],
        "workflow": _g("workflow", f"学习 {module}：阅读官方文档 → 最小示例验证 → 集成项目 → 测试与观测 → 性能与安全审查。"),
        "performance": _g("performance", f"{module} 性能：Profiling 定位热点；优先算法与 I/O；避免过早微优化。"),
        "security": _g("security", f"{module} 安全：输入校验、最小权限、敏感数据不入日志；关注 {domain} 安全公告。"),
        "case_study": _g("case_study", f"典型 {domain} 项目中 {module} 用于核心链路；拆分职责、补充测试与监控可显著降低故障率。"),
        "configuration": _g("configuration", f.get("config") or f"{module} 相关选项应外部化配置，区分 dev/staging/prod。"),
        "debugging": _g("debugging", f"排查 {module}：复现最小用例 → 日志/trace → 对照文档与源码 → 补充回归测试。"),
        "comparison": _g("comparison", f"选型 {module} 时对比 {domain} 内置方案与第三方库的功能、性能、维护成本与团队熟悉度。"),
        "pitfalls": pitfalls[:3],
        "practices": practices[:4],
        "references": references[:3],
    }


def _build_module_content() -> Dict[Tuple[str, str], dict]:
    content = {}
    for cfg in DOMAINS_CONFIG:
        if cfg["name"] not in LANG_DOMAINS:
            continue
        domain = cfg["name"]
        for module in cfg["modules"]:
            content[(domain, module)] = _generate_module(domain, module)
    return content


def _serialize_module_content(content: dict) -> str:
    lines = ["MODULE_CONTENT: Dict[Tuple[str, str], dict] = {"]
    for (domain, module), d in sorted(content.items()):
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        blob = blob.replace(": null", ": None").replace(": null,", ": None,")
        indented = textwrap.indent(blob, "    ")
        lines.append(f"    ({domain!r}, {module!r}): {indented.strip()},")
    lines.append("}")
    return "\n".join(lines)


def _serialize_overviews() -> str:
    lines = ["DOMAIN_OVERVIEWS: Dict[str, dict] = {"]
    for name, d in sorted(DOMAIN_OVERVIEWS.items()):
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        indented = textwrap.indent(blob, "    ")
        lines.append(f"    {name!r}: {indented.strip()},")
    lines.append("}")
    return "\n".join(lines)


def main():
    content = _build_module_content()
    header = textwrap.dedent('''\
        # -*- coding: utf-8 -*-
        """编程语言领域手工教程内容库

        覆盖 C/C++/Python/JS/TS/Java/Go/Rust/PHP/C# 及函数式与 OOP 范式。
        每个 (domain, module) 含 intro、concepts、mechanism、internals 等完整字段。
        """

        from typing import Dict, Tuple

    ''')
    body = _serialize_module_content(content) + "\n\n\n" + _serialize_overviews() + "\n"
    OUTPUT.write_text(header + body, encoding="utf-8")
    print(f"Wrote {OUTPUT} — {len(content)} modules, {len(DOMAIN_OVERVIEWS)} overviews")


if __name__ == "__main__":
    main()
