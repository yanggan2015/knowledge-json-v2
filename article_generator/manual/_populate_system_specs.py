#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate MODULE_SNIPPETS with hand-authored technical content for all 系统底层 modules."""

from _system_module_specs import _add, _concepts, _pitfalls, MODULE_SNIPPETS  # noqa: F401

# =============================================================================
# Linux内核 (10)
# =============================================================================
_add("Linux内核", "内核基础与启动",
    intro="Linux 内核是操作系统核心，负责硬件抽象、资源调度与安全隔离。启动链从固件移交控制权，经 GRUB 加载 vmlinuz 与 initramfs，完成子系统初始化后启动用户态 init。",
    concepts=_concepts(
        ("内核镜像", "vmlinuz 含压缩内核与解压桩；initramfs 提供早期用户态工具，在挂载真实根分区前加载必要驱动。"),
        ("boot_params", "GRUB 通过 cmdline 传入 root=、init= 等参数，内核 setup_arch 解析并影响设备枚举与调度策略。"),
        ("start_kernel", "依次初始化内存、调度器、中断、VFS；kernel_init 线程最后 exec 用户空间 init 进程。"),
        ("设备树/ACPI", "ARM 用 DTB 描述硬件拓扑；x86 通过 ACPI 表获取 CPU、中断与电源管理信息。"),
        ("initcall 机制", "按优先级执行各子系统初始化函数，失败常导致 kernel panic 或无法挂载根文件系统。"),
    ),
    mechanism="BIOS/UEFI POST 后 GRUB 加载内核→setup_arch 架构初始化→mm_init 建立页表→trap_init 设置 IDT→各 initcall 注册驱动→挂载根文件系统→执行 /sbin/init。",
    internals="早期用 memblock 分配器，伙伴系统就绪后释放 bootmem。initramfs 由 cpio 解压至 rootfs，switch_root 切换到真实根。",
    workflow="排障时编辑 GRUB cmdline 加 init=/bin/sh；dmesg 查看驱动加载；dracut 重建 initramfs 补全 virtio 等驱动。",
    performance="精简 initramfs 缩短启动；systemd-analyze blame 定位慢单元；nohz_full 减少空闲 CPU tick 干扰。",
    security="Secure Boot 校验内核签名；lockdown 限制 /dev/mem；IMA/EVM 可度量启动链完整性。",
    case_study="云主机换内核后无法启动：initramfs 缺 virtio_blk，dracut --force 重建后恢复。",
    configuration="GRUB /etc/default/grub 设置 GRUB_CMDLINE_LINUX；make menuconfig 定制内核功能与 LOCALVERSION。",
    debugging="console=ttyS0 串口日志；initcall_debug 打印各 initcall 耗时；earlyprintk 调试极早阶段。",
    comparison="SysV init 串行脚本 vs systemd 并行单元依赖，后者显著缩短启动时间。",
    pitfalls=_pitfalls(
        ("initramfs 过旧", "内核升级后未 dracut --force，根文件系统驱动缺失导致 mount failed。"),
        ("cmdline 遗留排障参数", "nomodeset、acpi=off 等参数遗留在生产环境引发性能退化。"),
        ("内核模块版本不匹配", "uname -r 与 /lib/modules 不一致导致 insmod invalid module format。"),
    ),
    practices=["升级内核后重建 initramfs 并保留回退条目", "cmdline 纳入配置管理", "阅读 kernel-parameters.txt 再改参数", "用 systemd-analyze 量化启动"],
    references=["Linux Kernel Documentation: admin-guide/boot.rst", "GRUB Manual", "dracut 官方文档"],
)

