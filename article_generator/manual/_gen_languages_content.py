#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_languages.py with hand-authored technical content."""

from __future__ import annotations
import textwrap

OUTPUT = "/workspace/article_generator/manual/content_languages.py"

LANG_DOMAINS = [
    "C语言", "C++", "Python核心", "Python高级", "JavaScript核心", "TypeScript",
    "Java核心", "Java并发", "Go语言", "Rust语言", "PHP", "C#", "函数式编程", "面向对象编程",
]


def _m(
    intro, concepts, mechanism, internals, workflow, performance,
    security, case_study, configuration, debugging, comparison,
    pitfalls, practices, references,
):
    return {
        "intro": intro,
        "concepts": [{"title": t, "body": b} for t, b in concepts],
        "mechanism": mechanism,
        "internals": internals,
        "workflow": workflow,
        "performance": performance,
        "security": security,
        "case_study": case_study,
        "configuration": configuration,
        "debugging": debugging,
        "comparison": comparison,
        "pitfalls": [{"title": t, "body": b} for t, b in pitfalls],
        "practices": list(practices),
        "references": list(references),
    }


# ===================================================================
# DOMAIN OVERVIEWS (14 domains)
# ===================================================================
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


def _refs(domain: str, *extra: str) -> list[str]:
    base = {
        "C语言": ["ISO/IEC 9899 C17", "《C 程序设计语言》K&R", "GNU C Manual"],
        "C++": ["cppreference.com", "《Effective Modern C++》", "C++ Core Guidelines"],
        "Python核心": ["docs.python.org 3", "《Fluent Python》", "PEP 8"],
        "Python高级": ["Python Internals", "《High Performance Python》", "asyncio 文档"],
        "JavaScript核心": ["MDN JavaScript Guide", "《You Don't Know JS》", "ECMA-262"],
        "TypeScript": ["typescriptlang.org Handbook", "《Programming TypeScript》", "DefinitelyTyped"],
        "Java核心": ["《Effective Java》", "OpenJDK 文档", "JLS Java Language Specification"],
        "Java并发": ["《Java Concurrency in Practice》", "JSR-133 JMM", "Doug Lea j.u.c 文档"],
        "Go语言": ["Effective Go", "Go Spec", "《Go 语言设计与实现》"],
        "Rust语言": ["The Rust Book", "Rustonomicon", "Rust Reference"],
        "PHP": ["php.net 手册", "PSR 标准", "《Modern PHP》"],
        "C#": ["Microsoft C# 文档", "《C# in Depth》", ".NET 文档"],
        "函数式编程": ["《Structure and Interpretation of Computer Programs》", "Category Theory for Programmers", "Haskell Wiki"],
        "面向对象编程": ["《Design Patterns》GoF", "《Refactoring》Fowler", "《Clean Architecture》"],
    }
    r = list(base.get(domain, ["官方文档", "权威书籍", "开源项目源码"]))
    for e in extra:
        if e and e not in r:
            r[0] = e  # replace first with module-specific when provided
    if extra and extra[0]:
        return [extra[0], r[1], r[2]]
    return r


# Module-specific content registry: (domain, module) -> kwargs for _m
# Each entry is hand-authored with real technical focus.

MODULE_SPECS: dict[tuple[str, str], dict] = {}

def _reg(domain, module, **kw):
    MODULE_SPECS[(domain, module)] = kw


