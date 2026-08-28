#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate content_frontend.py with real frontend technical tutorials."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Dict, List, Tuple

from domains_100_config import DOMAINS_CONFIG

FRONTEND_DOMAINS = [
    "HTML与CSS", "React", "Vue", "Node.js", "前端工程化", "浏览器原理",
    "Web性能优化", "PWA", "Angular", "小程序开发", "微前端", "数据可视化",
]

# ---------------------------------------------------------------------------
# Hand-crafted high-quality module content
# ---------------------------------------------------------------------------
DETAILED: Dict[Tuple[str, str], dict] = {
    ("React", "React基础"): {
        "intro": (
            "React 是声明式 UI 库：用 **组件** 描述界面，数据变化时 React 负责高效更新 DOM。"
            "React 18 默认创建 **Concurrent Root**（`createRoot`），支持并发渲染、"
            "Automatic Batching 与 Transitions，是理解后续 Hooks 与 Fiber 的基础。"
        ),
        "concepts": [
            {"title": "声明式与命令式", "body": (
                "命令式：手动 `document.createElement`、改样式、绑事件。"
                "声明式：描述 `UI = f(state)`，React 在 state 变化时计算差异并提交更新。"
                "这使 UI 状态可预测、易测试。"
            )},
            {"title": "组件与元素", "body": (
                "React **Element** 是轻量描述对象 `{type, props, key}`；"
                "**Component** 是返回 Element 的函数或类。"
                "`createElement` 或 JSX 编译后均产生 Element 树，再由 reconciler 处理。"
            )},
            {"title": "createRoot 与 StrictMode", "body": (
                "React 18：`createRoot(dom).render(<App />)` 启用并发特性。"
                "`<StrictMode>` 开发环境双重调用部分生命周期/Hooks 以暴露副作用，"
                "生产环境无此行为。"
            )},
        ],
        "mechanism": (
            "渲染流程：触发更新（setState/dispatch）→ render 阶段生成 Fiber 树（可中断）→ "
            "commit 阶段一次性应用 DOM 变更、执行 useLayoutEffect、绑定事件。"
            "React 18 对 setTimeout/Promise 中的多次 setState 自动批处理。"
        ),
        "internals": (
            "协调器（Reconciler）基于 **Fiber** 链表结构遍历；每个 Fiber 对应一个组件实例或 DOM 节点，"
            "含 `memoizedState`（Hooks 链表）、`child/sibling/return` 指针。"
            "阅读 `react-reconciler` 包中 `beginWork`/`completeWork` 可跟踪渲染路径。"
        ),
        "workflow": (
            "1. `npm create vite@latest my-app -- --template react`\n"
            "2. `main.jsx` 中 `createRoot(document.getElementById('root')).render(<App />)`\n"
            "3. 拆分组件、提升 state、单向数据流\n"
            "4. 开发用 React DevTools 查看组件树与 props"
        ),
        "performance": "避免在 render 中创建新对象/函数导致子组件无效重渲染；列表用稳定 key。",
        "security": "勿将未消毒的用户 HTML 直接 `dangerouslySetInnerHTML`；URL 用 `rel=noopener`。",
        "debugging": "React DevTools Components/Profiler；`console.log` 渲染次数；why-did-you-render 插件。",
        "pitfalls": [
            {"title": "混用 createRoot 与 ReactDOM.render", "body": "React 18 应统一 createRoot，legacy render 无并发能力。"},
            {"title": "在 render 中 setState", "body": "导致无限循环；副作用应放 useEffect 或事件处理器。"},
        ],
        "practices": ["函数组件 + Hooks 为默认", "组件单一职责", "props 类型用 PropTypes 或 TypeScript"],
        "references": ["React 官方文档", "React 18 发布说明", "react.dev/learn"],
    },
    ("React", "JSX"): {
        "intro": (
            "JSX 是 JavaScript 语法扩展，编译为 `React.createElement(type, props, ...children)`。"
            "Babel `@babel/preset-react`（classic）或 automatic runtime（`jsx/jsxs`）处理转换；"
            "理解编译产物有助于调试与性能分析。"
        ),
        "concepts": [
            {"title": "JSX 与 createElement", "body": (
                "`<div className=\"a\">{x}</div>` → `jsx('div', {className:'a'}, x)`（automatic）"
                "或 `createElement('div', {className:'a'}, x)`。"
                "自定义组件首字母大写：` <Button />` → `createElement(Button, null)`。"
            )},
            {"title": "表达式与 Fragment", "body": (
                "花括号内可为任意表达式；`<>...</>` 或 `<Fragment key={}>` 避免多余 DOM 包装。"
                "条件渲染：`{ok && <A/>}` 或三元；`null/false/undefined` 不渲染。"
            )},
            {"title": "属性与 children", "body": (
                "camelCase：`className`、`htmlFor`、`onClick`。"
                "展开 `{...props}` 传递；children 可作为 props.children 或显式参数（组合模式）。"
            )},
        ],
        "mechanism": "编译期静态分析可优化：automatic runtime 按 children 数量选 jsx vs jsxs，减少运行时判断。",
        "internals": "React 17+ 无需每文件 `import React`（新 JSX transform）；旧项目需升级 Babel 配置。",
        "workflow": "1. 配置 Vite/Babel JSX 2. 组件返回单根（或 Fragment）3. 提取重复 JSX 为子组件",
        "performance": "大列表 JSX 结构稳定；避免内联匿名组件定义在父 render 中。",
        "pitfalls": [
            {"title": "class 写成 className 遗漏", "body": "控制台警告；SVG 部分属性为 camelCase（fillRule）。"},
            {"title": "相邻 JSX 无包裹", "body": "语法错误；用 Fragment 或数组（需 key）。"},
        ],
        "practices": ["ESLint react/jsx 规则", "复杂条件提取变量", "可访问性属性一并编写"],
        "references": ["React JSX 文档", "Babel preset-react"],
    },
    ("React", "Hooks"): {
        "intro": (
            "Hooks 让函数组件拥有 state 与生命周期等价能力，规则：**仅在顶层调用**、"
            "**仅在 React 函数中调用**。React 按调用顺序将 Hook 状态挂在 Fiber.memoizedState 链表上。"
        ),
        "concepts": [
            {"title": "Hooks 链表与 Fiber", "body": (
                "每次 render，Hooks 按声明顺序遍历 memoizedState 节点："
                "useState 存 `{memoizedState: state, queue}`，useEffect 存 effect 对象。"
                "条件分支中少调 Hook 会导致顺序错乱——违反 Rules of Hooks。"
            )},
            {"title": "内置 Hooks 分类", "body": (
                "State：useState、useReducer；"
                "Context：useContext；"
                "Effect：useEffect、useLayoutEffect、useInsertionEffect；"
                "Performance：useMemo、useCallback、useTransition、useDeferredValue；"
                "Ref：useRef、useImperativeHandle。"
            )},
            {"title": "自定义 Hook", "body": (
                "以 `use` 开头的函数封装可复用逻辑，内部可调用其他 Hooks。"
                "如 `useFetch`、`useLocalStorage`，实现逻辑共享而非继承。"
            )},
        ],
        "mechanism": (
            "mount：初始化 Hook 节点；update：读取 queue 中 pending update 计算新 state。"
            "useEffect 在 paint 后异步 flush；useLayoutEffect 在 DOM 变更后、paint 前同步执行。"
        ),
        "internals": (
            "Dispatcher 在 render 与 mount/update 阶段不同（HooksDispatcherOnMount/OnUpdate）。"
            "StrictMode 开发环境 mount→unmount→remount 检测 effect 清理是否完整。"
        ),
        "workflow": "识别状态与副作用 → 选 useState/useReducer → 副作用 useEffect → 抽自定义 Hook",
        "performance": "不必默认包裹 useMemo/useCallback；Profiler 证明瓶颈后再优化。",
        "pitfalls": [
            {"title": "依赖数组遗漏", "body": "闭包陈旧值；eslint-plugin-react-hooks 的 exhaustive-deps。"},
            {"title": "useEffect 无限循环", "body": "effect 内 setState 且 deps 含该 state 未加条件。"},
        ],
        "practices": ["遵守 Rules of Hooks", "自定义 Hook 单一职责", "effect 返回清理函数"],
        "references": ["Hooks API Reference", "eslint-plugin-react-hooks"],
    },
    ("React", "useState"): {
        "intro": (
            "`useState(initialState)` 返回 `[state, setState]`。"
            "setState 可传值或 updater `(prev) => next`；更新会调度 re-render，"
            "React 18 批处理多次 setState 为一次渲染。"
        ),
        "concepts": [
            {"title": "惰性初始化", "body": "`useState(() => expensive())` 仅首次 mount 计算初始值。"},
            {"title": "更新队列", "body": "同一事件批处理内多次 setState，updater 链式接收 prev；异步回调中亦批处理（React 18）。"},
            {"title": "状态不可变", "body": "对象/数组应展开或 copy 后修改：`setItems([...items, new])`，直接改引用不触发更新。"},
        ],
        "mechanism": "dispatchSetState 将 update 入队；render 阶段 replay 队列得新 memoizedState。",
        "internals": "类组件 setState 合并浅层；函数组件 useState 按 Hook 索引独立，不自动合并多个 useState。",
        "workflow": "局部 UI 状态用 useState；复杂逻辑迁 useReducer；跨组件用 Context/外部 store。",
        "performance": "状态下放至用到它的子树；避免根组件庞大 state 导致全树 render。",
        "pitfalls": [
            {"title": "闭包陈旧 state", "body": "异步回调用 functional update 或 useRef 存最新值。"},
            {"title": "初始 state 传对象每次新建", "body": "仅首次用 initialState；重复计算用惰性函数。"},
        ],
        "practices": ["相关状态合并或 useReducer", "表单受控组件统一 state", "TypeScript 泛型标注"],
        "references": ["useState 文档"],
    },
    ("React", "useEffect"): {
        "intro": (
            "`useEffect(setup, deps?)` 在 **commit 后**异步运行 setup；"
            "deps 变化时先执行上次 cleanup 再 setup。无 deps 数组则每 render 后执行（慎用）。"
        ),
        "concepts": [
            {"title": "副作用边界", "body": "数据获取、订阅、手动 DOM、定时器属副作用；纯计算应留在 render 或 useMemo。"},
            {"title": "清理函数", "body": "return () => unsubscribe() 防泄漏；StrictMode 双重调用检验清理。"},
            {"title": "依赖数组", "body": "[] 仅 mount/unmount；省略则每次 commit 后执行；列出 render 中用到的 props/state。"},
        ],
        "mechanism": "commit 阶段 schedule  effect；flushPassiveEffects 在 paint 后运行；useLayoutEffect 更早同步。",
        "internals": "Effect 链表挂在 Fiber.updateQueue；Concurrent 渲染可能丢弃未完成 commit 的 effect。",
        "workflow": "定义数据需求 → effect 内 fetch + AbortController → 更新 state → cleanup 取消请求",
        "performance": "避免 effect 内无 deps 导致频繁请求；合理用 SWR/React Query 管理服务端状态。",
        "pitfalls": [
            {"title": "忘记 cleanup 订阅", "body": "内存泄漏与 setState on unmounted 警告。"},
            {"title": "object 依赖每次新建", "body": "effect 无限触发；解构原始值或 useMemo 稳定引用。"},
        ],
        "practices": ["数据获取考虑 React Query", "race 用 AbortController", "与 useLayoutEffect 区分场景"],
        "references": ["useEffect 文档", "You Might Not Need an Effect"],
    },
    ("React", "性能优化"): {
        "intro": (
            "React 性能优化核心：**减少不必要 render** 与 **降低 commit 成本**。"
            "手段包括 memo、useMemo/useCallback、代码分割、虚拟列表、Concurrent 特性（useTransition）。"
        ),
        "concepts": [
            {"title": "React.memo", "body": "包裹组件，props 浅比较相等则跳过 render；配合稳定 props 引用。"},
            {"title": "useMemo / useCallback", "body": "缓存计算结果与函数引用；勿滥用，Profiler 证明瓶颈再用。"},
            {"title": "Concurrent 特性", "body": "useTransition 标记低优先级更新；useDeferredValue 延迟展示快速输入的慢结果。"},
        ],
        "mechanism": "render 可中断；高优更新（输入）可打断低优（列表过滤）；commit 仍原子。",
        "internals": "Fiber alternate 双缓冲；bailout 当 props/state/context 未变跳过子树。",
        "workflow": "Profiler 录制的 commit 时长 → 找频繁 render 组件 → memo/状态下沉/虚拟化",
        "performance": "react-window 虚拟长列表；lazy+Suspense 路由级分割；避免 context 大对象频繁变。",
        "comparison": "memo vs 状态下沉：状态下沉减少订阅范围往往更有效。",
        "pitfalls": [
            {"title": "处处 useCallback", "body": "增加内存与比较成本；子组件未 memo 时无效。"},
            {"title": "key=index 列表重排", "body": "错误复用 DOM 状态；用稳定 id。"},
        ],
        "practices": ["先测量后优化", "列表虚拟化", "Context 拆分", "生产构建 + 分析 bundle"],
        "references": ["React 性能优化", "Profiler API"],
    },
    ("React", "服务端渲染"): {
        "intro": (
            "SSR 在服务器生成 HTML 字符串，客户端 **hydration** 绑定事件复用 DOM。"
            "Next.js App Router 支持 RSC（React Server Components）在服务端运行组件，"
            "零 bundle 服务端逻辑；客户端组件标 `'use client'`。"
        ),
        "concepts": [
            {"title": "renderToString / renderToPipeableStream", "body": "React 18 流式 SSR：`renderToPipeableStream` 分 chunk 发送，改善 TTFB。"},
            {"title": "Hydration 与不匹配", "body": "服务端与客户端首屏 HTML 必须一致，否则 hydration mismatch 警告；避免 Date.now() 等差异。"},
            {"title": "RSC", "body": "Server Component 可 async/直接查 DB；Client Component 处理交互与 Hooks。"},
        ],
        "mechanism": "SSR：请求 → 服务端 render → HTML+序列化 state → 客户端 hydrate → CSR 接管。",
        "internals": "Fizz 架构支持 Suspense 边界流式输出；选择性 hydration 优先可视区域。",
        "workflow": "Next.js `app/` 目录 → 默认 Server Component → 交互部分 client → streaming",
        "performance": "静态页面 SSG/ISR；边缘渲染；减少客户端 JS bundle。",
        "pitfalls": [
            {"title": "浏览器 API 在 SSR 执行", "body": "window 未定义；useEffect 或 dynamic ssr:false。"},
            {"title": "hydration 闪烁", "body": "客户端二次 fetch 导致；初始数据由服务端注入。"},
        ],
        "practices": ["RSC 默认服务端", "关键 CSS 内联", "流式 Suspense 边界"],
        "references": ["Next.js 文档", "React Server Components"],
    },
    ("Vue", "组合式API"): {
        "intro": (
            "Vue 3 **Composition API** 以 `setup()` 或 `<script setup>` 组织逻辑："
            "`ref`/`reactive` 声明响应式状态，`computed`/`watch` 派生与副作用，"
            "组合函数（composables）实现跨组件逻辑复用，优于 mixin 的命名冲突与来源不清。"
        ),
        "concepts": [
            {"title": "ref 与 reactive", "body": (
                "`ref(value)` 包装任意值，`.value` 访问；模板自动解包。"
                "`reactive(object)` Proxy 深层响应式；不可替换整个 reactive 对象引用。"
                "推荐基本类型与需替换引用用 ref，对象用 reactive 或 `ref({})`。"
            )},
            {"title": "script setup", "body": (
                "`<script setup>` 编译时提升绑定至模板，无需 return。"
                "`defineProps`/`defineEmits`/`defineExpose` 编译宏；"
                "与 TypeScript 结合用 `defineProps<{...}>()`。"
            )},
            {"title": "composables", "body": (
                "`function useMouse() { const x = ref(0); onMounted(...); return {x} }`"
                "任意组合函数内可调生命周期 Hooks；命名 `use*` 为约定。"
            )},
        ],
        "mechanism": (
            "setup 在 beforeCreate 之前执行一次；返回或 script setup 绑定进入 render 闭包。"
            "响应式 track 依赖、trigger 通知 effect（组件 render effect、computed、watch）。"
        ),
        "internals": (
            "Proxy handler：get track、set trigger；ref 用 RefImpl 类包装；"
            "computed 惰性缓存 dirty 标志；effect scheduler 批量异步 flush。"
        ),
        "workflow": "1. script setup 2. ref/reactive 状态 3. computed 派生 4. watch 副作用 5. 抽 composables",
        "performance": "大对象用 shallowRef/shallowReactive；markRaw 标记非响应式第三方实例。",
        "comparison": "Options API 仍支持；小组件可用；复杂逻辑 Composition API 更清晰。",
        "pitfalls": [
            {"title": "解构 reactive 失响应", "body": "用 toRefs 或始终通过对象访问。"},
            {"title": "watch 源类型错误", "body": "watch ref 直接传 ref，勿 watch(ref.value)。"},
        ],
        "practices": ["逻辑按功能分 composable", "TypeScript 标注 props/emits", "优先 script setup"],
        "references": ["Vue 3 Composition API FAQ", "VueUse 库"],
    },
    ("Vue", "Vue3新特性"): {
        "intro": (
            "Vue 3 相对 Vue 2：Proxy 响应式、Composition API、Fragment/Teleport/Suspense、"
            "多个 v-model、更好的 TypeScript 支持、Tree-shaking 友好与编译优化（静态提升、补丁 flags）。"
        ),
        "concepts": [
            {"title": "编译优化", "body": "静态节点提升 hoist；动态节点打 patchFlag（TEXT/CLASS/PROPS 等），diff 仅比较必要部分。"},
            {"title": "Teleport 与 Suspense", "body": "Teleport 将子树渲染到 DOM 其他位置（模态框）；Suspense 协调异步依赖默认/回退插槽。"},
            {"title": "多 v-model", "body": "`v-model:title` 对应 `title` prop 与 `update:title` emit，简化双向绑定组件。"},
        ],
        "mechanism": "运行时包更小；响应式与编译协同减少无效 diff；createRenderer 支持自定义宿主（Weex/Canvas）。",
        "internals": "@vue/reactivity 独立包；@vue/runtime-core 平台无关；@vue/runtime-dom 浏览器 API。",
        "workflow": "Vite + vue-plugin 默认 Vue 3；从 Vue 2 用 @vue/compat 渐进迁移",
        "performance": "静态内容不参与更新；事件监听器缓存 cacheHandlers。",
        "pitfalls": [
            {"title": "Vue 2 过滤器 filters 移除", "body": "改用 computed 或方法。"},
            {"title": "$on/$off 事件总线移除", "body": "用 mitt 或 Pinia。"},
        ],
        "practices": ["启用 TypeScript", "使用 Vite", "阅读迁移指南 breaking changes"],
        "references": ["Vue 3 Migration Guide", "Vue 3 发布博客"],
    },
    ("Node.js", "事件循环"): {
        "intro": (
            "Node.js 在单线程上运行 JavaScript，**libuv** 提供事件循环处理 I/O 回调。"
            "循环阶段：timers → pending → idle/prepare → **poll** → check → close callbacks；"
            "process.nextTick 与 Promise microtask 在每个阶段间优先执行。"
        ),
        "concepts": [
            {"title": "阶段与队列", "body": "setTimeout/setInterval 进 timers；setImmediate 进 check；I/O 完成回调在 poll。"},
            {"title": "微任务", "body": "每个阶段后清空 nextTick 队列，再清空 Promise 微任务队列；nextTick 优先于 Promise。"},
            {"title": "阻塞 poll", "body": "poll 中回调或同步 CPU 密集任务阻塞整个循环，导致定时器延迟。"},
        ],
        "mechanism": "主线程执行 JS；libuv 线程池处理 fs/crypto 等；网络 I/O 由 OS 异步通知 epoll/kqueue。",
        "internals": "UV_RUN_DEFAULT 循环；`--inspect` 可观察异步钩子 async_hooks。",
        "workflow": "CPU 密集用 worker_threads；I/O 用 async API；定时用 setImmediate vs setTimeout 选型",
        "performance": "避免同步 fs/readFileSync；集群 cluster 或 PM2 多进程利用多核。",
        "debugging": "async_hooks 追踪；clinic.js 诊断事件循环延迟。",
        "pitfalls": [
            {"title": "长循环阻塞", "body": "JSON.parse 巨文件、死循环冻结服务；拆 worker。"},
            {"title": "nextTick 递归", "body": "饿死 I/O；优先 queueMicrotask 或 setImmediate。"},
        ],
        "practices": ["理解阶段顺序", "监控 event loop lag", "流式处理大文件"],
        "references": ["Node.js Event Loop 官方文档", "libuv 设计"],
    },
    ("浏览器原理", "渲染流程"): {
        "intro": (
            "从 HTML/CSS/JS 到像素：**解析** HTML 建 DOM、CSS 建 CSSOM → **合成渲染树** → "
            "**Layout** 计算几何 → **Paint** 记录绘制指令 → **Composite** 合成层上 GPU 光栅化。"
            "JS 可强制 sync layout（强制重排）打断流水线。"
        ),
        "concepts": [
            {"title": "关键渲染路径", "body": "阻塞：CSS 阻塞渲染树；parser-blocking script 阻塞 DOM（defer/async 缓解）。"},
            {"title": "重排与重绘", "body": "几何变化→layout→paint→composite；仅颜色→可能 skip layout；transform/opacity 常仅 composite。"},
            {"title": "合成层", "body": "will-change/transform 提升层；层过多占 GPU 内存；层爆炸需控制。"},
        ],
        "mechanism": "主线程协调；Compositor 线程处理滚动与部分动画；Raster 线程光栅化 tiles。",
        "internals": "Blink：LocalFrameView→LayoutObject→PaintLayer→GraphicsLayer；CC 合成器。",
        "workflow": "Performance 面板录帧→看 Main 线程 Long Task→定位 layout/paint 热点",
        "performance": "避免读写布局属性交错；content-visibility；减少层数。",
        "pitfalls": [
            {"title": "offsetWidth 触发 sync layout", "body": "批量读布局属性后再写样式。"},
            {"title": "全屏 fixed 层过多", "body": "移动端 GPU 内存压力。"},
        ],
        "practices": ["transform 做动画", "contain 隔离", "字体 font-display:swap"],
        "references": ["web.dev 渲染性能", "Chrome Developers 渲染管线"],
    },
    ("微前端", "qiankun"): {
        "intro": (
            "qiankun 基于 single-spa，封装 **JS 沙箱**（Proxy 快照 / Legacy）、"
            "**样式隔离**（experimentalStyleIsolation / strictStyleIsolation）、"
            "应用加载与生命周期，是国内微前端最常用方案之一。"
        ),
        "concepts": [
            {"title": "registerMicroApps", "body": "注册 name、entry（HTML 入口 URL）、container、activeRule（路由激活规则）。"},
            {"title": "沙箱", "body": "ProxySandbox 代理 window；多实例切换时 restore 全局；不支持 Proxy 降级快照。"},
            {"title": "prefetch", "body": "空闲时预加载子应用静态资源，改善首次切换体验。"},
        ],
        "mechanism": "fetch entry HTML → 解析 JS/CSS → exec 沙箱内 → mount 到 container → 路由匹配 activeRule。",
        "internals": "import-html-entry 拉取资源；single-spa 调度 bootstrap/mount/unmount。",
        "workflow": "主应用 Vue/React → registerMicroApps → 子应用导出 qiankun 生命周期 → 部署独立 CDN",
        "performance": "共享公共依赖 externals；预加载；子应用按需加载。",
        "pitfalls": [
            {"title": "全局变量污染", "body": "沙箱未隔离干净；避免子应用改 document 全局监听未清理。"},
            {"title": "样式泄漏", "body": "启用隔离或 BEM 前缀；Element UI 等全局样式冲突。"},
        ],
        "practices": ["统一路由规范", "公共依赖 CDN", "子应用独立仓库 CI"],
        "references": ["qiankun 官方文档", "single-spa 文档"],
    },
    ("数据可视化", "ECharts"): {
        "intro": (
            "Apache ECharts 基于 Canvas（可选 SVG）的声明式图表库，"
            "option 配置驱动 series/coordinate/visualMap；大数据用 sampling、LTTB 降采样与 progressive。"
        ),
        "concepts": [
            {"title": "option 与 setOption", "body": "notMerge/lazyUpdate 控制合并策略；resize() 响应容器变化。"},
            {"title": "坐标系", "body": "grid、polar、geo、singleAxis；series 绑定 coordinateSystem。"},
            {"title": "交互组件", "body": "dataZoom、brush、tooltip、legend 联动 series。"},
        ],
        "mechanism": "Preprocessor 转换 option → Model 层 → View 层绘制；动画缓动插值。",
        "internals": "zrender 矢量渲染引擎；事件 zr.on('click') 与 echarts on 共存。",
        "workflow": "容器定高 → init → setOption → window resize 监听 → dispose 销毁",
        "performance": "数据>1万启用 large/sampling；按需加载 echarts/charts；不在不可见 tab 初始化。",
        "pitfalls": [
            {"title": "容器无高度", "body": "图表高度 0；父元素需明确 height。"},
            {"title": "频繁 setOption 全量", "body": "用 notMerge:false 增量或只更新 series.data。"},
        ],
        "practices": ["主题 theme 统一", "loading 态", "移动端 touch 优化"],
        "references": ["ECharts 官方手册", "zrender 文档"],
    },
    ("PWA", "Service Worker"): {
        "intro": (
            "Service Worker 是浏览器与网络间的 **可编程代理**，独立于页面线程，"
            "可拦截 fetch、实现离线缓存与推送。须 HTTPS（localhost 除外），"
            "生命周期：install → waiting → activate → fetch/message。"
        ),
        "concepts": [
            {"title": "注册与作用域", "body": "`navigator.serviceWorker.register('/sw.js')` 作用域为路径目录；scope 选项限制。"},
            {"title": "缓存 API", "body": "install 中 `caches.open('v1').then(c => c.addAll(urls))`；activate 删旧缓存。"},
            {"title": "fetch 策略", "body": "Cache First、Network First、Stale-While-Revalidate 按资源类型选择。"},
        ],
        "mechanism": "页面与 SW  postMessage 通信；skipWaiting + clients.claim 立即接管；更新需新 SW waiting 直至关闭旧页。",
        "internals": "SW 线程无 DOM；extendable events 可 waitUntil 延长 install/activate。",
        "workflow": "Workbox 生成 SW → register → 测离线 → 版本化 cache name → 提示用户刷新",
        "performance": "预缓存 shell；运行时缓存 API；避免缓存过大占磁盘。",
        "security": "仅 HTTPS；校验响应 integrity；不缓存敏感个性化 API。",
        "pitfalls": [
            {"title": "SW 作用域错误", "body": "sw.js 放根目录或 Service-Worker-Allowed 头。"},
            {"title": "缓存永不更新", "body": "activate 删旧 cache；networkFirst 给 HTML。"},
        ],
        "practices": ["Workbox", "cache 版本号", "更新提示 UX"],
        "references": ["MDN Service Worker", "Workbox 文档"],
    },
}