_add("Linux内核", "进程管理与调度",
    intro="进程是资源分配单位，线程是调度单位。Linux 用 task_struct 描述任务，CFS 按虚拟运行时间 vruntime 公平分配 CPU，上下文切换保存寄存器与内核栈。",
    concepts=_concepts(
        ("task_struct", "进程控制块，含 pid、状态、调度类、mm_struct 内存描述符、文件表与信号处理信息。"),
        ("进程状态", "TASK_RUNNING、INTERRUPTIBLE、UNINTERRUPTIBLE；僵尸 EXIT_ZOMBIE 需父进程 wait 回收。"),
        ("CFS 调度器", "红黑树按 vruntime 排序；nice 映射权重，高优先级任务获更多 CPU 份额。"),
        ("上下文切换", "switch_to 保存/恢复寄存器；涉及 TLB 刷新与 cache 失效，有可观开销。"),
        ("fork/exec", "copy_process 复制 task_struct 并 COW 页表；execve 替换地址空间加载 ELF。"),
    ),
    mechanism="每 tick 或抢占点检查 need_resched，pick_next_task 从 CFS 红黑树取 vruntime 最小者；SCHED_FIFO/RR 实时类优先于 CFS。",
    internals="schedule() 在 __schedule 切换 prev/next；多核通过 per-CPU runqueue 与负载均衡；写时复制延迟复制物理页。",
    workflow="fork/clone 创建进程；sched_setscheduler 设策略；ps/top 监控；taskset 绑核；cgroups cpu.max 限配额。",
    performance="线程数宜与 CPU 核数匹配；减少不必要切换；CPU 密集与 I/O 密集任务分池避免 cache 颠簸。",
    security="PR_SET_NO_NEW_PRIVS 与 seccomp 限制提权；hidepid 保护 /proc 进程信息；pid namespace 隔离视图。",
    case_study="订单服务线程从 500 降至核数配合异步 I/O，CPU 利用率降而吞吐升。",
    configuration="sysctl kernel.sched_*；cgroup v2 cpu.weight、cpu.max；sched_rt_runtime_us 限制 RT 带宽。",
    debugging="perf sched 记录切换；ftrace function_graph 跟踪 schedule；/proc/PID/stack 查 D 状态内核栈。",
    comparison="CFS 通用公平；SCHED_DEADLINE 适合周期实时任务；BFS 已退出主线。",
    pitfalls=_pitfalls(
        ("线程爆炸", "每请求一线程导致数千 task，切换与内存开销压垮系统。"),
        ("僵尸堆积", "父进程未 wait，大量 defunct 占用 pid 槽位。"),
        ("D 状态误判", "UNINTERRUPTIBLE 常等磁盘非 CPU 满，盲目加核无效。"),
    ),
    practices=["线程池大小参考核数与阻塞比", "处理 SIGCHLD 或 SA_NOCLDWAIT", "设 TasksMax 上限", "关键任务评估 SCHED_FIFO"],
    references=["Linux Kernel: scheduler/sched-design-CFS.rst", "man sched(7), clone(2)", "Brendan Gregg CPU 性能"],
)

_add("Linux内核", "内存管理",
    intro="内核通过伙伴系统管理页框、SLUB 分配内核对象、VMA 描述进程虚拟地址空间。缺页异常驱动按需分配与 page cache 填充。",
    concepts=_concepts(
        ("伙伴系统", "按 2^n 页合并空闲块；zone 区分 DMA、NORMAL、HIGHMEM 满足不同寻址需求。"),
        ("SLUB", "内核对象高速缓存，per-CPU slab 降低锁争用，kmalloc 最终来源。"),
        ("VMA 与页表", "vm_area_struct 描述区间；四级页表 PGD→PUD→PMD→PTE 完成地址翻译。"),
        ("页缓存", "文件读入 page cache，writeback 按 pdflush 策略刷脏页到块设备。"),
        ("OOM Killer", "内存耗尽按 badness 选进程终止，oom_score_adj 可保护关键服务。"),
    ),
    mechanism="首次访问触发缺页，handle_pte_fault 分配页框建 PTE；文件映射 MAP_SHARED 多进程共享 page cache 页。",
    internals="reverse mapping 支持回收；kswapd 回收 LRU 链表；THP 减少 TLB miss 但可能增延迟尖刺。",
    workflow="vm.swappiness 调换出；numactl 绑内存节点；监控 /proc/meminfo 与 smaps PSS。",
    performance="hugetlbfs 大页减 TLB 压力；避免跨 NUMA 远程访问；控制 mmap 数量防 VMA 爆炸。",
    security="KASLR 随机化布局；USERFAULTFD 需防滥用；mlock 敏感数据防换出到磁盘。",
    case_study="Redis 因 THP 延迟毛刺，设 transparent_hugepage=madvise 后 P99 稳定。",
    configuration="vm.overcommit_memory、vm.min_free_kbytes；cgroup memory.max；/sys/kernel/mm/hugepages/。",
    debugging="/proc/PID/smaps 分析 PSS；perf mem 记录缺页；kmemleak 检测内核泄漏。",
    comparison="jemalloc 多线程扩展性好于 glibc malloc；mmap 大块适合生命周期明确对象。",
    pitfalls=_pitfalls(
        ("忽视 swap", "RSS 不高但 swap 满仍严重抖动，需同时看 si/so。"),
        ("THP 一律开启", "数据库等延迟敏感场景 THP 合并可能阻塞毫秒级。"),
        ("OOM 误杀", "未调 oom_score_adj 导致关键进程被杀引发雪崩。"),
    ),
    practices=["关键进程设 memory.low 或 mlock", "监控 pgmajfault", "容器设 memory.max 留宿主机余量", "大页池启动早期预留"],
    references=["Linux Kernel: vm/index.rst", "Understanding the Linux Kernel", "man mmap(2), madvise(2)"],
)

