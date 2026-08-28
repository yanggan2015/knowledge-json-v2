#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Write complete _content_specs_languages.py with all 212 modules."""

from pathlib import Path

OUT = Path("/workspace/article_generator/manual/_content_specs_languages.py")

HEADER = '''# -*- coding: utf-8 -*-
"""Hand-authored technical specs for all programming language modules."""

from typing import Dict, Tuple

LANG_SPECS: Dict[str, Dict[str, dict]] = {}
LANG_DETAILED: Dict[Tuple[str, str], dict] = {}

def _add(domain, module, core, internal, **kw):
    LANG_SPECS.setdefault(domain, {})[module] = {"core": core, "internal": internal, **kw}

'''

# fmt: domain, module, core, internal, kwargs dict as string lines
def A(d, m, c, i, **kw):
    parts = [f'_add({d!r}, {m!r}, {c!r}, {i!r}']
    for k, v in kw.items():
        if isinstance(v, str):
            parts.append(f', {k}={v!r}')
        elif isinstance(v, list):
            inner = ', '.join(
                f'({a!r}, {b!r})' if isinstance(x, tuple) else repr(x)
                for x in v
                for a, b in ([x] if False else [x if isinstance(x, tuple) else (x, x)])
            )
            # handle list of tuples
            items = []
            for x in v:
                if isinstance(x, tuple):
                    items.append(f'({x[0]!r}, {x[1]!r})')
                elif isinstance(x, dict):
                    items.append(repr(x))
                else:
                    items.append(repr(x))
            parts.append(f', {k}=[{", ".join(items)}]')
        else:
            parts.append(f', {k}={v!r}')
    return ''.join(parts) + ')\n'


