# -*- coding: utf-8 -*-
"""Extended technical facts for all backend & data/devops modules."""

from __future__ import annotations

from typing import Dict

# domain -> module -> {core, internal, mechanism?, workflow?, performance?}
EXTENDED_FACTS: Dict[str, Dict[str, dict]] = {}

def _add(domain: str, module: str, **kwargs):
    EXTENDED_FACTS.setdefault(domain, {})[module] = kwargs


# ===== 后端架构 =====
_add("后端架构", "架构概述", core="架构是质量属性（可用性、可扩展性、安全）的结构性决策集合。", internal="C4 Model：Context/Container/Component/Code 四级抽象沟通。")
_add("后端架构", "单体架构", core="单进程/单部署单元，模块间函数调用，事务本地 ACID 简单。", internal="模块化单体是微服务前合理阶段，避免分布式过早。")
_add("后端架构", "分层架构", core="Presentation→Business→Persistence 单向依赖，防循环引用。", internal="六边形/洋葱架构将领域置于核心，适配器在外。")
_add("后端架构", "微服务架构", core="按业务能力拆分服务，独立数据库，API/事件通信。", internal="Conway 定律：组织边界影响服务边界。")
_add("后端架构", "SOA", core="ESB 中心化集成 vs 微服务去 ESB 智能端点 dumb pipe。", internal="WSDL/SOAP 重量级，REST/gRPC 更轻。")
_add("后端架构", "事件驱动", core="Event Sourcing 存事件流；CQRS 读写分离模型。", internal="Outbox 模式保证 DB 与消息双写一致。")
_add("后端架构", "CQRS", core="Command 改状态走写模型；Query 走读模型投影。", internal="EventStoreDB、Axon 等框架实现。")
_add("后端架构", "DDD", core="限界上下文、聚合根、领域事件；Ubiquitous Language。", internal="战术模式：Entity/ValueObject/Repository。")
_add("后端架构", "API设计", core="API 是架构边界契约；内外部 API 分离（BFF）。", internal="API First：OpenAPI 驱动实现与 Mock。")
_add("后端架构", "数据架构", core="每服务私有数据库；Saga 协调跨服务一致性。", internal="CDC 同步读模型；避免共享 DB 反模式。")
_add("后端架构", "缓存架构", core="多级缓存：CDN→本地→Redis；Cache-Aside 为主。", internal="一致性窗口与 TTL 业务可接受。")
_add("后端架构", "消息架构", core="异步解耦；至少一次投递 + 消费者幂等。", internal="Topic 按域划分；死信与重试队列。")
_add("后端架构", "高可用", core="冗余 + 故障转移；SLA 99.9%≈8.76h/年 downtime。", internal="Active-Active 需冲突解决；Active-Passive 简单。")
_add("后端架构", "高并发", core="水平扩展无状态服务；异步化削峰。", internal="Little 定律：L=λW；队列缓冲平滑流量。")
_add("后端架构", "可扩展", core="Scale up vs scale out；分片与分区扩展数据层。", internal="AKF 扩展立方：X/Y/Z 轴。")
_add("后端架构", "安全架构", core="零信任：永不信任始终验证；纵深防御。", internal="STRIDE 威胁建模；OAuth2/mTLS 服务间。")
_add("后端架构", "后端架构最佳实践", core="演进式架构 + ADR 记录决策；可逆决策优先。", internal="Well-Architected 六大支柱对照评审。")

# ===== RESTful API =====
_add("RESTful API", "REST概述", core="Roy Fielding 论文：资源、表述、统一接口、无状态、可缓存。", internal="Richardson 成熟度模型 Level 0–3。")
_add("RESTful API", "资源建模", core="名词复数 URI：/orders/{id}/items；避免动词路径。", internal="资源 vs 子资源 vs 控制器资源权衡。")
_add("RESTful API", "HTTP方法", core="GET 安全幂等；POST 创建；PUT 全量替换；PATCH 部分更新；DELETE 删除。", internal="405 Method Not Allowed 正确返回 Allow 头。")
_add("RESTful API", "状态码", core="2xx 成功；4xx 客户端错；5xx 服务端错；429 限流。", internal="Problem Details RFC 7807 统一错误体。")
_add("RESTful API", "URI设计", core="小写连字符；版本 /v1 或 Accept 头；过滤 ?status=active。", internal="HATEOAS _links  hypermedia 导航。")
_add("RESTful API", "请求与响应", core="Content-Type application/json；压缩 gzip/br。", internal="Idempotency-Key 头防 POST 重复提交。")
_add("RESTful API", "版本控制", core="URI 版本直观；Header Accept-Version 解耦 URL。", internal="弃用策略：Sunset 头 + 文档公告期。")
_add("RESTful API", "认证授权", core="Bearer JWT 或 OAuth2；API Key 用于 B2B。", internal="Scope 粒度授权；mTLS 高安全场景。")
_add("RESTful API", "分页", core="cursor 优于 offset 深分页；Link rel=next/prev。", internal="keyset pagination 用 (created_at,id) 元组。")
_add("RESTful API", "过滤排序", core="?sort=-created_at&filter[status]=paid 或 RSQL。", internal="白名单字段防 SQL/NoSQL 注入。")
_add("RESTful API", "错误处理", core="{code, message, details[], trace_id} 结构。", internal="4xx 不 retry；5xx 指数退避 retry。")
_add("RESTful API", "API文档", core="OpenAPI 3.1 单源真相；Swagger UI/Redoc 渲染。", internal="contract-first 生成 server stub 与 client SDK。")
_add("RESTful API", "API测试", core="Postman/Newman；Pact 消费者驱动契约。", internal="Schemathesis 基于 OpenAPI fuzz。")
_add("RESTful API", "性能优化", core="ETag/If-None-Match 304；字段 sparse fieldsets。", internal="HTTP/2 多路复用减连接数。")
_add("RESTful API", "安全", core="Rate limit；CORS 最小 origin；输入校验。", internal="OWASP API Security Top 10。")
_add("RESTful API", "HATEOAS", core="响应含 _links：self、next、related。", internal="HAL/JSON-LD/Siren 超媒体格式。")
_add("RESTful API", "REST最佳实践", core="幂等 PUT/DELETE；POST 创建返回 201 Location。", internal="Google API Design Guide 对齐。")

# ===== 微服务架构 =====
_add("微服务架构", "微服务概述", core="Sam Newman：小、自治、围绕业务能力、独立部署。", internal="分布式单体：拆分过细通信开销大于收益。")
_add("微服务架构", "服务拆分", core="按 DDD 限界上下文；数据所有权随服务走。", internal="绞杀者模式逐步从单体迁移。")
_add("微服务架构", "服务通信", core="同步 REST/gRPC；异步 Kafka/RabbitMQ。", internal="gRPC HTTP/2 + Protobuf 高性能。")
_add("微服务架构", "服务发现", core="Consul/Eureka/Nacos 注册与健康检查。", internal="客户端发现 vs 服务端发现（LB）。")
_add("微服务架构", "API网关", core="路由、鉴权、限流、聚合 BFF。", internal="Kong/Spring Cloud Gateway/Envoy。")
_add("微服务架构", "配置中心", core="Nacos/Apollo 动态配置 + 灰度。", internal="12-Factor 配置与代码分离。")
_add("微服务架构", "服务熔断", core="Hystrix/Resilience4j：失败率阈值打开熔断。", internal="半开状态试探恢复。")
_add("微服务架构", "服务降级", core="返回默认值或缓存；非核心功能关闭。", internal="舱壁隔离线程池。")
_add("微服务架构", "限流", core="令牌桶/漏桶；Sentinel 热点参数限流。", internal="分布式限流 Redis+Lua。")
_add("微服务架构", "分布式事务", core="2PC 强一致代价高；Saga 补偿；TCC Try-Confirm-Cancel。", internal="Seata AT/TCC/Saga 模式。")
_add("微服务架构", "链路追踪", core="OpenTelemetry trace_id 贯穿；Span 父子关系。", internal="Jaeger/Zipkin 可视化调用链。")
_add("微服务架构", "日志聚合", core="JSON 结构化 + trace_id；ELK/Loki 集中检索。", internal="Fluent Bit DaemonSet 采集。")
_add("微服务架构", "监控告警", core="RED：Rate Errors Duration；SLI/SLO。", internal="Micrometer + Prometheus。")
_add("微服务架构", "容器化部署", core="镜像 immutable；K8s Deployment 滚动更新。", internal="Helm Chart 参数化多环境。")
_add("微服务架构", "服务网格", core="Istio sidecar 流量管理 mTLS。", internal="数据面 Envoy；控制面 istiod。")
_add("微服务架构", "微服务测试", core="测试金字塔 + 契约测试 + 测试容器。", internal="Testcontainers 集成真实依赖。")
_add("微服务架构", "微服务最佳实践", core="可观测性三件套；混沌工程验证韧性。", internal="Google SRE 错误预算文化。")

