# -*- coding: utf-8 -*-
"""领域与模块级深度文字内容库"""

# 领域级导语（真实技术背景）
DOMAIN_INTROS = {
    "React": (
        "React 是 Facebook 开源的 UI 库，以组件化与声明式编程为核心。"
        "React 18 引入并发渲染、Automatic Batching 与 Suspense 增强，"
        "配合 Vite 与 React Router 可构建现代单页应用。"
    ),
    "Vue": (
        "Vue 3 采用 Composition API 与响应式 Proxy 重构内核，"
        "模板与脚本协同，渐进式框架设计使团队可按需引入路由、状态管理等能力。"
    ),
    "Flask": (
        "Flask 是 Python 生态中的轻量 WSGI Web 框架，核心精简，"
        "通过蓝图、扩展与 Jinja2 模板按需组装完整应用，适合中小型服务与 API。"
    ),
    "Docker": (
        "Docker 将应用与依赖打包为镜像，基于 Linux Namespace 与 Cgroups 实现隔离，"
        "Docker Compose 与 Kubernetes 构成现代交付链路的基础层。"
    ),
    "Kubernetes": (
        "Kubernetes 是容器编排事实标准，以 Pod 为调度单元，"
        "通过 Deployment、Service、Ingress 等对象声明期望状态，控制器持续 reconcile。"
    ),
    "Go语言": (
        "Go 由 Google 设计，强调简洁与高效并发：goroutine 轻量、channel 通信、"
        "静态编译单二进制，广泛应用于云原生与基础设施。"
    ),
    "Rust语言": (
        "Rust 以所有权、借用与生命周期在编译期保证内存安全，"
        "零成本抽象使其在系统编程与高性能服务中快速增长。"
    ),
    "大语言模型": (
        "大语言模型基于 Transformer 架构，通过大规模预训练习得语言表示，"
        "微调与提示工程使其适配问答、摘要、代码生成等下游任务。"
    ),
    "MySQL": (
        "MySQL 8 默认 InnoDB 引擎，支持事务、行级锁与 MVCC，"
        "B+树索引、执行计划优化与主从复制是生产运维的核心议题。"
    ),
    "Redis": (
        "Redis 是内存数据结构存储，单线程事件模型保证操作原子性，"
        "支持字符串、哈希、列表、集合、有序集合及 Stream 等多种结构。"
    ),
    "Spring Boot": (
        "Spring Boot 基于 Spring 生态，通过自动配置与 Starter 降低接入成本，"
        "内嵌 Tomcat/Jetty，适合构建企业级 REST 服务与微服务。"
    ),
    "Python核心": (
        "Python 以可读性与丰富标准库著称，3.12 持续优化性能与类型系统，"
        "是数据、Web、自动化等多场景的主流语言。"
    ),
    "JavaScript核心": (
        "JavaScript 是 Web 原生语言，ES2024 持续演进，"
        "事件驱动、原型链与异步模型是理解浏览器与 Node.js 的基础。"
    ),
    "TypeScript": (
        "TypeScript 为 JavaScript 添加静态类型，编译期捕获错误，"
        "大型前端与 Node 项目普遍采用 strict 模式提升可维护性。"
    ),
    "Node.js": (
        "Node.js 基于 V8 与 libuv，单线程事件循环处理 I/O，"
        "适合高并发 I/O 密集型 API 与实时应用。"
    ),
    "Linux内核": (
        "Linux 内核管理进程调度、内存、文件系统、网络与设备驱动，"
        "理解内核有助于性能调优、驱动开发与问题根因分析。"
    ),
    "计算机网络": (
        "计算机网络分层模型（物理、链路、网络、传输、应用）"
        "是理解 TCP/IP、HTTP、DNS 与安全协议的理论基础。"
    ),
    "数据结构与算法": (
        "数据结构与算法是程序效率的基石："
        "数组、链表、树、图与排序、搜索、动态规划等贯穿面试与工程优化。"
    ),
    "机器学习": (
        "机器学习从数据中学习模式，涵盖监督、无监督与强化学习，"
        "scikit-learn 提供经典算法实现，是入门与实践的常用工具。"
    ),
    "深度学习": (
        "深度学习以多层神经网络自动提取特征，"
        "PyTorch 与 TensorFlow 是训练与部署的主流框架，GPU 加速至关重要。"
    ),
    "微服务架构": (
        "微服务将单体拆分为可独立部署的服务，"
        "带来弹性与团队自治，也引入分布式一致性、观测与治理挑战。"
    ),
    "Git版本控制": (
        "Git 是分布式版本控制系统，分支、合并与 rebase 支撑协作开发，"
        "是现代软件工程不可或缺的基础设施。"
    ),
    "Nginx": (
        "Nginx 是高性能 Web 服务器与反向代理，"
        "事件驱动架构支撑海量并发连接，广泛用于负载均衡与静态资源服务。"
    ),
    "Web性能优化": (
        "Web 性能直接影响转化与留存，Core Web Vitals（LCP、INP、CLS）"
        "是 Google 提出的用户体验度量标准。"
    ),
    "浏览器原理": (
        "浏览器是多进程架构：主进程、渲染进程、GPU 进程等协作完成"
        "HTML 解析、CSS 布局、JavaScript 执行与合成显示。"
    ),
    "密码学": (
        "密码学提供机密性、完整性与身份认证能力，"
        "对称加密、非对称加密、哈希与数字签名是 TLS 与身份体系的基础。"
    ),
    "认证授权": (
        "认证验证「你是谁」，授权决定「你能做什么」，"
        "Session、JWT、OAuth2 是 Web 与 API 安全的核心模式。"
    ),
}