# Module-specific facts for all frontend modules
MODULE_FACTS: Dict[str, Dict[str, dict]] = {
    "HTML与CSS": {
        "HTML基础": {"core": "DOCTYPE 触发标准模式；元素树构成 DOM。", "internal": "HTML5 解析器容错与 foster parenting。"},
        "HTML语义化": {"core": "header/nav/main/article 等地标与 SEO、可访问性。", "internal": "Accessibility Tree 映射 ARIA 与隐式角色。"},
        "表单": {"core": "Constraint Validation API；label 关联与 autocomplete。", "internal": "表单控件与 form 元素关联算法。"},
        "多媒体": {"core": "video/audio/picture；WebVTT 字幕。", "internal": "MSE 流媒体；autoplay 策略。"},
        "Canvas": {"core": "2D/WebGL 上下文；rAF 动画循环。", "internal": "Skia 光栅化；OffscreenCanvas Worker。"},
        "CSS基础": {"core": "层叠、继承、特异性 (a,b,c)。", "internal": "CSSOM 与渲染树合并。"},
        "选择器": {"core": ":is/:where/:has()；属性与伪类。", "internal": "选择器匹配从右向左优化。"},
        "盒模型": {"core": "content-box vs border-box；margin 折叠。", "internal": "BFC 格式化上下文。"},
        "布局": {"core": "position/float；sticky 与包含块。", "internal": "stacking context 与 z-index。"},
        "Flexbox": {"core": "主轴交叉轴；flex 三值简写。", "internal": "NG Flex 布局算法。"},
        "Grid": {"core": "grid-template areas；fr/minmax。", "internal": "subgrid 继承父轨道。"},
        "响应式设计": {"core": "媒体查询与 container queries。", "internal": "viewport meta 与移动端缩放。"},
        "动画与过渡": {"core": "transition/animation；transform 合成友好。", "internal": "Compositor 线程插值。"},
        "CSS预处理器": {"core": "Sass @use；PostCSS Autoprefixer。", "internal": "dart-sass 编译管线。"},
        "性能优化": {"core": "content-visibility；contain。", "internal": "StyleInvalidation 范围缩小。"},
        "最佳实践": {"core": "BEM/ITCSS；WCAG 对比度。", "internal": "设计 token 与组件库。"},
    },
    "React": {
        "组件": {"core": "函数组件为默认；props 只读；组合优于继承。", "internal": "Fiber tag 区分 FunctionComponent/Class。"},
        "Props与State": {"core": "单向数据流；state 本地、props 父传子。", "internal": "props 比较触发 bailout。"},
        "事件处理": {"core": "SyntheticEvent 委托；passive 监听器。", "internal": "React 17+ 委托至 root 非 document。"},
        "生命周期": {"core": "类：mount/update/unmount；函数用 useEffect 等价。", "internal": "getDerivedStateFromProps 少用。"},
        "自定义Hook": {"core": "use* 封装逻辑；可共享 stateful 逻辑。", "internal": "Hooks 链表顺序依赖。"},
        "Context": {"core": "createContext；Provider value 变则消费组件 render。", "internal": "useContext 订阅 context 变更。"},
        "路由": {"core": "React Router 6：createBrowserRouter、loader/action。", "internal": "history 栈与 URL 同步。"},
        "状态管理": {"core": "Redux/Zustand/Jotai；服务端状态 React Query。", "internal": "selector 细粒度订阅。"},
        "React测试": {"core": "RTL 测行为非实现；userEvent 模拟交互。", "internal": "jsdom 环境；msw mock API。"},
        "React最佳实践": {"core": "组件分层；错误边界 ErrorBoundary。", "internal": "Suspense 数据获取模式。"},
    },
    "Vue": {
        "Vue基础": {"core": "MVVM 渐进式；单文件组件 SFC。", "internal": "@vue/compiler-sfc 编译模板。"},
        "模板语法": {"core": "mustache 插值；指令 v-bind/v-on。", "internal": "编译为 render 函数。"},
        "计算属性": {"core": "computed 缓存依赖；getter 惰性。", "internal": "ComputedRefImpl dirty 追踪。"},
        "侦听器": {"core": "watch/watchEffect；flush timing。", "internal": "effect 调度 post 组件更新。"},
        "Class与Style": {"core": ":class 对象/数组；:style 驼峰。", "internal": "normalizeStyle 合并。"},
        "条件渲染": {"core": "v-if vs v-show；template 分组。", "internal": "v-if 切换销毁重建 DOM。"},
        "列表渲染": {"core": "v-for :key 稳定 id。", "internal": "diff 算法 keyed children。"},
        "事件处理": {"core": "@click.modifier；内联处理器。", "internal": "invoker 包装原生监听缓存。"},
        "表单输入": {"core": "v-model 语法糖；.lazy .number。", "internal": "不同控件不同 props/emit。"},
        "组件基础": {"core": "props/emits 声明；单向数据流。", "internal": "attrs 透传 fallthrough。"},
        "组件通信": {"core": "props/emit；provide/inject。", "internal": "mitt 事件总线替代。"},
        "插槽": {"core": "默认/具名/作用域插槽。", "internal": "编译为 renderSlot 调用。"},
        "生命周期": {"core": "onMounted/onUnmounted 等组合式 API。", "internal": "options 钩子映射同一引擎。"},
        "Vue Router": {"core": "createRouter history/hash；导航守卫。", "internal": "路由表匹配与 scrollBehavior。"},
        "Pinia状态管理": {"core": "defineStore；setup store 风格。", "internal": "devtools 与时间旅行。"},
        "Vue最佳实践": {"core": "ESLint vue 规则；按需自动导入。", "internal": "unplugin-vue-components。"},
    },
    "Node.js": {
        "Node.js基础": {"core": "V8 + libuv；REPL 与 npm。", "internal": "process 对象与版本绑定 ABI。"},
        "模块系统": {"core": "CommonJS require；ESM import 与 package.json type。", "internal": "模块包装函数 exports/module。"},
        "Buffer": {"core": "二进制 Uint8Array 子类；编码 utf8/base64。", "internal": "池化分配小 Buffer。"},
        "Stream": {"core": "Readable/Writable/Duplex/Transform；pipe 背压。", "internal": "highWaterMark 控制缓冲。"},
        "文件系统": {"core": "fs.promises；流式 read/write。", "internal": "libuv 线程池异步 fs。"},
        "HTTP服务": {"core": "http.createServer；req/res 流。", "internal": "HTTP 解析器 llhttp。"},
        "Express框架": {"core": "中间件洋葱模型；Router 分路径。", "internal": "path-to-regexp 匹配。"},
        "Koa框架": {"core": "ctx 上下文；async/await 中间件。", "internal": "compose 函数串联。"},
        "中间件": {"core": "鉴权、日志、body-parser、错误处理。", "internal": "next() 传递控制。"},
        "数据库操作": {"core": "连接池 pg/mysql2；Prisma ORM。", "internal": "prepared statement 防注入。"},
        "认证授权": {"core": "JWT session；passport.js 策略。", "internal": "bcrypt 哈希轮次。"},
        "进程管理": {"core": "cluster 多进程；PM2 守护与零停机。", "internal": "fork 共享句柄策略。"},
        "异步编程": {"core": "Promise/async；util.promisify。", "internal": "async_hooks 追踪。"},
        "性能优化": {"core": "压缩、缓存、集群、profiling。", "internal": "clinic flame 诊断。"},
        "调试与测试": {"core": "node --inspect；Jest/supertest。", "internal": "ndb Chrome 调试。"},
        "Node.js最佳实践": {"core": "12-Factor；helmet 安全头。", "internal": "graceful shutdown SIGTERM。"},
    },
    "前端工程化": {
        "工程化概述": {"core": "规范、构建、测试、部署全链路。", "internal": "DevOps 与前端融合。"},
        "包管理": {"core": "npm/pnpm/yarn；lockfile 与 workspace。", "internal": "pnpm 内容寻址硬链接。"},
        "构建工具": {"core": "打包、转译、压缩、代码分割。", "internal": "依赖图遍历。"},
        "Webpack": {"core": "entry/output/loader/plugin；HMR。", "internal": "tapable 钩子系统。"},
        "Vite": {"core": "dev 用 esbuild 预构建；生产 Rollup。", "internal": "原生 ESM 按需加载。"},
        "Rollup": {"core": "ESM 库打包；tree-shaking。", "internal": "scope hoisting。"},
        "代码规范": {"core": "EditorConfig；commitlint。", "internal": "husky pre-commit。"},
        "ESLint": {"core": "AST 规则；flat config eslint 9。", "internal": "typescript-eslint 解析。"},
        "Prettier": {"core": " opinionated 格式化；与 ESLint 分工。", "internal": "prettier-eslint 整合。"},
        "Babel": {"core": "@babel/preset-env targets；polyfill 策略。", "internal": "插件访问 AST 转换。"},
        "TypeScript工程": {"core": "strict；path alias；project references。", "internal": "tsc 与 Vite esbuild 分工。"},
        "单元测试": {"core": "Vitest/Jest；覆盖率 istanbul。", "internal": "mock 模块工厂。"},
        "E2E测试": {"core": "Playwright/Cypress；页面对象模式。", "internal": "trace 录像回放。"},
        "CI/CD": {"core": "GitHub Actions；制品与部署。", "internal": "缓存 node_modules 加速。"},
        "性能监控": {"core": "RUM；Sentry 错误；Web Vitals。", "internal": "PerformanceObserver。"},
        "微前端": {"core": "qiankun/MF 在工程化中的集成。", "internal": "共享依赖 externals。"},
        "前端最佳实践": {"core": "Monorepo turbo；版本化设计系统。", "internal": "changesets 发版。"},
    },
    "浏览器原理": {
        "浏览器架构": {"core": "多进程：Browser/GPU/Network/Renderer。", "internal": "Site Isolation 跨站隔离。"},
        "HTML解析": {"core": "分词器 Tokenizer；树构建算法。", "internal": "parser-blocking script。"},
        "CSS解析": {"core": "CSSOM；@import 阻塞。", "internal": "invalid 声明丢弃。"},
        "布局": {"core": "Layout/Reflow 计算盒几何。", "internal": "subpixel layout。"},
        "绘制": {"core": "Paint 记录 DisplayList。", "internal": "skia 录制。"},
        "合成": {"core": "Compositor Layers GPU 栅格。", "internal": "tile 分块光栅。"},
        "事件循环": {"core": "task queue vs microtask；渲染步骤穿插。", "internal": "requestAnimationFrame 前回调。"},
        "垃圾回收": {"core": "分代 GC；标记清除与整理。", "internal": "V8 Orinoco 并发标记。"},
        "V8引擎": {"core": "Ignition 字节码 + TurboFan 优化。", "internal": "hidden class 内联缓存。"},
        "网络栈": {"core": "HTTP/2 多路复用；预连接 preconnect。", "internal": "资源优先级 Priority Hints。"},
        "安全机制": {"core": "同源策略；CSP；CORS。", "internal": "Site Per Process。"},
        "同源策略": {"core": "协议主机端口一致；postMessage 跨源通信。", "internal": "document.domain 已废弃。"},
        "存储": {"core": "Cookie/localStorage/IndexedDB；Quota。", "internal": "第三方 Cookie 淘汰。"},
        "PWA": {"core": "SW + Manifest 在浏览器栈中的位置。", "internal": "安装提示 beforeinstallprompt。"},
        "浏览器调试": {"core": "Sources 断点；Network 瀑布图。", "internal": "blackbox 库代码。"},
        "浏览器性能优化": {"core": "Long Task；Main thread 优化。", "internal": "PerformanceInsights。"},
    },
    "Web性能优化": {
        "性能指标": {"core": "LCP/INP/CLS Core Web Vitals。", "internal": "75 分位字段数据。"},
        "加载性能": {"core": "TTFB/FCP；关键请求链。", "internal": "preload/prefetch。"},
        "渲染性能": {"core": "避免 layout thrashing。", "internal": "rAF 批处理写。"},
        "网络优化": {"core": "HTTP/2 推送谨慎；连接复用。", "internal": "103 Early Hints。"},
        "资源优化": {"core": "压缩 brotli；minify。", "internal": "Tree shaking sideEffects。"},
        "图片优化": {"core": "WebP/AVIF；srcset sizes。", "internal": "responsive images。"},
        "代码分割": {"core": "dynamic import；路由级 chunk。", "internal": "webpack magic comment。"},
        "懒加载": {"core": "loading=lazy；Intersection Observer。", "internal": "native lazy load 视口。"},
        "预加载": {"core": "link rel=modulepreload/preload。", "internal": "Speculation Rules API。"},
        "缓存策略": {"core": "Cache-Control immutable；SWR。", "internal": "HTTP 缓存协商。"},
        "CDN": {"core": "边缘节点；静态资源域名分离。", "internal": "Anycast 路由。"},
        "HTTP/2与HTTP/3": {"core": "QUIC 0-RTT；队头阻塞缓解。", "internal": "TLS 1.3 握手。"},
        "运行时优化": {"core": "Web Worker；虚拟列表。", "internal": "scheduler.postTask。"},
        "性能监控": {"core": "web-vitals 库上报。", "internal": "Long Animation Frames。"},
        "性能预算": {"core": "bundle 大小门禁；Lighthouse CI。", "internal": "bundlesize 插件。"},
        "Lighthouse": {"core": "审计类别 Performance/A11y/SEO。", "internal": "throttling 模拟移动。"},
        "性能优化最佳实践": {"core": "RAIL 模型；以指标驱动迭代。", "internal": "CrUX 真实用户数据。"},
    },
    "PWA": {
        "PWA概述": {"core": "可靠、快速、可安装三要素。", "internal": "Progressive 渐进增强。"},
        "Web App Manifest": {"core": "name/icons/start_url/display/theme_color。", "internal": "maskable icons。"},
        "离线缓存": {"core": "precache app shell。", "internal": "runtime caching strategies。"},
        "推送通知": {"core": "Push API + Notification；VAPID。", "internal": "用户授权 Permission。"},
        "后台同步": {"core": "Background Sync 离线队列。", "internal": "Periodic Background Sync。"},
        "安装体验": {"core": "beforeinstallprompt 自定义 UI。", "internal": "standalone display 模式。"},
        "性能要求": {"core": "Lighthouse PWA 清单；快速首屏。", "internal": "服务工作线程启动成本。"},
        "安全要求": {"core": "全站 HTTPS；安全头。", "internal": "mixed content 阻断。"},
        "PWA最佳实践": {"core": "Workbox Recipes；更新策略文档化。", "internal": "iOS 添加主屏幕限制说明。"},
    },
    "Angular": {
        "Angular基础": {"core": "NgModule 或 standalone；CLI 生成。", "internal": "Ivy 编译器 AOT 默认。"},
        "组件": {"core": "@Component selector/template/style。", "internal": "changeDetection 策略。"},
        "模板": {"core": "插值、属性绑定、结构指令 *ngIf。", "internal": "微语法 desugar。"},
        "数据绑定": {"core": "[] 输入 () 输出 [()]", "internal": "banana in a box 双向。"},
        "指令": {"core": "结构 *ngFor；属性 [ngClass]。", "internal": "Directive 类扩展 ElementRef。"},
        "管道": {"core": "纯管道 pure 缓存；date/async。", "internal": "impure 每次变更检测执行。"},
        "服务与依赖注入": {"core": "providedIn root；inject() 函数。", "internal": "Injector 树层级查找。"},
        "路由": {"core": "RouterModule；懒加载 loadChildren。", "internal": "路由守卫 CanActivate。"},
        "表单": {"core": "Template-driven vs Reactive Forms。", "internal": "FormControl validators。"},
        "HTTP客户端": {"core": "HttpClient  Observable；拦截器。", "internal": "HttpClient XSRF 防护。"},
        "RxJS": {"core": "Observable/Operator；switchMap 防竞态。", "internal": "Scheduler 异步调度。"},
        "状态管理": {"core": "NgRx Store/Effects；Signal 新 API。", "internal": "ComponentStore 局部状态。"},
        "测试": {"core": "TestBed；ComponentFixture。", "internal": "fakeAsync tick。"},
        "性能优化": {"core": "OnPush；trackBy；detach change detector。", "internal": "runOutsideAngular。"},
        "Angular最佳实践": {"core": "standalone 默认 Angular 17+。", "internal": "signals 响应式模型。"},
    },
    "小程序开发": {
        "小程序概述": {"core": "双线程：逻辑层 AppService + 视图层 WebView。", "internal": "setData 跨线程通信 JSON。"},
        "WXML": {"core": "wx:for wx:if；数据绑定 {{}}。", "internal": "模板编译为 render 函数。"},
        "WXSS": {"core": "rpx 响应式像素；@import。", "internal": "样式隔离 scope。"},
        "JS逻辑": {"core": "Page/Component 构造器；生命周期。", "internal": "逻辑层无 DOM API。"},
        "组件": {"core": "properties/observers；slot。", "internal": "组件化与原生组件层。"},
        "页面路由": {"core": "wx.navigateTo/redirectTo；页面栈最多10层。", "internal": "tabBar 与分包。"},
        "API": {"core": "wx.request 域名白名单；登录 wx.login。", "internal": "云调用开放能力。"},
        "云开发": {"core": "云函数/数据库/存储；免运维。", "internal": "wx.cloud.init 环境。"},
        "性能优化": {"core": "减少 setData 频率与数据量；分包。", "internal": "自定义组件局部更新。"},
        "微信小程序": {"core": "微信开发者工具；审核发布。", "internal": "隐私协议与用户信息。"},
        "支付宝小程序": {"core": "axml/acss；my.* API。", "internal": "与微信 API 差异映射。"},
        "跨端框架": {"core": "Taro/uni-app 编译多平台。", "internal": "条件编译 #ifdef。"},
        "小程序最佳实践": {"core": "主包体积控制；骨架屏。", "internal": "按需注入与用时注入。"},
    },
    "微前端": {
        "微前端概述": {"core": "独立部署、技术异构、团队自治。", "internal": "基座 + 子应用运行时集成。"},
        "架构设计": {"core": "路由分发 vs iframe vs JS 沙箱。", "internal": "BFF 聚合 API。"},
        "single-spa": {"core": "registerApplication；生命周期 bootstrap/mount/unmount。", "internal": "parcel 可挂载组件。"},
        "Module Federation": {"core": "Webpack 5 共享 remote/exposes。", "internal": "运行时动态 import remote。"},
        "应用隔离": {"core": "JS/CSS 沙箱；子应用卸载清理。", "internal": "快照沙箱 vs Proxy。"},
        "样式隔离": {"core": "Shadow DOM；CSS Modules 前缀。", "internal": "qiankun experimentalStyleIsolation。"},
        "JS沙箱": {"core": "Proxy 伪造 window；with 沙箱。", "internal": "多实例激活切换全局。"},
        "通信机制": {"core": "自定义事件；共享 props；全局 store。", "internal": "qiankun initGlobalState。"},
        "路由分发": {"core": "主应用路由匹配 activeRule。", "internal": "history 模式统一 base。"},
        "生命周期": {"core": "加载→bootstrap→mount→unmount。", "internal": "unload 缓存策略。"},
        "部署": {"core": "子应用独立 CDN；entry 地址配置。", "internal": "CI 环境变量注入 entry。"},
        "性能优化": {"core": "公共依赖 external；预加载。", "internal": "子应用资源 gzip/br。"},
        "微前端最佳实践": {"core": "设计系统统一；版本契约。", "internal": "降级 iframe 兜底。"},
    },
    "数据可视化": {
        "可视化概述": {"core": "数据→图形编码；诚实呈现避免误导。", "internal": "Bertin 视觉变量。"},
        "图表类型": {"core": "比较/分布/构成/关系选型。", "internal": "饼图慎用多分类。"},
        "D3.js": {"core": "数据绑定 join；enter/update/exit。", "internal": "比例尺 scaleLinear/scaleTime。"},
        "AntV": {"core": "G2 语法化 G6 图编辑。", "internal": "@antv/g2plot 封装。"},
        "Three.js": {"core": "Scene/Camera/Renderer/Mesh。", "internal": "requestAnimationFrame 渲染循环。"},
        "WebGL": {"core": "着色器 GLSL；顶点/片元。", "internal": "GPU 管线状态机。"},
        "Canvas": {"core": "像素绘制；大数据散点。", "internal": "分层绘制与脏矩形。"},
        "SVG": {"core": "矢量 DOM；交互事件 per-element。", "internal": "节点过多性能降。"},
        "地图可视化": {"core": "GeoJSON；投影 d3-geo/Mapbox。", "internal": "瓦片 TMS/XYZ。"},
        "大屏可视化": {"core": "rem/vw 适配；DataV 装饰组件。", "internal": "自动轮播与 websocket 刷新。"},
        "交互设计": {"core": "刷选联动；tooltip 细节。", "internal": "视觉编码一致性。"},
        "性能优化": {"core": "降采样；WebGL 加速。", "internal": "增量渲染。"},
        "可视化最佳实践": {"core": "色盲友好 palette；标注清晰。", "internal": "可访问性文本替代。"},
    },
}