# ===== Spring Boot =====
_add("Spring Boot", "Spring Boot基础", core="@SpringBootApplication = @Configuration + @EnableAutoConfiguration + @ComponentScan。", internal="SpringApplication.run 启动内嵌 Tomcat。")
_add("Spring Boot", "Starter", core="spring-boot-starter-web 传递依赖 BOM 对齐版本。", internal="spring-boot-dependencies 管理版本。")
_add("Spring Boot", "Web开发", core="@RestController + @GetMapping；HttpMessageConverter JSON。", internal="DispatcherServlet HandlerMapping 链。")
_add("Spring Boot", "数据访问", core="Spring Data JPA Repository；@Transactional 代理。", internal="Hibernate Session 一级缓存。")
_add("Spring Boot", "安全", core="Spring Security FilterChain；BCrypt 密码。", internal="SecurityContextHolder ThreadLocal。")
_add("Spring Boot", "缓存", core="@Cacheable/@CacheEvict；Redis/Caffeine。", internal="AOP 代理拦截缓存逻辑。")
_add("Spring Boot", "消息", core="Spring AMQP/Kafka Template；@KafkaListener。", internal="消息转换器 MessageConverter。")
_add("Spring Boot", "任务调度", core="@Scheduled cron；Quartz 集群。", internal="TaskScheduler 线程池配置。")
_add("Spring Boot", "监控", core="Actuator /health /metrics；Micrometer registry。", internal="HealthIndicator 自定义探针。")
_add("Spring Boot", "测试", core="@SpringBootTest @MockBean Slice 测试。", internal="TestRestTemplate 集成测试。")
_add("Spring Boot", "配置管理", core="application.yml profile；@ConfigurationProperties。", internal="Environment 属性源优先级。")
_add("Spring Boot", "日志", core="Logback/log4j2；MDC traceId。", internal="logging.level 包级动态调整。")
_add("Spring Boot", "性能优化", core="连接池 HikariCP；lazy-init 慎用。", internal="JVM GC 调优 G1/ZGC。")
_add("Spring Boot", "部署", core="jar 内嵌容器；Docker 多阶段构建。", internal="Spring Boot 3 原生镜像 GraalVM。")
_add("Spring Boot", "Spring Cloud", core="Nacos 注册；OpenFeign 声明式 HTTP；Gateway。", internal="LoadBalancerClient 客户端 LB。")
_add("Spring Boot", "Spring Boot最佳实践", core="分层 controller/service/repository；DTO 隔离实体。", internal="ProblemDetail RFC 7807 异常。")

# ===== 认证授权 =====
_add("认证授权", "认证概述", core="Something you know/have/are 三因素。", internal="认证 ≠ 授权；先身份后权限。")
_add("认证授权", "Session", core="服务端存 session_id；Cookie HttpOnly Secure SameSite。", internal="Redis 集中 session 支持水平扩展。")
_add("认证授权", "Cookie", core="Set-Cookie 属性控制生命周期与作用域。", internal="JWT 存 Cookie 防 XSS 需 CSRF 防护。")
_add("认证授权", "OAuth2", core="授权码 flow：redirect→code→token。", internal="PKCE 防公共客户端 code 拦截。")
_add("认证授权", "OpenID Connect", core="ID Token JWT 含 sub；UserInfo endpoint。", internal="OIDC Discovery .well-known/openid-configuration。")
_add("认证授权", "SSO单点登录", core="CAS/SAML/OIDC 中央 IdP；SP 信任断言。", internal="Ticket-granting cookie 域共享。")
_add("认证授权", "RBAC", core="User→Role→Permission；Spring @PreAuthorize。", internal="角色继承与权限聚合。")
_add("认证授权", "ABAC", core="属性策略 XACML；细粒度数据行级。", internal="OPA Rego 策略即代码。")
_add("认证授权", "多因素认证", core="TOTP RFC 6238；WebAuthn/FIDO2 无密码。", internal="备份码与设备信任策略。")
_add("认证授权", "密码安全", core="Argon2id/bcrypt 慢哈希；盐唯一。", internal="Have I Been Pwned 泄露检测。")
_add("认证授权", "Token管理", core="Refresh rotation；revocation list。", internal="Opaque token introspection endpoint。")
_add("认证授权", "API安全", core="Scope 限制；mTLS 客户端证书。", internal="API Gateway 统一鉴权。")
_add("认证授权", "权限设计", core="最小权限；数据权限与功能权限分离。", internal="Casbin 模型 PERMISSION 引擎。")
_add("认证授权", "认证授权最佳实践", core="零信任持续验证；审计登录失败。", internal="OWASP ASVS 认证章节。")

# ===== API设计 =====
_add("API设计", "API设计原则", core="一致性、可预测、向后兼容、开发者体验。", internal="Postel 法则：严出宽进。")
_add("API设计", "REST设计", core="见 RESTful API 领域；资源导向。", internal="Microsoft REST API Guidelines。")
_add("API设计", "GraphQL设计", core="Schema 优先；Mutation 命名动词。", internal="Relay 全局 ID 与连接规范。")
_add("API设计", "RPC设计", core="gRPC service/rpc/message Protobuf。", internal="Streaming：unary/server/client/bidi。")
_add("API设计", "API版本", core="SemVer；breaking change 升 major。", internal="Deprecation policy 6–12 月。")
_add("API设计", "API文档", core="OpenAPI/AsyncAPI/GraphQL SDL。", internal="Redocly lint 规范检查。")
_add("API设计", "API测试", core="Dredd/Schemathesis 契约验证。", internal="Consumer-driven Pact。")
_add("API设计", "API网关", core="南北向流量入口；插件化扩展。", internal="Kong plugin chain。")
_add("API设计", "API安全", core="OAuth2 + scope；输入 schema 校验。", internal="GraphQL depth limit。")
_add("API设计", "API性能", core="分页、压缩、CDN 缓存 GET。", internal="GraphQL DataLoader N+1。")
_add("API设计", "API生命周期", core="Design→Build→Deploy→Deprecate→Retire。", internal="API catalog 治理。")
_add("API设计", "API治理", core="Lint、Review、Breaking change 检测。", internal="Backstage API plugin。")
_add("API设计", "API市场", core="开发者门户；API key 自助申请。", internal="Monetization 计量计费。")
_add("API设计", "API设计模式", core="Pagination、Bulk、Webhook 回调。", internal="Long polling vs SSE vs WebSocket。")
_add("API设计", "API最佳实践", core="Error model 统一；Request ID 贯穿。", internal="Stripe API 设计标杆。")