# 模块级深度段落（跨领域复用 + 特化）
MODULE_DEEP = {
    "Hooks": (
        "React Hooks 让函数组件拥有状态与副作用能力，规则要求仅在顶层调用、"
        "不在条件分支中调用。useState 管理局部状态，useEffect 处理副作用，"
        "自定义 Hook 抽取可复用逻辑。Hooks 的实现依赖 Fiber 链表与调度器。"
    ),
    "useState": (
        "useState 返回当前状态与更新函数。更新可传入新值或 updater 函数。"
        "React 18 在事件处理中自动批处理多次 setState，减少渲染次数。"
        "状态更新异步调度，不可假设 setState 后立即读到新值。"
    ),
    "useEffect": (
        "useEffect 在浏览器绘制完成后执行，适合请求、订阅、手动 DOM 操作。"
        "依赖数组决定何时重新执行；空数组表示仅挂载时执行一次。"
        "返回清理函数，在卸载或下次 effect 前运行，防止内存泄漏。"
    ),
    "路由": (
        "路由将 URL 路径映射到处理逻辑或组件。静态路由固定匹配，"
        "动态路由用参数捕获变化段。嵌套路由支持布局共享与权限分层。"
    ),
    "蓝图": (
        "Flask 蓝图将应用拆分为可注册的子模块，每个蓝图可有独立路由前缀与模板目录，"
        "大型项目按业务域组织代码，避免单文件膨胀。"
    ),
    "goroutine": (
        "goroutine 由 Go runtime 调度，初始栈约 2KB，远小于 OS 线程。"
        "GOMAXPROCS 控制并行度。goroutine 泄漏是常见生产问题，"
        "需确保 channel 关闭或 context 取消后 goroutine 能退出。"
    ),
    "channel": (
        "channel 是 goroutine 间通信管道。无缓冲 channel 发送与接收同步；"
        "有缓冲 channel 在未满时可异步发送。close 后接收方读到零值与 false。"
        "select 多路复用多个 channel 操作。"
    ),
    "所有权": (
        "Rust 每个值有唯一所有者，赋值或传参时所有权转移（move）。"
        "基本类型实现了 Copy trait 可隐式复制。所有权系统在编译期消除"
        "悬垂指针与 double free，无需 GC。"
    ),
    "索引": (
        "B+树索引是 InnoDB 默认结构，叶子节点存数据或主键，支持范围扫描。"
        "联合索引遵循最左前缀。覆盖索引避免回表。过多索引拖慢写入，"
        "需根据查询模式权衡。"
    ),
    "事务": (
        "事务保证原子性、一致性、隔离性、持久性（ACID）。"
        "隔离级别从读未提交到串行化逐级加强。MVCC 通过版本链实现非阻塞读。"
        "长事务占用锁与 undo 空间，应尽量避免。"
    ),
    "Pod": (
        "Pod 是 K8s 最小调度单元，共享网络命名空间与存储卷。"
        "通常一个 Pod 一个主容器；Sidecar 模式添加日志、代理等辅助容器。"
        "Pod 无常驻性，由控制器维持期望副本数。"
    ),
    "Service": (
        "Service 提供稳定 ClusterIP 或 NodePort，通过 Label Selector 关联 Pod。"
        "kube-proxy 或 CNI 实现流量转发。Headless Service 用于直连 Pod 场景。"
    ),
    "Transformer": (
        "Transformer 完全基于注意力，摒弃 RNN 顺序依赖。Encoder-Decoder 结构"
        "中 Self-Attention 建模序列内部关系，Multi-Head 并行多组注意力。"
        "位置编码注入顺序信息。GPT 类模型为 Decoder-only。"
    ),
    "事件循环": (
        "JavaScript 事件循环：调用栈执行同步代码，微任务队列（Promise）"
        "优先于宏任务队列（setTimeout）。Node.js 额外有 timers、poll、check 等阶段。"
        "理解顺序是避免异步 bug 的关键。"
    ),
    "垃圾回收": (
        "V8 采用分代 GC：新生代 Scavenge，老生代 Mark-Sweep 与 Mark-Compact。"
        "增量与并发标记减少停顿。避免意外全局引用导致对象无法回收。"
    ),
    "Service Worker": (
        "Service Worker 在独立线程运行，可拦截 fetch 实现缓存策略："
        "Cache First、Network First、Stale-While-Revalidate 等。"
        "是 PWA 离线能力的核心。"
    ),
    "JWT": (
        "JWT 由 Header、Payload、Signature 三段 Base64URL 组成。"
        "服务端用密钥验证签名，Payload 可含 exp、sub 等声明。"
        "JWT 无状态但无法主动失效，需配合短过期与刷新令牌策略。"
    ),
    "OAuth2": (
        "OAuth2 定义授权码、隐式、密码、客户端凭证四种模式。"
        "授权码模式最安全，适合服务端应用。Access Token 访问资源，"
        "Refresh Token 续期。OIDC 在 OAuth2 上增加身份层。"
    ),
    "虚拟内存": (
        "虚拟地址经页表映射到物理页。缺页中断加载磁盘页。"
        "TLB 加速地址转换。进程隔离依赖独立页表。"
    ),
    "TCP": (
        "TCP 三次握手建立连接，四次挥手关闭。滑动窗口与拥塞控制调节发送速率。"
        "Keep-Alive 检测死连接。UDP 无连接、不保证可靠，适合实时场景。"
    ),
}