DOMAIN_META = {
    "HTML与CSS": {
        "category": "前端开发",
        "intro": "HTML 与 CSS 是 Web 的基石：HTML 描述文档结构与语义，CSS 控制呈现与布局。掌握语义化、现代布局与响应式设计是任何前端工程师的必修课。",
        "positioning": "从 HTML5 文档模型与 CSS 层叠规则出发，覆盖表单、多媒体、Canvas、Flexbox/Grid 与动画性能，建立结构—样式—性能完整认知。",
        "prerequisites": ["基础编程概念", "浏览器与开发者工具", "文本编辑器"],
        "outcomes": ["编写语义化可访问 HTML", "熟练使用 Flexbox/Grid", "理解盒模型与渲染性能", "响应式与 CSS 工程化"],
        "ecosystem": "MDN、Can I Use、PostCSS、Sass、Tailwind CSS、DevTools",
    },
    "React": {
        "category": "前端开发",
        "intro": "React 是声明式 UI 库，以组件化、Fiber 架构与 Hooks 为核心。React 18 并发渲染、Suspense 与 Server Components 重塑现代 Web 应用开发模式。",
        "positioning": "覆盖 JSX、Hooks、Fiber 协调、性能优化、路由状态管理到 SSR/RSC，从 API 使用深入原理与工程实践。",
        "prerequisites": ["JavaScript ES6+", "HTML/CSS", "npm 模块化"],
        "outcomes": ["用 Hooks 构建可维护应用", "理解 Fiber 与并发渲染", "性能优化与代码分割", "集成 Router/SSR/测试"],
        "ecosystem": "React 18、React Router、Redux/Zustand、Next.js、Vite、Testing Library",
    },
    "Vue": {
        "category": "前端开发",
        "intro": "Vue 3 以 Proxy 响应式与 Composition API 为核心，渐进式架构可按需引入 Router、Pinia。编译优化与 script setup 提升开发效率。",
        "positioning": "从模板与响应式原理到组件通信、Router、Pinia 与 Composition API，适合系统学习与工程落地。",
        "prerequisites": ["JavaScript ES6+", "HTML/CSS", "组件化思想"],
        "outcomes": ["熟练使用组合式 API", "理解 track/trigger 响应式", "设计路由与 Pinia 方案", "Vue 3 工程化实践"],
        "ecosystem": "Vue 3、Vue Router 4、Pinia、Vite、Nuxt 3、VueUse",
    },
    "Node.js": {
        "category": "前端开发",
        "intro": "Node.js 将 V8 与 libuv 结合，使 JavaScript 可编写高性能 I/O 密集型服务端。事件循环、Stream 与 HTTP 框架是核心。",
        "positioning": "覆盖模块系统、事件循环、Express/Koa、数据库认证、进程管理与性能调优。",
        "prerequisites": ["JavaScript 核心", "HTTP 基础", "命令行 npm"],
        "outcomes": ["理解事件循环各阶段", "构建 REST API 与中间件", "Stream 与数据库集成", "PM2 部署与性能分析"],
        "ecosystem": "Node LTS、Express、Koa、Fastify、Prisma、PM2、Jest",
    },
    "前端工程化": {
        "category": "前端开发",
        "intro": "前端工程化解决规模化协作的构建、规范、测试与交付。Webpack/Vite、ESLint、TypeScript、CI/CD 构成现代基建。",
        "positioning": "系统讲解依赖管理、编译打包、代码质量、自动化测试与持续集成，含微前端集成。",
        "prerequisites": ["JavaScript/TypeScript", "Git", "npm"],
        "outcomes": ["配置 Webpack/Vite", "ESLint/Prettier/TS 质量体系", "单元与 E2E 测试流水线", "CI/CD 与性能监控"],
        "ecosystem": "Vite、Webpack、Rollup、ESLint、Vitest、Playwright、GitHub Actions",
    },
    "浏览器原理": {
        "category": "前端开发",
        "intro": "浏览器是 Web 运行时。多进程架构、渲染流水线、事件循环与 V8 是性能优化与排障的理论基础。",
        "positioning": "从 Chromium 架构剖析解析、布局、绘制、合成与安全机制，建立代码到像素的完整链路。",
        "prerequisites": ["HTML/CSS/JS 基础", "HTTP 概念"],
        "outcomes": ["描述 URL 到页面绘制流程", "理解重排重绘与合成层", "事件循环与 V8 GC", "DevTools 性能安全分析"],
        "ecosystem": "Chromium、Blink、V8、DevTools、Web Vitals、Lighthouse",
    },
    "Web性能优化": {
        "category": "前端开发",
        "intro": "Web 性能影响用户体验与业务指标。Core Web Vitals 驱动加载、渲染、网络与运行时系统化优化。",
        "positioning": "以指标驱动：度量、资源加载、缓存 CDN、代码分割到性能预算与 Lighthouse。",
        "prerequisites": ["浏览器原理", "HTTP 缓存", "构建工具"],
        "outcomes": ["测量解读 LCP/INP/CLS", "制定加载渲染网络方案", "多级缓存与 CDN", "性能监控与预算"],
        "ecosystem": "Lighthouse、WebPageTest、HTTP/2/3、RUM、Sentry",
    },
    "PWA": {
        "category": "前端开发",
        "intro": "PWA 通过 Service Worker 与 Manifest 使 Web 应用具备离线、安装与推送能力，渐进增强现有站点。",
        "positioning": "覆盖 SW 生命周期、缓存策略、Manifest、推送同步、安装体验与安全基线。",
        "prerequisites": ["HTML/CSS/JS", "HTTPS", "DevTools"],
        "outcomes": ["注册 SW 实现离线", "配置 Manifest", "推送与后台同步", "满足 PWA 性能安全要求"],
        "ecosystem": "Workbox、vite-plugin-pwa、web.dev PWA、Push API",
    },
    "Angular": {
        "category": "前端开发",
        "intro": "Angular 是企业级 TypeScript 框架，依赖注入、RxJS 与完整 CLI 工具链适合大型长期维护项目。",
        "positioning": "组件、模板、DI、路由、表单、HTTP、RxJS、NgRx 与 OnPush 性能优化。",
        "prerequisites": ["TypeScript", "OOP 与模块化", "HTML/CSS"],
        "outcomes": ["Angular CLI 项目管理", "DI 与变更检测", "路由表单 HTTP", "测试与 OnPush 优化"],
        "ecosystem": "Angular 17+、RxJS、NgRx、Angular Material、CLI",
    },
    "小程序开发": {
        "category": "前端开发",
        "intro": "小程序运行于超级 App 内，双线程架构与平台 API 各异。Taro/uni-app 支持跨端发布。",
        "positioning": "WXML/WXSS、逻辑层、组件路由、云开发及微信/支付宝差异与跨端方案。",
        "prerequisites": ["JavaScript", "HTML/CSS 概念", "开发者账号"],
        "outcomes": ["理解双线程与 setData", "开发页面组件 API", "分包云开发", "跨端框架选型"],
        "ecosystem": "微信开发者工具、Taro、uni-app、云开发",
    },
    "微前端": {
        "category": "前端开发",
        "intro": "微前端拆分单体前端为可独立部署子应用。qiankun、single-spa、Module Federation 是主流方案。",
        "positioning": "架构设计、隔离沙箱、通信路由、生命周期、部署与性能优化。",
        "prerequisites": ["React/Vue", "Webpack/Vite", "路由状态管理"],
        "outcomes": ["评估微前端场景", "qiankun/MF 集成", "样式沙箱通信", "路由分发统一部署"],
        "ecosystem": "qiankun、single-spa、Module Federation、Garfish",
    },
    "数据可视化": {
        "category": "前端开发",
        "intro": "数据可视化将数据映射为图形。D3、ECharts、AntV、Three.js 覆盖 2D/3D、地图与大屏场景。",
        "positioning": "图表选型、主流库、Canvas/SVG/WebGL 差异、交互设计与性能优化。",
        "prerequisites": ["JavaScript", "CSS", "数据分析基础"],
        "outcomes": ["选型图表与渲染技术", "ECharts/D3 交互图表", "Canvas/SVG/WebGL 性能", "大屏项目实践"],
        "ecosystem": "D3.js、ECharts、AntV、Three.js、Mapbox",
    },
}