# ===== Serverless =====
_add("Serverless", "Serverless概述", core="FaaS + BaaS；按调用计费；无服务器非无运维。", internal="CNCF Serverless WG 定义。")
_add("Serverless", "函数计算", core="事件触发 handler；stateless 短生命周期。", internal="Lambda execution context 复用。")
_add("Serverless", "事件驱动", core="S3/Queue/HTTP 触发器映射函数。", internal="EventBridge 事件总线路由。")
_add("Serverless", "AWS Lambda", core="handler(event, context)；128MB–10GB；15min 上限。", internal="/tmp 512MB–10GB 临时存储。")
_add("Serverless", "阿里云函数计算", core="HTTP 触发器；NAS 挂载；GPU 实例。", internal="镜像函数自定义运行时。")
_add("Serverless", "API网关", core="Lambda + API Gateway REST/HTTP API。", internal="JWT authorizer 边缘鉴权。")
_add("Serverless", "无服务器架构", core="Step Functions 编排；DynamoDB 状态。", internal="Choreography vs Orchestration。")
_add("Serverless", "冷启动", core="Init duration：下载代码→启动 runtime→init 代码。", internal="Provisioned concurrency；SnapStart Java。")
_add("Serverless", "状态管理", core="外部化 DynamoDB/S3；函数内存不持久。", internal="Durable Functions 编排状态。")
_add("Serverless", "调试", core="SAM local invoke；CloudWatch Logs Insights。", internal="X-Ray 分布式追踪。")
_add("Serverless", "部署", core="IaC SAM/Serverless Framework；蓝绿 alias。", internal="Lambda layers 共享依赖。")
_add("Serverless", "成本优化", core="ARM Graviton；内存与 duration 权衡。", internal="CloudWatch 成本异常告警。")
_add("Serverless", "安全", core="IAM 最小权限；VPC 访问私有资源。", internal="Secrets Manager 注入环境变量。")
_add("Serverless", "性能", core="连接池复用 RDS Proxy；包体积 <50MB。", internal="Global accelerator 边缘。")
_add("Serverless", "Serverless最佳实践", core="幂等 handler；DLQ 失败消息。", internal="Well-Architected Serverless Lens。")

# ===== GraphQL =====
_add("GraphQL", "GraphQL概述", core="单一 endpoint POST；客户端声明字段集。", internal="Facebook 2012 内部；2015 开源。")
_add("GraphQL", "Query", core="读操作；并行解析无依赖字段。", internal="GraphQL query 只是 schema 子集。")
_add("GraphQL", "Mutation", core="写操作；顺序执行非并行。", internal="payload + clientMutationId。")
_add("GraphQL", "Subscription", core="WebSocket graphql-ws 协议推送。", internal="Redis pub/sub 多实例广播。")
_add("GraphQL", "Resolver", core="(parent,args,ctx,info)=>；默认读 parent[field]。", internal="info.fieldNodes 优化查询。")
_add("GraphQL", "类型系统", core="Scalar/Object/Interface/Union/Enum/Input。", internal="Interface 实现类型 introspection。")
_add("GraphQL", "指令", core="@deprecated @include(if:) @skip(if:)。", internal="自定义 directive 扩展。")
_add("GraphQL", "缓存", core="APQ Automatic Persisted Queries；CDN GET。", internal="Entity cache normalized Apollo。")
_add("GraphQL", "性能优化", core="DataLoader batch+cache；查询复杂度限制。", internal="Query cost analysis。")
_add("GraphQL", "安全", core="深度/广度限制；禁用 introspection 生产。", internal="Persisted query whitelist。")
_add("GraphQL", "工具链", core="GraphiQL/GraphQL Playground；codegen。", internal="graphql-eslint schema lint。")
_add("GraphQL", "Apollo", core="Apollo Server/Router；Federation 子图。", internal="@key @extends 实体扩展。")
_add("GraphQL", "GraphQL最佳实践", core="Mutation 设计粗粒度；错误 extensions 码。", internal="GraphQL over HTTP spec。")

# ===== WebSocket =====
_add("WebSocket", "WebSocket概述", core="RFC 6455；ws/wss；全双工持久连接。", internal="对比 SSE 单向；对比长轮询开销。")
_add("WebSocket", "握手协议", core="GET Upgrade: websocket；Sec-WebSocket-Key Accept 计算。", internal="101 Switching Protocols。")
_add("WebSocket", "数据帧", core="Opcode text/binary/ping/pong/close；mask 客户端→服务端。", internal="分片消息 FIN 位。")
_add("WebSocket", "服务端实现", core="Spring @ServerEndpoint；Node ws 库。", internal="事件 loop 单线程注意 blocking。")
_add("WebSocket", "客户端实现", core="new WebSocket(url)；onmessage/onclose。", internal="浏览器自动 mask；重连需自实现。")
_add("WebSocket", "心跳检测", core="ping/pong 或应用层 heartbeat JSON。", internal="proxy 空闲超时需小于心跳间隔。")
_add("WebSocket", "断线重连", core="指数退避；resume token 恢复会话。", internal="Last-Event-ID 类似 session。")
_add("WebSocket", "房间管理", core="join/leave room；broadcast to room。", internal="Redis adapter 跨节点广播。")
_add("WebSocket", "广播", core="fan-out 所有连接；房间隔离。", internal="背压：慢客户端 drop 或 queue。")
_add("WebSocket", "性能优化", core="二进制 Protobuf；消息批处理。", internal="连接数受 ulimit 与内存限制。")
_add("WebSocket", "安全", core="wss TLS；Origin 校验；auth 首帧 token。", internal="Rate limit 防 flood。")
_add("WebSocket", "负载均衡", core="Sticky session；IP hash。", internal="Redis pub/sub 无 sticky 方案。")
_add("WebSocket", "WebSocket最佳实践", core="心跳+重连+幂等消息 ID。", internal="Socket.IO fallback polling。")

# ===== 消息队列 =====
_add("消息队列", "消息队列概述", core="异步通信；削峰填谷；最终一致。", internal="Queue vs Pub/Sub 模型。")
_add("消息队列", "JMS", core="Java Message Service；Point-to-Point vs Pub/Sub。", internal="ActiveMQ Artemis 实现。")
_add("消息队列", "AMQP", core="RabbitMQ 协议；Exchange 路由键绑定 Queue。", internal="direct/topic/fanout/headers exchange。")
_add("消息队列", "RabbitMQ", core="Erlang 实现；ack/nack；prefetch QoS。", internal="镜像队列高可用。")
_add("消息队列", "RocketMQ", core="NameServer；事务消息 half message。", internal="顺序消息单队列单 consumer。")
_add("消息队列", "Pulsar", core="BookKeeper 存消息；tenant/namespace 多租。", internal="分层存算分离。")
_add("消息队列", "消息模型", core="点对点竞争消费；发布订阅广播。", internal="Consumer Group Kafka 模式。")
_add("消息队列", "消息可靠性", core="生产者 ack；持久化；消费者 manual ack。", internal="at-most-once/at-least-once/exactly-once。")
_add("消息队列", "消息顺序", core="单 partition 全局序；key 同实体同 partition。", internal="RocketMQ 顺序消费 lock。")
_add("消息队列", "消息事务", core="本地事务 + 消息；RocketMQ 事务回查。", internal="Outbox pattern 替代。")
_add("消息队列", "死信队列", core="DLQ 存放多次失败消息人工处理。", internal="TTL + DLX RabbitMQ。")
_add("消息队列", "延迟队列", core="RocketMQ delay level；RabbitMQ TTL+DLX。", internal="Redis ZSET 定时 score。")
_add("消息队列", "性能优化", core="批量发送；压缩；partition 并行。", internal="零拷贝 Kafka sendfile。")
_add("消息队列", "最佳实践", core="幂等 consumer；监控 lag；消息 schema 演进。", internal="CloudEvents 标准 envelope。")

