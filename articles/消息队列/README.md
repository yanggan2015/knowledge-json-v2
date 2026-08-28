# 消息队列 学习指南

> **分类**：后端开发 ｜ **技术生态**：Kafka、RabbitMQ、RocketMQ、Pulsar、Spring AMQP


## 领域定位

消息队列解耦生产者与消费者，提供异步、削峰与最终一致性。Kafka 适合日志流，RabbitMQ 适合复杂路由，RocketMQ 适合事务消息。

覆盖消息模型、可靠性、顺序、事务与死信，是分布式系统必备基础设施。

本领域常用技术栈与工具包括：Kafka、RabbitMQ、RocketMQ、Pulsar、Spring AMQP。

## 学习目标

- 能选型 Kafka/RabbitMQ/RocketMQ
- 能保证 at-least-once 与幂等消费
- 能设计延迟队列与死信处理
- 能监控 lag 与 rebalance

## 前置知识

- 并发编程
- 网络基础
- 数据库事务概念

## 学习路径

```mermaid
flowchart TD
    M0[消息队列概述]
    M1[JMS]
    M2[AMQP]
    M3[Kafka]
    M4[RabbitMQ]
    M5[RocketMQ]
    M6[Pulsar]
    M7[消息模型]
    M0 --> M1
    M1 --> M2
    M2 --> M3
    M3 --> M4
    M4 --> M5
    M5 --> M6
    M6 --> M7
```

1. **消息队列概述**
2. **JMS**
3. **AMQP**
4. **Kafka**
5. **RabbitMQ**
6. **RocketMQ**
7. **Pulsar**
8. **消息模型**

## 模块体系

- **消息队列概述**
- **JMS**
- **AMQP**
- **Kafka**
- **RabbitMQ**
- **RocketMQ**
- **Pulsar**
- **消息模型**
- **消息可靠性**
- **消息顺序**
- **消息事务**
- **死信队列**
- **延迟队列**
- **性能优化**
- **最佳实践**

## 难度分布

| 入门 | 21 | 21% |
| 实战 | 18 | 18% |
| 进阶 | 28 | 28% |
| 高级 | 33 | 33% |

## 章节索引

### 消息队列概述

- [消息队列概述核心概念与原理](chapters/001-消息队列概述核心概念与原理.md) ｜ 入门
- [消息队列概述的实现机制详解](chapters/002-消息队列概述的实现机制详解.md) ｜ 入门
- [消息队列概述的关键技术点](chapters/003-消息队列概述的关键技术点.md) ｜ 入门
- [消息队列概述的源码级分析](chapters/004-消息队列概述的源码级分析.md) ｜ 入门
- [消息队列概述的配置与使用](chapters/005-消息队列概述的配置与使用.md) ｜ 入门
- [消息队列概述的常见问题与解决方案](chapters/006-消息队列概述的常见问题与解决方案.md) ｜ 入门
- [消息队列概述的性能优化技巧](chapters/007-消息队列概述的性能优化技巧.md) ｜ 入门

### JMS

- [JMS核心概念与原理](chapters/008-JMS核心概念与原理.md) ｜ 入门
- [JMS的实现机制详解](chapters/009-JMS的实现机制详解.md) ｜ 入门
- [JMS的关键技术点](chapters/010-JMS的关键技术点.md) ｜ 入门
- [JMS的源码级分析](chapters/011-JMS的源码级分析.md) ｜ 入门
- [JMS的配置与使用](chapters/012-JMS的配置与使用.md) ｜ 入门
- [JMS的常见问题与解决方案](chapters/013-JMS的常见问题与解决方案.md) ｜ 入门
- [JMS的性能优化技巧](chapters/014-JMS的性能优化技巧.md) ｜ 入门

### AMQP

- [AMQP核心概念与原理](chapters/015-AMQP核心概念与原理.md) ｜ 入门
- [AMQP的实现机制详解](chapters/016-AMQP的实现机制详解.md) ｜ 入门
- [AMQP的关键技术点](chapters/017-AMQP的关键技术点.md) ｜ 入门
- [AMQP的源码级分析](chapters/018-AMQP的源码级分析.md) ｜ 入门
- [AMQP的配置与使用](chapters/019-AMQP的配置与使用.md) ｜ 入门
- [AMQP的常见问题与解决方案](chapters/020-AMQP的常见问题与解决方案.md) ｜ 入门
- [AMQP的性能优化技巧](chapters/021-AMQP的性能优化技巧.md) ｜ 入门

### Kafka