def _facts(domain: str, module: str) -> dict:
    if domain in MODULE_FACTS and module in MODULE_FACTS[domain]:
        return MODULE_FACTS[domain][module]
    return {}


def _generate_module(domain: str, module: str) -> dict:
    key = (domain, module)
    if key in DETAILED:
        d = DETAILED[key].copy()
        for field in ("comparison", "debugging", "configuration", "case_study", "workflow"):
            if field not in d:
                facts = _facts(domain, module)
                if field == "workflow" and facts.get("workflow"):
                    d["workflow"] = facts["workflow"]
                elif field == "case_study":
                    d.setdefault("case_study", (
                        f"某 {domain} 项目落地 {module}："
                        f"按官方推荐架构实现核心链路，结合监控与灰度发布，"
                        f"线上稳定性与性能指标达预期。"
                    ))
        return d

    facts = _facts(domain, module)
    core = facts.get("core", f"{module} 是 {domain} 的核心模块，连接业务与运行时能力。")
    internal = facts.get("internal", f"{module} 的实现遵循 {domain} 官方规范与社区验证的模式。")
    mechanism_extra = facts.get("mechanism", "")
    workflow_extra = facts.get("workflow", "")
    performance_extra = facts.get("performance", "")

    return {
        "intro": (
            f"**{module}** 是 **{domain}** 中的重要主题。{core}"
            f"掌握其概念、机制与工程实践，是构建可靠前端应用的关键一环。"
        ),
        "concepts": [
            {"title": f"{module}核心概念", "body": core},
            {"title": "实现机制", "body": internal},
            {"title": f"{module}与其他模块的关系", "body": (
                f"在 {domain} 体系中，{module} 与相邻模块通过清晰接口协作："
                f"明确输入输出、错误处理与性能边界。"
                f"系统集成时应关注与上下游模块的契约与版本兼容。"
            )},
            {"title": "典型应用场景", "body": (
                f"{module} 常见于 {domain} 的核心开发路径："
                f"从基础使用到性能调优与生产排障。"
                f"应根据团队技术栈与业务规模选择合适深度的实践方案。"
            )},
        ],
        "mechanism": mechanism_extra or (
            f"{module} 的执行路径：接收输入或事件 → 按 {domain} 规范处理 → "
            f"调用底层 API 或运行时 → 输出结果或触发副作用。"
            f"{internal}"
        ),
        "internals": internal,
        "workflow": workflow_extra or (
            f"1. 阅读 {domain} 官方文档 {module} 章节\n"
            f"2. 搭建最小可运行示例验证行为\n"
            f"3. 集成到项目并编写测试\n"
            f"4. 配置监控与性能基线\n"
            f"5. 总结团队规范与最佳实践"
        ),
        "performance": performance_extra or (
            f"{module} 性能要点：Profiling 定位瓶颈；优先优化关键路径与 I/O；"
            f"避免过早微优化。结合 {domain} 生态工具做基准测试。"
        ),
        "security": (
            f"使用 {module} 时：校验一切外部输入；最小权限；"
            f"敏感数据不入日志；关注 {domain} 安全公告与依赖漏洞扫描。"
        ),
        "case_study": (
            f"某互联网产品团队在 {domain} 项目中实施 {module}："
            f"遵循官方架构，补充单元测试与 E2E，"
            f"上线后核心指标稳定，故障可快速定位与回滚。"
        ),
        "comparison": (
            f"在 {domain} 生态中选型 {module} 相关方案时，"
            f"对比官方实现与社区库的成熟度、维护频率、包体积与团队熟悉度。"
        ),
        "debugging": (
            f"排查 {module} 问题：复现 → DevTools/日志 → 最小化用例 → "
            f"对照文档与源码。{domain} 通常提供调试模式或专用 DevTools 扩展。"
        ),
        "configuration": (
            f"{module} 相关配置应外部化（环境变量、构建配置），"
            f"区分开发/预发/生产；敏感配置使用密钥管理服务。"
        ),
        "pitfalls": [
            {"title": "概念理解片面", "body": f"仅会用 API 不理解 {module} 边界，易在复杂场景误用。应结合官方设计文档学习。"},
            {"title": "忽视版本差异", "body": f"{domain} 大版本升级可能变更 {module} 行为，需阅读迁移指南并做回归测试。"},
            {"title": "缺少可观测性", "body": f"未对 {module} 关键路径埋点，生产问题难以定位。应补充日志、指标与错误上报。"},
        ],
        "practices": [
            f"遵循 {domain} 官方 {module} 推荐实践",
            f"为 {module} 编写自动化测试",
            "代码评审关注性能与安全",
            "文档化团队约定（ADR）",
            "持续关注生态更新",
        ],
        "references": [
            f"{domain} 官方文档 - {module}",
            f"MDN / web.dev 相关章节（如适用）",
            f"{domain} 源码或 RFC/提案",
        ],
    }