CONCEPT_EXPLAINERS = [
    "从定义出发：它解决什么问题、不解决什么问题，边界在哪里。",
    "从结构出发：核心组成部分是什么，彼此如何协作。",
    "从流程出发：一次完整调用或生命周期经历哪些阶段。",
    "从数据出发：输入输出是什么格式，状态如何变迁。",
    "从关系出发：它与上下游模块的依赖与接口契约。",
    "从实践出发：典型应用场景与反模式（不该用的场景）。",
    "从演进出发：历史上为何出现、未来可能如何变化。",
    "从度量出发：如何评估它是否工作正常、性能是否达标。",
]

PITFALL_ADVICE = {
    "概念": "回到官方定义画一张概念图，与同事讲解一遍，确保能用自己的话复述。",
    "性能": "用 Profiler 或压测建立基线，对比优化前后数据，避免凭感觉优化。",
    "配置": "核对环境变量、配置文件与部署清单是否一致，使用配置 diff 工具排查。",
    "兼容": "列出依赖版本矩阵，在 CI 中跑集成测试覆盖主要组合。",
    "安全": "做威胁建模与权限审计，最小权限原则，敏感操作留审计日志。",
    "理解": "阅读官方文档与一篇深度文章，结合小实验验证理解。",
    "集成": "定义清晰的接口契约与错误码，联调前用契约测试验证双方。",
    "监控": "补充关键路径指标与告警，确保问题能主动发现而非用户投诉。",
    "默认": "写下预期行为与边界条件清单，用测试或检查项逐条验证后再上线。",
}


def get_domain_intro(domain: str) -> str:
    return DOMAIN_INTROS.get(domain, (
        f"{domain} 是当前技术生态中的重要方向，"
        f"系统学习需兼顾概念、原理与工程实践。"
    ))


def get_module_deep(module: str) -> str:
    if module in MODULE_DEEP:
        return MODULE_DEEP[module]
    for key, text in MODULE_DEEP.items():
        if key in module or module in key:
            return text
    return ""


