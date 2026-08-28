#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate frontend.py with high-quality Chinese tutorial content."""

from __future__ import annotations

OUTPUT = "/workspace/article_generator/manual/domains/frontend.py"

DOMAINS = {
    "HTML与CSS": [
        "HTML基础", "HTML语义化", "表单", "多媒体", "Canvas",
        "CSS基础", "选择器", "盒模型", "布局", "Flexbox",
        "Grid", "响应式设计", "动画与过渡", "CSS预处理器", "性能优化", "最佳实践",
    ],
    "React": [
        "React基础", "JSX", "组件", "Props与State", "事件处理",
        "生命周期", "Hooks", "useState", "useEffect", "自定义Hook",
        "Context", "性能优化", "路由", "状态管理", "服务端渲染",
        "React测试", "React最佳实践",
    ],
    "Vue": [
        "Vue基础", "模板语法", "计算属性", "侦听器", "Class与Style",
        "条件渲染", "列表渲染", "事件处理", "表单输入", "组件基础",
        "组件通信", "插槽", "生命周期", "Vue Router", "Pinia状态管理",
        "组合式API", "Vue3新特性", "Vue最佳实践",
    ],
    "Node.js": [
        "Node.js基础", "模块系统", "事件循环", "Buffer", "Stream",
        "文件系统", "HTTP服务", "Express框架", "Koa框架", "中间件",
        "数据库操作", "认证授权", "进程管理", "异步编程", "性能优化",
        "调试与测试", "Node.js最佳实践",
    ],
    "前端工程化": [
        "工程化概述", "包管理", "构建工具", "Webpack", "Vite",
        "Rollup", "代码规范", "ESLint", "Prettier", "Babel",
        "TypeScript工程", "单元测试", "E2E测试", "CI/CD", "性能监控",
        "微前端", "前端最佳实践",
    ],
    "浏览器原理": [
        "浏览器架构", "渲染流程", "HTML解析", "CSS解析", "布局",
        "绘制", "合成", "事件循环", "垃圾回收", "V8引擎",
        "网络栈", "安全机制", "同源策略", "存储", "PWA",
        "浏览器调试", "浏览器性能优化",
    ],
    "Web性能优化": [
        "性能指标", "加载性能", "渲染性能", "网络优化", "资源优化",
        "图片优化", "代码分割", "懒加载", "预加载", "缓存策略",
        "CDN", "HTTP/2与HTTP/3", "运行时优化", "性能监控", "性能预算",
        "Lighthouse", "性能优化最佳实践",
    ],
    "PWA": [
        "PWA概述", "Service Worker", "Web App Manifest", "离线缓存", "推送通知",
        "后台同步", "后台同步", "安装体验", "性能要求", "安全要求", "PWA最佳实践",
    ],
    "Angular": [
        "Angular基础", "组件", "模板", "数据绑定", "指令",
        "管道", "服务与依赖注入", "路由", "表单", "HTTP客户端",
        "RxJS", "状态管理", "测试", "性能优化", "Angular最佳实践",
    ],
    "小程序开发": [
        "小程序概述", "WXML", "WXSS", "JS逻辑", "组件",
        "页面路由", "API", "云开发", "性能优化", "微信小程序",
        "支付宝小程序", "跨端框架", "小程序最佳实践",
    ],
    "微前端": [
        "微前端概述", "架构设计", "qiankun", "single-spa", "Module Federation",
        "应用隔离", "样式隔离", "JS沙箱", "通信机制", "路由分发",
        "生命周期", "部署", "性能优化", "微前端最佳实践",
    ],
    "数据可视化": [
        "可视化概述", "图表类型", "D3.js", "ECharts", "AntV",
        "Three.js", "WebGL", "Canvas", "SVG", "地图可视化",
        "大屏可视化", "交互设计", "性能优化", "可视化最佳实践",
    ],
}

# Fix PWA duplicate
DOMAINS["PWA"] = [
    "PWA概述", "Service Worker", "Web App Manifest", "离线缓存", "推送通知",
    "后台同步", "安装体验", "性能要求", "安全要求", "PWA最佳实践",
]