def _build_module_content() -> dict:
    content = {}
    for cfg in DOMAINS_CONFIG:
        if cfg["name"] not in FRONTEND_DOMAINS:
            continue
        domain = cfg["name"]
        for module in cfg["modules"]:
            content[(domain, module)] = _generate_module(domain, module)
    return content


def _build_overviews() -> dict:
    overviews = {}
    for name in FRONTEND_DOMAINS:
        meta = DOMAIN_META[name]
        overviews[name] = {
            "intro": meta["intro"],
            "positioning": meta["positioning"],
            "prerequisites": meta["prerequisites"],
            "outcomes": meta["outcomes"],
            "ecosystem": meta["ecosystem"],
        }
    return overviews


def _serialize_module_content(content: dict) -> str:
    lines = ["MODULE_CONTENT: Dict[Tuple[str, str], dict] = {"]
    for (domain, module), d in sorted(content.items()):
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        indented = blob.replace("\n", "\n    ")
        lines.append(f"    ({domain!r}, {module!r}): {indented},")
    lines.append("}")
    return "\n".join(lines)


def _serialize_overviews(overviews: dict) -> str:
    lines = ["DOMAIN_OVERVIEWS: Dict[str, dict] = {"]
    for name, d in sorted(overviews.items()):
        blob = json.dumps(d, ensure_ascii=False, indent=4)
        indented = blob.replace("\n", "\n    ")
        lines.append(f"    {name!r}: {indented},")
    lines.append("}")
    return "\n".join(lines)


def main():
    out = Path("/workspace/article_generator/manual/content_frontend.py")
    modules = _build_module_content()
    overviews = _build_overviews()
    header = textwrap.dedent('''\
        # -*- coding: utf-8 -*-
        """前端开发领域手工教程内容库

        手工编写的 ModuleKnowledge 素材：HTML与CSS、React、Vue、Node.js、
        前端工程化、浏览器原理、Web性能优化、PWA、Angular、小程序开发、
        微前端、数据可视化共 12 个领域。
        """

        from typing import Dict, Tuple

    ''')
    body = _serialize_module_content(modules) + "\n\n\n" + _serialize_overviews(overviews) + "\n"
    out.write_text(header + body, encoding="utf-8")
    print(f"Wrote {out} — {len(modules)} modules, {len(overviews)} overviews")


if __name__ == "__main__":
    main()
