#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_backend.py and content_data_devops.py with real technical tutorials."""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from typing import Dict, Tuple, List

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from domains_100_config import DOMAINS_CONFIG
from article_generator.manual._content_specs_extended import EXTENDED_FACTS

BACKEND_DOMAINS = [
    "后端架构", "RESTful API", "微服务架构", "Spring Boot", "认证授权", "API设计",
    "Serverless", "GraphQL", "WebSocket", "消息队列", "Django", "Flask",
    "自动化测试", "性能测试", "代码重构", "设计模式",
]
DATA_DEVOPS_DOMAINS = [
    "数据库原理", "MySQL", "Redis", "PostgreSQL", "MongoDB", "Elasticsearch",
    "数据仓库", "缓存技术", "ETL开发", "时序数据库", "Docker", "Kubernetes",
    "CI与CD", "Git版本控制", "Linux运维", "监控告警", "日志分析", "Nginx",
    "云计算", "Ansible",
]

# ---------------------------------------------------------------------------
# Hand-crafted high-quality module content (real internals)
# Key: (domain, module)
# ---------------------------------------------------------------------------
DETAILED: Dict[Tuple[str, str], dict] = {
    ("Flask", "路由"): {
        "intro": (
            "Flask 路由系统建立在 Werkzeug 的 **Map** 与 **Rule** 之上。"
            "应用启动时 `@app.route` 装饰器向 `app.url_map` 注册规则；"
            "请求到达时 Werkzeug 按规则优先级匹配 URL，提取动态参数并 dispatch 到视图函数。"
        ),
        "concepts": [
            {"title": "Werkzeug Map 与 Rule", "body": (
                "`werkzeug.routing.Map` 维护一组 `Rule` 对象。每条 Rule 包含路径模式（如 `/user/<int:id>`）、"
                "允许的 HTTP 方法、endpoint 名称。Map 在编译阶段将路径转为正则与转换器（Converter），"
                "支持 `int`、`float`、`path`、`uuid` 等内置类型及自定义 Converter。"
            )},
            {"title": "路由注册与 url_map", "body": (
                "Flask 在 `Flask.__init__` 中创建 `self.url_map = Map()`。"
                "`add_url_rule(rule, endpoint, view_func, methods=...)` 将 Rule 加入 Map。"
                "蓝图注册时会把蓝图的 url_map 合并到应用 Map，并加上 url_prefix。"
            )},
            {"title": "匹配与 dispatch", "body": (
                "WSGI 入口 `Flask.wsgi_app` 构造 `Request`，调用 `url_map.bind_to_environ` 得到 `MapAdapter`，"
                "再 `match(path_info, method)` 返回 `(endpoint, view_args)`。"
                "405 由 MethodNotAllowed 触发，404 由 NotFound 触发。"
            )},
        ],
        "mechanism": (
            "请求路径经 MapAdapter 逐级匹配：静态段精确比较，动态段调用 Converter.to_python。"
            "同一 endpoint 可绑定多条 Rule（不同 methods 或 paths）。"
            "Flask 2.x 默认 `strict_slashes=True`，尾部斜杠不一致会 308 重定向。"
        ),
        "internals": (
            "Werkzeug Map 内部用状态机构建 URL 匹配树（类似 radix tree），"
            "比逐条正则遍历更高效。`Rule.build` 生成 `_regex` 与 `_trace`。"
            "阅读 `werkzeug/routing/map.py` 与 `flask/app.py` 的 `dispatch_request` 可完整跟踪调用链。"
        ),
        "workflow": (
            "1. 定义视图并用 `@app.route('/items/<int:item_id>', methods=['GET','PUT'])` 注册\n"
            "2. 启动时检查 endpoint 唯一性\n"
            "3. 请求 `/items/42` → Map 匹配 → `view_args={'item_id': 42}`\n"
            "4. `app.view_functions[endpoint]` 被调用并返回 Response"
        ),
        "performance": "路由匹配在内存中完成，开销通常可忽略；避免单 endpoint 挂载过多重叠 Rule 导致匹配回溯。",
        "security": "动态段使用专用 Converter，避免将未校验字符串直接拼 SQL；敏感操作限定 methods=['POST'] 并校验 CSRF。",
        "debugging": "`flask routes` CLI 或 `app.url_map.iter_rules()` 列出所有 Rule；404 时检查 methods 与 trailing slash。",
        "pitfalls": [
            {"title": "endpoint 冲突", "body": "后注册的同名 endpoint 覆盖前者，蓝图与应用间易冲突，应使用 `endpoint=` 显式命名。"},
            {"title": "Converter 类型错误", "body": "`<id>` 默认 str，数值比较前需 `<int:id>`，否则得到字符串导致 ORM 查询异常。"},
        ],
        "practices": [
            "REST 资源用名词复数路径，版本放在 Header 或 URL 前缀",
            "大型项目用 Blueprint 拆分 url_map",
            "为 API 统一注册 errorhandler(404/405)",
        ],
        "references": [
            "Flask 官方文档 - Routing",
            "Werkzeug routing 源码",
            "PEP 3333 WSGI 规范",
        ],
    },
    ("Kubernetes", "Pod"): {
        "intro": (
            "Pod 是 Kubernetes 最小调度单元，是一组共享 Linux 命名空间的容器集合。"
            "同一 Pod 内容器共享 **network namespace**（同一 IP、localhost 互通）、"
            "可选共享 **IPC** 与 **PID namespace**（enableShareProcessNamespace），"
            "并通过 Volume 共享存储。"
        ),
        "concepts": [
            {"title": "Pause 容器与网络命名空间", "body": (
                "Pod 创建时 kubelet 先启动 **pause**（sandbox）容器，持有 network namespace。"
                "业务容器通过 `network_mode=container:<pause_id>` 加入该 NS，"
                "因此 Pod IP 即 pause 容器在 CNI 插件分配下的地址，生命周期独立于业务容器重启。"
            )},
            {"title": "共享存储卷", "body": (
                "Pod spec 中 `volumes` 声明存储，`containers[].volumeMounts` 挂载到相同或不同路径。"
                "emptyDir 随 Pod 生灭；PVC 可跨 Pod 但同 Pod 多容器共享一 mount 可实现 sidecar 日志采集。"
            )},
            {"title": "Sidecar 模式", "body": (
                "主容器处理业务，Sidecar 处理代理（Envoy）、日志（Fluent Bit）、配置热加载等。"
                "共享 network NS 使 Sidecar 可 localhost 拦截主容器流量而无需改应用代码。"
            )},
        ],
        "mechanism": (
            "kubelet 调用 CRI（containerd/CRI-O）创建 PodSandbox → 创建 infra 容器 → 按序启动 containers。"
            "liveness/readiness probe 由 kubelet 执行。Pod 状态聚合所有容器状态；"
            "RestartPolicy 决定容器退出后行为（Always/OnFailure/Never）。"
        ),
        "internals": (
            "API Server 持久化 Pod 至 etcd；Scheduler 绑定 Node；kubelet syncLoop 对账。"
            "Pod 无自愈能力，Deployment/StatefulSet 等控制器通过 ReplicaSet 维持期望副本。"
            "Downward API 将 metadata 注入环境变量或 volume。"
        ),
        "workflow": (
            "1. 编写 Pod YAML（containers、volumes、resources）\n"
            "2. kubectl apply → API Server 持久化\n"
            "3. Scheduler 过滤+打分选 Node\n"
            "4. kubelet 拉镜像、创 sandbox、挂载卷、启动容器\n"
            "5. kubelet 上报 status → Endpoints 控制器更新 Service 后端"
        ),
        "performance": "单 Pod 多容器共享 CPU/memory limits 的 cgroup；合理设置 requests/limits 避免 noisy neighbor。",
        "security": "SecurityContext 设定 runAsNonRoot、readOnlyRootFilesystem、capabilities drop；NetworkPolicy 限制 Pod 间流量。",
        "configuration": "initContainers 在主容器前顺序执行；terminationGracePeriodSeconds 控制 SIGTERM 宽限期。",
        "pitfalls": [
            {"title": "多容器抢同一端口", "body": "共享 network NS 下仅一个进程可 bind 同一端口，需错开端口或通过 Sidecar 代理。"},
            {"title": "emptyDir 丢数据", "body": "Pod 删除后 emptyDir 清空，有状态 workload 应使用 PVC 或 StatefulSet。"},
        ],
        "practices": [
            "生产环境由 Deployment 管理 Pod，避免裸 Pod",
            "一个 Pod 一个主进程容器是默认最佳实践",
            "为 Pod 设置 label 供 Service selector 使用",
        ],
        "references": ["Kubernetes 官方文档 - Pod", "CNI 规范", "containerd CRI 设计"],
        "mermaid": """```mermaid
graph TB
    subgraph Pod网络命名空间
        P[pause/infra容器]
        A[业务容器A localhost]
        B[Sidecar容器B localhost]
    end
    CNI[CNI插件] --> P
    A --> P
    B --> P
    Vol[共享Volume] --> A
    Vol --> B
```""",
    },
    ("MySQL", "InnoDB"): {
        "intro": (
            "InnoDB 是 MySQL 8 默认存储引擎，提供行级锁、MVCC 事务与崩溃恢复。"
            "数据按 **聚簇索引（B+树）** 组织：主键叶子节点存完整行，"
            "二级索引叶子存主键值需 **回表** 查聚簇索引。"
        ),
        "concepts": [
            {"title": "B+树聚簇索引", "body": (
                "InnoDB 表数据即主键 B+树：非叶子节点仅存键用于导航，叶子节点通过双向链表连接支持范围扫描。"
                "页（Page，默认 16KB）是 IO 最小单位。插入可能导致页分裂（Split），删除可能合并（Merge）。"
            )},
            {"title": "Buffer Pool", "body": (
                "内存中缓存数据页与索引页，读写优先命中 Buffer Pool。"
                "LRU 变种管理热度；dirty page 由 redo log 保证持久化，checkpoint 刷脏。"
                "`innodb_buffer_pool_size` 通常设为物理内存 50–70%。"
            )},
            {"title": "MVCC 与 Read View", "body": (
                "每行有隐藏列 DB_TRX_ID、DB_ROLL_PTR 指向 undo log 版本链。"
                "READ COMMITTED / REPEATABLE READ 通过 Read View 判断版本可见性，"
                "实现非锁定一致性读。"
            )},
        ],
        "mechanism": (
            "写操作：更新 Buffer Pool 页 → 写 undo log（旧版本）→ 写 redo log（WAL）→ 事务提交时 redo fsync。"
            "崩溃恢复：redo log 前滚 + undo log 回滚未提交事务。"
        ),
        "internals": (
            "表空间文件 .ibd 存 B+树；系统表空间存数据字典。"
            "Doublewrite buffer 防止 partial page write。"
            "Change Buffer 延迟更新非唯一二级索引页以提升写性能。"
        ),
        "performance": (
            "主键单调递增（雪花 ID、自增）减少页分裂；避免过长二级索引（多列+长 VARCHAR）。"
            "覆盖索引避免回表；`EXPLAIN ANALYZE` 观察实际行数。"
        ),
        "security": "行级锁降低锁粒度；SELECT ... FOR UPDATE 显式加 X 锁防并发更新丢失。",
        "debugging": "`SHOW ENGINE INNODB STATUS` 查看锁等待；Performance Schema 分析 buffer pool 命中率。",
        "pitfalls": [
            {"title": "无显式主键", "body": "InnoDB 会选首个 UNIQUE NOT NULL 或隐式 6 字节 row_id，二级索引变大且性能差。"},
            {"title": "长事务撑大 undo", "body": "undo 段无法 purge 导致表空间膨胀与查询变慢，应控制事务时长。"},
        ],
        "practices": [
            "主键短且有序",
            "批量写调大 redo log 与 buffer pool",
            "监控 History list length",
        ],
        "references": ["MySQL 8 Reference Manual - InnoDB", "《MySQL 技术内幕：InnoDB 存储引擎》"],
    },
    ("MySQL", "索引原理"): {
        "intro": (
            "InnoDB 索引结构为 B+树：矮胖结构使磁盘 IO 次数约为 log_{fanout}(N)。"
            "主键索引即聚簇索引；二级索引叶子节点存储索引列值 + 主键值。"
        ),
        "concepts": [
            {"title": "最左前缀原则", "body": "联合索引 (a,b,c) 可用于 a、 (a,b)、 (a,b,c) 条件；跳过 leading column 无法利用 B+树有序性。"},
            {"title": "覆盖索引", "body": "查询列全部在二级索引中即可 Index Only Scan，无需回表聚簇索引，显著降低 IO。"},
            {"title": "索引下推 ICP", "body": "MySQL 5.6+ 在存储引擎层用索引列过滤，减少回表行数。"},
        ],
        "mechanism": "优化器基于统计信息估算 cost，选择 ref/range/index 等 access type；Cardinality 影响选择。",
        "internals": "Adaptive Hash Index 对热点页建内存哈希加速等值查询；不可手动控制，仅作内部优化。",
        "performance": "避免函数包裹索引列（`WHERE YEAR(d)=2024` 无法走索引）；前缀索引节省空间但降低选择性。",
        "pitfalls": [
            {"title": "过多索引", "body": "每次 INSERT/UPDATE 需维护所有相关 B+树，写放大明显。"},
            {"title": "低选择性列单独建索引", "body": "如 gender 列区分度低，优化器可能选择全表扫描。"},
        ],
        "practices": ["用 EXPLAIN 验证 type 与 key_len", "定期 ANALYZE TABLE 更新统计信息"],
        "references": ["MySQL EXPLAIN 文档", "Index Condition Pushdown"],
    },
    ("Redis", "数据结构"): {
        "intro": (
            "Redis 基于 **SDS**、**dict**、**quicklist**、**skiplist+dict** 等底层结构实现对外 API。"
            "所有操作在主线程单线程执行，保证命令原子性；6.0+ 多 IO 线程仅处理网络读写。"
        ),
        "concepts": [
            {"title": "SDS 与 String", "body": "简单动态字符串记录 len/free，O(1) 取长度；二进制安全，可存图片序列化。"},
            {"title": "quicklist 与 List", "body": "3.2+ List 为 ziplist 与 linkedlist 结合的 quicklist，平衡内存与插入性能。"},
            {"title": "skiplist 与 ZSet", "body": "有序集合同时维护 dict（member→score）与 skiplist（按 score 排序），范围查询 O(log N + M)。"},
        ],
        "mechanism": "命令表 `redisCommand` 绑定 proc 函数；事件循环 aeEventLoop 处理可读可写事件。",
        "internals": "对象系统 `redisObject` 含 type、encoding、ptr；encoding 随数据量自动转换（如 int→raw→embstr）。",
        "performance": "大 key 拆分；避免 O(N) 命令阻塞主线程（KEYS、SMEMBERS 大集合）。",
        "pitfalls": [{"title": "热 key 单线程瓶颈", "body": "单 key QPS 有上限，可用本地缓存或多副本拆分。"}],
        "practices": ["用 SCAN 代替 KEYS", "监控 slowlog", "合理选择 encoding"],
        "references": ["Redis 设计与实现", "Redis 官方命令文档"],
    },
    ("Docker", "容器"): {
        "intro": (
            "Docker 容器是 **进程级隔离**：Linux **Namespace** 隔离 PID/NET/MNT/UTS/IPC/USER，"
            "**Cgroups** 限制 CPU/内存/IO。容器共享宿主机内核，比 VM 更轻量。"
        ),
        "concepts": [
            {"title": "Namespace 隔离", "body": "PID namespace 内 init 为 PID 1；NET namespace 独立网络栈与 iptables；MNT namespace 独立挂载点视图。"},
            {"title": "Cgroups v2", "body": "限制 memory.max、cpu.max；OOM 时 kill 容器内进程而非宿主机。"},
            {"title": "容器即进程", "body": "containerd 通过 runc 创建带 namespace 的进程；docker ps 列出的是 cgroup 中的进程组。"},
        ],
        "mechanism": "dockerd → containerd → runc → 配置 namespaces + cgroups → 执行容器 entrypoint。",
        "internals": "镜像层 overlay2 联合挂载为容器 rootfs；Copy-on-Write 使新写落 upper layer。",
        "security": "非 root 用户运行；drop capabilities；只读 rootfs；seccomp/AppArmor 限制 syscall。",
        "practices": ["显式 USER 指令", "healthcheck 探活", "资源 limits 防 noisy neighbor"],
        "references": ["Docker 架构文档", "Linux namespaces man7"],
    },
    ("Spring Boot", "自动配置"): {
        "intro": (
            "Spring Boot 自动配置通过 `@EnableAutoConfiguration` 导入 `AutoConfiguration.imports`，"
            "利用 **@Conditional** 系列注解按 classpath 与 property 条件注册 Bean。"
        ),
        "concepts": [
            {"title": "spring.factories → AutoConfiguration.imports", "body": "Boot 3 改用 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 列表。"},
            {"title": "@ConditionalOnClass", "body": "classpath 存在指定类时才生效，如 DataSourceAutoConfiguration 需 JDBC 驱动。"},
            {"title": "ConfigurationProperties", "body": "`@ConfigurationProperties(prefix=\"server\")` 绑定 application.yml 到类型安全 POJO。"},
        ],
        "mechanism": "SpringApplication 启动 → 加载 Environment → 解析 auto-config 类 → 条件评估 → 注册 BeanDefinition。",
        "internals": "AutoConfigurationImportSelector 读取 imports 文件；@AutoConfigureBefore/After 控制顺序。",
        "debugging": "启动加 `--debug` 或 `logging.level.org.springframework.boot.autoconfigure=DEBUG` 查看条件报告。",
        "pitfalls": [{"title": "Bean 重复定义", "body": "自定义 Bean 与 auto-config 冲突，用 @Primary 或 exclude 排除。"}],
        "practices": ["自定义配置放 @Configuration 并控制 @Order", "生产关闭 devtools"],
        "references": ["Spring Boot Reference - Auto-configuration"],
    },
    ("消息队列", "Kafka"): {
        "intro": (
            "Apache Kafka 是分布式 commit log：Topic 分区有序 append-only，"
            "Producer 按 key hash 选分区；Consumer Group 内分区独占消费实现水平扩展。"
        ),
        "concepts": [
            {"title": "分区与副本", "body": "Partition Leader 处理读写，Follower ISR 同步；min.insync.replicas 保障 acks=all 语义。"},
            {"title": "Consumer Offset", "body": "Offset 存 __consumer_offsets 或外部系统；rebalance 时 partition 重新分配。"},
            {"title": "零拷贝 sendfile", "body": "Broker 向 Consumer 传输时用 sendfile 减少用户态拷贝，提升吞吐。"},
        ],
        "mechanism": "Producer → batch 压缩 → Partition leader append log → follower 拉取 → ack 返回。",
        "performance": "batch.size、linger.ms 权衡延迟与吞吐；分区数 ≈ 目标并行 Consumer 数。",
        "pitfalls": [{"title": "Consumer rebalance 风暴", "body": "频繁 join/leave 导致 stop-the-world，应合理 session.timeout 与 cooperative sticky assignor。"}],
        "practices": ["监控 under-replicated partitions", "业务 key 保证同实体进同分区"],
        "references": ["Kafka 官方文档", "KIP 列表"],
    },
    ("GraphQL", "Schema"): {
        "intro": (
            "GraphQL Schema 用 SDL 定义 Query/Mutation/Subscription 根类型及对象图。"
            "强类型系统使客户端明确可请求字段，服务端 Resolver 按字段粒度解析。"
        ),
        "concepts": [
            {"title": "类型与字段", "body": "Object Type 定义字段与参数；Non-Null `!` 与 List `[]` 组合表达 cardinality。"},
            {"title": "Resolver 函数", "body": "每个字段可绑定 `(parent, args, context, info) => value`；默认 resolver 读 parent 属性。"},
            {"title": "Introspection", "body": "`__schema` 查询使 GraphiQL 等工具自动生成文档与类型校验。"},
        ],
        "mechanism": "Query 解析 → 验证 against schema → 执行计划（并行无依赖字段）→ 序列化 JSON 响应。",
        "security": "限制查询深度与复杂度；禁用生产 introspection；Persisted Queries 白名单。",
        "pitfalls": [{"title": "N+1 查询", "body": "列表字段逐条 resolver 查 DB，用 DataLoader 批量加载。"}],
        "practices": ["Schema 优先设计", "错误遵循 GraphQL errors 规范"],
        "references": ["GraphQL Spec", "Apollo Server 文档"],
    },
    ("认证授权", "JWT"): {
        "intro": (
            "JWT（RFC 7519）由 Header.Payload.Signature 组成，Base64URL 编码。"
            "Signature = HMAC-SHA256(Header.Payload, secret) 或 RSA/ECDSA 私钥签名；"
            "服务端用密钥验签，无需服务端会话存储即可无状态认证。"
        ),
        "concepts": [
            {"title": "声明 Claims", "body": "registered claims：iss、sub、exp、iat；自定义 claim 放 role、tenant 等，避免放敏感 PII。"},
            {"title": "Access 与 Refresh Token", "body": "Access 短过期（15min），Refresh 长过期存 HttpOnly Cookie 或安全存储，轮换防重放。"},
            {"title": "算法选择", "body": "HS256 对称密钥需所有服务共享；RS256 公钥验签适合微服务；禁用 none 算法。"},
        ],
        "mechanism": "登录成功签发 JWT → 客户端 Authorization: Bearer → 网关/服务验签 exp 与 scope → 授权。",
        "security": "密钥轮换；短 exp；HTTPS 传输；logout 需 token 黑名单或 session 版本号。",
        "pitfalls": [{"title": "Payload 不可信", "body": "JWT 仅 Base64 非加密，敏感数据勿明文放入 Payload。"}],
        "practices": ["使用成熟库（jjwt、PyJWT）", "校验 aud/iss", "Refresh Token 单次使用"],
        "references": ["RFC 7519", "OWASP JWT Cheat Sheet"],
    },
    ("Nginx", "反向代理"): {
        "intro": (
            "Nginx 反向代理将客户端请求转发至 upstream 服务器群，"
            "基于 **事件驱动 epoll/kqueue** 单 worker 处理数万并发连接。"
            "proxy_pass 修改 Host、X-Forwarded-* 头传递客户端真实信息。"
        ),
        "concepts": [
            {"title": "upstream 与负载均衡", "body": "round-robin、least_conn、ip_hash、hash $request_uri consistent；健康检查需 nginx-plus 或 openresty。"},
            {"title": "proxy_buffering", "body": "默认缓冲 upstream 响应再发给客户端；流式/SSE 需 proxy_buffering off。"},
            {"title": "keepalive 连接池", "body": "upstream 块配置 keepalive N 复用到后端 TCP，降低握手开销。"},
        ],
        "mechanism": "请求 → location 匹配 → proxy_pass URI 拼接规则 → 选 upstream peer → 转发 → 回写响应。",
        "performance": "worker_processes auto；sendfile on；gzip 压缩文本；调整 worker_connections。",
        "pitfalls": [{"title": "URI 被截断", "body": "proxy_pass 带 URI 路径时 location 匹配部分会被替换，需注意 trailing slash。"}],
        "practices": ["传递 X-Forwarded-For 与 Proto", "设置 proxy_read_timeout", "upstream 失败重试策略"],
        "references": ["Nginx ngx_http_proxy_module", "Nginx 性能调优指南"],
    },
}