# ===== Django =====
_add("Django", "Django基础", core="django-admin startproject；settings.py 配置中心。", internal="WSGI/ASGI 双入口。")
_add("Django", "MTV架构", core="Model-Template-View；ORM 即 Model 层。", internal="对比 MVC Controller≈View。")
_add("Django", "URL路由", core="urls.py path() re_path()；include() 嵌套。", internal="URLResolver 递归匹配。")
_add("Django", "视图", core="FBV/CBV；View 类 as_view()。", internal="dispatch 分派 http method。")
_add("Django", "模板", core="Django Template Language；{% csrf_token %}。", internal="模板继承 block/extends。")
_add("Django", "ORM", core="QuerySet lazy evaluation；filter/exclude/annotate。", internal="SQL 编译器 Query 类。")
_add("Django", "表单", core="Form/ModelForm validation；CSRF middleware。", internal="clean_<field> 钩子。")
_add("Django", "认证", core="User 模型；authenticate/login；Permission。", internal="AUTH_USER_MODEL 自定义用户。")
_add("Django", "Admin", core="ModelAdmin 注册；list_display/actions。", internal="autodiscover admin modules。")
_add("Django", "中间件", core="请求/响应处理链；SecurityMiddleware。", internal="MiddlewareMixin process_request。")
_add("Django", "缓存", core="cache framework；Redis/Memcached backend。", internal="cache_page 装饰器。")
_add("Django", "信号", core="post_save/pre_delete；receiver 装饰器。", internal="弱引用防内存泄漏。")
_add("Django", "REST Framework", core="Serializer/ViewSet/Router；Browsable API。", internal="Authentication/Permission 类。")
_add("Django", "性能优化", core="select_related/prefetch_related；only/defer。", internal="database connection pooling。")
_add("Django", "Django最佳实践", core="settings split；custom management commands。", internal="12-factor django-environ。")

# ===== 自动化测试 =====
_add("自动化测试", "测试概述", core="测试金字塔：单元>集成>E2E；Shift-left。", internal="TDD 红绿重构循环。")
_add("自动化测试", "单元测试", core="隔离依赖；fast feedback；AAA 模式。", internal="测试替身：stub/mock/fake/spy。")
_add("自动化测试", "集成测试", core="真实 DB/HTTP；Testcontainers。", internal="@SpringBootTest @DataJpaTest slice。")
_add("自动化测试", "端到端测试", core="模拟用户路径；慢且脆。", internal="Page Object 模式。")
_add("自动化测试", "Jest", core="JavaScript expect/mock；snapshot testing。", internal="jsdom 模拟 DOM。")
_add("自动化测试", "Pytest", core="fixture conftest；parametrize；assert 重写。", internal="plugin 生态 pytest-cov。")
_add("自动化测试", "JUnit", core="JUnit 5 @Test @BeforeEach；AssertJ。", internal="Extension Model 扩展。")
_add("自动化测试", "Selenium", core="WebDriver 协议；元素定位 CSS/XPath。", internal="Grid 分布式浏览器。")
_add("自动化测试", "Cypress", core="同域注入；time travel debug。", internal="不支持多 tab。")
_add("自动化测试", "Playwright", core="auto-wait；多浏览器 Chromium/Firefox/WebKit。", internal="trace viewer 录屏。")
_add("自动化测试", "Mock", core="Mockito when/then；unittest.mock patch。", internal="verify interaction 次数。")
_add("自动化测试", "测试覆盖率", core="行/分支覆盖；80% 非目标覆盖质量。", internal="JaCoCo istanbul coverage。")
_add("自动化测试", "CI测试", core="PR 门禁；并行 shard；flaky 检测。", internal="test quarantine 隔离不稳定。")
_add("自动化测试", "测试策略", core="风险驱动；关键路径 E2E。", internal="Testing Trophy Kent C. Dodds。")
_add("自动化测试", "自动化测试最佳实践", core="测试独立；数据 factory；不依赖顺序。", internal="Mutation testing 有效性。")

# ===== 性能测试 =====
_add("性能测试", "性能测试概述", core="负载/压力/浸泡/ spike 测试类型。", internal="非功能需求 NFR 验证。")
_add("性能测试", "负载测试", core="预期负载下验证 SLA。", internal="逐步 ramp-up 虚拟用户。")
_add("性能测试", "压力测试", core="超负载找 breaking point。", internal="观察恢复能力。")
_add("性能测试", "并发测试", core="多用户同时操作同一资源。", internal="race condition 暴露。")
_add("性能测试", "JMeter", core="Thread Group；HTTP Sampler；监听器。", internal="Groovy BeanShell 脚本。")
_add("性能测试", "Locust", core="Python 定义 User task；分布式 master-worker。", internal="gevent 协程模拟用户。")
_add("性能测试", "Gatling", core="Scala DSL；高性能异步。", internal="HTML 报告详实。")
_add("性能测试", "性能指标", core="RT 响应时间；TPS/QPS；并发数；错误率。", internal="P50/P95/P99 百分位。")
_add("性能测试", "性能分析", core="APM flame graph；瓶颈 CPU/IO/GC。", internal="Little 定律验证。")
_add("性能测试", "性能调优", core="缓存/索引/连接池/异步。", internal="调优验证对比 baseline。")
_add("性能测试", "瓶颈定位", core="USE 法：Utilization Saturation Errors。", internal="off-CPU profiling。")
_add("性能测试", "性能测试最佳实践", core="生产-like 环境；隔离依赖；监控关联。", internal="Coordinated omission 避免。")

# ===== 代码重构 =====
_add("代码重构", "重构概述", core="Martin Fowler：不改变行为改善结构。", internal="小步提交 + 测试保护。")
_add("代码重构", "坏味道识别", core="长函数、大类、重复、发散式变化。", internal="Feature Envy 特性依恋。")
_add("代码重构", "提取函数", core="Extract Method 命名表达意图。", internal="IDE 自动处理作用域。")
_add("代码重构", "内联函数", core="Inline Method 过度拆分时合并。", internal="权衡可读性与 indirection。")
_add("代码重构", "提取变量", core="Extract Variable 解释复杂表达式。", internal="Replace Temp with Query。")
_add("代码重构", "重命名", core="Rename Symbol 全项目一致。", internal="Ubiquitous Language 对齐。")
_add("代码重构", "移动函数", core="Move Method 到更合适类。", internal="Move Field 数据随行为走。")
_add("代码重构", "数据重组", core="Encapsulate Field；Replace Data Value。", internal="Split Temporary Variable。")
_add("代码重构", "条件逻辑简化", core="Decompose Conditional；Guard Clause。", internal="Replace Nested Conditional with Guard Clauses。")
_add("代码重构", "多态替换条件", core="Replace Conditional with Polymorphism。", internal="Strategy/State 模式。")
_add("代码重构", "重构模式", core="Branch by Abstraction；Parallel Change。", internal="Strangler Fig 渐进替换。")
_add("代码重构", "安全重构", core="Characterization test 锁定行为。", internal="Approval testing 快照。")
_add("代码重构", "重构工具", core="IDE Refactor；SonarLint 提示。", internal="OpenRewrite 大规模迁移。")
_add("代码重构", "重构最佳实践", core="Boy Scout Rule；重构与功能分离 PR。", internal="Technical debt quadrant。")