# ---------- C 语言 (13) ----------
for _mod, _intro, _mech, _int, _wf, _perf, _sec, _case, _conf, _dbg, _cmp, _concepts, _pit, _prac in [
("C语言基础", "C 程序从 main 入口经编译链接为机器码；理解翻译单元、链接符号与 ABI 是阅读任何 C 代码的前提。",
 "预处理展开宏与 #include → 编译器生成目标文件 → 链接器解析符号合并 .o 与 libc → 加载器映射 ELF/PE 并跳转 _start。",
 "GCC c-parser / Clang Lexer 将源码转为 AST；cc1 输出汇编，as 生成 .o；ld 处理 GOT/PLT 与重定位。",
 "编写 .c/.h → gcc -std=c17 -Wall -O2 → 运行；多文件项目用 Makefile 声明依赖。",
 "PGO 与 LTO 跨单元内联；热点循环可向量化（-ftree-vectorize）。",
 "栈保护 -fstack-protector；FORTIFY_SOURCE 检查 libc 边界；禁用 gets 等危险 API。",
 "嵌入式：startup 设置 SP、清零 BSS、调用 main；无 OS 时直接 MMIO。",
 "CFLAGS/CXXFLAGS、-D 宏、-I/-L 路径；交叉编译指定 --target。",
 "gdb break/ watch；ASan -fsanitize=address；编译保留 -g。",
 "C 无 GC/泛型，ABI 最稳定，适合 OS/驱动/FFI；Rust/Go 在安全性上更现代。",
 [("翻译单元", "每个 .c 独立编译；static 内部链接，extern 跨文件。"), ("main 与启动", "argc/argv 传参；CRT 初始化堆栈与全局对象。"),
  ("标准版本", "C17/C23 新特性；MSVC/GCC 扩展需条件编译。"), ("可移植类型", "stdint.h 固定宽度；char 符号性实现定义。")],
 [("忽略警告", "-Wall 应视为错误。"), ("头文件定义变量", "导致多重定义。"), ("依赖 UB", "有符号溢出可被优化掉。")],
 ["CI 启用 -Werror", "头文件 include guard", "API 用 Doxygen", "跨平台用 stdint.h"]),
("数据类型", "C 类型决定内存布局与对齐；sizeof/_Alignof 影响结构体 padding、网络协议与硬件寄存器映射。",
 "表达式遵循 integer promotions；usual arithmetic conversions 统一操作数类型后运算。",
 "Itanium ABI 规定结构体传参方式；位域布局实现定义，不可移植假设。",
 "声明→初始化→运算注意提升→赋值检查截断→跨模块用 int32_t 等。",
 "结构体字段重排减少 padding；位域省空间但访问慢。",
 "有符号/无符号混比导致边界检查失效。",
 "协议结构体 __attribute__((packed)) + htons 处理 endian。",
 "stdbool.h、complex.h；C11 _Generic 类型选择。",
 "-Wformat；gdb p 查看布局。",
 "C11 _Generic 模拟泛型；C++ template 更安全。",
 [("整数提升", "char/short 提升为 int 参与运算。"), ("指针 decay", "数组名常 decay 为 T*。"),
  ("对齐", "padding 由对齐要求决定；packed 可能 unaligned fault。"), ("typedef", "创建别名非新类型。")],
 [("假设 int 32 位", "用 stdint。"), ("memcpy 含 padding", "逐字段或 memset。"), ("符号混用", "-1 > 0U 为真。")],
 ["对外接口 stdint.h", "画内存布局图", "-Wconversion", "序列化显式 endian"]),
("运算符与表达式", "C 运算符优先级与结合性决定求值顺序；逻辑短路、位运算与序列点是常见面试与 bug 来源。",
 "除法向零截断；% 结果符号同被除数；移位 >= 位宽是 UB。",
 "编译器常量折叠在编译期完成；volatile 禁止优化重排。",
 "写表达式时加括号明确意图；避免 i++ + i++ 等未指定顺序。",
 "位运算替代乘除 2 的幂；短路避免副作用。",
 "无检查运算溢出是漏洞面。",
 "权限位掩码用 unsigned 与显式 mask。",
 "编译器扩展 ??=（C23）。",
 "-Wsequence-point；简化复杂表达式。",
 "与 Python/Java 不同，C 几乎无运算符重载。",
 [("优先级", "算术>移位>关系>逻辑>赋值。"), ("短路", "&& || 不评估右侧。"),
  ("副作用", "同一表达式多次修改同一对象未指定顺序。"), ("位运算", "& | ^ ~ << >> 用于标志位。")],
 [("混淆 = 与 ==", "笔误常见。"), ("移位负数", "UB。"), ("宏参数多次求值", "用 do-while 或 inline。")],
 ["复杂条件拆变量", "宏用括号保护参数", "位运算用 unsigned", "C23 逐步采用"]),
("流程控制", "if/else、switch、for/while/do-while 与 goto 构成控制流；switch 的 fall-through 与 Duff's device 是经典技巧。",
 "switch 常编译为跳转表或二分；范围 case（GCC extension）优化稠密枚举。",
 "setjmp/longjmp 非本地跳转跳过析构（C++ 混编危险）。",
 "先画控制流图再编码；循环不变式写注释。",
 "热路径减少分支；likely/unlikely 宏提示分支预测。",
 "switch 缺 default 可能遗漏枚举新值。",
 "状态机用 enum + switch 清晰可读。",
 "C23 #warning、#embed。",
 "gdb until/ finish 跟踪循环。",
 "与 Rust match 比，C switch 无穷尽检查。",
 [("if 与 ?: ", "三元运算符右结合。"), ("switch fall-through", "需 break 或注释 intentional。"),
  ("循环", "for 最常用；do-while 至少一次。"), ("goto cleanup", "集中资源释放惯用法。")],
 [("死循环条件", "浮点比较慎用。"), ("switch 无 break", "意外贯穿。"), ("goto 滥用", "仅 cleanup 标签。")],
 ["状态机 enum", "循环边界单元测试", "早返回减嵌套", "McCabe 复杂度控制"]),
("函数", "函数是 C 模块化单元；原型声明、static 内部函数、inline 与函数指针支撑回调与 OOP-in-C 模式。",
 "调用约定（cdecl/stdcall）决定参数入栈顺序与谁清理栈；x86-64 System V 用寄存器传参。",
 "inline 建议编译器内联；LTO 跨文件内联；never inline 防代码膨胀。",
 "头文件声明原型；.c 定义；static 限制可见性；函数指针 typedef 简化。",
 "小函数 inline；递归注意栈深度；尾递归未必优化。",
 "函数指针来自不可信输入可劫持控制流。",
 "qsort/bsearch 回调比较函数；事件分发函数表。",
 "static inline 放头文件；GNU attribute hot/cold。",
 "gdb info functions；断点在回调。",
 "函数指针 vs C++ std::function 开销对比。",
 [("原型", "无原型调用旧式默认提升（废弃）。"), ("static", "内部链接隐藏符号。"),
  ("函数指针", "回调与状态机。"), ("可变参数", "stdarg.h；类型安全靠约定。")],
 [("缺少原型", "隐式 int。"), ("递归无终止", "栈溢出。"), ("va_list 类型错", "UB。")],
 ["头文件完整原型", "static 隐藏实现", "回调文档化线程安全", "大函数拆分"]),
("数组与指针", "数组与指针关系密切但不同；指针算术、const 正确性与指针别名规则影响优化与正确性。",
 "a[i] 等价 *(a+i)；restrict 承诺无别名助优化。",
 "strict aliasing：通过不兼容类型指针访问对象是 UB。",
 "传递数组 decay 为指针；长度须另传；灵活数组成员 FAM 用于变长 struct。",
 "行优先矩阵行指针数组缓存友好。",
 "越界读写经典漏洞。",
 "缓冲区用 size 参数；strnlen 替代 strlen。",
 "编译选项 -fno-strict-aliasing 调试别名问题。",
 "watchpoint 监视指针；ASan 报 heap-buffer-overflow。",
 "C 无 slice 类型；C++ span 更安全。",
 [("decay", "sizeof(array) vs sizeof(pointer)。"), ("指针算术", "仅同对象数组内有效。"),
  ("const T*", "不能改指向对象；const 位置影响指针本身。"), ("void*", "通用指针需 cast。")],
 [("返回局部数组", "悬垂指针。"), ("未初始化指针", "随机崩溃。"), ("指针相减跨数组", "UB。")],
 ["传 size+指针", "restrict 助优化", "边界检查封装", "禁返回栈数组地址"]),
("结构体与联合", "struct 聚合成员；union 共享存储；位域与柔性数组实现紧凑协议与变长消息。",
 "成员对齐插入 padding；offsetof 宏查询偏移。",
 "union 写一读另一类型是 type punning；C99 常用 memcpy 实现合法 pun。",
 "设计 API 返回 struct 而非多个 out 参数；opaque struct 隐藏实现。",
 "小 struct 值传递；大 struct 指针传递。",
 "union 解析网络包需验证 tag 防类型混淆。",
 "TLV 协议用 struct + union enum tag。",
 "#pragma pack 与文档化布局。",
 "p *(MyStruct*)addr 查看内存。",
 "与 C++ class 比无方法、构造析构需手动。",
 [("struct", "成员顺序影响大小。"), ("union", "所有成员同地址。"),
  ("位域", "实现定义宽度与符号。"), ("柔性数组", "C99 末尾 [0] 或 []。")],
 [("未初始化 padding", "memcmp 不一致。"), ("别名 union", "违反 strict aliasing。"), ("位域跨字节", "不可移植。")],
 ["文档化布局", "opaque 指针", "tagged union", "offsetof 验证"]),
("内存管理", "C 手动 malloc/calloc/realloc/free；堆栈分配、内存池与碎片是性能与稳定性关键。",
 "malloc 从 brk/mmap 获页；free 合并相邻块；glibc ptmalloc 多 arena 减锁争用。",
 "mmap 大块直接映射；mprotect 改页权限；jemalloc/tcmalloc 替代分配器。",
 "谁分配谁释放；配对 free； realloc 失败原块仍有效。",
 "对象池复用；栈分配 alloca/_alloca 慎用。",
 "double-free、UAF、泄漏；启用 ASan/Valgrind。",
 "网络服务器 per-connection 池化 buffer。",
 "MALLOC_ARENA_MAX、LD_PRELOAD jemalloc。",
 "Valgrind memcheck；ASan leak；mtrace。",
 "GC 语言省心；C 需明确所有权。",
 [("malloc/free", "堆生命周期手动管理。"), ("calloc", "清零分配。"),
  ("realloc", "可能移动块。"), ("栈溢出", "大数组放堆。")],
 [("泄漏", "无 free。"), ("double free", "崩溃或 exploit。"), ("realloc 丢指针", "泄漏旧块。")],
 ["RAII 包装（C++）", "统一 alloc 层", "CI 跑 ASan", "大小为 0 的 malloc 合法"]),
("文件IO", "stdio（fopen/fread）与 POSIX（open/read/write）两层 API；缓冲、定位与 errno 错误处理是重点。",
 "stdio 全缓冲/行缓冲/无缓冲；setvbuf 控制；fflush 刷用户缓冲。",
 "内核 page cache；read/write 系统调用；O_DIRECT 绕过 cache。",
 "打开→读/写循环→ferror/feof 检查→fclose；二进制模式 Windows 下 \"rb\"。",
 "大块 fread/fwrite；mmap 大文件；sendfile 零拷贝。",
 "路径遍历、TOCTOU；fopen 用户路径需校验。",
 "日志轮转 append 模式；配置文件只读打开。",
 "setvbuf _IOFBF；O_SYNC 持久化。",
 "strace 跟踪 syscall；errno  perror。",
 "stdio 便携；POSIX 更底层可控。",
 [("FILE*", "stdio 抽象。"), ("fd", "POSIX 整数句柄。"),
  ("errno", "线程局部错误码。"), ("二进制 IO", "struct 读写注意 endian。")],
 [("忘记 fclose", "泄漏 fd。"), ("文本模式", "Windows CRLF。"), ("忽略返回值", "部分读。")],
 ["检查返回值", "RAII fclose", "大文件 mmap", "路径白名单"]),
("预处理", "预处理器在编译前处理 #include/#define/#if；宏是元编程与跨平台条件编译核心。",
 "词法替换非 AST 操作；宏展开递归终止于未再匹配的宏名。",
 "预编译输出 .i；#line 保留行号供诊断。",
 "头文件 guard；#ifdef 平台分支；X 宏生成重复代码。",
 "复杂宏改 inline 函数或 _Generic。",
 "宏注入若来自不可信源危险。",
 "LOG 宏带 __FILE__/__LINE__；ASSERT 宏。",
 "-E -dM 查看宏定义。",
 "gcc -E 查看展开；clang -cc1 -dump-tokens。",
 "与 C++ template/constexpr if 对比。",
 [("#include", "尖括号系统头，引号本地。"), ("#define", "对象宏与函数宏。"),
  ("#if/#ifdef", "条件编译。"), ("#pragma", "once、pack、message。")],
 [("宏无类型", "多次求值副作用。"), ("缺少括号", "优先级 bug。"), ("过深嵌套 #if", "难维护。")],
 ["复杂逻辑用 static inline", "X 宏文档化", "clang-format 不格式化宏区", "Prefer enum/const"]),
("高级特性", "C99/C11/C23 带来 VLAs（可选）、复合字面量、指定初始化、_Generic、_Static_assert 等现代能力。",
 "_Generic 编译期多态；_Atomic 与 stdatomic.h 无锁；threads.h 可选线程。",
 "stdalign.h、stdnoreturn.h；C23 #embed 二进制嵌入。",
 "指定初始化 .field=value 清晰；复合字面量 (struct S){1,2} 临时对象。",
 "atomics 比 mutex 轻但仅简单类型。",
 "_Static_assert 编译期约束 API。",
 "插件系统 _Generic 分派版本 API。",
 "-std=c23 -embed-dir。",
 "static_assert 失败信息可读。",
 "C23 逐步接近 C++ 部分特性仍更简单。",
 [("指定初始化", "C99 顺序无关。"), ("复合字面量", "左值临时。"),
  ("_Generic", "类型选择表达式。"), ("stdatomic", "memory_order 语义。")],
 [("VLA 栈溢出", "大数组禁 VLA。"), ("atomics 误用", "需 memory_order。"), ("threads.h 可移植", "部分编译器缺失。")],
 ["优先标准特性", "atomics 查手册", "static_assert API", "弃用 VLA"]),
("C标准库", "C 标准库提供 stdio、stdlib、string、math、time 等；理解实现差异与线程安全属性至关重要。",
 "glibc/musl/BSD libc 行为细节不同；reentrant 函数 _r 后缀。",
 "printf 解析格式串；locale 影响 collation；setlocale 非线程安全。",
 "查 man 确认 POSIX 扩展；优先 strlcpy（BSD）或 snprintf 防溢出。",
 "qsort 快排 O(n log n)；bsearch 需有序。",
 "gets 移除；strcpy 改 strncpy/snprintf。",
 "配置解析用 strtol 检 errno。",
 "feature test macro _POSIX_C_SOURCE。",
 "LD_DEBUG 查动态链接；glibc malloc 钩子调试。",
 "C++ iostream 更重；C stdio 更轻量。",
 [("stdio.h", "格式化 IO。"), ("stdlib.h", "malloc/exit/atoi。"),
  ("string.h", "memcpy/strlen。"), ("errno.h", "错误报告。")],
 [("atoi 无检错", "用 strtol。"), ("strcpy 溢出", "限长复制。"), ("非 reentrant", "多线程 setlocale。")],
 ["snprintf 限长", "查 man 线程安全", "避免 gets/strcpy", "封装错误处理"]),
("C语言最佳实践", "可维护 C 代码靠清晰模块边界、一致命名、自动化测试与静态分析；MISRA/CERT C 指导安全关键领域。",
 "模块 .c+.h 配对；最小暴露 API；错误码 enum 统一。",
 "Coverity/clang-tidy cppcoreguidelines 子集；CBMC 形式化验证关键路径。",
 "代码审查清单：所有权、错误路径、线程、边界。",
 "单元测试 Unity/CMocka；fuzz AFL/libFuzzer。",
 "CERT C 禁 dangerous function；MISRA 禁递归等。",
 "OpenSSL 式清晰 error stack；SQLite 单文件库典范。",
 ".clang-format；CI cppcheck。",
 "复现最小用例；git bisect。",
 "与 Rust 比 C 需更多纪律换灵活。",
 [("编码规范", "Linux kernel style 或团队标准。"), ("错误处理", "goto cleanup 或 early return。"),
  ("测试", "表驱动测试。"), ("文档", "头文件注释契约。")],
 [("无测试遗留 C", "改一行崩全局。"), ("宏代替函数", "难调试。"), ("全局 mutable", "线程噩梦。")],
 ["CI 静态分析", "Fuzz 边界", "错误码文档", "定期依赖审计"]),
]:
    _reg("C语言", _mod,
         intro=_intro, mechanism=_mech, internals=_int, workflow=_wf,
         performance=_perf, security=_sec, case_study=_case, configuration=_conf,
         debugging=_dbg, comparison=_cmp, concepts=_concepts, pitfalls=_pit, practices=_prac)

print(f"C语言 registered: {sum(1 for k in MODULE_SPECS if k[0]=='C语言')}")