_add("Linux内核", "中断与时间",
    intro="硬件通过中断通知 CPU；Linux 将处理拆为硬中断顶半部与 softirq/tasklet/工作队列底半部。时钟源与 hrtimer 驱动调度与定时器。",
    concepts=_concepts(
        ("IRQ 处理", "request_irq 注册 handler；顶半部快速应答，耗时工作 deferred 到底半部。"),
        ("软中断", "NET_RX、TIMER 等在内核上下文批量处理，ksoftirqd 线程辅助。"),
        ("时钟源", "TSC/HPET/arch_timer 经 clocksource 框架选择；jiffies 为全局节拍。"),
        ("hrtimer", "纳秒级高精度定时器，支撑 nanosleep、itimer 与多媒体同步。"),
        ("NO_HZ", "动态 tick 在空闲 CPU 停止节拍，降低功耗与无关中断。"),
    ),
    mechanism="设备断言 IRQ→do_IRQ 调用 handler→软中断或 threaded IRQ 处理数据；NAPI 网卡收包典型路径。",
    internals="local_irq_save 防重入；IRQ affinity 绑核分散负载；NTP 调整 timekeeping。",
    workflow="echo CPU mask > /proc/irq/N/smp_affinity；chrony 同步；clock_gettime(CLOCK_MONOTONIC) 测间隔。",
    performance="中断合并降低 PPS 但增延迟；RPS/RFS 分散软中断到处理 CPU。",
    security="中断风暴可致锁死；rate limit 未知 IRQ；限制 timer_create 滥用。",
    case_study="10GbE 中断全在 CPU0，配置 RSS 与 irqbalance 后吞吐提升 40%。",
    configuration="/proc/interrupts 观察分布；threadirqs 内核参数；ethtool 中断合并参数。",
    debugging="trace_irqsoff 找关中断过长；ftrace irq 事件；cat /proc/interrupts 对比各 CPU。",
    comparison="tickless 适合 idle 多的服务器；实时系统可能固定 tick 便于确定性采样。",
    pitfalls=_pitfalls(
        ("硬中断做重活", "IRQ handler 里持锁过久导致丢包与 watchdog 超时。"),
        ("NTP 时间回拨", "未用 monotonic 时钟，step 导致定时器错乱。"),
        ("IRQ 全堆一核", "未设 affinity，网络与磁盘中断争用单核。"),
    ),
    practices=["网卡开启 NAPI 与合理 coalescing", "生产用 chrony 监控 offset", "延迟测量用 MONOTONIC_RAW", "高 PPS 评估 XDP"],
    references=["Linux Kernel: core-api/interrupts.rst", "Documentation/timers/NO_HZ.txt", "man clock_gettime(3)"],
)