# ===== 设计模式 ===== (all modules)
for m, core, internal in [
    ("设计模式概述", "GoF 23 种；面向接口编程；组合优于继承。", "模式是沟通词汇非银弹。"),
    ("创建型模式", "封装对象创建；隐藏 new 细节。", "工厂与建造者分离构造与表示。"),
    ("结构型模式", "类/对象组合形成更大结构。", "Decorator vs Proxy 意图不同。"),
    ("行为型模式", "对象协作与职责分配。", "Observer/Mediator 解耦发送接收。"),
    ("抽象工厂", "产品族创建；换整套实现。", "UI Windows/Mac factory。"),
    ("建造者", "分步构建复杂对象；Director 可选。", "StringBuilder/Lombok @Builder。"),
    ("原型", "clone 复制；Java Cloneable。", "深拷贝 vs 浅拷贝。"),
    ("适配器", "类适配器继承 vs 对象适配器组合。", "InputStreamReader 适配字节流。"),
    ("代理", "静态/动态代理 JDK/CGLIB。", "Spring AOP 方法拦截。"),
    ("外观", "Facade 简化子系统接口。", "SLF4J 日志门面。"),
    ("桥接", "抽象与实现分离维度。", "JDBC Driver 桥接。"),
    ("组合", "树形结构统一 Leaf/Composite。", "文件系统目录文件。"),
    ("享元", "共享内在状态 extrinsic 外部传入。", "String intern；线程池。"),
    ("命令", "请求对象化；undo/redo。", "Runnable 命令模式。"),
    ("迭代器", "foreach 隐藏聚合遍历。", "Java Iterator fail-fast。"),
    ("模板方法", "骨架固定步骤子类重写。", "HttpServlet doGet/doPost。"),
    ("状态", "State 对象替代条件分支。", "TCP 连接状态机。"),
    ("访问者", "双分派添加操作而不改类。", "Compiler AST Visitor。"),
    ("中介者", "Mediator 集中交互减耦合。", "MVC Controller 中介。"),
    ("备忘录", "Memento 保存恢复状态。", "Git stash 快照。"),
    ("解释器", "语法树解释；DSL 简单语法。", "正则引擎；SQL parser。"),
    ("责任链", "Chain 传递请求直到处理。", "Servlet Filter 链；Netty pipeline。"),
    ("设计模式最佳实践", "YAGNI；先简单后模式；模式组合。", "Head First 理解意图。"),
]:
    _add("设计模式", m, core=core, internal=internal)

# ===== 数据库原理 =====
_add("数据库原理", "数据库概述", core="DBMS 管理数据持久化与并发；关系 vs 非关系。", internal="ANSI SPARC 三级模式。")
_add("数据库原理", "关系模型", core="关系=表；元组=行；属性=列；域=类型。", internal="Codd 12 规则。")
_add("数据库原理", "SQL", core="DDL/DML/DCL/TCL；声明式查询。", internal="SQL-92/99/2003 标准演进。")
_add("数据库原理", "关系代数", core="选择σ 投影π 连接⋈ 并∪ 差−。", internal="优化器代数等价变换。")
_add("数据库原理", "范式", core="1NF 原子；2NF 消除部分依赖；3NF 消除传递依赖；BCNF。", internal="反范式换查询性能。")
_add("数据库原理", "事务ACID", core="Atomicity Consistency Isolation Durability。", internal="ACID vs BASE 分布式。")
_add("数据库原理", "并发控制", core="乐观 MVCC vs 悲观锁。", internal="两阶段锁 2PL。")
_add("数据库原理", "锁机制", core="共享锁 S / 排他锁 X；意向锁。", internal="死锁检测 wait-for graph。")
_add("数据库原理", "索引", core="B+树、Hash、Bitmap 索引类型。", internal="聚簇 vs 非聚簇。")
_add("数据库原理", "查询优化", core="逻辑优化+物理优化；cost-based。", internal="动态规划 join order。")
_add("数据库原理", "存储引擎", core="页式存储；buffer pool；WAL。", internal="LSM vs B+Tree。")
_add("数据库原理", "日志", core="redo undo binlog 三种日志角色。", internal="WAL write-ahead logging。")
_add("数据库原理", "备份恢复", core="物理备份 vs 逻辑备份；PITR。", internal="RPO RTO 目标。")
_add("数据库原理", "分布式数据库", core="CAP；Paxos/Raft 共识。", internal="Spanner TrueTime。")
_add("数据库原理", "NoSQL", core="KV/Document/Column/Graph 四类。", internal="最终一致与可调一致。")
_add("数据库原理", "NewSQL", core="分布式 SQL；TiDB/CockroachDB。", internal="存算分离架构。")
_add("数据库原理", "数据库最佳实践", core="规范命名；迁移脚本；least privilege。", internal="慢查询治理流程。")

# ===== MySQL (extend) =====
_add("MySQL", "MyISAM", core="表锁；非事务；MYI/MYD 文件。", internal="crash 易损坏需 repair。")
_add("MySQL", "读写分离", core="ProxySQL 路由；读从写主。", internal="主从延迟读己之写问题。")
_add("MySQL", "分库分表", core="垂直拆库水平拆表；ShardingSphere。", internal="全局 ID 雪花/号段。")
_add("MySQL", "高可用", core="MHA/Orchestrator failover；Group Replication。", internal="半同步 replication。")
_add("MySQL", "备份恢复", core="mysqldump vs xtrabackup 热备。", internal="binlog position 恢复点。")
_add("MySQL", "性能调优", core="innodb_buffer_pool；慢日志 long_query_time。", internal="sys schema 诊断视图。")
_add("MySQL", "监控", core="Performance Schema；Exporter Prometheus。", internal="SHOW GLOBAL STATUS。")
_add("MySQL", "安全", core="最小权限账号；SSL 连接；audit plugin。", internal="sql_mode STRICT。")
_add("MySQL", "MySQL最佳实践", core="utf8mb4；DECIMAL 金额；禁止 SELECT *。", internal="Online DDL pt-osc。")

# ===== Redis (extend) =====
_add("Redis", "String", core="SET GET INCR；bitmap 位操作。", internal="embstr 44B 以下内嵌。")
_add("Redis", "Hash", core="HSET HGET 字段映射；适合对象。", internal="ziplist 编码小 hash。")
_add("Redis", "List", core="LPUSH RPOP 队列；BLPOP 阻塞。", internal="quicklist 节点 ziplist。")
_add("Redis", "Set", core="SADD SISMEMBER 去重集合。", internal="intset 整数集合编码。")
_add("Redis", "ZSet", core="ZADD score 排序；ZRANGE 范围。", internal="skiplist + dict 双结构。")
_add("Redis", "Bitmap", core="SETBIT GETBIT BITCOUNT；签到。", internal="String 底层位数组。")
_add("Redis", "HyperLogLog", core="PFADD PFCOUNT 基数估计；误差 0.81%。", internal="16384 桶 harmonic mean。")
_add("Redis", "Geo", core="GEOADD GEORADIUS 地理位置；Geohash。", internal="ZSet 编码 score 为 Geohash。")
_add("Redis", "Stream", core="XADD XREADGROUP 消费者组；ACK。", internal="radix tree 存消息 ID。")
_add("Redis", "主从复制", core="REPLICAOF；全量 RDB + 增量 buffer。", internal="PSYNC 部分重同步。")
_add("Redis", "哨兵", core="Sentinel 监控 master 自动 failover。", internal="Raft-like 选举 quorum。")
_add("Redis", "限流", core="滑动窗口 ZSET+Lua；令牌桶。", internal="Redis Cell 模块。")
_add("Redis", "性能优化", core="pipeline 批量；避免 big key。", internal="memory fragmentation active defrag。")
_add("Redis", "Redis最佳实践", core="键名规范；TTL 必设；maxmemory-policy。", internal="hot key 本地缓存。")