- [Kafka核心概念与原理](chapters/022-Kafka核心概念与原理.md) ｜ 进阶
- [Kafka的实现机制详解](chapters/023-Kafka的实现机制详解.md) ｜ 进阶
- [Kafka的关键技术点](chapters/024-Kafka的关键技术点.md) ｜ 进阶
- [Kafka的源码级分析](chapters/025-Kafka的源码级分析.md) ｜ 进阶
- [Kafka的配置与使用](chapters/026-Kafka的配置与使用.md) ｜ 进阶
- [Kafka的常见问题与解决方案](chapters/027-Kafka的常见问题与解决方案.md) ｜ 进阶
- [Kafka的性能优化技巧](chapters/028-Kafka的性能优化技巧.md) ｜ 进阶

### RabbitMQ

- [RabbitMQ核心概念与原理](chapters/029-RabbitMQ核心概念与原理.md) ｜ 进阶
- [RabbitMQ的实现机制详解](chapters/030-RabbitMQ的实现机制详解.md) ｜ 进阶
- [RabbitMQ的关键技术点](chapters/031-RabbitMQ的关键技术点.md) ｜ 进阶
- [RabbitMQ的源码级分析](chapters/032-RabbitMQ的源码级分析.md) ｜ 进阶
- [RabbitMQ的配置与使用](chapters/033-RabbitMQ的配置与使用.md) ｜ 进阶
- [RabbitMQ的常见问题与解决方案](chapters/034-RabbitMQ的常见问题与解决方案.md) ｜ 进阶
- [RabbitMQ的性能优化技巧](chapters/035-RabbitMQ的性能优化技巧.md) ｜ 进阶

### RocketMQ

- [RocketMQ核心概念与原理](chapters/036-RocketMQ核心概念与原理.md) ｜ 进阶
- [RocketMQ的实现机制详解](chapters/037-RocketMQ的实现机制详解.md) ｜ 进阶
- [RocketMQ的关键技术点](chapters/038-RocketMQ的关键技术点.md) ｜ 进阶
- [RocketMQ的源码级分析](chapters/039-RocketMQ的源码级分析.md) ｜ 进阶
- [RocketMQ的配置与使用](chapters/040-RocketMQ的配置与使用.md) ｜ 进阶
- [RocketMQ的常见问题与解决方案](chapters/041-RocketMQ的常见问题与解决方案.md) ｜ 进阶
- [RocketMQ的性能优化技巧](chapters/042-RocketMQ的性能优化技巧.md) ｜ 进阶

### Pulsar

- [Pulsar核心概念与原理](chapters/043-Pulsar核心概念与原理.md) ｜ 进阶
- [Pulsar的实现机制详解](chapters/044-Pulsar的实现机制详解.md) ｜ 进阶
- [Pulsar的关键技术点](chapters/045-Pulsar的关键技术点.md) ｜ 进阶
- [Pulsar的源码级分析](chapters/046-Pulsar的源码级分析.md) ｜ 进阶
- [Pulsar的配置与使用](chapters/047-Pulsar的配置与使用.md) ｜ 进阶
- [Pulsar的常见问题与解决方案](chapters/048-Pulsar的常见问题与解决方案.md) ｜ 进阶
- [Pulsar的性能优化技巧](chapters/049-Pulsar的性能优化技巧.md) ｜ 进阶

### 消息模型

- [消息模型核心概念与原理](chapters/050-消息模型核心概念与原理.md) ｜ 高级
- [消息模型的实现机制详解](chapters/051-消息模型的实现机制详解.md) ｜ 高级
- [消息模型的关键技术点](chapters/052-消息模型的关键技术点.md) ｜ 高级
- [消息模型的源码级分析](chapters/053-消息模型的源码级分析.md) ｜ 高级
- [消息模型的配置与使用](chapters/054-消息模型的配置与使用.md) ｜ 高级
- [消息模型的常见问题与解决方案](chapters/055-消息模型的常见问题与解决方案.md) ｜ 高级
- [消息模型的性能优化技巧](chapters/056-消息模型的性能优化技巧.md) ｜ 高级

### 消息可靠性

- [消息可靠性核心概念与原理](chapters/057-消息可靠性核心概念与原理.md) ｜ 高级
- [消息可靠性的实现机制详解](chapters/058-消息可靠性的实现机制详解.md) ｜ 高级
- [消息可靠性的关键技术点](chapters/059-消息可靠性的关键技术点.md) ｜ 高级
- [消息可靠性的源码级分析](chapters/060-消息可靠性的源码级分析.md) ｜ 高级
- [消息可靠性的配置与使用](chapters/061-消息可靠性的配置与使用.md) ｜ 高级
- [消息可靠性的常见问题与解决方案](chapters/062-消息可靠性的常见问题与解决方案.md) ｜ 高级
- [消息可靠性的性能优化技巧](chapters/063-消息可靠性的性能优化技巧.md) ｜ 高级