def build_lines():
    lines = []
    # C 语言 (13)
    c_lang = [
        ("C语言基础", "C 程序从 main 经预处理、编译、汇编、链接生成可执行文件；翻译单元独立编译。", "GCC/Clang：词法/语法→AST→IR→机器码；CRT 初始化 BSS 后跳转 main。"),
        ("数据类型", "基本/派生类型；sizeof/_Alignof；整数提升与 usual arithmetic conversions。", "结构体 padding 由对齐决定；位域布局实现定义。"),
        ("运算符与表达式", "优先级与结合性；短路求值；位运算与序列点。", "移位≥位宽 UB；volatile 禁止优化。"),
        ("流程控制", "if/switch/for/while；switch 跳转表；goto cleanup 释放资源。", "setjmp/longjmp 非本地跳转。"),
        ("函数", "原型声明；static 内部链接；inline 与函数指针。", "x86-64 System V 调用约定寄存器传参。"),
        ("数组与指针", "decay；指针算术；restrict 无别名优化。", "strict aliasing 规则；越界 UB。"),
        ("结构体与联合", "struct/union；位域；柔性数组成员 FAM。", "offsetof；#pragma pack。"),
        ("内存管理", "malloc/calloc/realloc/free；内存池与碎片。", "ptmalloc/jemalloc；ASan/Valgrind。"),
        ("文件IO", "stdio FILE* 与 POSIX fd；缓冲与 errno。", "page cache；O_DIRECT。"),
        ("预处理", "#include/#define/#if；宏词法替换。", "预编译 .i；X 宏生成代码。"),
        ("高级特性", "C99/C11/C23：_Generic、stdatomic、指定初始化。", "_Static_assert；threads.h。"),
        ("C标准库", "stdio/stdlib/string；glibc/musl 差异。", "reentrant 函数；FORTIFY_SOURCE。"),
        ("C语言最佳实践", "MISRA/CERT C；模块 .c+.h；静态分析与 Fuzz。", "Linux kernel style；goto cleanup。"),
    ]
    for m, c, i in c_lang:
        lines.append(A("C语言", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("核心机制", c), ("底层", i), ("工程", f"{m} 在系统编程中的典型用法。"), ("工具链", "gcc/gdb/Valgrind/ASan。")],
            pitfalls=[("忽略 -Wall", "隐藏 UB 与 bug。"), ("内存错误", "UAF/泄漏/double-free。"), ("未定义行为", "有符号溢出等。")],
            practices=["-std=c17 -Wall -Werror", "stdint.h 可移植", "RAII 边界用 C++", "CI 静态分析"],
            references=["ISO C17", "K&R C 程序设计语言", "GCC Manual"]))

    # C++ (15)
    cpp = [
        ("C++基础", "C++ 扩展类、命名空间、引用、重载；编译 name mangling 与 ODR。", "Clang AST→LLVM IR；Itanium ABI vtable 布局。"),
        ("类与对象", "封装与访问控制；Rule of Five；this 指针。", "对象布局：vptr 在虚类对象首部。"),
        ("继承与多态", "虚函数动态绑定；vtable/vptr；纯虚抽象类。", "多重继承多 vptr；虚继承菱形共享。"),
        ("运算符重载", "成员/非成员 operator；不可重载 :: .* 等。", "operator+ 常非成员对称；<=> C++20。"),
        ("模板", "函数/类模板实例化；SFINAE；概念 C++20。", "两阶段名字查找；ADL；代码膨胀。"),
        ("STL容器", "vector/map/unordered_map；迭代器失效规则。", "Allocator/PMR；红黑树/哈希桶。"),
        ("STL算法", "<algorithm> 迭代器范围；执行策略并行。", "intro sort；ranges C++20 惰性视图。"),
        ("智能指针", "unique_ptr/shared_ptr/weak_ptr；make_shared。", "控制块强/弱引用；自定义 deleter。"),
        ("异常处理", "try/catch 栈展开；noexcept；异常保证。", "Itanium unwinding __cxa_throw。"),
        ("RTTI与类型转换", "typeid/dynamic_cast；四 cast。", "需多态类才能 dynamic_cast 引用。"),
        ("Lambda与函数对象", "闭包类 operator()；捕获/init capture。", "std::function 类型擦除可能堆分配。"),
        ("并发编程", "thread/mutex/atomic/condition_variable；jthread。", "memory_order；TSan 查数据竞争。"),
        ("C++11/14/17/20新特性", "移动语义/auto/ranges/模块/协程。", "右值引用 T&&；完美转发 forward。"),
        ("设计模式", "GoF 在 C++ 用虚函数/模板/RAII。", "Pimpl/Strategy std::function/CRTP。"),
        ("性能优化", "RVO/LTO/PGO；cache locality；false sharing。", "perf/VTune；Compiler Explorer。"),
    ]
    for m, c, i in cpp:
        lines.append(A("C++", m, c, i,
            intro=c, mechanism=c, internals=i,
            concepts=[("核心原理", c), ("底层实现", i), ("工程实践", f"{m} 在 C++ 项目中需结合 RAII 与 const 正确性。"), ("性能考量", f"{m} 热点路径应 profile 后优化。")],
            pitfalls=[("忽略 Rule of Five", "资源类浅拷贝双删。"), ("异常安全", "强 guarantee 设计。"), ("ABI 变更", "跨 DLL 接口稳定。")]))

    # Python核心 (15)
    py_core = [
        ("Python基础", "Python3 缩进语法；CPython 字节码虚拟机执行。", "Parser→AST→code object→CEval 栈解释。"),
        ("数据类型", "对象模型；不可变 int/str/tuple vs 可变 list/dict。", "PyObject 头 refcnt+type*；dict 开放寻址。"),
        ("流程控制", "if/for/while/try；无 switch 用 dict/if-elif。", "异常栈 traceback；else/finally 语义。"),
        ("函数", "def/lambda；*args/**kwargs；LEGB 作用域。", "函数对象 __code__/__defaults__。"),
        ("模块与包", "import 缓存 sys.modules；__init__.py 包。", "importlib  machinery；相对/绝对导入。"),
        ("面向对象", "class/new/instance；MRO C3；描述符协议。", "__dict__ 命名空间；slots 省内存。"),
        ("异常处理", "try/except/else/finally；异常链 __cause__。", "BaseException 层次；自定义异常类。"),
        ("文件IO", "open/with 上下文；文本/二进制；pathlib。", "缓冲 io 模块；encoding 默认 utf-8。"),
        ("迭代器与生成器", "__iter__/__next__；yield 暂停帧。", "generator 对象 gi_frame；惰性序列。"),
        ("装饰器", "@wrapper；functools.wraps 保留元数据。", "闭包返回替换函数；带参装饰器三层。"),
        ("上下文管理器", "__enter__/__exit__；contextlib.contextmanager。", "with 保证 __exit__ 即使异常。"),
        ("正则表达式", "re 模块；compile 缓存；raw string 模式。", "NFA/DFA 引擎；分组与非贪婪。"),
        ("标准库", "datetime/json/os/sys/collections 等 batteries。", "bisect/heapq 算法；dataclass 3.7+。"),
        ("虚拟环境与包管理", "venv 隔离；pip/pyproject.toml；wheel。", "PYTHONPATH；editable install。"),
        ("Python最佳实践", "PEP8/black/mypy；pytest；logging 非 print。", "EAFP vs LBYL；显式优于隐式。"),
    ]
    for m, c, i in py_core:
        lines.append(A("Python核心", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("语言机制", c), ("CPython 实现", i), ("惯用法", f"Pythonic {m} 用法见官方文档。"), ("标准库", f"stdlib 对 {m} 的支持。")],
            pitfalls=[("可变默认参数", "def f(a=[]) 共享。"), ("import 循环", "重构或延迟导入。"), ("GIL 误用", "CPU 密集用 multiprocessing。")]))

    # Python高级 (15)
    py_adv = [
        ("Python内存管理", "引用计数+分代 GC；循环引用 gc.collect。", "PyMalloc 小对象 arena；tracemalloc。"),
        ("GIL与并发", "GIL 互斥字节码执行；IO 密集多线程仍有效。", "sys.setswitchinterval；nogil 实验分支。"),
        ("多线程与多进程", "threading vs multiprocessing；进程 spawn/fork。", "Queue/Pipe；Manager 共享状态。"),
        ("asyncio异步", "事件循环 coroutine；await 挂起点。", "selector/epoll；Task/Future；uvloop 加速。"),
        ("元编程", "type/__new__/元类；exec/eval 动态代码。", "__getattribute__ 拦截；import hooks。"),
        ("描述符与属性", "descriptor protocol __get__/__set__；property。", "数据描述符优先于实例 dict。"),
        ("类型注解", "typing Generics/Protocol；mypy 静态检查。", "PEP 484/585/604；runtime get_type_hints。"),
        ("C扩展", "CPython C-API PyObject*；扩展模块 .so。", "refcount 增减；GIL Py_BEGIN_ALLOW_THREADS。"),
        ("性能分析与优化", "cProfile/profile；line_profiler；Cython/Numba。", "__slots__；局部变量绑定加速。"),
        ("设计模式", "Python 动态特性简化模式；单例模块级。", "装饰器实现策略/观察者。"),
        ("函数式编程", "map/filter/reduce；functools partial。", "itertools；不可变 tuple/frozenset。"),
        ("数据处理", "pandas/numpy 生态；CSV/JSON 解析。", "生成器处理大文件；内存映射。"),
        ("Web开发基础", "WSGI/ASGI；Flask/Django/FastAPI 选型。", "请求生命周期；中间件链。"),
        ("测试与调试", "pytest fixtures；pdb/ipdb；mock.patch。", "hypothesis 属性测试；coverage。"),
        ("Python高级技巧", "__slots__/__prepare__；singledispatch。", "contextvars 异步上下文；walrus :="),
    ]
    for m, c, i in py_adv:
        lines.append(A("Python高级", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("原理", c), ("实现", i), ("场景", f"{m} 适用边界。"), ("工具", f"相关 profiling/debug 工具。")],
            pitfalls=[("GIL CPU 密集", "用多进程。"), ("async 混阻塞", "阻塞 call 用 run_in_executor。"), ("C 扩展泄漏", "refcount 配对。")]))

    # JavaScript核心 (17)
    js = [
        ("JS基础语法", "动态弱类型；语句与表达式；严格模式 use strict。", "V8 Ignition 字节码+TurboFan JIT。"),
        ("数据类型", "7 primitive+Object；typeof/null 历史 bug。", "装箱 Boolean/object；Symbol 唯一键。"),
        ("运算符", "== 抽象相等 vs ===；+ 字符串拼接。", "ToPrimitive/toString/valueOf。"),
        ("流程控制", "switch/for-in/for-of；label break。", "for-of 迭代器协议。"),
        ("函数", "function/arrow；无重载；first-class。", "arrow 词法 this/arguments。"),
        ("对象与原型", "对象字面量；__proto__ 链；Object.create。", "Hidden class/Shape；属性描述符。"),
        ("数组", "稀疏数组；push/pop/map/filter。", "length 可写；类数组 arguments。"),
        ("闭包与作用域", "词法作用域；闭包捕获绑定。", "TDZ let/const；块级作用域。"),
        ("this绑定", "默认/隐式/显式/new 绑定规则。", "call/apply/bind；箭头无 own this。"),
        ("ES6+新特性", "let/const/class/destructuring/spread。", "Proxy/Reflect；Optional chaining ?.。"),
        ("异步编程", "callback→Promise→async/await 演进。", "macrotask vs microtask 队列。"),
        ("Promise与async/await", "Promise 三态；then 链；async 返回 Promise。", "V8 async 状态机变换。"),
        ("模块化", "ESM import/export vs CJS require。", "静态分析 tree-shaking；循环依赖。"),
        ("DOM操作", "querySelector/Node API；重排重绘成本。", "DocumentFragment 批量更新。"),
        ("事件处理", "冒泡/捕获；addEventListener；事件委托。", "passive 监听器滚动优化。"),
        ("错误处理", "try/catch；Error 子类；unhandledrejection。", "window.onerror；Error.cause。"),
        ("JS最佳实践", "ESLint/Prettier；避免全局；模块化。", "严格相等；const 默认。"),
    ]
    for m, c, i in js:
        lines.append(A("JavaScript核心", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("语义", c), ("引擎", i), ("模式", f"{m} 常用模式。"), ("规范", "ECMA-262 对应章节。")],
            pitfalls=[("隐式 coercion", "用 ===。"), ("this 丢失", "bind/箭头。"), ("浮点精度", "Decimal.js/BigInt。")]))

    # TypeScript (15)
    ts = [
        ("TypeScript基础", "JS 超集；编译擦除类型；.ts→.js。", "tsc AST 类型检查+emit。"),
        ("类型系统", "structural typing；union/intersection。", "类型推断 contextual typing。"),
        ("接口", "interface 可合并；extends 多继承。", "implements 类契约。"),
        ("类", "public/private/protected；readonly。", "参数属性 constructor 简写。"),
        ("泛型", "<T> 函数/类/接口；约束 extends。", "infer 条件类型提取。"),
        ("枚举", "numeric/string enum；const enum 内联。", "反向映射 numeric only。"),
        ("类型守卫", "typeof/instanceof/in；自定义 is 谓词。", "控制流收窄 narrowing。"),
        ("装饰器", "experimentalDecorators；类/方法/metadata。", "TC39 新标准 stage 3。"),
        ("模块", "ESM 为主；export type 类型导出。", "moduleResolution node16/bundler。"),
        ("命名空间", "namespace 遗留；prefer module。", "declare global  augmentation。"),
        ("tsconfig配置", "strict 全家桶；paths 别名。", "composite/project references。"),
        ("与JavaScript互操作", "allowJs/checkJs；JSDoc @type。", "declare module '*.vue'。"),
        ("类型体操", "条件/映射/模板字面量类型。", "utility Partial/Required/Pick。"),
        ("工程化", "eslint-typescript；monorepo references。", "declaration/sourceMap。"),
        ("最佳实践", "prefer interface 对象形状；unknown 非 any。", "strictNullChecks 必开。"),
    ]
    for m, c, i in ts:
        lines.append(A("TypeScript", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("类型设计", c), ("编译器", i), ("模式", f"{m} 实践。"), ("strict", "严格模式价值。")],
            pitfalls=[("any 泛滥", "失去类型安全。"), ("类型断言滥用", "优先守卫。"), ("循环类型", "interface 自引用限。")]))

    # Java核心 (15)
    java = [
        ("Java基础", "JVM 字节码；main 入口；package/import。", "javac→.class；JVM 解释+JIT。"),
        ("面向对象", "class/interface；封装继承多态。", "HotSpot 对象头 mark/klass。"),
        ("集合框架", "List/Set/Map 层次；ArrayList/HashMap。", "hashCode/equals 契约；树化链表。"),
        ("异常处理", "checked vs unchecked；try-with-resources。", "Suppressed exceptions。"),
        ("泛型", "类型擦除；通配符 ? extends/super。", "桥方法 bridge method。"),
        ("注解", "@Override/@FunctionalInterface；运行时反射读。", "Retention/ Target 元注解。"),
        ("反射", "Class.forName；Method.invoke；动态代理。", "setAccessible 模块限制。"),
        ("IO与NIO", "Stream 阻塞 IO；Channel/Buffer/Selector NIO。", "零拷贝 transferTo；mmap。"),
        ("多线程基础", "Thread/Runnable；synchronized volatile。", "happens-before 规则 JMM。"),
        ("JVM内存模型", "堆/栈/方法区/PC；对象分配 Eden。", "TLAB 线程本地分配。"),
        ("垃圾回收", "Serial/Parallel/G1/ZGC；分代收集。", "GC roots；SafePoint；STW。"),
        ("类加载机制", "双亲委派；自定义 ClassLoader。", "链接验证准备解析初始化。"),
        ("Java8新特性", "Lambda/Stream/Optional/default 方法。", "invokedynamic Lambda 生成。"),
        ("模块化系统", "JPMS module-info；requires/exports。", "强封装 internal API。"),
        ("Java最佳实践", "Effective Java；Immutability；Builder。", "SpotBugs/Checkstyle。"),
    ]
    for m, c, i in java:
        lines.append(A("Java核心", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("平台机制", c), ("JVM", i), ("API", f"java.* 相关类。"), ("实践", "Effective Java 条目。")],
            pitfalls=[("equals/hashCode", "不一致破坏 HashMap。"), ("字符串 + 循环", "StringBuilder。"), ("反射性能", "MethodHandle 替代。")]))

    # Java并发 (15)
    jconc = [
        ("线程基础", "Thread 生命周期；interrupt 协作取消。", "内核线程 1:1；JVM 挂载 native。"),
        ("线程池", "ThreadPoolExecutor 核心/最大/队列/拒绝。", "Worker 循环 getTask/runWorker。"),
        ("synchronized", "监视器锁 monitorenter/exit；锁升级。", "偏向→轻量→重量；ObjectMonitor。"),
        ("Lock体系", "ReentrantLock 可中断/公平；tryLock。", "AQS 队列 CLH 变体。"),
        ("原子类", "AtomicInteger CAS；LongAdder 分段。", "Unsafe/compareAndSet；ABA 问题。"),
        ("并发容器", "ConcurrentHashMap 分段/CAS+synchronized。", "CopyOnWriteArrayList 读多写少。"),
        ("AQS原理", "state+CLH 队列；独占/共享模板。", "ReentrantLock/CountDownLatch 基于 AQS。"),
        ("Condition", "await/signal 条件队列；与 Lock 配合。", "ConditionObject 链表等待。"),
        ("CountDownLatch", "一次性倒数；await 阻塞。", "state 计数 CAS 减。"),
        ("CyclicBarrier", "可重用栅栏；Generation 破环。", "barrier action 线程回调。"),
        ("Semaphore", "信号量许可；限流。", "共享模式 AQS state。"),
        ("Future与CompletableFuture", "异步结果；thenApply 组合。", "ForkJoinPool.commonPool 默认。"),
        ("ForkJoinPool", "工作窃取 deque；分治任务。", "RecursiveTask/Action。"),
        ("并发设计模式", "生产者消费者；线程封闭；不变性。", "Guarded suspension；Balking。"),
        ("并发性能调优", "锁粒度；无锁结构；JMH 基准。", "async-profiler 火焰图。"),
    ]
    for m, c, i in jconc:
        lines.append(A("Java并发", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("并发原语", c), ("实现", i), ("JMM", "happens-before 关联。"), ("诊断", "jstack/JFR。")],
            pitfalls=[("锁顺序死锁", "固定顺序加锁。"), ("Double-checked locking", "需 volatile。"), ("线程池 OOM", "有界队列。")]))

    # Go (16)
    go = [
        ("Go基础", "简洁语法；package main；导出大写。", "cmd/compile→plan9 obj→链接。"),
        ("数据类型", "struct/array/slice/map/channel 类型。", "slice 头 ptr/len/cap。"),
        ("流程控制", "if/for/switch；无 while；defer LIFO。", "defer 函数返回前执行。"),
        ("函数", "多返回值；命名返回值；变参 ...T。", "闭包捕获变量地址。"),
        ("结构体与方法", "值/指针 receiver；嵌入 embedding。", "方法集 method set 规则。"),
        ("接口", "隐式实现；iface 动态类型。", "空接口 any；类型断言 .(T)。"),
        ("goroutine", "go 关键字；M:N 调度；GMP 模型。", "runtime/proc.go G/M/P；work stealing。"),
        ("channel", "CSP 通信；无/有缓冲；close 语义。", "hchan 环形队列+等待队列。"),
        ("并发模式", "worker pool；context 取消；errgroup。", "fan-out/fan-in pipeline。"),
        ("错误处理", "error 接口；errors.Is/As；wrap %w。", "panic/recover 非常规路径。"),
        ("包管理", "go mod；MVS 最小版本；replace/exclude。", "sumdb 校验模块哈希。"),
        ("测试", "testing 包；table-driven；benchmark。", "go test -race -cover。"),
        ("反射", "reflect.Type/Value；可设置性 CanSet。", "性能开销；json 标签。"),
        ("泛型", "Go1.18 type parameters；constraints。", "实例化单态化；无特化。"),
        ("性能优化", "pprof；逃逸分析；sync.Pool。", "GOGC 调 GC；避免 unnecessary alloc。"),
        ("Go最佳实践", "Effective Go；accept interfaces return structs。", "golangci-lint；context 传首参。"),
    ]
    for m, c, i in go:
        extra = {}
        if m == "goroutine":
            extra = dict(
                intro="goroutine 是 Go 用户态轻量线程，初始栈约 2KB，runtime 在 OS 线程上 M:N 调度；go 关键字启动。",
                mechanism="GMP：G goroutine、M OS 线程、P 逻辑处理器；P 持 runq，M 需绑 P 执行 G；work stealing 平衡负载。",
                internals="runtime/proc.go；schedule 取 G；sysmon 监控；Go1.14+ 异步抢占 signal。",
                concepts=[("GMP 调度", "GOMAXPROCS 设 P 数；阻塞 syscall M 与 P 分离。"), ("栈增长", "连续栈复制扩容。"), ("调度点", "channel/锁/GC/syscall/Sleep。"), ("泄漏", "pprof goroutine 定位。")],
                performance="避免短任务频繁 go；CPU 密集配 GOMAXPROCS。",
                case_study="net/http 每连接 goroutine；高 QPS 用 pool 或 netpoll。",
                debugging="GODEBUG=schedtrace；go tool trace；/debug/pprof/goroutine。",
                comparison="vs pthread 更轻；vs async/await 显式 go。",
            )
        elif m == "channel":
            extra = dict(
                intro="channel 是 CSP 通信原语；无缓冲同步握手，缓冲解耦生产消费。",
                mechanism="hchan 环形队列+send/recv 等待队列+mutex；无缓冲 send/recv 配对完成。",
                internals="runtime/chan.go；close 后 recv 零值 ok=false；向 closed send panic。",
                concepts=[("无缓冲", "make(chan T) rendezvous。"), ("缓冲", "make(chan T,n) 满/空阻塞。"), ("close", "range 读尽；select 检测。"), ("select", "随机公平；default 非阻塞。")],
                performance="无缓冲严格同步；大缓冲占内存掩盖背压。",
                case_study="pipeline fan-out/fan-in；WaitGroup 聚合。",
                debugging="-race；deadlock 常无人读。",
                comparison="vs mutex+cond 组合数据与同步。",
            )
        kw = dict(intro=extra.get("intro", c), mechanism=extra.get("mechanism", c),
            internals=extra.get("internals", i),
            concepts=extra.get("concepts", [("机制", c), ("runtime", i), ("用法", f"{m} idiomatic 模式。"), ("注意", f"{m} 边界条件。")]),
            pitfalls=[("goroutine 泄漏", "channel 阻塞无读。") if m in ("goroutine","channel") else ("未处理 error", "检查 err。"), ("共享内存", "需 sync。"), ("nil map 写", "panic。")])
        for opt in ("performance", "case_study", "debugging", "comparison"):
            if extra.get(opt):
                kw[opt] = extra[opt]
        lines.append(A("Go语言", m, c, i, **kw))

    # Rust (16)
    rust = [
        ("Rust基础", "rustc/cargo；fn main；表达式导向。", "HIR/MIR/LLVM 编译管线。"),
        ("所有权", "每值单一所有者；移动 Move；Copy trait。", "RAII drop 自动析构。"),
        ("借用与引用", "&T 共享借用；&mut T 独占；借用规则。", "编译期 borrow checker。"),
        ("生命周期", "'a 标注引用有效范围；省略规则。", "生命周期子类型 outlives。"),
        ("结构体与枚举", "struct/enum；Option/Result 代数类型。", "niche optimization None 空指针。"),
        ("模式匹配", "match 穷尽；if let/destructure。", "ref mut binding；@ binding。"),
        ("trait", "impl Trait；dyn 动态分发 vtable。", "trait object fat pointer。"),
        ("泛型", "单态化；where 约束；associated type。", "零成本抽象。"),
        ("错误处理", "Result<T,E>；? 传播；panic unwinding/abort。", "anyhow/thiserror crate。"),
        ("集合", "Vec/HashMap/BTreeMap；迭代器 adaptors。", "hashbrown  SwissTable。"),
        ("模块与包", "mod/use；crate 单元；pub 可见性。", "2018 edition path。"),
        ("闭包与迭代器", "Fn/FnMut/FnOnce；Iterator trait。", "collect/filter/map 惰性链。"),
        ("智能指针", "Box/Rc/Arc/RefCell/Mutex。", "内部可变性；Weak 破循环。"),
        ("并发安全", "Send/Sync marker；线程 spawn；Mutex。", "数据竞争编译拒绝。"),
        ("异步编程", "async/await；Future poll；Tokio runtime。", "Pin 自引用；Waker 唤醒。"),
        ("Rust最佳实践", "clippy；rustfmt；deny warnings。", "cargo test/bench；miri 检测 UB。"),
    ]
    for m, c, i in rust:
        lines.append(A("Rust语言", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("所有权视角", c), ("编译器", i), ("惯用法", f"{m} idiomatic Rust。"), ("标准库", f"std::{m} 相关。")],
            pitfalls=[(" fighting borrow checker", "重构数据结构。"), ("unwrap 生产", "用 ?/match。"), ("unsafe 滥用", "最小 unsafe 块。")]))

    # PHP (15)
    php = [
        ("PHP基础", "<?php 标签；Web 嵌入或 CLI；弱类型。", "Zend Engine  opcode 执行。"),
        ("数据类型", "scalar/array/object/null；类型声明 7+。", "zval 结构 refcnt/type。"),
        ("流程控制", "if/switch/foreach；alternative syntax。", "foreach by-value/by-ref。"),
        ("函数", "全局/命名空间函数；默认参数。", "call_user_func；闭包 use。"),
        ("数组", "ordered hash table；混合键。", "数组函数 array_map/reduce。"),
        ("面向对象", "class/extends/implements；trait。", "魔术方法 __get/__call。"),
        ("异常处理", "try/catch/finally；Throwable。", "Error vs Exception 7+。"),
        ("文件操作", "fopen/fread；SplFileInfo。", "流 wrappers php://。"),
        ("数据库操作", "PDO 预处理；mysqli。", "SQL 注入防预编译。"),
        ("PHP7+新特性", "标量类型；return type；?? ?->。", "JIT PHP8；Fibers 8.1。"),
        ("Composer", "PSR-4 autoload；composer.json。", "vendor/；platform reqs。"),
        ("Laravel基础", "Eloquent ORM；路由/中间件/Blade。", "服务容器 IoC；facade。"),
        ("性能优化", "OPcache；预加载 preload。", "Redis session；FPM pm 调优。"),
        ("安全编程", "XSS htmlspecialchars；CSRF token。", "password_hash ARGON2ID。"),
        ("PHP最佳实践", "PSR-12；PHPStan level；PHPUnit。", "禁用 mysql_* 遗留。"),
    ]
    for m, c, i in php:
        lines.append(A("PHP", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("Web 模型", c), ("Zend", i), ("安全", "OWASP PHP。"), ("PSR", "互操作标准。")],
            pitfalls=[("类型松散", "开启 strict_types。"), ("SQL 拼接", "必须 PDO bind。"), ("文件包含", "白名单 path。")]))

    # C# (15)
    cs = [
        ("C#基础", ".NET CLR；Main；namespace；值/引用类型。", "Roslyn 编译；IL + JIT/RTR。"),
        ("类型系统", "struct class record；nullable 引用类型。", "boxing 值→object 堆。"),
        ("面向对象", "class/interface；virtual override。", "sealed abstract 修饰。"),
        ("泛型", "泛型类/方法；约束 where T:class。", "JIT 共享引用类型泛型。"),
        ("委托与事件", "Delegate multicast；event 封装。", "Func/Action 内置委托。"),
        ("LINQ", " IEnumerable 扩展；SQL 风格查询。", "表达式树 vs 委托；IQueryable。"),
        ("异步编程", "async/await Task；ConfigureAwait。", "状态机 IAsyncStateMachine。"),
        ("属性与反射", "Property get/set；Attribute 元数据。", "Reflection.Emit 动态。"),
        ("异常处理", "try/catch/finally；filter when。", "AggregateException Task。"),
        ("集合", "List/Dictionary/Concurrent；Span Memory。", "BCL System.Collections。"),
        (".NET平台", "CLR GC；程序集；NuGet。", "Core vs Framework vs 5+。"),
        ("ASP.NET基础", "Kestrel；Middleware pipeline；DI。", "Minimal APIs；Controller。"),
        ("依赖注入", "IServiceCollection 生命周期。", "Scoped/Singleton/Transient。"),
        ("性能优化", "ArrayPool；ValueTask；Source Generator。", "dotMemory/PerfView。"),
        ("C#最佳实践", "CA 分析器；nullable enable；record 不可变。", "xUnit；StyleCop。"),
    ]
    for m, c, i in cs:
        lines.append(A("C#", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("CLR 机制", c), ("编译", i), ("BCL", f"{m} API。"), ("模式", "async/DI/LINQ 组合。")],
            pitfalls=[("async void", "仅事件用。"), ("捕获异常空", "日志+重抛。"), ("字符串拼接循环", "StringBuilder。")]))

    # 函数式编程 (15)
    fp = [
        ("函数式编程概述", "λ 演算；声明式 vs 命令式；副作用隔离。", "Turing 完备；图灵与 Church 对偶。"),
        ("纯函数", "相同输入相同输出；无副作用 referential transparency。", "便于推理与并行。"),
        ("不可变性", "persistent 数据结构 structural sharing。", "Copy-on-write；frozen object。"),
        ("高阶函数", "函数作参数/返回值；map/filter/reduce。", "组合子 combinator。"),
        ("闭包", "捕获自由变量；词法环境。", "内存：closure 对象。"),
        ("柯里化", "多参→单参链；partial application。", "Auto-currying Haskell。"),
        ("组合", "f∘g；pipe 数据流；point-free。", "compose 右到左。"),
        ("函子", "Functor fmap/map 保结构。", "List/Maybe 实例。"),
        ("Monad", "flatMap/bind 链式上下文。", "IO/State/Maybe/Reader monad。"),
        ("模式匹配", "代数类型 destructuring；穷尽检查。", "Haskell/Rust/Scala match。"),
        ("代数数据类型", "sum product type；Option/Either。", "类型建模领域。"),
        ("惰性求值", "thunk 按需；无限结构。", "Haskell 默认 lazy；Stream。"),
        ("递归", "尾递归优化 TCO；mutual recursion。", "Scheme trampoline。"),
        ("函数式并发", "STM；Actor；不可变消息。", "Clojure core.async。"),
        ("函数式设计模式", "Lens/Prism；Free monad；Tagless final。", "函数式架构 CQRS+Event。"),
    ]
    for m, c, i in fp:
        lines.append(A("函数式编程", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("理论", c), ("实现", i), ("语言", "Haskell/Scala/Clojure 示例。"), ("实践", "JS/Python 函数式子集。")],
            pitfalls=[("Monad 过度", "简单用 Optional。"), ("lazy 空间泄漏", "严格求值点。"), ("不可变性能", "持久结构或 copy-on-write。")]))

    # 面向对象编程 (15)
    oop = [
        ("面向对象概述", "对象=数据+行为；消息传递；Simula/Smalltalk 起源。", "UML 类图；职责驱动设计。"),
        ("类与对象", "实例化；构造；状态与方法。", "类变量 vs 实例变量。"),
        ("封装", "private 隐藏 invariant；getter/setter 审慎。", "Demeter 法则。"),
        ("继承", "is-a；代码复用；方法重写。", " fragile base class 问题。"),
        ("多态", "Subtype 替换；动态分派。", "接口多态 vs 继承多态。"),
        ("抽象类与接口", "abstract 部分实现；interface 契约。", "Java 8+ default 方法。"),
        ("组合优于继承", "has-a delegation；Strategy 注入。", "Favor composition over inheritance。"),
        ("SOLID原则", "SRP/OCP/LSP/ISP/DIP 五原则。", "依赖倒置抽象稳定。"),
        ("设计模式", "GoF 23；创建/结构/行为。", "模式非银弹；问题驱动。"),
        ("UML建模", "类/序列/状态/组件图。", "Mermaid 轻量替代。"),
        ("面向对象分析", "用例→领域名词→候选类。", "CRC 卡；名词动词分析。"),
        ("面向对象设计", "GRASP 职责分配；Design by Contract。", "耦合内聚权衡。"),
        ("重构", "Martin Fowler 坏味道；小步测试保护。", "Extract Method/Move Field。"),
        ("领域建模", "DDD 实体/值对象/聚合。", "Ubiquitous Language。"),
        ("面向对象最佳实践", "测试驱动；CI；代码审查。", "Evans/Fowler/GoF 经典。"),
    ]
    for m, c, i in oop:
        lines.append(A("面向对象编程", m, c, i, intro=c, mechanism=c, internals=i,
            concepts=[("OOP 概念", c), ("设计", i), ("反模式", "继承滥用/God class。"), ("工具", "UML/IDE 重构。")],
            pitfalls=[("贫血模型", "行为散落服务层。"), ("深层继承", "超 3 层警惕。"), ("违反 LSP", "子类破坏契约。")]))

    return lines