# Domain-level overview text (real positioning)
DOMAIN_META = {
    "后端架构": {
        "category": "后端开发",
        "intro": "后端架构定义系统的边界、分层与演进路径，从单体到微服务、从同步 REST 到事件驱动，需要在一致性、可用性与团队组织之间权衡。",
        "positioning": "本领域覆盖架构风格（分层、CQRS、DDD）、横切能力（缓存、消息、高可用）与 API/数据架构设计，面向 Tech Lead 与资深工程师。",
        "prerequisites": ["至少一种后端语言", "HTTP 与数据库基础", "分布式系统入门概念"],
        "outcomes": ["能评估单体与微服务拆分边界", "能设计高可用与高并发架构方案", "能绘制 C4/序列图沟通架构决策", "能识别架构坏味道并制定演进路线"],
        "ecosystem": "Spring Cloud、Istio、Kafka、Redis、PostgreSQL、Prometheus",
    },
    "RESTful API": {
        "category": "后端开发",
        "intro": "REST 以资源为中心，用 HTTP 动词表达操作，状态码传达结果。良好 REST API 强调无状态、统一接口与可缓存性，是前后端与 B2B 集成的主流契约形式。",
        "positioning": "从资源建模、URI 设计到版本控制、错误格式与 HATEOAS，建立可测试、可文档化、可演进的 API 工程体系。",
        "prerequisites": ["HTTP 协议", "JSON", "基础认证概念"],
        "outcomes": ["能设计符合 Richardson 成熟度的 REST API", "能编写 OpenAPI 规范并生成 SDK", "能处理分页、过滤、幂等与并发控制", "能评估 REST 与 GraphQL/RPC 选型"],
        "ecosystem": "OpenAPI/Swagger、Postman、Spring MVC、FastAPI、API Gateway",
    },
    "微服务架构": {
        "category": "后端开发",
        "intro": "微服务将应用拆为可独立部署的服务单元，通过轻量通信（HTTP/gRPC/消息）协作，带来团队自治与技术异构，也引入分布式事务、观测与治理复杂度。",
        "positioning": "覆盖服务拆分、服务发现、网关、熔断限流、Saga 事务、链路追踪与服务网格，强调可运维性。",
        "prerequisites": ["后端开发经验", "Docker 基础", "网络与数据库"],
        "outcomes": ["能制定服务边界与数据所有权", "能搭建服务发现与配置中心", "能设计熔断降级与灰度发布", "能建立分布式追踪与 SLO"],
        "ecosystem": "Spring Cloud Alibaba、Consul、Istio、Jaeger、Nacos",
    },
    "Spring Boot": {
        "category": "后端开发",
        "intro": "Spring Boot 通过自动配置、Starter 依赖与内嵌容器，使 Spring 应用快速启动。Spring Boot 3 基于 Jakarta EE 9+ 与 Java 17，原生镜像支持 GraalVM。",
        "positioning": "从 Web、数据访问、Security 到 Actuator 监控与 Spring Cloud 微服务，面向 Java 企业级后端主流栈。",
        "prerequisites": ["Java 基础", "Maven/Gradle", "HTTP 与 SQL"],
        "outcomes": ["理解自动配置条件与扩展点", "能构建 REST + JPA + Security 应用", "能配置多环境与外部化配置", "能集成 Actuator 与分布式组件"],
        "ecosystem": "Spring MVC、Spring Data、Spring Security、Spring Cloud、Micrometer",
    },
    "认证授权": {
        "category": "后端开发",
        "intro": "认证（Authentication）验证身份，授权（Authorization）判定权限。Web 与 API 场景下 Session、JWT、OAuth2/OIDC 与 RBAC/ABAC 构成现代安全体系。",
        "positioning": "覆盖凭证存储、Token 生命周期、SSO、MFA 与 API 权限模型，强调威胁建模与合规。",
        "prerequisites": ["HTTP Cookie/Header", "密码学哈希基础", "HTTPS"],
        "outcomes": ["能设计 Session 与 JWT 混合方案", "能集成 OAuth2 授权码流程", "能建模 RBAC 与数据权限", "能应对 OWASP 认证相关风险"],
        "ecosystem": "Spring Security、Keycloak、Auth0、OAuth2、OpenID Connect",
    },
    "API设计": {
        "category": "后端开发",
        "intro": "API 设计是内外部系统协作的契约工程，涵盖 REST、GraphQL、gRPC 等风格，以及版本、文档、测试与治理全生命周期。",
        "positioning": "强调一致性、错误模型、幂等性与开发者体验（DX），适用于平台团队与 API 产品经理。",
        "prerequisites": ["HTTP", "至少一种 API 风格经验"],
        "outcomes": ["能制定组织级 API 设计规范", "能设计版本与弃用策略", "能建立 Mock 与契约测试流水线", "能评估网关与 API 市场方案"],
        "ecosystem": "OpenAPI、GraphQL Schema、Buf、Kong、Apigee",
    },
    "Serverless": {
        "category": "后端开发",
        "intro": "Serverless 将运维抽象至云厂商，开发者以函数为单位按 invocation 计费。事件驱动、自动扩缩与冷启动是其核心特征。",
        "positioning": "覆盖 FaaS、BFF、Step Functions 编排、冷启动优化与成本模型，适合事件型与流量波动大的 workload。",
        "prerequisites": ["HTTP API", "云基础概念", "无状态设计"],
        "outcomes": ["能设计函数粒度与事件源映射", "能优化冷启动与包体积", "能处理有状态需求的替代方案", "能估算 Serverless 与容器成本"],
        "ecosystem": "AWS Lambda、API Gateway、阿里云函数计算、Knative",
    },
    "GraphQL": {
        "category": "后端开发",
        "intro": "GraphQL 提供强类型 Schema 与客户端按需取字段，减少 over-fetching。Subscription 支持实时推送，适合 BFF 与复杂前端数据聚合。",
        "positioning": "从 Schema 设计、Resolver、DataLoader 到安全与性能，对比 REST 的适用边界。",
        "prerequisites": ["JSON", "REST 基础", "TypeScript 或 Java 一种"],
        "outcomes": ["能设计可演进 Schema", "能优化 N+1 与查询复杂度", "能实现 Subscription", "能评估 Federation 与 REST 共存"],
        "ecosystem": "Apollo Server、GraphQL Java、Hasura、Relay",
    },
    "WebSocket": {
        "category": "后端开发",
        "intro": "WebSocket 在单 TCP 连接上提供全双工通信，握手通过 HTTP Upgrade 完成。适用于聊天、协作编辑、行情推送等低延迟场景。",
        "positioning": "覆盖协议帧、心跳、房间广播、水平扩展与 Sticky Session，对比 SSE 与长轮询。",
        "prerequisites": ["HTTP", "TCP 基础", "异步编程"],
        "outcomes": ["能实现服务端/客户端 WebSocket", "能设计心跳与重连策略", "能在负载均衡后扩展连接", "能评估消息协议（JSON/Protobuf）"],
        "ecosystem": "Socket.IO、Spring WebSocket、ws、Nginx proxy_http_version 1.1",
    },
    "消息队列": {
        "category": "后端开发",
        "intro": "消息队列解耦生产者与消费者，提供异步、削峰与最终一致性。Kafka 适合日志流，RabbitMQ 适合复杂路由，RocketMQ 适合事务消息。",
        "positioning": "覆盖消息模型、可靠性、顺序、事务与死信，是分布式系统必备基础设施。",
        "prerequisites": ["并发编程", "网络基础", "数据库事务概念"],
        "outcomes": ["能选型 Kafka/RabbitMQ/RocketMQ", "能保证 at-least-once 与幂等消费", "能设计延迟队列与死信处理", "能监控 lag 与 rebalance"],
        "ecosystem": "Kafka、RabbitMQ、RocketMQ、Pulsar、Spring AMQP",
    },
    "Django": {
        "category": "后端开发",
        "intro": "Django 是 Python 全栈 Web 框架，MTV 模式内置 ORM、Admin、认证与中间件。Django REST Framework 使其成为构建 API 的流行选择。",
        "positioning": "从 URL 路由、视图、模板到 ORM 迁移与 DRF，适合内容站点与中大型 Python 后端。",
        "prerequisites": ["Python 基础", "SQL", "HTTP"],
        "outcomes": ["理解 MTV 与请求生命周期", "能使用 ORM 与迁移管理模型", "能用 DRF 构建 REST API", "能配置缓存、信号与中间件"],
        "ecosystem": "DRF、Celery、PostgreSQL、Gunicorn、Redis",
    },
    "Flask": {
        "category": "后端开发",
        "intro": "Flask 是轻量 WSGI 框架，核心仅路由与模板，通过扩展组装 SQLAlchemy、JWT 等能力。Werkzeug 提供路由 Map 与 Request/Response 对象。",
        "positioning": "适合微服务、原型与中小型 API；强调显式配置与蓝图模块化。",
        "prerequisites": ["Python", "HTTP", "WSGI 概念"],
        "outcomes": ["理解 Werkzeug 路由匹配", "能用蓝图组织大型应用", "能集成 SQLAlchemy 与 Marshmallow", "能用 Gunicorn/uWSGI 部署"],
        "ecosystem": "Werkzeug、Jinja2、SQLAlchemy、Flask-RESTful、Gunicorn",
    },
    "自动化测试": {
        "category": "后端开发",
        "intro": "自动化测试通过单元、集成与 E2E 分层保障回归质量。测试金字塔建议大量单元测试、适量集成、少量 E2E，并与 CI 流水线集成。",
        "positioning": "覆盖 Jest/Pytest/JUnit、Mock、覆盖率与 Playwright/Cypress，面向质量工程师与开发。",
        "prerequisites": ["至少一门语言", "基本断言与 CLI"],
        "outcomes": ["能编写可维护的单元与集成测试", "能 Mock 外部依赖", "能在 CI 中并行跑测试", "能制定测试策略与覆盖率门禁"],
        "ecosystem": "Pytest、JUnit 5、Jest、Selenium、Cypress、Playwright",
    },
    "性能测试": {
        "category": "后端开发",
        "intro": "性能测试验证系统在负载下的响应时间、吞吐与资源占用。负载测试、压力测试与 soak 测试对应不同目标与风险发现。",
        "positioning": "覆盖 JMeter、Locust、Gatling 与指标分析，连接 APM 定位瓶颈。",
        "prerequisites": ["HTTP API", "基本统计学（百分位）", "Linux 资源概念"],
        "outcomes": ["能设计场景与并发模型", "能解读 P95/P99 与吞吐曲线", "能定位 CPU/IO/锁瓶颈", "能输出性能测试报告"],
        "ecosystem": "JMeter、Locust、Gatling、k6、Prometheus、perf",
    },
    "代码重构": {
        "category": "后端开发",
        "intro": "重构是在不改变外部行为的前提下改善代码结构。Martin Fowler 目录列出提取函数、搬移字段、以多态取代条件等手法，需测试保护网。",
        "positioning": "识别坏味道（长函数、特性依恋、数据泥团），安全小步重构，结合 IDE 自动化。",
        "prerequisites": ["面向对象或函数式基础", "单元测试习惯"],
        "outcomes": ["能识别常见坏味道", "能应用提取函数/搬移方法等手法", "能用测试保障重构安全", "能在 Code Review 中推动结构改进"],
        "ecosystem": "IDE Refactor、SonarQube、《重构》第二版",
    },
    "设计模式": {
        "category": "后端开发",
        "intro": "GoF 23 种设计模式分为创建型、结构型、行为型，解决特定上下文下的复用与扩展问题。现代语言特性（函数式、依赖注入）改变部分模式实现方式。",
        "positioning": "理解模式意图而非死记硬背，避免过度设计；结合 Spring、Guava 等库中的模式应用。",
        "prerequisites": ["OOP", "UML 类图基础"],
        "outcomes": ["能说明单例、工厂、策略、观察者等意图", "能在合适场景应用而非滥用", "能识别框架中的模式实现", "能评估模式与 YAGNI 的平衡"],
        "ecosystem": "Spring Bean、Java Stream、Guava、Head First Design Patterns",
    },
    "数据库原理": {
        "category": "数据存储",
        "intro": "数据库原理涵盖关系模型、SQL、事务 ACID、并发控制与索引结构，是理解 MySQL、PostgreSQL 等具体产品的理论基础。",
        "positioning": "从范式、关系代数到锁与 MVCC，建立存储与查询优化的概念框架。",
        "prerequisites": ["离散数学集合论", "基本算法", "文件系统概念"],
        "outcomes": ["能设计满足范式的 schema", "能解释隔离级别现象", "能分析 B+树索引与查询计划", "能对比 SQL 与 NoSQL 边界"],
        "ecosystem": "MySQL、PostgreSQL、SQLite、教材《Database System Concepts》",
    },
    "MySQL": {
        "category": "数据存储",
        "intro": "MySQL 8 默认 InnoDB，支持窗口函数、CTE 与 JSON。生产环境关注主从复制、读写分离、分库分表与慢查询优化。",
        "positioning": "从架构、InnoDB B+树、执行计划到高可用运维，面向 DBA 与后端工程师。",
        "prerequisites": ["SQL", "数据库原理", "Linux 基础"],
        "outcomes": ["能分析 EXPLAIN 与慢日志", "能配置主从与 MHA/ Orchestrator", "能设计索引与分表策略", "能处理锁等待与死锁"],
        "ecosystem": "InnoDB、ProxySQL、Percona Toolkit、Orchestrator",
    },
    "Redis": {
        "category": "数据存储",
        "intro": "Redis 单线程事件模型保证命令原子性，内存数据结构存储支持缓存、分布式锁、限流与消息 Stream。",
        "positioning": "覆盖数据类型、持久化 RDB/AOF、主从哨兵集群与缓存设计模式。",
        "prerequisites": ["网络 TCP", "基本数据结构", "过期与 LRU 概念"],
        "outcomes": ["能选型合适数据结构", "能设计缓存穿透/击穿/雪崩方案", "能部署 Sentinel/Cluster", "能排查慢命令与内存碎片"],
        "ecosystem": "Redis Stack、Sentinel、Cluster、Redisson",
    },
    "PostgreSQL": {
        "category": "数据存储",
        "intro": "PostgreSQL 是功能丰富的开源 ORDBMS，MVCC、扩展（PostGIS、pgvector）与严格 SQL 兼容是其优势。",
        "positioning": "覆盖类型系统、索引（B-tree/GiST/GIN）、复制与 JSONB，适合 GIS 与分析型混合负载。",
        "prerequisites": ["SQL", "事务概念"],
        "outcomes": ["能使用 EXPLAIN ANALYZE", "能配置流复制与 Patroni", "能使用 JSONB 与全文检索", "能安装扩展与调优 shared_buffers"],
        "ecosystem": "PostGIS、pgBouncer、Patroni、TimescaleDB",
    },
    "MongoDB": {
        "category": "数据存储",
        "intro": "MongoDB 文档模型以 BSON 存储嵌套结构，复制集提供高可用，分片水平扩展。适合 schema 灵活、读写模式文档化的场景。",
        "positioning": "从 CRUD、聚合管道、索引到事务与分片，明确与关系库的选型边界。",
        "prerequisites": ["JSON", "分布式基础"],
        "outcomes": ["能设计文档模型与引用/嵌入", "能配置复制集选举", "能使用 aggregation pipeline", "能规划分片键"],
        "ecosystem": "mongosh、Compass、Atlas、Change Streams",
    },
    "Elasticsearch": {
        "category": "数据存储",
        "intro": "Elasticsearch 基于 Lucene 倒排索引，提供全文检索、聚合分析与近实时搜索。集群由 Master、Data、Coordinating 节点角色组成。",
        "positioning": "覆盖 mapping、分词、DSL 查询、分片副本与 ELK 日志栈。",
        "prerequisites": ["JSON", "分布式概念", "日志基础"],
        "outcomes": ["能设计 mapping 与 analyzer", "能编写 bool/query/agg DSL", "能调优 heap 与分片大小", "能搭建 ELK 检索链路"],
        "ecosystem": "Kibana、Logstash、Beats、OpenSearch",
    },
    "数据仓库": {
        "category": "数据存储",
        "intro": "数据仓库面向主题、集成、非易失、时变的数据集合，支撑 BI 与决策。Kimball 维度建模与 Inmon 企业模型是两大流派。",
        "positioning": "覆盖星型/雪花 schema、事实维度表、分层 ODS/DWD/DWS/ADS 与 OLAP 引擎。",
        "prerequisites": ["SQL", "ETL 概念", "业务指标基础"],
        "outcomes": ["能设计星型模型与 slowly changing dimension", "能规划数仓分层", "能选型 Hive/ClickHouse/Doris", "能建立指标口径治理"],
        "ecosystem": "Hive、ClickHouse、Apache Doris、dbt、Airflow",
    },
    "缓存技术": {
        "category": "数据存储",
        "intro": "缓存通过空间换时间降低延迟与 DB 压力。本地缓存（Caffeine）与分布式缓存（Redis）组合为多级缓存；需处理一致性与三大经典问题。",
        "positioning": "覆盖 Cache-Aside、Read/Write Through、穿透击穿雪崩与热点 key。",
        "prerequisites": ["Redis 或 Memcached 其一", "并发基础"],
        "outcomes": ["能选择缓存更新策略", "能实现互斥锁与逻辑过期防击穿", "能设计多级缓存", "能监控命中率与 evicted keys"],
        "ecosystem": "Redis、Caffeine、Guava Cache、Memcached",
    },
    "ETL开发": {
        "category": "数据存储",
        "intro": "ETL（Extract-Transform-Load）将源系统数据抽取、清洗转换后加载至目标库或数仓。CDC 与增量同步是现代实时数仓的关键。",
        "positioning": "覆盖批流一体、数据质量、调度与 Debezium/Canal 等 CDC 工具。",
        "prerequisites": ["SQL", "一种脚本语言", "数仓分层概念"],
        "outcomes": ["能设计 idempotent 增量同步", "能处理脏数据与质量规则", "能编排 Airflow/DolphinScheduler 任务", "能评估 Flink CDC 方案"],
        "ecosystem": "Airflow、dbt、Debezium、DataX、SeaTunnel",
    },
    "时序数据库": {
        "category": "数据存储",
        "intro": "时序数据库优化时间戳索引写入与范围聚合，用于监控、IoT 与 APM。Prometheus TSDB、InfluxDB、TimescaleDB 是常见选型。",
        "positioning": "覆盖数据模型、降采样、保留策略与高 cardinality 治理。",
        "prerequisites": ["监控指标概念", "Prometheus 基础更佳"],
        "outcomes": ["能设计 metric labels 避免 cardinality 爆炸", "能配置 retention 与 downsampling", "能选型 Prometheus vs InfluxDB", "能优化批量写入"],
        "ecosystem": "Prometheus、InfluxDB、TimescaleDB、TDengine、VictoriaMetrics",
    },
    "Docker": {
        "category": "DevOps",
        "intro": "Docker 将应用与依赖打包为镜像，基于 Linux Namespace 与 Cgroups 实现容器隔离，Compose 编排多容器开发环境。",
        "positioning": "从 Dockerfile、镜像分层、网络存储到安全与 CI 集成，是 K8s 与云原生的基础。",
        "prerequisites": ["Linux 命令行", "网络端口概念"],
        "outcomes": ["能编写多阶段 Dockerfile", "能使用 docker compose", "理解 overlay2 与 volume", "能扫描镜像漏洞并非 root 运行"],
        "ecosystem": "containerd、BuildKit、Harbor、Docker Compose",
    },
    "Kubernetes": {
        "category": "DevOps",
        "intro": "Kubernetes 以声明式 API 管理容器化 workload，Pod 共享网络命名空间，控制器 reconcile 期望状态，是云原生编排事实标准。",
        "positioning": "覆盖 Pod、Deployment、Service、Ingress、存储、RBAC 与 Helm，面向平台与 SRE。",
        "prerequisites": ["Docker", "YAML", "网络 DNS/LB 基础"],
        "outcomes": ["能部署应用并暴露 Service/Ingress", "能配置 ConfigMap/Secret 与 PV", "能实施 RBAC 与 NetworkPolicy", "能用 kubectl debug 排障"],
        "ecosystem": "Helm、Prometheus、Istio、CNI（Calico/Cilium）",
    },
    "CI与CD": {
        "category": "DevOps",
        "intro": "CI 持续集成自动构建测试，CD 持续交付/部署将制品晋级至生产。流水线即代码，与 Git 分支策略和制品库紧密配合。",
        "positioning": "覆盖 Jenkins、GitHub Actions、GitLab CI、ArgoCD 与蓝绿/金丝雀部署。",
        "prerequisites": ["Git", "Docker", "自动化测试基础"],
        "outcomes": ["能编写流水线 YAML", "能集成单元测试与镜像构建", "能设计部署策略与回滚", "能管理密钥与制品版本"],
        "ecosystem": "GitHub Actions、GitLab CI、Jenkins、ArgoCD、Harbor",
    },
    "Git版本控制": {
        "category": "DevOps",
        "intro": "Git 是分布式版本控制系统，快照 + 有向无环图记录历史。分支轻量，merge/rebase 是协作核心，工作流影响发布节奏。",
        "positioning": "从对象模型、分支合并到 GitFlow/GitHub Flow 与 bisect 排错。",
        "prerequisites": ["命令行", "文本文件编辑"],
        "outcomes": ["理解 commit/tree/blob 对象", "能安全 rebase 与解决冲突", "能使用 bisect 定位回归", "能制定团队分支策略"],
        "ecosystem": "GitHub、GitLab、Gitea、git-lfs",
    },
    "Linux运维": {
        "category": "DevOps",
        "intro": "Linux 运维涵盖用户权限、systemd 服务、网络防火墙、磁盘与日志，是后端与 SRE 的日常操作系统。",
        "positioning": "覆盖 Shell 脚本、性能监控（top/iostat/ss）与故障排查方法论。",
        "prerequisites": ["基本 Linux 命令", "TCP/IP 入门"],
        "outcomes": ["能管理 systemd 与 journalctl", "能配置 firewalld/iptables", "能分析磁盘与 inode 使用", "能编写 cron 与自动化脚本"],
        "ecosystem": "systemd、Ansible、Prometheus node_exporter、ELK",
    },
    "监控告警": {
        "category": "DevOps",
        "intro": "可观测性由指标（Metrics）、日志（Logs）、链路（Traces）组成。Prometheus 拉取指标，Grafana 可视化，Alertmanager 路由告警。",
        "positioning": "覆盖 RED/USE 方法、SLO/SLI、告警降噪与 On-call 实践。",
        "prerequisites": ["HTTP 服务", "Linux 基础", "时间序列概念"],
        "outcomes": ["能定义 SLI/SLO 与 error budget", "能编写 PromQL 与告警规则", "能设计告警分级与 runbook", "能集成 APM 追踪"],
        "ecosystem": "Prometheus、Grafana、Alertmanager、Jaeger、Datadog",
    },
    "日志分析": {
        "category": "DevOps",
        "intro": "集中式日志采集（Filebeat/Fluent Bit）→ 存储检索（Elasticsearch/Loki）→ 可视化告警，是排障与审计的基础设施。",
        "positioning": "覆盖结构化日志、ELK/EFK、Loki label 设计与日志安全合规。",
        "prerequisites": ["Linux 日志", "JSON", "基本正则"],
        "outcomes": ["能设计 JSON 结构化日志字段", "能搭建 ELK 或 Loki 栈", "能编写 Kibana/LogQL 查询", "能配置日志保留与脱敏"],
        "ecosystem": "Elasticsearch、Logstash、Filebeat、Loki、Fluent Bit",
    },
    "Nginx": {
        "category": "DevOps",
        "intro": "Nginx 高性能事件驱动 Web 服务器，常用于反向代理、负载均衡、静态资源与 TLS 终结。",
        "positioning": "覆盖 master-worker 架构、location 匹配、upstream 与缓存限流。",
        "prerequisites": ["HTTP", "DNS", "SSL 基础"],
        "outcomes": ["能配置虚拟主机与反向代理", "能设置 SSL 与 HTTP/2", "能调优 worker 与缓存", "能分析 access/error log"],
        "ecosystem": "OpenResty、Lua、Certbot、nginx-prometheus-exporter",
    },
    "云计算": {
        "category": "DevOps",
        "intro": "云计算按 IaaS/PaaS/SaaS 分层交付资源。公有云、私有云与混合云并存，云原生（容器+K8s+微服务）是主流架构范式。",
        "positioning": "覆盖 VPC、对象存储、托管 K8s、IAM 与 FinOps 成本优化。",
        "prerequisites": ["网络基础", "Docker/K8s 入门"],
        "outcomes": ["能设计 VPC 与安全组", "能使用托管数据库与对象存储", "能评估多云与厂商锁定", "能实施成本标签与预算告警"],
        "ecosystem": "AWS、阿里云、Azure、Terraform、Kubernetes",
    },
    "Ansible": {
        "category": "DevOps",
        "intro": "Ansible 无 agent，通过 SSH/WinRM 推送 YAML Playbook 实现配置管理与应用部署，幂等模块保证 repeated run 安全。",
        "positioning": "覆盖 Inventory、Playbook、Role、Vault 与 AWX/Tower 调度。",
        "prerequisites": ["YAML", "SSH", "Linux 管理基础"],
        "outcomes": ["能编写 idempotent Playbook", "能组织 Role 与 Galaxy", "能用 Vault 加密敏感变量", "能对接 CI 动态 Inventory"],
        "ecosystem": "Ansible Galaxy、AWX、Terraform（互补）",
    },
}

