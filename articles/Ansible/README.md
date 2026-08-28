# Ansible 学习指南

> **分类**：DevOps ｜ **技术生态**：Ansible Galaxy、AWX、Terraform（互补）


## 领域定位

Ansible 无 agent，通过 SSH/WinRM 推送 YAML Playbook 实现配置管理与应用部署，幂等模块保证 repeated run 安全。

覆盖 Inventory、Playbook、Role、Vault 与 AWX/Tower 调度。

本领域常用技术栈与工具包括：Ansible Galaxy、AWX、Terraform（互补）。

## 学习目标

- 能编写 idempotent Playbook
- 能组织 Role 与 Galaxy
- 能用 Vault 加密敏感变量
- 能对接 CI 动态 Inventory

## 前置知识

- YAML
- SSH
- Linux 管理基础

## 学习路径

```mermaid
flowchart TD
    M0[Ansible基础]
    M1[Inventory]
    M2[Ad-Hoc]
    M3[Playbook]
    M4[Role]
    M5[模块]
    M6[变量]
    M7[模板]
    M0 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> M5
    M5 --> M6
    M6 --> M7
```

1. **Ansible基础**
2. **Inventory**
3. **Ad-Hoc**
4. **Playbook**
5. **Role**
6. **模块**
7. **变量**
8. **模板**

## 模块体系

- **Ansible基础**
- **Inventory**
- **Ad-Hoc**
- **Playbook**
- **Role**
- **模块**
- **变量**
- **模板**
- **条件循环**
- **标签**
- **Vault**
- **最佳实践**

## 难度分布

| 入门 | 15 | 25% |
| 实战 | 15 | 25% |
| 进阶 | 15 | 25% |
| 高级 | 15 | 25% |

## 章节索引

### Ansible基础

- [Ansible基础核心概念与原理](chapters/001-Ansible基础核心概念与原理.md) ｜ 入门
- [Ansible基础的实现机制详解](chapters/002-Ansible基础的实现机制详解.md) ｜ 入门
- [Ansible基础的关键技术点](chapters/003-Ansible基础的关键技术点.md) ｜ 入门
- [Ansible基础的源码级分析](chapters/004-Ansible基础的源码级分析.md) ｜ 入门
- [Ansible基础的配置与使用](chapters/005-Ansible基础的配置与使用.md) ｜ 入门

### Inventory

- [Inventory核心概念与原理](chapters/006-Inventory核心概念与原理.md) ｜ 入门
- [Inventory的实现机制详解](chapters/007-Inventory的实现机制详解.md) ｜ 入门
- [Inventory的关键技术点](chapters/008-Inventory的关键技术点.md) ｜ 入门
- [Inventory的源码级分析](chapters/009-Inventory的源码级分析.md) ｜ 入门
- [Inventory的配置与使用](chapters/010-Inventory的配置与使用.md) ｜ 入门

### Ad-Hoc

- [Ad-Hoc核心概念与原理](chapters/011-Ad-Hoc核心概念与原理.md) ｜ 入门
- [Ad-Hoc的实现机制详解](chapters/012-Ad-Hoc的实现机制详解.md) ｜ 入门
- [Ad-Hoc的关键技术点](chapters/013-Ad-Hoc的关键技术点.md) ｜ 入门
- [Ad-Hoc的源码级分析](chapters/014-Ad-Hoc的源码级分析.md) ｜ 入门
- [Ad-Hoc的配置与使用](chapters/015-Ad-Hoc的配置与使用.md) ｜ 入门

### Playbook

- [Playbook核心概念与原理](chapters/016-Playbook核心概念与原理.md) ｜ 进阶
- [Playbook的实现机制详解](chapters/017-Playbook的实现机制详解.md) ｜ 进阶
- [Playbook的关键技术点](chapters/018-Playbook的关键技术点.md) ｜ 进阶
- [Playbook的源码级分析](chapters/019-Playbook的源码级分析.md) ｜ 进阶
- [Playbook的配置与使用](chapters/020-Playbook的配置与使用.md) ｜ 进阶