# ===== PostgreSQL =====
for m, core, internal in [
    ("PostgreSQL基础", "对象关系型；schema 命名空间；扩展丰富。", "initdb 集群 data directory。"),
    ("架构", "Postmaster 主进程；backend 每连接一进程。", "Shared Buffer 全局缓存。"),
    ("数据类型", "JSONB GIS UUID array；domain 自定义。", "TOAST 大行外存。"),
    ("索引", "B-tree Hash GiST GIN BRIN。", "部分索引 WHERE 条件。"),
    ("查询优化", "EXPLAIN ANALYZE；statistics target。", "Genetic Query Optimizer。"),
    ("事务", "ACID；默认 READ COMMITTED。", "两阶段提交 prepared transaction。"),
    ("MVCC", "xmin/xmax 行版本；VACUUM 回收。", "Snapshot 可见性判断。"),
    ("锁", "表锁 RowExclusive；advisory lock。", "deadlock_timeout 检测。"),
    ("扩展", "CREATE EXTENSION postgis pgvector。", "C 语言 hook 自定义。"),
    ("全文检索", "tsvector tsquery；GIN 索引。", "中文 zhparser。"),
    ("JSON", "JSONB 二进制存储；->> 操作符。", "GIN jsonb_path_ops。"),
    ("GIS", "PostGIS geometry geography。", "ST_DWithin 空间索引。"),
    ("复制", "流复制 WAL shipping；同步 replica。", "逻辑复制 publication。"),
    ("高可用", "Patroni + etcd；PgBouncer 连接池。", "Switchover vs Failover。"),
    ("性能调优", "shared_buffers work_mem；autovacuum。", "pg_stat_statements。"),
    ("备份恢复", "pg_dump pg_basebackup；PITR WAL。", "pgBackRest。"),
    ("PostgreSQL最佳实践", "连接池必须；EXPLAIN 审查；定期 VACUUM。", "分区表 declarative。"),
]:
    _add("PostgreSQL", m, core=core, internal=internal)

# ===== MongoDB =====
for m, core, internal in [
    ("MongoDB基础", "文档 BSON；集合 collection。", "mongod 守护进程。"),
    ("文档模型", "嵌入 vs 引用；反范式换读性能。", "Schema validation $jsonSchema。"),
    ("CRUD", "insertOne find updateOne deleteOne。", "bulkWrite  ordered。"),
    ("索引", "单字段复合多键 TTL text。", "ESR 规则 Equality Sort Range。"),
    ("聚合", "pipeline $match $group $lookup。", "allowDiskUse 大聚合。"),
    ("复制集", "Primary Secondary Arbiter；oplog。", "选举 majority 投票。"),
    ("分片", "shard key 选择；chunk 迁移。", "balancer 自动均衡。"),
    ("事务", "4.0 副本集；4.2 分片；multi-doc ACID。", "snapshot read concern。"),
    ("性能优化", "projection 减字段；hint 强制索引。", "连接池 maxPoolSize。"),
    ("安全", "SCRAM auth；RBAC role；TLS。", "field level encryption。"),
    ("备份恢复", "mongodump vs 快照；PITR oplog。", "Atlas continuous backup。"),
    ("MongoDB最佳实践", "shard key 不可变；避免大文档 16MB。", "schema 版本化。"),
]:
    _add("MongoDB", m, core=core, internal=internal)

# ===== Elasticsearch =====
for m, core, internal in [
    ("ES基础", "Near Real Time；index 逻辑命名空间。", "Lucene segment 不可变。"),
    ("架构", "Master/Data/Ingest/Coordinating 节点。", "cluster state 元数据。"),
    ("索引", "settings mappings aliases。", "rollover 按大小时间。"),
    ("文档", "_id _source _version。", "optimistic concurrency control。"),
    ("映射", "dynamic mapping；keyword vs text。", "multi-fields 多分析。"),
    ("查询DSL", "bool must/should/filter。", "query vs filter context 评分。"),
    ("聚合", "bucket metric pipeline。", "composite 分页聚合。"),
    ("分词", "analyzer tokenizer+filter；IK 中文。", "synonym 同义词。"),
    ("集群", "discovery zen2；split-brain min_master_nodes。", "voting only master。"),
    ("分片", "primary+replica；routing 公式。", "rebalance 阈值。"),
    ("性能优化", "forcemerge 段；bulk 批量写入。", "circuit breaker JVM。"),
    ("高可用", "replica 故障转移；跨 AZ。", "snapshot repository S3。"),
    ("安全", "X-Pack TLS RBAC。", "index level security。"),
    ("ELK栈", "Beats→Logstash→ES→Kibana。", "ECS 字段规范。"),
    ("ES最佳实践", "避免深分页 search_after；mapping 预定义。", "hot-warm-cold 架构。"),
]:
    _add("Elasticsearch", m, core=core, internal=internal)

# ===== 数据仓库 =====
for m, core, internal in [
    ("数据仓库概述", "Bill Inmon 企业级 vs Kimball 维度。", "OLTP vs OLAP 工作负载。"),
    ("维度建模", "事实表+维度表；粒度定义。", "SCD 缓慢变化维 Type1/2/3。"),
    ("星型雪花", "星型 denormalized；雪花 normalized 维表。", "事实表占 80% 存储。"),
    ("事实表", "事务快照累积；可加性度量。", "semi-additive 库存。"),
    ("维度表", "退化维；junk dimension。", "role-playing dimension 日期。"),
    ("ETL", "Extract Transform Load 批处理。", "ELT 云数仓原生。"),
    ("分层架构", "ODS→DWD→DWS→ADS。", "OneData 指标一致。"),
    ("OLAP", "MOLAP ROLAP HOLAP。", "Cube 预聚合。"),
    ("指标体系", "原子/派生/复合指标；口径文档。", "Metrics Store。"),
    ("数据治理", "元数据血缘；质量规则。", "Data Catalog。"),
    ("性能优化", "分区列；列存压缩；物化视图。", "pre-aggregation。"),
    ("Hive", "HDFS 上 SQL；MapReduce/Tez/Spark。", "分区表 partition。"),
    ("ClickHouse", "MergeTree 引擎；列存。", "物化视图增量。"),
    ("Doris", "MPP 实时分析；Rollup。", "Broker Load 导入。"),
    ("数据仓库最佳实践", "维度一致；避免宽表爆炸；文档化口径。", "dbt transform 即代码。"),
]:
    _add("数据仓库", m, core=core, internal=internal)

# ===== 缓存技术 =====
for m, core, internal in [
    ("缓存概述", "时间局部性+空间局部性。", "Cache hit ratio 核心指标。"),
    ("缓存策略", "Cache-Aside Read/Write Through/Write Behind。", "Refresh ahead 预刷新。"),
    ("缓存穿透", "查不存在 key；布隆过滤器。", "空值缓存短 TTL。"),
    ("缓存击穿", "热 key 过期；互斥锁 singleflight。", "逻辑过期异步重建。"),
    ("缓存雪崩", "大量 key 同时过期。", "TTL 随机抖动。"),
    ("缓存一致性", "先更 DB 再删缓存；延迟双删。", "Canal 订阅 binlog 删缓存。"),
    ("本地缓存", "Caffeine Guava LRU/LFU。", "Heap 限制 size。"),
    ("分布式缓存", "Redis Cluster 分片。", "一致性 hash 虚拟节点。"),
    ("多级缓存", "L1 本地 L2 Redis L3 DB。", "Near cache 命中率。"),
    ("缓存预热", "启动加载热点；定时刷新。", "canary 预热。"),
    ("缓存降级", "Redis 故障直读 DB。", "熔断限流保护 DB。"),
    ("热点key", "Local cache 副本；key 拆分。", "Redis 多副本读。"),
    ("大key", "拆分 hash；压缩；unlink 异步删。", "避免 HGETALL 大 hash。"),
    ("性能优化", "pipeline；连接池；序列化 Protobuf。", "avoid KEYS command。"),
    ("缓存最佳实践", "必设 TTL；监控 evicted；key 规范。", "容量规划 maxmemory。"),
]:
    _add("缓存技术", m, core=core, internal=internal)