# 领域 → 主要技术栈/框架
DOMAIN_STACK = {
    "React": {"lang": "JavaScript/TypeScript", "framework": "React 18+", "ecosystem": "Vite, React Router, Redux/Zustand"},
    "Vue": {"lang": "JavaScript/TypeScript", "framework": "Vue 3", "ecosystem": "Vite, Vue Router, Pinia"},
    "Angular": {"lang": "TypeScript", "framework": "Angular 17+", "ecosystem": "RxJS, NgRx"},
    "Node.js": {"lang": "JavaScript/TypeScript", "framework": "Node.js 20+", "ecosystem": "Express, Koa, Fastify"},
    "TypeScript": {"lang": "TypeScript", "framework": "TypeScript 5+", "ecosystem": "tsconfig, tsc, ESLint"},
    "JavaScript核心": {"lang": "JavaScript", "framework": "ES2024", "ecosystem": "V8, Node.js, Browser"},
    "HTML与CSS": {"lang": "HTML/CSS", "framework": "Web标准", "ecosystem": "Flexbox, Grid, CSS Variables"},
    "Spring Boot": {"lang": "Java", "framework": "Spring Boot 3", "ecosystem": "Spring MVC, Spring Data, Spring Security"},
    "Django": {"lang": "Python", "framework": "Django 5", "ecosystem": "DRF, Celery, Django ORM"},
    "Flask": {"lang": "Python", "framework": "Flask 3", "ecosystem": "Jinja2, SQLAlchemy, Flask-RESTful"},
    "Python核心": {"lang": "Python", "framework": "Python 3.12", "ecosystem": "pip, venv, pytest"},
    "Python高级": {"lang": "Python", "framework": "Python 3.12", "ecosystem": "asyncio, multiprocessing, Cython"},
    "Java核心": {"lang": "Java", "framework": "Java 21", "ecosystem": "JVM, Maven, Gradle"},
    "Java并发": {"lang": "Java", "framework": "JUC", "ecosystem": "ThreadPoolExecutor, CompletableFuture"},
    "Go语言": {"lang": "Go", "framework": "Go 1.22+", "ecosystem": "goroutine, channel, go mod"},
    "Rust语言": {"lang": "Rust", "framework": "Rust 2021", "ecosystem": "cargo, tokio, serde"},
    "Rust系统编程": {"lang": "Rust", "framework": "Rust", "ecosystem": "libc, nix, bindgen"},
    "C语言": {"lang": "C", "framework": "C11/C17", "ecosystem": "gcc, clang, make"},
    "C++": {"lang": "C++", "framework": "C++20", "ecosystem": "STL, CMake, clang"},
    "C#": {"lang": "C#", "framework": ".NET 8", "ecosystem": "ASP.NET Core, LINQ"},
    "PHP": {"lang": "PHP", "framework": "PHP 8.3", "ecosystem": "Composer, Laravel"},
    "Docker": {"lang": "Shell/YAML", "framework": "Docker 24+", "ecosystem": "Dockerfile, docker compose"},
    "Kubernetes": {"lang": "YAML/Go", "framework": "K8s 1.29+", "ecosystem": "kubectl, Helm, CRD"},
    "Redis": {"lang": "多种", "framework": "Redis 7", "ecosystem": "Redis Stack, Sentinel, Cluster"},
    "MySQL": {"lang": "SQL", "framework": "MySQL 8", "ecosystem": "InnoDB, Percona, ProxySQL"},
    "PostgreSQL": {"lang": "SQL", "framework": "PostgreSQL 16", "ecosystem": "pg_stat, extensions"},
    "MongoDB": {"lang": "JavaScript/SQL", "framework": "MongoDB 7", "ecosystem": "mongosh, Compass"},
    "Elasticsearch": {"lang": "JSON/DSL", "framework": "ES 8", "ecosystem": "Kibana, Logstash"},
    "Nginx": {"lang": "Nginx配置", "framework": "Nginx 1.25+", "ecosystem": "OpenResty, Lua"},
    "Git版本控制": {"lang": "Git", "framework": "Git 2.43+", "ecosystem": "GitHub, GitLab"},
    "CI与CD": {"lang": "YAML", "framework": "GitHub Actions", "ecosystem": "Jenkins, GitLab CI"},
    "微服务架构": {"lang": "多语言", "framework": "微服务", "ecosystem": "Spring Cloud, Istio, Consul"},
    "GraphQL": {"lang": "GraphQL", "framework": "Apollo/GraphQL", "ecosystem": "Relay, Prisma"},
    "大语言模型": {"lang": "Python", "framework": "PyTorch/HF", "ecosystem": "Transformers, LangChain"},
    "机器学习": {"lang": "Python", "framework": "scikit-learn", "ecosystem": "NumPy, Pandas, Jupyter"},
    "深度学习": {"lang": "Python", "framework": "PyTorch 2", "ecosystem": "CUDA, TensorBoard"},
    "区块链": {"lang": "Solidity/Go", "framework": "Ethereum", "ecosystem": "Web3.js, Hardhat"},
    "Linux内核": {"lang": "C", "framework": "Linux 6.x", "ecosystem": "kprobe, ftrace, perf"},
    "Linux系统编程": {"lang": "C", "framework": "POSIX", "ecosystem": "glibc, epoll"},
    "Linux运维": {"lang": "Shell", "framework": "systemd", "ecosystem": "Ansible, Prometheus"},
    "浏览器原理": {"lang": "JavaScript", "framework": "Chromium", "ecosystem": "V8, Blink, DevTools"},
    "Web性能优化": {"lang": "JavaScript", "framework": "Web标准", "ecosystem": "Lighthouse, Web Vitals"},
    "前端工程化": {"lang": "JavaScript", "framework": "Vite/Webpack", "ecosystem": "ESLint, Babel, pnpm"},
}

