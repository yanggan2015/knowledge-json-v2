# PWA 学习指南

> **分类**：前端开发 ｜ **技术生态**：Workbox、vite-plugin-pwa、web.dev PWA、Push API


## 领域定位

PWA 通过 Service Worker 与 Manifest 使 Web 应用具备离线、安装与推送能力，渐进增强现有站点。

覆盖 SW 生命周期、缓存策略、Manifest、推送同步、安装体验与安全基线。

本领域常用技术栈与工具包括：Workbox、vite-plugin-pwa、web.dev PWA、Push API。

## 学习目标

- 注册 SW 实现离线
- 配置 Manifest
- 推送与后台同步
- 满足 PWA 性能安全要求

## 前置知识

- HTML/CSS/JS
- HTTPS
- DevTools

## 学习路径

```mermaid
flowchart TD
    M0[PWA概述]
    M1[Service Worker]
    M2[Web App Manifest]
    M3[离线缓存]
    M4[推送通知]
    M5[后台同步]
    M6[安装体验]
    M7[性能要求]
    M0 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> M5
    M5 --> M6
    M6 --> M7
```

1. **PWA概述**
2. **Service Worker**
3. **Web App Manifest**
4. **离线缓存**
5. **推送通知**
6. **后台同步**
7. **安装体验**
8. **性能要求**

## 模块体系

- **PWA概述**
- **Service Worker**
- **Web App Manifest**
- **离线缓存**
- **推送通知**
- **后台同步**
- **安装体验**
- **性能要求**
- **安全要求**
- **PWA最佳实践**

## 难度分布

| 入门 | 12 | 20% |
| 实战 | 12 | 20% |
| 进阶 | 18 | 30% |
| 高级 | 18 | 30% |

## 章节索引

### PWA概述

- [PWA概述核心概念与原理](chapters/001-PWA概述核心概念与原理.md) ｜ 入门
- [PWA概述的实现机制详解](chapters/002-PWA概述的实现机制详解.md) ｜ 入门
- [PWA概述的关键技术点](chapters/003-PWA概述的关键技术点.md) ｜ 入门
- [PWA概述的源码级分析](chapters/004-PWA概述的源码级分析.md) ｜ 入门
- [PWA概述的配置与使用](chapters/005-PWA概述的配置与使用.md) ｜ 入门
- [PWA概述的常见问题与解决方案](chapters/006-PWA概述的常见问题与解决方案.md) ｜ 入门

### Service Worker

- [Service Worker核心概念与原理](chapters/007-Service-Worker核心概念与原理.md) ｜ 入门
- [Service Worker的实现机制详解](chapters/008-Service-Worker的实现机制详解.md) ｜ 入门
- [Service Worker的关键技术点](chapters/009-Service-Worker的关键技术点.md) ｜ 入门
- [Service Worker的源码级分析](chapters/010-Service-Worker的源码级分析.md) ｜ 入门
- [Service Worker的配置与使用](chapters/011-Service-Worker的配置与使用.md) ｜ 入门
- [Service Worker的常见问题与解决方案](chapters/012-Service-Worker的常见问题与解决方案.md) ｜ 入门

### Web App Manifest

- [Web App Manifest核心概念与原理](chapters/013-Web-App-Manifest核心概念与原理.md) ｜ 进阶
- [Web App Manifest的实现机制详解](chapters/014-Web-App-Manifest的实现机制详解.md) ｜ 进阶
- [Web App Manifest的关键技术点](chapters/015-Web-App-Manifest的关键技术点.md) ｜ 进阶
- [Web App Manifest的源码级分析](chapters/016-Web-App-Manifest的源码级分析.md) ｜ 进阶
- [Web App Manifest的配置与使用](chapters/017-Web-App-Manifest的配置与使用.md) ｜ 进阶
- [Web App Manifest的常见问题与解决方案](chapters/018-Web-App-Manifest的常见问题与解决方案.md) ｜ 进阶

### 离线缓存

- [离线缓存核心概念与原理](chapters/019-离线缓存核心概念与原理.md) ｜ 进阶
- [离线缓存的实现机制详解](chapters/020-离线缓存的实现机制详解.md) ｜ 进阶
- [离线缓存的关键技术点](chapters/021-离线缓存的关键技术点.md) ｜ 进阶
- [离线缓存的源码级分析](chapters/022-离线缓存的源码级分析.md) ｜ 进阶
- [离线缓存的配置与使用](chapters/023-离线缓存的配置与使用.md) ｜ 进阶
- [离线缓存的常见问题与解决方案](chapters/024-离线缓存的常见问题与解决方案.md) ｜ 进阶