# ===== ETL开发 =====
for m, core, internal in [
    ("ETL概述", "数据集成批流；数据管道。", "ELT 云原生转变。"),
    ("数据抽取", "全量增量；JDBC Sqoop。", "CDC binlog 实时。"),
    ("数据转换", "清洗标准化；UDF Spark SQL。", "维度映射 lookup。"),
    ("数据加载", "bulk load；COPY PostgreSQL。", "幂等 overwrite/merge。"),
    ("数据清洗", "去重空值异常；规则引擎。", "Great Expectations。"),
    ("数据质量", "完整性准确性一致性。", "DQ score 仪表盘。"),
    ("调度", "Airflow DAG；依赖 sensors。", "cron vs interval。"),
    ("增量同步", "水位线 timestamp/id。", "merge into upsert。"),
    ("CDC", "Debezium Kafka Connect。", "Canal Maxwell。"),
    ("性能优化", "并行 partition；列裁剪。", "pushdown predicate。"),
    ("工具", "DataX SeaTunnel Flink CDC。", "dbt SQL transform。"),
    ("ETL最佳实践", "幂等 job；监控 lag；schema evolution。", "dead letter 脏数据。"),
]:
    _add("ETL开发", m, core=core, internal=internal)

# ===== 时序数据库 =====
for m, core, internal in [
    ("时序数据概述", "时间戳+metric+tags+value。", "高写入范围查询。"),
    ("InfluxDB", "measurement tag field；Flux 查询。", "TSM 存储引擎。"),
    ("Prometheus", "pull 模型；PromQL；TSDB block。", "remote write 长期存储。"),
    ("TimescaleDB", "PostgreSQL 扩展 hypertable。", "continuous aggregate。"),
    ("TDengine", "超级表 tag 列；国产 IoT。", "列存压缩。"),
    ("数据模型", "metric 命名规范；label cardinality。", "high cardinality 禁忌。"),
    ("写入优化", "batch remote write；WAL。", "out-of-order 样本。"),
    ("查询优化", "recording rules 预计算。", "query range step。"),
    ("降采样", "rollup downsampling。", "retention policy。"),
    ("保留策略", "TTL 自动删除；tiered storage。", "compaction。"),
    ("时序数据库最佳实践", "label 低基数；recording rule；容量规划。", "Thanos 长期 Prometheus。"),
]:
    _add("时序数据库", m, core=core, internal=internal)

# ===== Docker (extend) =====
for m, core, internal in [
    ("Docker基础", "docker run/build/ps；client-server API。", "dockerd daemon。"),
    ("存储", "volume bind mount tmpfs。", "mount propagation。"),
    ("数据卷", "named volume 持久化；docker volume create。", "volume driver 插件。"),
    ("Registry", "Docker Hub Harbor 私有。", "manifest list 多架构。"),
    ("多阶段构建", "AS builder/runtime 减小镜像。", "COPY --from=stage。"),
    ("安全", "non-root USER；scan trivy。", "seccomp profile。"),
    ("性能优化", "层缓存顺序；.dockerignore。", "BuildKit cache mount。"),
    ("日志", "json-file log driver；fluentd。", "log rotate max-size。"),
    ("监控", "cadvisor metrics；docker stats。", "healthcheck CMD。"),
    ("最佳实践", "一个进程一个容器；immutable 镜像。", "pin 基础镜像 digest。"),
]:
    _add("Docker", m, core=core, internal=internal)

# ===== Kubernetes (extend) =====
for m, core, internal in [
    ("Namespace", "资源隔离；ResourceQuota LimitRange。", "kube-system default。"),
    ("StatefulSet", "稳定网络 ID；OrderedReady。", "headless service DNS。"),
    ("DaemonSet", "每节点一 Pod；日志 agent。", "taint 容忍调度。"),
    ("Job", "一次性任务；completions parallelism。", "backoffLimit。"),
    ("CronJob", "schedule cron 表达式。", "concurrencyPolicy。"),
    ("网络策略", "NetworkPolicy ingress/egress。", "CNI Calico Cilium。"),
    ("资源限制", "requests limits QoS class。", "OOMKill 优先级。"),
    ("Operator", "CRD + controller reconcile。", "kubebuilder SDK。"),
    ("监控", "metrics-server HPA；kube-state-metrics。", "Prometheus operator。"),
    ("日志", "kubectl logs；sidecar 采集。", "EFK daemonset。"),
    ("安全", "PodSecurity admission；PSP 废弃。", "falco runtime。"),
    ("性能优化", "VPA 垂直扩缩；topology spread。", "preemption 优先级。"),
    ("K8s最佳实践", "声明式 GitOps；limit 必设；probe 必配。", "PDB 中断预算。"),
]:
    _add("Kubernetes", m, core=core, internal=internal)

# ===== CI与CD =====
for m, core, internal in [
    ("CI/CD概述", "DevOps 核心实践；左移质量。", "DORA 四个关键指标。"),
    ("持续集成", "频繁合并 main；自动化测试。", "trunk based development。"),
    ("持续交付", "随时可发布；手动批准上生产。", "release candidate。"),
    ("持续部署", "自动上生产；feature flag。", "canary analysis。"),
    ("流水线", "stage job step；DAG 依赖。", "pipeline as code。"),
    ("Jenkins", "Jenkinsfile declarative；agent。", "plugin 生态。"),
    ("GitLab CI", ".gitlab-ci.yml；runner。", "include template。"),
    ("GitHub Actions", "workflow on push；matrix。", "reusable workflow。"),
    ("ArgoCD", "GitOps sync；app of apps。", "helm kustomize。"),
    ("制品管理", "Harbor Nexus；immutable tag。", "SBOM 供应链。"),
    ("自动化测试", "CI 门禁 unit integration。", "test report artifact。"),
    ("部署策略", "rolling blue-green canary。", "flagger progressive。"),
    ("回滚", "helm rollback；k8s rollout undo。", "db migration 可逆。"),
    ("安全", "SAST DAST；secret scan。", "OIDC cloud 免密钥。"),
    ("CI/CD最佳实践", "快速反馈 <10min；环境一致。", "deployment frequency 度量。"),
]:
    _add("CI与CD", m, core=core, internal=internal)

# ===== Git版本控制 (extend) =====
for m, core, internal in [
    ("版本控制", "快照而非差异；DAG 历史。", "分布式每人全副本。"),
    ("工作流", "feature branch PR review。", "protected branch。"),
    ("GitFlow", "develop release hotfix。", "复杂已不推荐小团队。"),
    ("GitHub Flow", "main 部署；短分支 PR。", "简单适合 Web。"),
    ("标签", "annotated tag 签名。", "semver release tag。"),
    ("储藏", "stash pop 临时保存。", "stash branch。"),
    ("子模块", "git submodule 固定 commit。", "subtree 替代。"),
    ("大文件", "git-lfs pointer。", "filter-repo 清理历史。"),
    ("冲突解决", "<<<< marker；merge tool。", "ours/theirs 策略。"),
    ("历史改写", "rebase interactive squash。", "reflog 救援。"),
    ("Git最佳实践", "小 commit 清晰 message。", "Conventional Commits。"),
]:
    _add("Git版本控制", m, core=core, internal=internal)

