# -*- coding: utf-8 -*-
"""系统底层 12 领域概述素材"""

DOMAIN_OVERVIEWS = {
    "Linux内核": {
        "intro": (
            "Linux 内核是开源操作系统核心，管理 CPU、内存、设备与网络，向上提供系统调用与 POSIX 语义。"
            "理解启动链、调度器、虚拟内存与驱动模型，是内核开发、性能调优与故障排查的基础。"
        ),
        "positioning": "面向内核开发者、系统程序员与 SRE，以 Linux 6.x 主线为参照，结合源码与观测工具讲解机制。",
        "prerequisites": ["C 语言与指针", "计算机组成原理", "操作系统基本概念", "命令行与 GDB 基础"],
        "outcomes": [
            "读懂 task_struct、VMA、sk_buff 等核心数据结构及其协作关系",
            "能使用 perf、ftrace、eBPF 定位内核热点与延迟问题",
            "理解系统调用、中断、同步原语与文件系统 VFS 的实现路径",
            "具备阅读内核源码、编写简单内核模块与驱动的基础能力",
        ],
        "ecosystem": "Linux 6.x, GRUB/systemd, perf, ftrace, bpftrace, BCC, crash, kdump, LKML",
    },
    "Linux系统编程": {
        "intro": (
            "Linux 系统编程在 POSIX 语义之上使用系统调用实现进程、文件、信号、线程与 IPC。"
            "掌握 open/read/write、fork/exec、pthread、epoll 等 API 是编写高性能服务端与工具链的必备技能。"
        ),
        "positioning": "面向 C/C++/Rust 系统程序员，侧重 man page 与内核行为的一致性理解及生产级错误处理。",
        "prerequisites": ["C 语言", "Linux 命令行", "基本网络概念", "Makefile/编译链接基础"],
        "outcomes": [
            "熟练使用文件 I/O、进程控制、信号与多种 IPC 机制",
            "能编写多线程程序并处理竞态、死锁与 EINTR 重试",
            "掌握 epoll 边缘/水平触发与 Reactor 网络模型",
            "能编写守护进程、处理僵尸进程并正确使用内存映射",
        ],
        "ecosystem": "glibc/musl, pthread, epoll/kqueue, strace, ltrace, valgrind, systemd",
    },
    "操作系统原理": {
        "intro": (
            "操作系统原理从抽象层面讲解进程、内存、文件与 I/O 的管理策略，"
            "涵盖调度算法、同步互斥、虚拟内存、死锁与磁盘调度等经典问题，为理解 Linux/Windows 内核提供理论框架。"
        ),
        "positioning": "面向计算机专业学生与工程师的理论补强，强调概念模型与算法分析，配合实验加深理解。",
        "prerequisites": ["C 语言", "数据结构与算法", "计算机组成原理", "离散数学基础"],
        "outcomes": [
            "形式化描述进程状态转换、调度策略与同步问题",
            "分析页面置换算法、工作集模型与虚拟内存设计权衡",
            "理解死锁四个必要条件及银行家、检测与恢复策略",
            "能将理论概念映射到 Linux 具体实现（CFS、inode、elevator）",
        ],
        "ecosystem": "Silberschatz OS 教材, xv6/minix 教学内核, Linux man pages",
    },
    "计算机网络": {
        "intro": (
            "计算机网络按 OSI/TCP-IP 分层讲解物理传输、路由交换、传输可靠性与应用协议。"
            "从以太网帧到 HTTP/3，理解各层首部字段、状态机与拥塞控制是网络编程与排障的核心。"
        ),
        "positioning": "面向网络工程师与后端开发者，结合 Wireshark 抓包与 socket 编程实践。",
        "prerequisites": ["二进制与十六进制", "基本编程能力", "操作系统基础", "概率统计基础"],
        "outcomes": [
            "手工解析 Ethernet/IP/TCP 首部并理解校验与分片",
            "掌握 TCP 三次握手、滑动窗口、拥塞控制与 TIME_WAIT",
            "能使用 socket API 编写客户端/服务端并处理非阻塞 I/O",
            "理解 DNS、HTTP、TLS 及常见网络安全机制",
        ],
        "ecosystem": "Wireshark, tcpdump, iperf3, curl, RFC 791/793/2616/8446, Linux iproute2",
    },
    "编译原理": {
        "intro": (
            "编译原理讲解将高级语言翻译为机器码的全过程：词法分析、语法分析、语义分析、"
            "中间表示、优化与代码生成。LLVM/GCC 是现代工具链的理论基础。"
        ),
        "positioning": "面向编译器开发者、DSL 设计者及希望深入理解语言实现的工程师。",
        "prerequisites": ["C 语言", "数据结构与算法", "自动机理论", "汇编语言基础"],
        "outcomes": [
            "手写递归下降或 LR 分析器解析表达式与语句",
            "理解符号表、类型检查、三地址码与 SSA 形式",
            "掌握常见优化：常量折叠、DCE、循环不变量外提",
            "了解链接、加载、PLT/GOT 与 JIT 基本原理",
        ],
        "ecosystem": "Flex/Bison, LLVM, GCC, ANTLR, Compiler Explorer (godbolt.org)",
    },
    "计算机组成原理": {
        "intro": (
            "计算机组成原理从硬件视角讲解数据表示、存储层次、指令集、CPU 微架构、总线与 I/O。"
            "理解取指-译码-执行周期与 Cache 局部性是性能优化与底层编程的基石。"
        ),
        "positioning": "面向所有需要理解「程序如何在硅片上运行」的开发者，衔接汇编、OS 与体系结构。",
        "prerequisites": ["数字逻辑基础", "C 语言", "二进制运算", "基本电路概念"],
        "outcomes": [
            "完成定点/浮点运算与补码溢出分析",
            "解释 Cache 命中、替换策略与写回/写穿差异",
            "阅读 MIPS/ARM 汇编并跟踪流水线冒险",
            "分析总线带宽、DMA 与多核一致性协议基础",
        ],
        "ecosystem": "RISC-V/MIPS 模拟器, Intel SDM, ARM Architecture Reference Manual",
    },
    "汇编语言": {
        "intro": (
            "汇编语言是机器指令的人类可读形式，直接操控寄存器、栈与内存。"
            "x86_64 与 ARM 汇编是逆向工程、内核启动、性能关键路径与嵌入式开发的必备技能。"
        ),
        "positioning": "面向底层开发者与安全研究员，强调调用约定、寻址方式与 ABI 兼容性。",
        "prerequisites": ["C 语言", "计算机组成原理", "十六进制与位运算", "Linux 命令行"],
        "outcomes": [
            "编写 x86_64 与 ARM 汇编函数并正确遵守调用约定",
            "理解栈帧、局部变量布局与缓冲区溢出原理（防御视角）",
            "使用 GDB 单步汇编并阅读反汇编输出",
            "掌握常见优化：循环展开、SIMD 内联汇编基础",
        ],
        "ecosystem": "NASM/GAS, objdump, GDB, Compiler Explorer, ARM Keil/GCC",
    },
    "嵌入式系统": {
        "intro": (
            "嵌入式系统将计算能力嵌入设备，受功耗、成本与实时性约束。"
            "涵盖 MCU/SoC 选型、RTOS、外设驱动、低功耗设计与现场调试。"
        ),
        "positioning": "面向嵌入式软件工程师与硬件协同开发者，侧重 ARM Cortex-M 与常见 RTOS 生态。",
        "prerequisites": ["C 语言", "数字电路基础", "汇编语言基础", "操作系统概念"],
        "outcomes": [
            "阅读芯片数据手册配置时钟、GPIO、UART/SPI/I2C",
            "在 FreeRTOS/Zephyr 上创建任务、队列与信号量",
            "设计低功耗模式切换与唤醒源管理",
            "使用 JTAG/SWD 与逻辑分析仪进行联调",
        ],
        "ecosystem": "STM32/NXP, FreeRTOS, Zephyr, Yocto, OpenOCD, logic analyzer",
    },
    "驱动开发": {
        "intro": (
            "Linux 设备驱动连接内核与硬件，按字符、块、网络设备分类，遵循统一设备模型。"
            "掌握 probe/remove、中断处理、DMA 与 sysfs 是驱动工程师的核心能力。"
        ),
        "positioning": "面向内核驱动开发者，以 Linux 驱动模型为主，覆盖平台/PCI/USB 等总线。",
        "prerequisites": ["C 语言", "Linux 内核基础", "计算机组成原理", "数字电路与总线基础"],
        "outcomes": [
            "编写字符设备驱动并实现 file_operations",
            "处理硬中断、线程化 IRQ 与 DMA 一致性映射",
            "阅读设备树 binding 并完成 platform 驱动 probe",
            "使用 dynamic_debug、sysfs 与逻辑分析仪排障",
        ],
        "ecosystem": "Linux LDD3, Device Tree, udev, modprobe, devmem2(调试), oscilloscope",
    },
    "虚拟化技术": {
        "intro": (
            "虚拟化在物理硬件上运行多个隔离的操作系统实例，通过 Hypervisor 虚拟化 CPU、内存与 I/O。"
            "KVM、Xen 与硬件辅助虚拟化（Intel VT-x/AMD-V）是现代数据中心的基础。"
        ),
        "positioning": "面向云平台与基础设施工程师，讲解 Type-1/2 Hypervisor 原理与性能调优。",
        "prerequisites": ["操作系统原理", "Linux 内核基础", "x86 体系结构", "计算机网络"],
        "outcomes": [
            "解释 VM Entry/Exit、EPT/NPT 二级地址翻译",
            "区分全虚拟化、半虚拟化与硬件辅助路径",
            "配置 KVM 虚拟机 CPU/内存/virtio 设备",
            "分析虚拟化开销来源并应用 pinning、大页等优化",
        ],
        "ecosystem": "KVM/QEMU, libvirt, Xen, VMware ESXi, virtio, VFIO",
    },
    "容器技术": {
        "intro": (
            "容器通过 Linux Namespace 隔离视图、Cgroups 限制资源、UnionFS 层叠文件系统实现轻量打包。"
            "Docker 与 OCI 标准使应用交付一致化，Kubernetes 负责编排与调度。"
        ),
        "positioning": "面向 DevOps 与平台工程师，从内核机制到 Docker/K8s 生产实践。",
        "prerequisites": ["Linux 系统管理", "计算机网络", "基本脚本编写", "虚拟化概念"],
        "outcomes": [
            "手工用 unshare/nsenter 理解 Namespace 隔离范围",
            "配置 Cgroups v2 限制 CPU、内存与 IO",
            "构建多阶段 Dockerfile 并优化镜像层与缓存",
            "设计容器网络（bridge/overlay）与安全策略",
        ],
        "ecosystem": "Docker, containerd, runc, CNI, BuildKit, OCI image-spec",
    },
    "实时系统": {
        "intro": (
            "实时系统保证任务在截止时间内完成，分为硬实时（错过即失效）与软实时（可容忍偶尔超时）。"
            "调度算法、优先级继承、确定性 I/O 与 RTOS/RT-Linux 是核心主题。"
        ),
        "positioning": "面向工业控制、汽车电子与通信设备工程师，强调可调度性分析与最坏情况响应时间。",
        "prerequisites": ["操作系统原理", "C 语言", "嵌入式基础", "概率与调度理论入门"],
        "outcomes": [
            "区分硬实时/软实时/尽力而为并选择合适调度策略",
            "使用 RMS/EDF 进行可调度性分析",
            "配置 PREEMPT_RT 补丁与 CPU 隔离降低抖动",
            "设计容错与看门狗机制保障安全关键系统",
        ],
        "ecosystem": "FreeRTOS, Zephyr, PREEMPT_RT, Xenomai, RTEMS, WCET 分析工具",
    },
}