MODULE_HINTS = {
    "Hooks": "React Hooks 在函数组件中提供状态与副作用能力，遵循「只在顶层调用」规则。",
    "useState": "useState 返回状态值与更新函数，更新触发重新渲染，批量更新在事件处理中合并。",
    "useEffect": "useEffect 在渲染提交后执行副作用，依赖数组控制触发时机，清理函数在卸载或重渲染前执行。",
    "goroutine": "Go 的 goroutine 是轻量级线程，由 Go runtime 调度，通过 channel 通信共享内存。",
    "channel": "channel 是 Go 并发核心，无缓冲 channel 同步传递，有缓冲 channel 异步传递。",
    "路由": "路由负责 URL 与处理逻辑的映射，支持静态、动态与嵌套路由。",
    "中间件": "中间件在请求处理链中插入逻辑，典型模式为洋葱模型。",
    "事件循环": "事件循环将回调注册到队列，在单线程中交替执行，避免阻塞。",
    "垃圾回收": "GC 自动回收不可达对象，现代实现多采用分代与并发标记。",
    "索引": "数据库索引加速查询，B+树是 InnoDB 默认索引结构，需权衡读写性能。",
    "事务": "事务保证 ACID，隔离级别决定并发读写时的可见性与锁行为。",
    "容器": "容器共享宿主机内核，通过 Namespace 与 Cgroups 实现隔离与资源限制。",
    "Pod": "Pod 是 K8s 最小调度单元，通常一个 Pod 运行一个主容器及辅助容器。",
    "Service": "K8s Service 提供稳定访问端点，通过 Label Selector 关联 Pod。",
    "Deployment": "Deployment 管理 ReplicaSet，支持滚动更新与回滚。",
    "JWT": "JWT 由 Header.Payload.Signature 组成，服务端用密钥验证签名完整性。",
    "OAuth2": "OAuth2 授权框架定义四种授权模式，access token 用于资源访问。",
    "Transformer": "Transformer 基于自注意力机制，并行处理序列，是 LLM 的基础架构。",
    "注意力机制": "注意力计算 Query-Key 相似度加权 Value，实现长距离依赖建模。",
    "所有权": "Rust 所有权系统在编译期保证内存安全，每个值有唯一所有者。",
    "借用与引用": "借用允许临时访问而不转移所有权，编译器通过生命周期检查引用有效性。",
    "进程管理": "操作系统通过 PCB 管理进程状态，调度器决定 CPU 分配策略。",
    "虚拟内存": "虚拟内存通过页表映射，支持进程隔离与按需分页。",
    "TCP": "TCP 提供可靠字节流，三次握手建立连接，滑动窗口控制流量。",
    "HTTP": "HTTP 基于请求-响应模型，HTTP/2 多路复用，HTTP/3 基于 QUIC。",
    "Service Worker": "Service Worker 在后台线程拦截网络请求，实现离线缓存与推送。",
    "Webpack": "Webpack 以模块入口构建依赖图，loader 转换资源，plugin 扩展构建流程。",
    "Vite": "Vite 开发时用 esbuild 预构建依赖，生产用 Rollup 打包，HMR 极快。",
}


def get_stack(domain: str) -> dict:
    default = {"lang": "通用", "framework": domain, "ecosystem": "行业标准工具链"}
    return DOMAIN_STACK.get(domain, default)


def get_module_hint(module: str) -> str:
    if module in MODULE_HINTS:
        return MODULE_HINTS[module]
    for key, hint in MODULE_HINTS.items():
        if key in module or module in key:
            return hint
    return f"「{module}」是该领域的核心知识模块，理解其原理与边界是工程实践的基础。"