_add("Linux内核", "同步机制",
    intro="多核并发访问共享数据需自旋锁、mutex、rwsem、RCU 等原语，在正确性与性能间权衡，并配合内存屏障防止 CPU 重排。",
    concepts=_concepts(
        ("spinlock", "忙等适合极短临界区；不可在可能睡眠的硬中断上下文用 mutex。"),
        ("mutex", "睡眠锁，争用线程入队阻塞，适合持锁时间较长的路径。"),
        ("rwsem", "读者共享写者独占，读多写少降低争用。"),
        ("RCU", "读侧无锁，写者延迟释放，适合以遍历为主的数据结构。"),
        ("内存序", "smp_mb/smp_rmb 防重排；atomic_t 与 cmpxchg 实现无锁计数。"),
    ),
    mechanism="锁争用导致 cache line bouncing；per-CPU 变量减少共享；RCU grace period 后安全 kfree。",
    internals="futex 支撑用户态 pthread mutex；lockdep 检测死锁；PREEMPT_RT 将部分 spinlock 转 mutex。",
    workflow="内核 spin_lock_irqsave；用户态 pthread_mutex；定义全局锁顺序防 AB-BA 死锁。",
    performance="缩小临界区、读写分离、per-CPU 缓存；RCU 读多写少最优。",
    security="竞态可导致权限提升；HARDENED_USERCOPY 缓解堆溢出；锁未初始化是 CVE 常见根因。",
    case_study="全局计数器改 per-CPU 累加后汇总，锁争用消失，QPS 提升 15%。",
    configuration="CONFIG_PROVE_LOCKING、CONFIG_KCSAN 调试构建；应用 -fsanitize=thread。",
    debugging="perf lock 统计争用；/proc/lockdep；ftrace 跟踪 mutex_lock 慢路径。",
    comparison="spinlock 不可睡眠；RCU 读扩展性好但写延迟高；seqlock 适合 jiffies 等低频写。",
    pitfalls=_pitfalls(
        ("中断上下文用 mutex", "触发 sleeping in invalid context 内核崩溃。"),
        ("锁粒度过大", "大锁限制多核扩展，应拆分或改用 RCU。"),
        ("RCU 过早释放", "未 synchronize_rcu 即 kfree 导致 use-after-free。"),
    ),
    practices=["文档化锁获取顺序", "读多写少用 RCU", "测试内核开 lockdep", "热点用无锁环形队列"],
    references=["Linux Kernel: RCU/index.rst", "Is Parallel Programming Hard", "man pthread_mutex(3)"],
)

_add("Linux内核", "文件系统VFS",
    intro="VFS 统一 inode、dentry、file 抽象，ext4/xfs/btrfs 实现 super_block 操作表。路径解析与页缓存协作完成读写。",
    concepts=_concepts(
        ("inode", "文件元数据：权限、大小、时间戳；i_mapping 指向 page cache 地址空间。"),
        ("dentry 缓存", "目录项哈希加速路径查找；negative dentry 缓存不存在路径。"),
        ("file 对象", "打开文件实例，f_op 读写；与进程 fd 表通过 struct file 关联。"),
        ("ext4 日志", "journal 保证元数据一致性，ordered 模式兼顾性能与安全。"),
        ("O_DIRECT", "绕过 page cache，数据库常配合块对齐使用。"),
    ),
    mechanism="open 经 path_lookup 遍历 dentry→inode_permission 检查→read 命中 page cache 或 read_folio 读盘。",
    internals="bio 提交块层；ext4 extent 树管理映射；overlayfs 联合挂载容器镜像层。",
    workflow="挂载 noatime、discard；fstrim 回收 SSD；数据库目录单独挂载调优。",
    performance="顺序写与 readahead；XFS 大文件并行扩展性好；避免过度 fsync。",
    security="nosuid、nodev 挂载；SELinux 文件上下文；fscrypt 静态加密。",
    case_study="日志服务迁 XFS 并调队列深度，磁盘 util 降 30%。",
    configuration="fstab 选项；sysctl fs.aio-max-nr；/sys/block/*/queue 调度器。",
    debugging="strace open/stat；blktrace；iostat -x 看 await 与 util。",
    comparison="ext4 通用；xfs 大文件优；btrfs 快照校验但运维复杂。",
    pitfalls=_pitfalls(
        ("忽视 atime", "数据库目录应 noatime 减写放大。"),
        ("DIO 未对齐", "O_DIRECT 要求扇区对齐否则失败。"),
        ("dentry 撑爆内存", "海量小文件遍历耗尽 RAM，调 vfs_cache_pressure。"),
    ),
    practices=["关键数据目录单独挂载", "定期 fstrim", "理解 journal 模式", "容器注意 overlay 写层性能"],
    references=["Linux Kernel: filesystems/vfs.rst", "ext4.wiki.kernel.org", "man open(2), mount(8)"],
)