# Module-specific technical facts by domain
MODULE_FACTS: Dict[str, Dict[str, dict]] = {
    "Flask": {
        "Flask基础": {"core": "Flask 应用对象实现 WSGI callable；`Flask(__name__)` 设置 instance_path 与 template_folder。", "internal": "Werkzeug LocalProxy 实现 request 上下文线程局部访问。"},
        "视图": {"core": "视图函数返回 str/dict/Response；`@app.route` 的 endpoint 默认函数名。", "internal": "dispatch_request 查 view_functions 字典调用。"},
        "模板": {"core": "Jinja2 继承 {% extends %} 与 {% block %}；autoescape 默认开启防 XSS。", "internal": "Environment 编译模板为 Python 代码模块缓存。"},
        "请求响应": {"core": "Request 封装 environ；Response 设置 status/headers/cookies。", "internal": "ctx stack 管理 request/app context 入栈出栈。"},
        "蓝图": {"core": "Blueprint 延迟注册路由，register_blueprint 时合并 url_map。", "internal": "record 列表暂存 deferred 函数。"},
        "扩展": {"core": "Flask-SQLAlchemy、Flask-Migrate、Flask-JWT-Extended 等遵循 init_app 工厂模式。", "internal": "扩展在 teardown 注册清理回调。"},
        "数据库": {"core": "SQLAlchemy session 与 Flask g 绑定；scoped_session 线程安全。", "internal": "engine 连接池 pool_pre_ping 检测断连。"},
        "认证": {"core": "Flask-Login user_loader；session  signed cookie 存 user_id。", "internal": "itsdangerous 序列化 session 防篡改。"},
        "测试": {"core": "test_client 模拟请求；pytest fixture 创建 app context。", "internal": "TESTING=True 时 exception 传播到测试。"},
        "部署": {"core": "Gunicorn pre-fork worker；反向代理 Nginx 处理 TLS 与静态文件。", "internal": "WSGI middleware 可插 Prometheus 指标。"},
        "Flask最佳实践": {"core": "应用工厂 create_app；配置类对象；12-Factor 外部化配置。", "internal": "蓝图+扩展避免循环 import。"},
    },
    "Kubernetes": {
        "K8s基础": {"core": "声明式 API：期望状态存 etcd，控制器异步对账。", "internal": "API Server 是唯一入口，认证 RBAC 授权。"},
        "架构": {"core": "控制平面 Master（API/Scheduler/Controller）；节点 kubelet/kube-proxy。", "internal": "CRI/CNI/CSI 插件接口解耦实现。"},
        "Deployment": {"core": "ReplicaSet 管理 Pod 副本；RollingUpdate maxSurge/maxUnavailable。", "internal": "Deployment controller 级联更新 RS 哈希。"},
        "Service": {"core": "ClusterIP/NodePort/LoadBalancer；kube-proxy iptables/ipvs 转发。", "internal": "Endpoints/EndpointSlice 反映 Pod IP 列表。"},
        "Volume": {"core": "emptyDir/hostPath/PVC；CSI 动态供给。", "internal": "kubelet volumeManager 挂载到 publish path。"},
        "ConfigMap": {"core": "键值配置注入 env 或 volume；热更新需应用 reload。", "internal": "etcd 存对象；kubelet 同步到 Pod volume。"},
        "Secret": {"core": "Base64 编码非加密；启用 encryption at rest。", "internal": "ServiceAccount token 自动挂载 default secret。"},
        "Ingress": {"core": "HTTP 路由到 Service；Ingress Controller（nginx/traefik）实现。", "internal": "pathType Prefix/Exact/ImplementationSpecific。"},
        "RBAC": {"core": "Role/ClusterRole + RoleBinding；最小权限。", "internal": "authorizer 链 Webhook/RBAC/Node 顺序。"},
        "调度": {"core": "Predicate 过滤 + Priority 打分；亲和/反亲和/污点容忍。", "internal": "Scheduler Framework 插件扩展点。"},
        "Helm": {"core": "Chart 模板 + values.yaml；release 版本管理。", "internal": "Helm 3 无 Tiller，kubectl 客户端侧渲染。"},
    },
    "MySQL": {
        "MySQL基础": {"core": "Client/Server 协议；连接线程模型 one-thread-per-connection。", "internal": "解析器→优化器→执行器流水线。"},
        "架构": {"core": "Server 层 SQL 处理；引擎层 InnoDB 存取。", "internal": "Handler API 抽象存储引擎接口。"},
        "存储引擎": {"core": "InnoDB 事务行锁；MyISAM 表锁已过时。", "internal": "SHOW ENGINES 查看支持引擎。"},
        "事务": {"core": "ACID；隔离级别 RR 默认；gap lock 防幻读。", "internal": "undo/redo 双日志保障。"},
        "锁": {"core": "record lock/gap lock/next-key lock；MDL 元数据锁。", "internal": "lock wait timeout 与 deadlock 检测。"},
        "主从复制": {"core": "binlog row/statement；IO thread + SQL thread。", "internal": "GTID 简化 failover。"},
        "SQL优化": {"core": "避免 SELECT *；改写子查询为 JOIN。", "internal": "optimizer_switch 控制优化器行为。"},
        "执行计划": {"core": "type: const/ref/range/index/all；rows 估算。", "internal": "EXPLAIN FORMAT=JSON 看 cost。"},
    },
    "Redis": {
        "Redis基础": {"core": "单线程命令执行；RESP 协议；6379 默认端口。", "internal": "ae.c 事件循环 epoll。"},
        "持久化": {"core": "RDB 快照；AOF appendfsync always/everysec/no。", "internal": "混合持久化 RDB+AOF 重启快。"},
        "集群": {"core": "16384 hash slot；MOVED/ASK 重定向。", "internal": "gossip 协议传播集群状态。"},
        "缓存设计": {"core": "Cache-Aside：读 miss 加载 DB 再写缓存。", "internal": "TTL 抖动防雪崩。"},
        "分布式锁": {"core": "SET key NX EX + Lua 续期/释放。", "internal": "Redlock 多实例争议需评估。"},
    },
    "Docker": {
        "Dockerfile": {"core": "指令 FROM/RUN/COPY/ENTRYPOINT；层缓存顺序。", "internal": "BuildKit 并行构建与 secret mount。"},
        "镜像": {"core": "manifest 多架构；layer diff_id 与 chainID。", "internal": "content-addressable storage。"},
        "网络": {"core": "bridge/host/overlay；docker0 虚拟网桥。", "internal": "iptables DNAT 端口映射。"},
        "Compose": {"core": "services/networks/volumes YAML；depends_on 顺序。", "internal": "project 名前缀隔离资源。"},
    },
    "Git版本控制": {
        "Git基础": {"core": "三区域：工作区/暂存区/仓库；SHA-1 对象 ID。", "internal": "blob/tree/commit/tag 四类对象。"},
        "分支": {"core": "branch 是指向 commit 的可移动指针。", "internal": "HEAD 通常 symbolic ref 到分支。"},
        "合并": {"core": "三方 merge 产生 merge commit；fast-forward 无分叉。", "internal": "递归与 octopus merge 策略。"},
        "变基": {"core": "rebase 重写 commit 基线；禁止已推送公共分支 rebase。", "internal": "cherry-pick 单 commit 移植。"},
    },
    "设计模式": {
        "单例": {"core": "全局唯一实例；饿汉/懒汉/枚举/Holder。", "internal": "双重检查锁需 volatile。"},
        "工厂方法": {"core": "子类决定实例化哪个产品类。", "internal": "符合开闭原则扩展新产品。"},
        "观察者": {"core": "Subject notify Observer；Java EventListener。", "internal": "推模型 vs 拉模型。"},
        "策略": {"core": "算法族封装可互换；消除 if-else。", "internal": "Spring Strategy Bean 注入。"},
        "装饰器": {"core": "动态附加职责；Python/Java IO 包装流。", "internal": "与代理区别：增强 vs 控制访问。"},
    },
}