### Role

- [Role核心概念与原理](chapters/021-Role核心概念与原理.md) ｜ 进阶
- [Role的实现机制详解](chapters/022-Role的实现机制详解.md) ｜ 进阶
- [Role的关键技术点](chapters/023-Role的关键技术点.md) ｜ 进阶
- [Role的源码级分析](chapters/024-Role的源码级分析.md) ｜ 进阶
- [Role的配置与使用](chapters/025-Role的配置与使用.md) ｜ 进阶

### 模块

- [模块核心概念与原理](chapters/026-模块核心概念与原理.md) ｜ 进阶
- [模块的实现机制详解](chapters/027-模块的实现机制详解.md) ｜ 进阶
- [模块的关键技术点](chapters/028-模块的关键技术点.md) ｜ 进阶
- [模块的源码级分析](chapters/029-模块的源码级分析.md) ｜ 进阶
- [模块的配置与使用](chapters/030-模块的配置与使用.md) ｜ 进阶

### 变量

- [变量核心概念与原理](chapters/031-变量核心概念与原理.md) ｜ 高级
- [变量的实现机制详解](chapters/032-变量的实现机制详解.md) ｜ 高级
- [变量的关键技术点](chapters/033-变量的关键技术点.md) ｜ 高级
- [变量的源码级分析](chapters/034-变量的源码级分析.md) ｜ 高级
- [变量的配置与使用](chapters/035-变量的配置与使用.md) ｜ 高级

### 模板

- [模板核心概念与原理](chapters/036-模板核心概念与原理.md) ｜ 高级
- [模板的实现机制详解](chapters/037-模板的实现机制详解.md) ｜ 高级
- [模板的关键技术点](chapters/038-模板的关键技术点.md) ｜ 高级
- [模板的源码级分析](chapters/039-模板的源码级分析.md) ｜ 高级
- [模板的配置与使用](chapters/040-模板的配置与使用.md) ｜ 高级

### 条件循环

- [条件循环核心概念与原理](chapters/041-条件循环核心概念与原理.md) ｜ 高级
- [条件循环的实现机制详解](chapters/042-条件循环的实现机制详解.md) ｜ 高级
- [条件循环的关键技术点](chapters/043-条件循环的关键技术点.md) ｜ 高级
- [条件循环的源码级分析](chapters/044-条件循环的源码级分析.md) ｜ 高级
- [条件循环的配置与使用](chapters/045-条件循环的配置与使用.md) ｜ 高级

### 标签

- [标签核心概念与原理](chapters/046-标签核心概念与原理.md) ｜ 实战
- [标签的实现机制详解](chapters/047-标签的实现机制详解.md) ｜ 实战
- [标签的关键技术点](chapters/048-标签的关键技术点.md) ｜ 实战
- [标签的源码级分析](chapters/049-标签的源码级分析.md) ｜ 实战
- [标签的配置与使用](chapters/050-标签的配置与使用.md) ｜ 实战

### Vault

- [Vault核心概念与原理](chapters/051-Vault核心概念与原理.md) ｜ 实战
- [Vault的实现机制详解](chapters/052-Vault的实现机制详解.md) ｜ 实战
- [Vault的关键技术点](chapters/053-Vault的关键技术点.md) ｜ 实战
- [Vault的源码级分析](chapters/054-Vault的源码级分析.md) ｜ 实战
- [Vault的配置与使用](chapters/055-Vault的配置与使用.md) ｜ 实战

### 最佳实践

- [最佳实践核心概念与原理](chapters/056-最佳实践核心概念与原理.md) ｜ 实战
- [最佳实践的实现机制详解](chapters/057-最佳实践的实现机制详解.md) ｜ 实战
- [最佳实践的关键技术点](chapters/058-最佳实践的关键技术点.md) ｜ 实战
- [最佳实践的源码级分析](chapters/059-最佳实践的源码级分析.md) ｜ 实战
- [最佳实践的配置与使用](chapters/060-最佳实践的配置与使用.md) ｜ 实战


---
*领域: Ansible*