# ===== Linux运维 =====
for m, core, internal in [
    ("Linux基础", "FHS 目录结构；man info。", "发行版 RHEL/Debian。"),
    ("用户管理", "useradd usermod；/etc/passwd shadow。", "sudoers visudo。"),
    ("权限管理", "rwx chmod chown；ACL setfacl。", "umask default。"),
    ("进程管理", "ps top htop；kill signal。", "nice renice 优先级。"),
    ("服务管理", "systemctl start enable。", "unit file Type=simple。"),
    ("软件包", "apt yum dnf；pin 版本。", "repo GPG 验证。"),
    ("网络配置", "ip addr route；DNS resolv.conf。", "NetworkManager nmcli。"),
    ("防火墙", "firewalld ufw iptables nftables。", "zone service port。"),
    ("磁盘管理", "fdisk lsblk mount fstab。", "LVM pv vg lv。"),
    ("文件系统", "ext4 xfs btrfs；inode。", "df du 空间。"),
    ("日志管理", "journalctl -u service。", "rsyslog /var/log。"),
    ("定时任务", "cron crontab；systemd timer。", "@reboot @daily。"),
    ("Shell脚本", "bash set -euo pipefail。", "shellcheck lint。"),
    ("性能监控", "vmstat iostat sar；ss netstat。", "perf ebpf。"),
    ("故障排查", "自上而下；复现；二分。", "USE 方法论。"),
    ("安全加固", "SSH key 禁密码；fail2ban。", "CIS benchmark。"),
    ("Linux运维最佳实践", "IaC 配置；变更窗口；runbook。", "immutable infrastructure。"),
]:
    _add("Linux运维", m, core=core, internal=internal)

# ===== 监控告警 =====
for m, core, internal in [
    ("监控概述", "Metrics Logs Traces 三支柱。", "可观测性 vs 监控。"),
    ("指标监控", "Counter Gauge Histogram Summary。", "Prometheus pull model。"),
    ("日志监控", "错误率 log-based metric。", "Loki LogQL。"),
    ("链路追踪", "OpenTelemetry W3C traceparent。", "span attribute。"),
    ("Prometheus", "PromQL rate histogram_quantile。", "federation remote write。"),
    ("Grafana", "dashboard panel；变量。", "alerting unified。"),
    ("AlertManager", "group route inhibit。", "silence maintenance。"),
    ("Zabbix", "agent item trigger。", "传统 IT 监控。"),
    ("APM", "SkyWalking Pinpoint。", "auto instrumentation。"),
    ("告警设计", "symptom based；runbook link。", "on-call rotation。"),
    ("SLA/SLO", "error budget burn rate。", "multi-window alert。"),
    ("容量规划", "趋势预测 headroom。", "load test 验证。"),
    ("性能分析", "flamegraph pprof。", "off-cpu wait。"),
    ("监控最佳实践", "少而精告警；actionable。", "dashboard as code。"),
]:
    _add("监控告警", m, core=core, internal=internal)

# ===== 日志分析 =====
for m, core, internal in [
    ("日志概述", "结构化 JSON 可检索。", "日志级别 DEBUG INFO WARN ERROR。"),
    ("日志采集", "Filebeat Fluent Bit agent。", "stdout 容器日志。"),
    ("日志存储", "ES index lifecycle hot warm。", "S3 冷存储。"),
    ("日志检索", "Kibana KQL；Lucene query。", "full text vs keyword。"),
    ("日志分析", "aggregation 趋势；异常检测。", "pattern 聚类。"),
    ("ELK栈", "Elasticsearch Logstash Kibana。", "Beats 轻量采集。"),
    ("EFK栈", "Fluentd 替代 Logstash。", "Kubernetes 常见。"),
    ("Loki", "label 索引非全文；LogQL。", "promtail 采集。"),
    ("日志告警", "ElastAlert；Grafana Loki ruler。", "threshold spike。"),
    ("日志安全", "脱敏 PII；RBAC；retention。", "audit trail 不可篡改。"),
    ("日志最佳实践", "trace_id 关联；统一 schema。", "采样 debug 生产。"),
]:
    _add("日志分析", m, core=core, internal=internal)

# ===== Nginx =====
for m, core, internal in [
    ("Nginx基础", "master-worker；nginx -t reload。", "conf.d sites-enabled。"),
    ("架构", "事件驱动 epoll；异步非阻塞。", "worker_connections 1024。"),
    ("配置", "directive context main/http/server/location。", "include 模块化。"),
    ("虚拟主机", "server_name；基于 name/IP。", "default_server。"),
    ("负载均衡", "upstream weight ip_hash least_conn。", "health_check 第三方。"),
    ("静态资源", "root alias；expires cache。", "gzip_static precompressed。"),
    ("缓存", "proxy_cache_path keys_zone。", "Cache-Control header。"),
    ("SSL/TLS", "ssl_certificate；TLS1.2+；OCSP stapling。", "Let's Encrypt certbot。"),
    ("HTTP/2", "listen 443 ssl http2。", "server push 已弃用。"),
    ("限流", "limit_req_zone burst nodelay。", "limit_conn 连接数。"),
    ("访问控制", "allow deny；auth_basic。", "satisfy any all。"),
    ("日志", "access_log json format；error_log warn。", "log_format 自定义。"),
    ("性能优化", "sendfile tcp_nopush；open_file_cache。", "worker_cpu_affinity。"),
    ("Nginx最佳实践", "TLS 现代配置；隐藏 version。", "rate limit 防 abuse。"),
]:
    _add("Nginx", m, core=core, internal=internal)

# ===== 云计算 =====
for m, core, internal in [
    ("云计算概述", "按需自助；资源池化；快速弹性。", "NIST 五大特征。"),
    ("IaaS", "VM 网络存储；EC2 ECS。", "用户管 OS 以上。"),
    ("PaaS", "托管运行时；Heroku Cloud Run。", "用户管应用。"),
    ("SaaS", "完整应用；Salesforce 365。", "多租户。"),
    ("公有云", "AWS Azure GCP 阿里云。", "region AZ 高可用。"),
    ("私有云", "OpenStack VMware。", "合规数据主权。"),
    ("混合云", "专线 VPN；统一管控。", "Terraform 多云。"),
    ("阿里云", "ECS OSS RDS ACK。", "国内合规。"),
    ("AWS", "EC2 S3 RDS EKS Lambda。", "Well-Architected。"),
    ("云原生", "容器微服务 DevOps。", "CNCF 项目景观。"),
    ("云安全", "IAM 最小权限；Security Group。", "KMS 加密。"),
    ("成本优化", "Reserved Spot；rightsizing。", "FinOps 文化。"),
    ("云计算最佳实践", "Infrastructure as Code；多 AZ。", "disaster recovery 演练。"),
]:
    _add("云计算", m, core=core, internal=internal)

# ===== Ansible =====
for m, core, internal in [
    ("Ansible基础", "agentless SSH；YAML playbook。", "inventory 主机清单。"),
    ("Inventory", "static ini；dynamic cloud。", "group group_vars host_vars。"),
    ("Ad-Hoc", "ansible ping -m shell。", "一次性命令。"),
    ("Playbook", "hosts tasks handlers。", "idempotent module。"),
    ("Role", "tasks defaults vars meta。", "ansible-galaxy install。"),
    ("模块", "copy template service yum。", "command vs shell 非幂等。"),
    ("变量", "vars precedence；register。", "facts setup module。"),
    ("模板", "Jinja2 {% %} {{ }}。", "template module。"),
    ("条件循环", "when；loop with_items。", "block rescue always。"),
    ("标签", "tags skip-tags。", "--tags deploy。"),
    ("Vault", "ansible-vault encrypt。", "vault-id 密码文件。"),
    ("最佳实践", "role 复用；check mode diff。", "ansible-lint 规范。"),
]:
    _add("Ansible", m, core=core, internal=internal)