### 推送通知

- [推送通知核心概念与原理](chapters/025-推送通知核心概念与原理.md) ｜ 进阶
- [推送通知的实现机制详解](chapters/026-推送通知的实现机制详解.md) ｜ 进阶
- [推送通知的关键技术点](chapters/027-推送通知的关键技术点.md) ｜ 进阶
- [推送通知的源码级分析](chapters/028-推送通知的源码级分析.md) ｜ 进阶
- [推送通知的配置与使用](chapters/029-推送通知的配置与使用.md) ｜ 进阶
- [推送通知的常见问题与解决方案](chapters/030-推送通知的常见问题与解决方案.md) ｜ 进阶

### 后台同步

- [后台同步核心概念与原理](chapters/031-后台同步核心概念与原理.md) ｜ 高级
- [后台同步的实现机制详解](chapters/032-后台同步的实现机制详解.md) ｜ 高级
- [后台同步的关键技术点](chapters/033-后台同步的关键技术点.md) ｜ 高级
- [后台同步的源码级分析](chapters/034-后台同步的源码级分析.md) ｜ 高级
- [后台同步的配置与使用](chapters/035-后台同步的配置与使用.md) ｜ 高级
- [后台同步的常见问题与解决方案](chapters/036-后台同步的常见问题与解决方案.md) ｜ 高级

### 安装体验

- [安装体验核心概念与原理](chapters/037-安装体验核心概念与原理.md) ｜ 高级
- [安装体验的实现机制详解](chapters/038-安装体验的实现机制详解.md) ｜ 高级
- [安装体验的关键技术点](chapters/039-安装体验的关键技术点.md) ｜ 高级
- [安装体验的源码级分析](chapters/040-安装体验的源码级分析.md) ｜ 高级
- [安装体验的配置与使用](chapters/041-安装体验的配置与使用.md) ｜ 高级
- [安装体验的常见问题与解决方案](chapters/042-安装体验的常见问题与解决方案.md) ｜ 高级

### 性能要求

- [性能要求核心概念与原理](chapters/043-性能要求核心概念与原理.md) ｜ 高级
- [性能要求的实现机制详解](chapters/044-性能要求的实现机制详解.md) ｜ 高级
- [性能要求的关键技术点](chapters/045-性能要求的关键技术点.md) ｜ 高级
- [性能要求的源码级分析](chapters/046-性能要求的源码级分析.md) ｜ 高级
- [性能要求的配置与使用](chapters/047-性能要求的配置与使用.md) ｜ 高级
- [性能要求的常见问题与解决方案](chapters/048-性能要求的常见问题与解决方案.md) ｜ 高级

### 安全要求

- [安全要求核心概念与原理](chapters/049-安全要求核心概念与原理.md) ｜ 实战
- [安全要求的实现机制详解](chapters/050-安全要求的实现机制详解.md) ｜ 实战
- [安全要求的关键技术点](chapters/051-安全要求的关键技术点.md) ｜ 实战
- [安全要求的源码级分析](chapters/052-安全要求的源码级分析.md) ｜ 实战
- [安全要求的配置与使用](chapters/053-安全要求的配置与使用.md) ｜ 实战
- [安全要求的常见问题与解决方案](chapters/054-安全要求的常见问题与解决方案.md) ｜ 实战

### PWA最佳实践

- [PWA最佳实践核心概念与原理](chapters/055-PWA最佳实践核心概念与原理.md) ｜ 实战
- [PWA最佳实践的实现机制详解](chapters/056-PWA最佳实践的实现机制详解.md) ｜ 实战
- [PWA最佳实践的关键技术点](chapters/057-PWA最佳实践的关键技术点.md) ｜ 实战
- [PWA最佳实践的源码级分析](chapters/058-PWA最佳实践的源码级分析.md) ｜ 实战
- [PWA最佳实践的配置与使用](chapters/059-PWA最佳实践的配置与使用.md) ｜ 实战
- [PWA最佳实践的常见问题与解决方案](chapters/060-PWA最佳实践的常见问题与解决方案.md) ｜ 实战


---
*领域: PWA*