_add("Linux内核", "网络协议栈",
    intro="内核网络栈自 socket 经 TCP/IP 到 NIC 驱动分层处理，sk_buff 贯穿各层，NAPI 与 GRO 提升收包效率。",
    concepts=_concepts(
        ("sk_buff", "网络包描述符，head/data/tail/end 指针支持协议头推拉。"),
        ("struct sock", "协议无关 socket；connect/sendmsg 进入 TCP/UDP 实现。"),
        ("TCP 状态机", "三次握手、滑动窗口；拥塞控制 Reno/CUBIC/BBR 调节发送速率。"),
        ("FIB 路由", "最长前缀匹配选路；ARP/NDISC 解析下一跳 L2 地址。"),
        ("netfilter", "iptables/nftables 在 PREROUTING/FORWARD/POSTROUTING 挂钩过滤与 NAT。"),
    ),
    mechanism="收包 NIC DMA→硬中断 NAPI poll→协议栈解析→socket 接收队列；发包经 qdisc 排队驱动 DMA。",
    internals="tcp_congestion_control 可插拔；XDP 驱动入口早期过滤；kTLS 内核态 TLS 卸载。",
    workflow="sysctl net.core/net.ipv4；ss -tin 看缓冲区；ethtool -g 调 ring；BBR 需 fq qdisc。",
    performance="调 rmem/wmem；TSO/GSO；RPS 分散软中断；本机转发评估 sockmap。",
    security="SYN cookie；rp_filter 反欺骗；nft 限速；TLS 保护数据面。",
    case_study="CDN 节点启用 BBR+fq，跨洲 RTT 200ms 吞吐较 cubic 提升约 25%。",
    configuration="sysctl.d 网络调优；tc qdisc；tcp_congestion_control 切换。",
    debugging="tcpdump；ss -s；dropwatch；bpftrace 跟踪内核网络事件。",
    comparison="CUBIC 丢包驱动降窗；BBR 模型带宽延迟，需注意缓冲区膨胀与公平性。",
    pitfalls=_pitfalls(
        ("半连接队列溢出", "somaxconn 与 sync backlog 过小致 connect 超时。"),
        ("rp_filter 误杀", "非对称路由环境丢合法包。"),
        ("未区分 GRO 与线速", "tcpdump 见大包是聚合结果非异常。"),
    ),
    practices=["调优前建 ss/nstat 基线", "长连接注意 keepalive", "多队列配 RSS/RPS", "防火墙处理 ESTABLISHED"],
    references=["Linux Kernel: networking/index.rst", "TCP/IP Illustrated Vol.1", "man tcp(7), ip(7)"],
)

_add("Linux内核", "设备驱动模型",
    intro="Linux 设备模型用 bus、device、driver 与 class 统一枚举匹配，sysfs 暴露属性，uevent 通知 udev 创建设备节点。",
    concepts=_concepts(
        ("kobject/sysfs", "内核对象与 sysfs 目录对应，供 udev 与调试读写属性。"),
        ("总线匹配", "match 比较 id_table 与硬件 ID，probe 初始化，remove 释放资源。"),
        ("platform 设备", "板级固定资源，设备树 compatible 关联驱动。"),
        ("runtime PM", "按需启停时钟与电源域，system PM 配合休眠唤醒。"),
        ("devres", "probe 失败自动回滚 ioremap、IRQ 等资源。"),
    ),
    mechanism="设备注册后遍历驱动列表调用 probe；driver core 维护 devices_kset 与 module 引用计数。",
    internals="设备树 reg/interrupts 描述资源；defer probe 等待依赖提供者就绪。",
    workflow="编写 platform_driver；lspci -k 查看绑定；modprobe 加载模块；udev rules 设权限。",
    performance="MSI 优于共享 IRQ；probe 避免长 sleep；threaded IRQ 降硬中断延迟。",
    security="sysfs 写属性需权限检查；DMA 经 IOMMU 映射；ioctl 校验 capability。",
    case_study="I2C 传感器按 binding 填 compatible，probe 读 chip ID 失败打印明确错误加速联调。",
    configuration="/etc/modprobe.d；udev rules；设备树 overlay 动态加载。",
    debugging="dynamic_debug；debugfs 寄存器 dump；ftrace probe 函数。",
    comparison="platform/PCI/USB 资源发现方式不同，probe/remove 生命周期类似。",
    pitfalls=_pitfalls(
        ("probe 顺序依赖", "未 defer 依赖时钟/GPIO 导致随机失败。"),
        ("sysfs 滥写", "无权限 writable attribute 可被本地提权。"),
        ("probe 泄漏资源", "错误路径未 devres 管理导致泄漏。"),
    ),
    practices=["遵循 devicetree bindings", "probe 用 dev_info 分级日志", "实现 runtime suspend", "提交前 checkpatch"],
    references=["Linux Kernel: driver-api/index.rst", "Linux Device Drivers 3e", "Documentation/ABI/stable/sysfs-*"],
)