DETAILED = '''
# ===================== LANG_DETAILED (rich modules) =====================
LANG_DETAILED[("Go语言", "goroutine")] = {
    "intro": (
        "goroutine 是 Go 用户态轻量线程，初始栈约 2KB，由 runtime 在 OS 线程上 **M:N 调度**。"
        "使用 `go f()` 启动，与 OS 线程解耦，使单机可承载大量并发任务。"
    ),
    "concepts": [
        {"title": "GMP 调度模型", "body": (
            "**G**（goroutine）、**M**（OS 线程）、**P**（逻辑处理器）构成调度核心。"
            "P 持有本地 run queue；M 必须绑定 P 才能执行 G；当 P 本地队列为空时从其他 P **work stealing**。"
            "GOMAXPROCS 控制 P 数量，默认等于 CPU 核数。"
        )},
        {"title": "栈管理与增长", "body": (
            "goroutine 栈初始很小（约 2KB），运行时按需 **连续栈复制** 扩容，"
            "相比 pthread 固定栈（常 MB 级）显著节省内存。"
        )},
        {"title": "调度与抢占", "body": (
            "channel 操作、锁竞争、系统调用、GC、time.Sleep 等触发调度点。"
            "Go 1.14 起引入基于信号的 **异步抢占**，避免 CPU 密集 goroutine 饿死其他 G。"
        )},
        {"title": "与 OS 线程关系", "body": (
            "阻塞 syscall 时 M 可能与 P 分离，P 可绑定新 M 继续执行其他 G。"
            "net 包集成 netpoll，网络 IO 不占用额外 OS 线程。"
        )},
        {"title": "泄漏诊断", "body": (
            "goroutine 泄漏常因 channel 永久阻塞且无接收者。"
            "使用 pprof `/debug/pprof/goroutine`、`go tool trace` 与 `runtime.NumGoroutine()` 监控。"
        )},
    ],
    "mechanism": (
        "runtime.schedule 从 P 的 runq 取 G 执行；G 阻塞时放入 wait queue 并让出 M。"
        "sysmon 后台线程监控网络/timer 与长时间运行的 G。"
    ),
    "internals": "核心代码位于 `runtime/proc.go`、`runtime/stack.go`；G 结构含 stack、sched、goid 等字段。",
    "workflow": "1. `go worker()` 启动\\n2. 通过 channel/context 协调退出\\n3. 用 WaitGroup 等待完成\\n4. pprof 验证无泄漏",
    "performance": "避免频繁创建生命周期极短的 goroutine；CPU 密集任务设置合适 GOMAXPROCS；IO 密集可大量 goroutine。",
    "security": "goroutine 共享地址空间，需 sync 保护共享数据；`-race` 检测数据竞争。",
    "case_study": "标准库 `net/http` 为每个连接启动 goroutine；高 QPS 场景可配合 worker pool 或 epoll 集成 netpoll。",
    "configuration": "GOMAXPROCS、GODEBUG=schedtrace=1000 观察调度；容器内正确设置 CPU quota。",
    "debugging": "Delve 调试多 goroutine；trace 可视化 G 生命周期；schedtrace 打印调度事件。",
    "comparison": "对比 pthread：创建/切换成本低；对比 Erlang process：共享内存需显式同步；对比 async/await：go 语法更显式。",
    "pitfalls": [
        {"title": "无限制 go", "body": "百万 goroutine 仍可能耗尽内存或调度开销过大，需背压与 pool。"},
        {"title": "泄漏", "body": "发送方阻塞于无接收者的 channel，或 WaitGroup 未 Done。"},
        {"title": "共享变量无 sync", "body": "数据竞争 UB，必须 mutex/atomic/channel 传递。"},
    ],
    "practices": [
        "用 context 传递取消信号",
        "errgroup 管理一组 goroutine 错误",
        "生产环境监控 goroutine 数量",
        "CPU 与 IO 任务区分并发模型",
    ],
    "references": [
        "Go runtime 调度器设计文档",
        "runtime/proc.go 源码",
        "《Go 语言设计与实现》调度章",
    ],
}

LANG_DETAILED[("Go语言", "channel")] = {
    "intro": (
        "channel 是 Go 的 CSP 通信原语，用于 goroutine 间 **传递值与同步**。"
        "**无缓冲 channel** 实现 rendezvous 同步握手；**有缓冲 channel** 允许有限异步。"
    ),
    "concepts": [
        {"title": "无缓冲 channel", "body": "make(chan T) 容量 0：send 阻塞直到另一 goroutine recv，反之亦然，形成同步点。"},
        {"title": "缓冲 channel", "body": "make(chan T, n) 可存 n 个元素；未满 send 不阻塞，未空 recv 不阻塞；用于削峰与 pipeline。"},
        {"title": "关闭语义", "body": "close(ch) 广播唤醒等待者；recv 取零值且 ok=false；向 closed channel send 导致 panic。"},
        {"title": "select 多路复用", "body": "select 随机公平选择就绪 case；default 非阻塞；nil channel 的 case 永不就绪。"},
        {"title": "方向类型", "body": "chan<- 只 send，<-chan 只 recv；函数签名约束 API 误用。"},
    ],
    "mechanism": "hchan 结构：环形队列 buf、sendq/recvq 等待链表、mutex；操作在 lock 保护下完成。",
    "internals": "实现见 runtime/chan.go；与 scheduler 协作在阻塞时 gopark/unpark。",
    "workflow": "设计消息类型 → 决定缓冲大小 → pipeline 串联 → context 取消 → close 由发送方或协调者执行",
    "performance": "无缓冲严格同步延迟低但切换多；过大缓冲占内存且延迟可见性；根据背压需求选容量。",
    "security": "channel 传递指针时注意共享突变；仅传递不可变或所有权转移消息更安全。",
    "case_study": "log aggregator：多 worker send 日志行到缓冲 channel，单 writer 落盘；fan-in 用 select 合并。",
    "configuration": "缓冲容量是设计参数；monitor channel len/cap 辅助调优（仅调试，非同步原语）。",
    "debugging": "deadlock detector；`-race`；dump hchan 状态需 delve/runtime trace。",
    "comparison": "vs mutex+cond：channel 组合同步与数据移动；vs Java BlockingQueue：语法级支持 select。",
    "pitfalls": [
        {"title": "重复 close", "body": "panic；用 sync.Once 或单一 owner close。"},
        {"title": "单向阻塞", "body": "无接收者的 send 永久阻塞，goroutine 泄漏。"},
        {"title": "nil channel", "body": "对 nil send/recv 永久阻塞；select 中 nil case 禁用。"},
    ],
    "practices": [
        "由接收方或协调者 close",
        "缓冲大小基于 benchmark 与背压",
        "优先用 channel 传递所有权而非共享内存",
        "复杂协议文档化消息顺序",
    ],
    "references": [
        "Go Spec — Channel types",
        "runtime/chan.go",
        "CSP 论文 Communicating Sequential Processes",
    ],
}
'''


def main():
    lines = [HEADER] + build_lines() + [DETAILED]
    OUT.write_text(''.join(lines), encoding='utf-8')
    # count
    text = OUT.read_text()
    count = text.count('_add(')
    print(f"Wrote {OUT} with {count} _add calls")


if __name__ == "__main__":
    main()