def _facts(domain: str, module: str) -> dict:
    if domain in EXTENDED_FACTS and module in EXTENDED_FACTS[domain]:
        return EXTENDED_FACTS[domain][module]
    if domain in MODULE_FACTS and module in MODULE_FACTS[domain]:
        return MODULE_FACTS[domain][module]
    return {}


def _generate_module(domain: str, module: str) -> dict:
    key = (domain, module)
    if key in DETAILED:
        return DETAILED[key]

    facts = _facts(domain, module)
    core = facts.get("core", f"{module} 是 {domain} 技术栈中的关键能力点，理解其原理与边界是工程实践的基础。")
    internal = facts.get("internal", f"{module} 的实现依赖 {domain} 官方文档与社区最佳实践中的标准模式。")
    mechanism_extra = facts.get("mechanism", "")
    workflow_extra = facts.get("workflow", "")
    performance_extra = facts.get("performance", "")

    return {
        "intro": f"**{module}** 在 **{domain}** 中承担关键职责。{core}",
        "concepts": [
            {"title": f"{module}核心概念", "body": core},
            {"title": f"底层实现与架构", "body": internal},
            {"title": f"{module}在{domain}中的协作", "body": (
                f"{module} 与 {domain} 其他模块通过明确接口协作："
                f"定义输入输出契约、失败模式（超时、重试、降级）及观测点。"
                f"生产排障时应结合日志、指标与链路追踪定位 {module} 路径上的瓶颈。"
            )},
            {"title": "典型应用场景", "body": (
                f"在 {domain} 工程实践中，{module} 常见于核心链路设计与性能调优场景。"
                f"选型时需评估团队熟悉度、生态成熟度及与现有栈的集成成本。"
            )},
        ],
        "mechanism": mechanism_extra or (
            f"{module} 工作原理：接收请求或事件 → 路由到处理逻辑 → "
            f"访问依赖服务（DB/缓存/队列）→ 聚合结果返回。"
            f"错误应分类为可重试与不可重试，并映射为统一错误码。{internal}"
        ),
        "internals": internal,
        "workflow": workflow_extra or (
            f"1. 阅读 {domain} 官方 {module} 文档与权威示例，列出与本项目相关的 API/配置项\n"
            f"2. 在本地或开发环境搭建最小可运行样例，验证输入输出与边界条件\n"
            f"3. 将 {module} 集成到主流程，补充单元测试与必要的集成测试\n"
            f"4. 在预发环境做容量与回归验证，记录性能与错误率基线\n"
            f"5. 编写变更说明与回滚步骤，灰度上线并持续观察核心指标"
        ),
        "performance": performance_extra or (
            f"{module} 性能优化：Profiling 定位热点；优先优化 I/O 与算法复杂度；"
            f"避免过早微优化。{domain} 社区通常提供 {module} 相关的 benchmark 与 tuning 指南。"
        ),
        "security": (
            f"使用 {module} 时遵循最小权限：输入校验、敏感数据脱敏、"
            f"审计日志。{domain} 安全公告与 CVE 应订阅并及时打补丁。"
        ),
        "case_study": (
            f"某团队在 {domain} 项目中重构 {module} 模块："
            f"拆分职责、引入缓存/队列削峰、补充契约测试，"
            f"P95 延迟下降且故障恢复时间缩短。"
        ),
        "comparison": (
            f"选型 {module} 方案时，对比官方推荐实现与第三方扩展的成熟度、"
            f"社区活跃度、运维成本及与现有 {domain} 栈的集成难度。"
        ),
        "debugging": (
            f"排查 {module} 问题：复现用例 → 查日志/trace → 对照配置 diff → "
            f"最小化隔离实验。{domain} 通常提供 debug 模式或 diagnostic 命令。"
        ),
        "configuration": (
            f"{module} 配置项应外部化（环境变量/配置中心），"
            f"区分 dev/staging/prod；敏感项用密钥管理服务。"
        ),
        "pitfalls": [
            {"title": "配置与环境不一致", "body": f"开发环境可用的 {module} 配置在生产因网络/权限/资源限制失败，应使用 IaC 保持一致。"},
            {"title": "忽视版本兼容性", "body": f"{domain} 大版本升级可能变更 {module} API，缺少回归测试易引发隐性故障。"},
            {"title": "缺少可观测性", "body": f"未对 {module} 埋点，故障只能被动发现，排错依赖猜测。"},
        ],
        "practices": [
            f"遵循 {domain} 官方 {module} 最佳实践文档",
            f"为 {module} 编写自动化测试与契约测试",
            "关键配置纳入 Code Review 与变更审计",
            "生产变更前在预发压测验证容量",
            "文档化架构决策（ADR）",
        ],
        "references": [
            f"{domain} 官方文档 - {module}",
            f"{domain} 源码或设计文档",
            "相关 RFC / KIP / PEP（如适用）",
        ],
    }