_add("Linux内核", "系统调用与IPC",
    intro="系统调用是用户态进入内核网关，经 syscall 指令触发。IPC 含管道、信号、共享内存、消息队列与 Unix domain socket。",
    concepts=_concepts(
        ("syscall 入口", "x86_64 syscall 指令查 sys_call_table 分发，保存 pt_regs。"),
        ("VDSO", "用户态映射内核页，gettimeofday 等无需陷入。"),
        ("pipe/FIFO", "pipe 单向字节流；mkfifo 命名管道供无关进程通信。"),
        ("共享内存", "shmget/shmat 映射同页，需信号量或 mutex 同步。"),
        ("Unix socket", "AF_UNIX 本机高效，SCM_RIGHTS 可传递 fd。"),
    ),
    mechanism="libc 包装 syscall；seccomp 过滤；copy_from_user 防非法指针访问。",
    internals="futex 支撑 pthread；eventfd/signalfd 与 epoll 集成；pidfd 进程管理新接口。",
    workflow="strace 观察；pipe 父子通信；mmap MAP_SHARED 大数据；socketpair 全双工。",
    performance="批量 read/write；splice 零拷贝；sendmmsg 批量网络 I/O。",
    security="seccomp-bpf 白名单；user namespace 隔离 IPC；ptrace_scope 限制调试。",
    case_study="日志代理用 splice 零拷贝 pipe 到 socket，CPU 降半。",
    configuration="kernel.yama.ptrace_scope；RLIMIT_MSGQUEUE；seccomp 配置文件。",
    debugging="strace -f -tt；perf trace；auditd 记录敏感 syscall。",
    comparison="pipe 简单单向；socket 可全双工传 fd；shm 最快需自管同步。",
    pitfalls=_pitfalls(
        ("TOCTOU", "access 与 open 之间文件被替换，应 O_NOFOLLOW。"),
        ("共享内存无锁", "多写者数据损坏。"),
        ("seccomp 过宽", "允许 execve 使沙箱失效。"),
    ),
    practices=["大块数据用 mmap", "容器审阅默认 seccomp", "Unix socket 做进程通知", "strace 仅排障用"],
    references=["Linux Kernel: core-api/syscall-api.rst", "man syscalls(2), unix(7)", "seccomp(2)"],
)

_add("Linux内核", "性能调优与追踪",
    intro="内核提供 perf、ftrace、bcc/eBPF 观测与调优，从 PMU 计数到动态追踪函数与内核态可编程分析。",
    concepts=_concepts(
        ("perf_event", "PMU 采样 CPU cycles、cache miss、page fault 等事件。"),
        ("ftrace", "函数图、irqsoff、调度跟踪，tracefs 控制。"),
        ("eBPF", "验证后加载字节码，kprobe/tracepoint 聚合指标或 XDP 处理。"),
        ("kprobes", "动态插桩内核函数，需控制 overhead。"),
        ("火焰图", "perf script 折叠栈可视化热点调用链。"),
    ),
    mechanism="perf mmap 环形缓冲读样本；eBPF verifier 保证安全，map 与用户态交互。",
    internals="BPF JIT 编译本地指令；uprobes 用户态插桩；ring buffer 多 CPU 无锁。",
    workflow="perf record/report；bpftrace 一行脚本；trace-cmd 录制；调优前建 baseline。",
    performance="先算法与 I/O 优化；off-CPU 分析锁与等待；NUMA 本地性。",
    security="eBPF 需 CAP_BPF；kprobes 误用可崩内核；生产控制采样率。",
    case_study="perf 显示 mutex 热点，改无锁队列后 P99 降 60%。",
    configuration="kernel.perf_event_paranoid；挂载 debugfs、bpffs。",
    debugging="perf sched timehist；bpftrace -e；function_graph tracer。",
    comparison="perf 通用采样；eBPF 可定制聚合与内核过滤，适合生产常驻。",
    pitfalls=_pitfalls(
        ("只盯 CPU", "iowait 高时优化算法无效。"),
        ("追踪开销过大", "100% 采样 Heisenberg 效应。"),
        ("符号未解析", "缺 debuginfo 火焰图仅见地址。"),
    ),
    practices=["linux-tools 匹配内核版本", "CI perf stat 回归", "eBPF 检测内核能力", "on+off CPU 火焰图结合"],
    references=["perf.wiki.kernel.org", "BPF Performance Tools (Gregg)", "Documentation/trace/ftrace.rst"],
)

# Continue in next part due to file size - use exec to load more
if __name__ == "__main__":
    import importlib.util
    spec = importlib.util.spec_from_file_location("more", __file__.replace("_populate_system_specs.py", "_populate_system_specs_part2.py"))
    try:
        more = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(more)
    except FileNotFoundError:
        pass
    print(f"Populated {len(MODULE_SNIPPETS)} snippets")