### 消息顺序

- [消息顺序核心概念与原理](chapters/064-消息顺序核心概念与原理.md) ｜ 高级
- [消息顺序的实现机制详解](chapters/065-消息顺序的实现机制详解.md) ｜ 高级
- [消息顺序的关键技术点](chapters/066-消息顺序的关键技术点.md) ｜ 高级
- [消息顺序的源码级分析](chapters/067-消息顺序的源码级分析.md) ｜ 高级
- [消息顺序的配置与使用](chapters/068-消息顺序的配置与使用.md) ｜ 高级
- [消息顺序的常见问题与解决方案](chapters/069-消息顺序的常见问题与解决方案.md) ｜ 高级
- [消息顺序的性能优化技巧](chapters/070-消息顺序的性能优化技巧.md) ｜ 高级

### 消息事务

- [消息事务核心概念与原理](chapters/071-消息事务核心概念与原理.md) ｜ 高级
- [消息事务的实现机制详解](chapters/072-消息事务的实现机制详解.md) ｜ 高级
- [消息事务的关键技术点](chapters/073-消息事务的关键技术点.md) ｜ 高级
- [消息事务的源码级分析](chapters/074-消息事务的源码级分析.md) ｜ 高级
- [消息事务的配置与使用](chapters/075-消息事务的配置与使用.md) ｜ 高级
- [消息事务的常见问题与解决方案](chapters/076-消息事务的常见问题与解决方案.md) ｜ 高级

### 死信队列

- [死信队列核心概念与原理](chapters/077-死信队列核心概念与原理.md) ｜ 高级
- [死信队列的实现机制详解](chapters/078-死信队列的实现机制详解.md) ｜ 高级
- [死信队列的关键技术点](chapters/079-死信队列的关键技术点.md) ｜ 高级
- [死信队列的源码级分析](chapters/080-死信队列的源码级分析.md) ｜ 高级
- [死信队列的配置与使用](chapters/081-死信队列的配置与使用.md) ｜ 高级
- [死信队列的常见问题与解决方案](chapters/082-死信队列的常见问题与解决方案.md) ｜ 高级

### 延迟队列

- [延迟队列核心概念与原理](chapters/083-延迟队列核心概念与原理.md) ｜ 实战
- [延迟队列的实现机制详解](chapters/084-延迟队列的实现机制详解.md) ｜ 实战
- [延迟队列的关键技术点](chapters/085-延迟队列的关键技术点.md) ｜ 实战
- [延迟队列的源码级分析](chapters/086-延迟队列的源码级分析.md) ｜ 实战
- [延迟队列的配置与使用](chapters/087-延迟队列的配置与使用.md) ｜ 实战
- [延迟队列的常见问题与解决方案](chapters/088-延迟队列的常见问题与解决方案.md) ｜ 实战

### 性能优化

- [性能优化核心概念与原理](chapters/089-性能优化核心概念与原理.md) ｜ 实战
- [性能优化的实现机制详解](chapters/090-性能优化的实现机制详解.md) ｜ 实战
- [性能优化的关键技术点](chapters/091-性能优化的关键技术点.md) ｜ 实战
- [性能优化的源码级分析](chapters/092-性能优化的源码级分析.md) ｜ 实战
- [性能优化的配置与使用](chapters/093-性能优化的配置与使用.md) ｜ 实战
- [性能优化的常见问题与解决方案](chapters/094-性能优化的常见问题与解决方案.md) ｜ 实战

### 最佳实践

- [最佳实践核心概念与原理](chapters/095-最佳实践核心概念与原理.md) ｜ 实战
- [最佳实践的实现机制详解](chapters/096-最佳实践的实现机制详解.md) ｜ 实战
- [最佳实践的关键技术点](chapters/097-最佳实践的关键技术点.md) ｜ 实战
- [最佳实践的源码级分析](chapters/098-最佳实践的源码级分析.md) ｜ 实战
- [最佳实践的配置与使用](chapters/099-最佳实践的配置与使用.md) ｜ 实战
- [最佳实践的常见问题与解决方案](chapters/100-最佳实践的常见问题与解决方案.md) ｜ 实战


---
*领域: 消息队列*