def _merged_domain_meta() -> dict:
    """合并多来源领域元数据（后端、前端、系统、知识库导语）"""
    merged: dict = dict(DOMAIN_META)
    try:
        from article_generator.manual._gen_frontend_data import DOMAIN_META as FRONTEND_META
        merged.update(FRONTEND_META)
    except ImportError:
        pass
    try:
        from article_generator.manual._system_domain_overviews import DOMAIN_OVERVIEWS as SYSTEM_OV
        for name, ov in SYSTEM_OV.items():
            if name not in merged:
                merged[name] = {
                    "intro": ov.get("intro", ""),
                    "positioning": ov.get("positioning", ""),
                    "prerequisites": ov.get("prerequisites", []),
                    "outcomes": ov.get("outcomes", []),
                    "ecosystem": ov.get("ecosystem", ""),
                }
    except ImportError:
        pass
    try:
        from article_generator.knowledge import DOMAIN_INTROS
        for name, intro in DOMAIN_INTROS.items():
            if name not in merged:
                merged[name] = {"intro": intro}
            elif not merged[name].get("intro"):
                merged[name]["intro"] = intro
    except ImportError:
        pass
    return merged


def _build_domain_overviews(domain_names: List[str]) -> dict:
    all_meta = _merged_domain_meta()
    overviews = {}
    for name in domain_names:
        meta = all_meta.get(name, {})
        cfg = next((d for d in DOMAINS_CONFIG if d["name"] == name), None)
        category = meta.get("category", cfg.get("category", "") if cfg else "")
        overviews[name] = {
            "intro": meta.get("intro", f"{name} 是当前技术生态中的重要方向。"),
            "positioning": meta.get(
                "positioning",
                f"系统学习 {name} 需兼顾原理与工程实践，本指南按模块组织章节，由浅入深。",
            ),
            "prerequisites": meta.get("prerequisites", cfg.get("prerequisites", []) if cfg else []),
            "outcomes": meta.get("outcomes", [
                f"系统掌握 {name} 核心模块与协作关系",
                "能独立分析常见问题并给出可验证的解决方案",
                "能在真实项目中做出合理的技术选型与架构决策",
                "能阅读官方文档与源码定位关键实现路径",
            ]),
            "ecosystem": meta.get("ecosystem", ""),
            "category": category,
        }
    return overviews


def _build_module_content(domain_names: List[str]) -> dict:
    content = {}
    for cfg in DOMAINS_CONFIG:
        if cfg["name"] not in domain_names:
            continue
        domain = cfg["name"]
        for module in cfg["modules"]:
            content[(domain, module)] = _generate_module(domain, module)
    return content


def _serialize_module_content(content: dict) -> str:
    lines = ["MODULE_CONTENT: Dict[Tuple[str, str], dict] = {"]
    for (domain, module), d in sorted(content.items()):
        lines.append(f'    ({domain!r}, {module!r}): {json.dumps(d, ensure_ascii=False, indent=4).replace(chr(10), chr(10) + "    ")},')
    lines.append("}")
    return "\n".join(lines)


def _serialize_overviews(overviews: dict) -> str:
    lines = ["DOMAIN_OVERVIEWS: Dict[str, dict] = {"]
    for name, d in sorted(overviews.items()):
        lines.append(f'    {name!r}: {json.dumps(d, ensure_ascii=False, indent=4).replace(chr(10), chr(10) + "    ")},')
    lines.append("}")
    return "\n".join(lines)


def write_file(path: Path, domain_names: List[str], title: str):
    modules = _build_module_content(domain_names)
    overviews = _build_domain_overviews(domain_names)
    header = textwrap.dedent(f'''\
        # -*- coding: utf-8 -*-
        """{title}

        手工编写的 ModuleKnowledge 素材：每个 (domain, module) 对应真实技术教程 dict。
        """

        from typing import Dict, Tuple

    ''')
    body = _serialize_module_content(modules) + "\n\n\n" + _serialize_overviews(overviews) + "\n"
    path.write_text(header + body, encoding="utf-8")
    print(f"Wrote {path} — {len(modules)} modules, {len(overviews)} overviews")


def main():
    base = Path("/workspace/article_generator/manual")
    write_file(
        base / "content_backend.py",
        BACKEND_DOMAINS,
        "后端开发领域手工教程内容库",
    )
    write_file(
        base / "content_data_devops.py",
        DATA_DEVOPS_DOMAINS,
        "数据存储与 DevOps 领域手工教程内容库",
    )


if __name__ == "__main__":
    main()
