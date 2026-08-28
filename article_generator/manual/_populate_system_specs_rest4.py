#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate remaining domains part 4: 虚拟化技术, 容器技术, 实时系统."""

import sys
sys.path.insert(0, "/workspace/article_generator/manual")
from _system_module_specs import _add, _concepts, _pitfalls, MODULE_SNIPPETS


def populate_part4():
    # ===== 虚拟化技术 (10) =====
    D = "虚拟化技术"
    virt = {
        "虚拟化概述": ("虚拟化在物理硬件上运行多个隔离 OS 实例。Type-1 Hypervisor 裸金属，Type-2 宿主型如 VirtualBox。", [
            ("Hypervisor", "管理 VM 与硬件，调度 vCPU，虚拟化内存与 I/O。"),
            ("VM 与容器", "VM 完整 OS 隔离强；容器共享内核轻量。"),
            ("硬件辅助", "Intel VT-x AMD-V 扩展，降低纯软件模拟开销。"),
            ("资源超分", "overcommit CPU 内存，依赖并非所有 VM 同时峰值。"),
            ("嵌套虚拟化", "VM 内再跑 Hypervisor，性能损耗大。"),
        ]),
        "CPU虚拟化": ("CPU 虚拟化通过 VMX/SVM 根与非根模式，VM Entry/Exit 处理敏感指令与异常。", [
            ("VMCS", "Intel 虚拟机控制结构，保存 guest/host 状态。"),
            ("敏感指令", "未虚拟化指令 trap 到 Hypervisor 模拟。"),
            ("vCPU 调度", "Hypervisor 将 vCPU 映射到 pCPU，pinning 绑核。"),
            ("嵌套页表", "EPT/NPT 二级地址翻译 GVA→GPA→HPA。"),
            ("时钟虚拟化", "TSC offset 与 constant_tsc 避免 guest 时间漂移。"),
        ]),
        "内存虚拟化": ("影子页表或 EPT 将 Guest 物理地址映射到 Host 物理地址，Balloon 驱动动态回收内存。", [
            ("影子页表", "软件维护 GVA→HPA，VM Exit 多，已少用。"),
            ("EPT Violation", "缺页或权限违规 exit，Hypervisor 建映射。"),
            ("内存气球", "virtio-balloon 回收空闲页给宿主机。"),
            ("大页", "宿主机 hugetlbfs 减 TLB miss，需规划。"),
            ("KSM", "合并相同内容页，安全场景慎用。"),
        ]),
        "IO虚拟化": ("设备直通 VFIO 将物理设备分配给 VM；virtio 半虚拟化设备高性能通用。", [
            ("全模拟", "QEMU 软件模拟 IDE 网卡，慢但兼容。"),
            ("virtio", "前后端驱动共享 ring buffer，paravirtualized。"),
            ("VFIO", "IOMMU 保护下直通 GPU/NVMe 到 VM。"),
            ("SR-IOV", "网卡硬件多 VF，每 VM 一虚拟功能。"),
            ("vhost", "内核 vhost 减 virtio 数据拷贝到用户态 QEMU。"),
        ]),
        "全虚拟化与半虚拟化": ("全虚拟化 guest 无修改，敏感指令 trap；半虚拟化 guest 主动 hypercall 提效。", [
            ("二进制翻译", "早期 VMware 动态翻译特权指令。"),
            ("Xen PV", "半虚拟化内核 aware hypervisor，已过渡 HVM。"),
            ("virtio 标准", "半虚拟化设备事实标准，跨 Hypervisor。"),
            ("Hypercall", "guest 主动请求 Hypervisor 服务。"),
            ("enlightenment", "Windows/Linux 识别 Hyper-V 优化路径。"),
        ]),
        "容器虚拟化": ("容器非传统虚拟化，Namespace+Cgroups 隔离，共享内核。与 VM 互补非替代。", [
            ("共享内核", "容器 escape 影响宿主机，安全边界弱于 VM。"),
            ("Kata/gVisor", "轻量 VM 或用户态内核增强隔离。"),
            ("Pod", "K8s 多容器共享 network namespace。"),
            ("镜像分层", "与 VM 磁盘镜像不同，联合文件系统。"),
            ("混合部署", "敏感 workload VM，微服务容器。"),
        ]),
        "KVM详解": ("KVM 将 Linux 变为 Type-1 Hypervisor，/dev/kvm 创建 VM，QEMU 设备模拟与用户态。", [
            ("kvm_ioctl", "KVM_CREATE_VM KVM_CREATE_VCPU KVM_RUN。"),
            ("QEMU", "设备模型与 virtio，ioeventfd 与 irqchip。"),
            ("libvirt", "管理 API virsh 定义 XML 域。"),
            ("CPU 模型", "host-passthrough 暴露主机特性或固定型号迁移。"),
            ("live migration", "内存预拷贝，停机时间毫秒级。"),
        ]),
        "Xen架构": ("Xen Hypervisor 层极薄，Dom0 特权域管理，DomU 客户域 PV 或 HVM。", [
            ("Dom0", "Linux 驱动硬件，toolstack 管理 DomU。"),
            ("XenStore", "键值配置与状态通信。"),
            ("grant table", "域间共享内存零拷贝。"),
            ("event channel", "域间中断通知机制。"),
            ("xl/libxl", "现代工具栈管理 VM。"),
        ]),
        "性能优化": ("虚拟化开销在 VM Exit、I/O 模拟与调度。CPU pinning、virtio、大页与 vhost 是关键优化。", [
            ("减少 Exit", "kvmclock virtio 减少敏感操作。"),
            ("CPU 亲和", "vCPU 绑 pCPU 减 cache 迁移。"),
            ("NUMA", "VM 内存分配在宿主机本地节点。"),
            ("IO 线程", "QEMU iothread 专用处理磁盘网络。"),
            ("禁用不必要设备", "未用设备不模拟减开销。"),
        ]),
        "虚拟化安全": ("Hypervisor 是信任根，CVE 影响所有 VM。侧信道 L1TF 等需微码与缓解。", [
            ("隔离", "VM 间内存 EPT 隔离，IOMMU 防 DMA 攻击。"),
            ("侧信道", "Cache timing 跨 VM 泄露，硬件缓解与调度隔离。"),
            ("快照安全", "内存快照含密钥，加密存储。"),
            ("可信计算", "vTPM 虚拟可信平台模块。"),
            ("最小 Dom0", "Xen Dom0 攻击面大，需加固。"),
        ]),
    }
    for mod, (intro, concepts) in virt.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 通过 Hypervisor 拦截敏感操作并模拟或直通硬件，向 Guest OS 呈现虚拟平台。",
            internals="KVM 内核模块与 QEMU 用户态协作；Intel SDM VMX 章节。",
            workflow="libvirt 定义 VM→virsh start→guest 安装→监控性能→按需调优 virtio/绑核。",
            performance="virtio+vhost；EPT 大页；避免 overcommit 导致 swap 抖动。",
            security="及时打宿主机内核补丁；敏感负载隔离物理机；启用 IOMMU。",
            case_study="数据库 VM 绑 NUMA 节点并直通 NVMe，延迟接近裸机 95%。",
            configuration="virsh edit CPU pinning/memoryBacking hugepages；QEMU -machine type。",
            debugging="perf kvm kvm_exit 统计 exit 原因；virsh domstats 资源。",
            comparison="KVM 生态广；Xen 云平台历史久；VMware 商业功能全。",
            pitfalls=_pitfalls(
                ("未装 virtio 驱动", "Windows guest 用 IDE 磁盘性能差。"),
                ("overcommit 内存", "所有 VM 同时峰值触发 OOM 杀 VM。"),
                ("迁移版本不一致", "live migration CPU 特性不匹配失败。"),
            ),
            practices=["Guest 装 virtio 驱动", "监控 VM Exit 率", "关键 VM 预留资源", "定期快照与备份"],
            references=["KVM Wiki", "Intel Virtualization Technology Spec", "QEMU Documentation"],
        )

    # ===== 容器技术 (10) =====
    D = "容器技术"
    ctr = {
        "容器概述": ("容器打包应用与依赖，共享宿主机内核，秒级启动。OCI 镜像与运行时标准促进生态互操作。", [
            ("镜像与容器", "镜像是只读模板，容器是可写层加运行实例。"),
            ("隔离级别", "进程级非硬件级，需纵深防御。"),
            ("不可变基础设施", "替换而非修补，版本化镜像部署。"),
            ("12-Factor", "配置外置、无状态、日志流等云原生原则。"),
            ("编排", "单机 Docker，集群 Kubernetes 调度。"),
        ]),
        "Namespace": ("Namespace 隔离进程视图：PID、NET、MNT、UTS、IPC、USER、Cgroup。", [
            ("PID namespace", "容器内 pid 1，独立进程树。"),
            ("NET namespace", "独立网卡、路由、iptables 规则。"),
            ("MNT namespace", "独立挂载点，容器根文件系统。"),
            ("USER namespace", "根用户映射宿主机普通用户，降权。"),
            ("unshare", "命令行创建新 namespace 实验。"),
        ]),
        "Cgroups": ("Cgroups 限制与统计 CPU、内存、IO、PID 数量。v2 统一层次单挂载点。", [
            ("cpu.max", "cgroup v2 CPU 配额微秒周期。"),
            ("memory.max", "硬限制超则 OOM kill 容器内进程。"),
            ("io.weight", "块 IO 权重相对调度。"),
            ("pids.max", "防 fork 炸弹。"),
            ("systemd", "slice 管理用户会话与容器资源。"),
        ]),
        "UnionFS": ("联合文件系统层叠只读层与可写层，CoW 写时复制。overlay2 是 Docker 默认存储驱动。", [
            ("overlay2", "lowerdir+upperdir+workdir 合并挂载。"),
            ("写时复制", "修改文件拷贝到 upper 层，lower 不变。"),
            ("whiteout", "删除 lower 文件在 upper 创建遮挡字符设备。"),
            ("层共享", "多镜像共享相同 lower 层省磁盘。"),
            ("性能", "大量小文件或深度层链性能降，需扁平化。"),
        ]),
        "Docker基础": ("Docker CLI 与 daemon 通信，pull/run/exec/logs 管理容器生命周期。", [
            ("dockerd", "守护进程管理镜像容器网络卷。"),
            ("containerd", "高层运行时，shim 管理容器进程。"),
            ("runc", "OCI 标准运行时，创建 namespace+cgroups。"),
            ("docker run", "-d 后台 -p 端口映射 -v 卷 -e 环境变量。"),
            ("docker compose", "多容器 YAML 定义一键启动。"),
        ]),
        "Docker镜像": ("Dockerfile 指令构建镜像，层缓存加速重复构建。多阶段构建减小最终镜像。", [
            ("FROM/RUN/COPY", "基础镜像、执行命令、复制文件各一层。"),
            ("缓存失效", "变更层及后续层重建，指令顺序影响缓存。"),
            ("多阶段", "构建阶段与运行阶段分离，只拷产物。"),
            ("镜像扫描", "Trivy 查 CVE，基础镜像选 slim/alpine。"),
            ("digest", "sha256 不可变引用，非 tag 浮动。"),
        ]),
        "Docker网络": ("bridge 默认 NAT 出网，host 共享宿主机网络，overlay 跨主机 VXLAN。", [
            ("bridge", "docker0 虚拟交换机，容器 veth 对。"),
            ("端口映射", "-p 宿主机:容器，iptables DNAT。"),
            ("自定义网络", "user-defined bridge 支持 DNS 服务名解析。"),
            ("macvlan", "容器获局域网 MAC，如同物理机。"),
            ("CNI", "K8s 网络插件 Calico/Flannel 标准。"),
        ]),
        "Docker存储": ("volume 由 Docker 管理，bind mount 绑宿主机路径，tmpfs 内存文件系统。", [
            ("named volume", "docker volume create 持久化，备份迁移方便。"),
            ("bind mount", "开发时挂载源码，注意权限 SELinux :z。"),
            ("存储驱动", "overlay2/devicemapper，选择影响性能。"),
            ("数据容器", "volume 可挂载到多容器共享。"),
            ("备份", "docker run --volumes-from 打包 volume。"),
        ]),
        "容器安全": ("最小镜像、非 root 运行、只读根文件系统、seccomp/AppArmor 降攻击面。", [
            ("用户命名空间", "--userns-remap root 映射非特权用户。"),
            ("capability", "--cap-drop ALL --cap-add NET_BIND_SERVICE。"),
            ("seccomp", "默认 profile 禁危险 syscall，自定义 JSON。"),
            ("镜像信任", "Docker Content Trust 签名验证。"),
            ("逃逸防护", "禁 privileged --device 谨慎挂载内核模块。"),
        ]),
        "容器编排基础": ("Kubernetes 声明式管理 Pod、Service、Deployment。控制平面 API Server 对账期望状态。", [
            ("Pod", "最小调度单元，共享 network namespace。"),
            ("Deployment", "ReplicaSet 滚动更新无状态应用。"),
            ("Service", "ClusterIP/NodePort/LoadBalancer 稳定访问。"),
            ("ConfigMap/Secret", "配置与敏感数据注入容器。"),
            ("声明式", "kubectl apply YAML，控制器 reconcile。"),
        ]),
    }
    for mod, (intro, concepts) in ctr.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 基于 Linux 内核 Namespace/Cgroups 与 OCI 运行时，实现隔离、资源限制与标准化交付。",
            internals="runc 调 unshare/setns 创建隔离；containerd shim 托底容器进程。",
            workflow="编写 Dockerfile→build→push registry→run/compose→监控日志资源。",
            performance="减小镜像层；合理使用缓存；生产用 volume 非 bind 大量小文件。",
            security="非 root、只读根、扫描 CVE、网络策略限制东西向流量。",
            case_study="Java 服务镜像从 800MB 多阶段构建到 200MB，拉取时间减 70%。",
            configuration="daemon.json 存储驱动与日志驱动；compose 资源 limits。",
            debugging="docker inspect；nsenter -t PID -n ip addr；crictl K8s 节点。",
            comparison="Docker Compose 单机；Swarm 简单编排；K8s 功能最全复杂度高。",
            pitfalls=_pitfalls(
                ("容器内跑 systemd", "需 privileged 多 PID，反模式应单进程。"),
                ("latest 标签漂移", "生产应用 digest 固定版本。"),
                ("数据写容器层", "删容器丢数据，需 volume 持久化。"),
            ),
            practices=["多阶段构建小镜像", "非 root USER 指令", "健康检查 HEALTHCHECK", "资源 requests/limits"],
            references=["OCI Runtime Spec", "Docker Documentation", "Kubernetes Docs"],
        )

    # ===== 实时系统 (10) =====
    D = "实时系统"
    rts = {
        "实时系统概述": ("实时系统在规定时间内正确响应，分硬实时（错过失效）与软实时（可容忍偶尔超时）。", [
            ("确定性", "响应时间可预测有上界，非平均快。"),
            ("截止期", "任务 relative/absolute deadline。"),
            ("安全关键", "航空汽车医疗，认证标准 DO-178C ISO 26262。"),
            ("抖动", "响应时间变化，实时系统力求小抖动。"),
            ("可预测性", "比峰值性能更重要，WCET 分析核心。"),
        ]),
        "实时调度": ("固定优先级抢占、速率单调 RMS、最早截止期 EDF 是经典算法，需可调度性分析。", [
            ("抢占式", "高优先级就绪立即抢占低优先级运行。"),
            ("RMS", "周期越短优先级越高，利用率上界 n(2^(1/n)-1)。"),
            ("EDF", "截止期最近者优先，动态优先级利用率高。"),
            ("优先级继承", "PI 协议防优先级倒置。"),
            ("带宽保留", "为 aperiodic 任务保留 CPU 带宽。"),
        ]),
        "实时内核": ("RTOS 如 FreeRTOS/VxWorks 微秒级切换；PREEMPT_RT 使 Linux 接近硬实时。", [
            ("内核抢占", "CONFIG_PREEMPT 全内核可抢占减延迟。"),
            ("PREEMPT_RT", "线程化中断、优先级继承 mutex、迁移到打补丁内核。"),
            ("tickless", "NO_HZ_FULL 空闲核无 tick 减干扰。"),
            ("CPU 隔离", "isolcpus 核专供实时任务，不跑普通进程。"),
            ("内存锁定", "mlockall 防换页抖动。"),
        ]),
        "实时通信": ("现场总线 CAN、EtherCAT、TSN 时间敏感网络保证确定性传输延迟。", [
            ("CAN", "仲裁 ID 非破坏位仲裁，汽车标准。"),
            ("EtherCAT", "以太网帧飞读飞写，纳秒级同步。"),
            ("TSN", "IEEE 802.1Qbv 时间感知整形，工业以太网。"),
            ("共享内存", "同板多核最快 IPC，需同步。"),
            ("无锁队列", "SPSC 环形缓冲核间传数据。"),
        ]),
        "实时IO": ("周期性采样控制循环，ADC 定时触发 DMA 传输，控制算法固定周期执行。", [
            ("采样周期", "Nyquist 定理采样率至少 2 倍信号带宽。"),
            ("抖动控制", "定时器硬件触发减软件调度抖动。"),
            ("DMA 双缓冲", "乒乓缓冲连续采样不丢点。"),
            ("数字滤波", "FIR/IIR 实时滤波需 bounded 执行时间。"),
            ("执行时间测量", "GPIO 翻转或 trace 测 WCET。"),
        ]),
        "确定性保证": ("禁用或隔离干扰源：关 CPU 频率调节、绑核、锁内存、避免动态分配。", [
            ("WCET", "最坏情况执行时间，静态分析或测量上界。"),
            ("禁止 malloc", "实时路径用静态池预分配。"),
            ("中断亲和", "非实时中断移出隔离核。"),
            ("缓存效应", "冷缓存 WCET 大于热缓存，分析取上界。"),
            ("形式化验证", "模型检测证明调度可行性。"),
        ]),
        "容错设计": ("冗余、表决、看门狗与恢复策略保障安全关键系统可靠运行。", [
            ("三模冗余", "TMR 三份计算表决纠错。"),
            ("看门狗", "独立硬件定时器，超时复位系统。"),
            ("优雅降级", "传感器失效切换备份或安全模式。"),
            ("checkpoint", "周期保存状态故障后恢复。"),
            ("故障检测", "心跳与范围检查发现异常。"),
        ]),
        "性能分析": ("响应时间分析 RMA、事件跟踪、逻辑分析仪测端到端延迟。", [
            ("RMA", "速率单调分析利用率是否可调度。"),
            ("跟踪", "ftrace trace_irqsoff 测关中断时长。"),
            ("cyclictest", "PREEMPT_RT 测周期唤醒最大延迟。"),
            ("histogram", "延迟分布直方图，关注尾延迟。"),
            ("负载测试", "最坏场景同时激活所有任务。"),
        ]),
        "实时Linux": ("PREEMPT_RT 补丁主线合并中；Xenomai 双内核 cobalt 微内核协程。", [
            ("cyclictest", "标准基准测 Linux 实时性微秒到毫秒。"),
            ("CONFIG_NO_HZ_FULL", "全动态 tick 专用核。"),
            ("threadirqs", "中断线程化可设 SCHED_FIFO 优先级。"),
            ("Xenomai", "cobalt 内核优先 Linux 作为 idle 域。"),
            ("应用优先级", "chrt -f 99 设 FIFO 最高需注意饿死其他。"),
        ]),
        "嵌入式实时": ("MCU 裸机或 FreeRTOS，中断驱动+周期任务，资源极度受限。", [
            ("super loop", "主循环轮询标志，极简无 OS。"),
            ("tick 中断", "1ms tick 驱动 vTaskDelay 时间片。"),
            ("临界区", "portENTER_CRITICAL 关中断保护短临界区。"),
            ("栈大小", "每个任务栈需实测峰值用量。"),
            ("功耗", "idle hook 进 WFI 等中断唤醒。"),
        ]),
    }
    for mod, (intro, concepts) in rts.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 通过确定性调度、资源预留与干扰隔离，保证关键任务在截止期内完成。",
            internals="RTOS 就绪队列位图 O(1) 选最高优先级；Linux RT 线程化中断与 PI mutex。",
            workflow="任务划分→WCET 估算→可调度性分析→实现→cyclictest/逻辑分析仪验证。",
            performance="减抖动比提平均吞吐更重要；隔离核与锁内存是关键手段。",
            security="安全关键系统认证流程严格；故障注入测试验证容错。",
            case_study="运动控制周期 1ms，PREEMPT_RT+isolcpus 后最大抖动从 200μs 降至 15μs。",
            configuration="kernel cmdline isolcpus nohz_full；chrt/sched_setattr；FreeRTOSConfig tick rate。",
            debugging="ftrace latency tracers；logic analyzer 对照软件时间戳；cyclictest -p。",
            comparison="硬实时 RTOS vs 软实时 Linux：前者可认证；后者生态丰富。",
            pitfalls=_pitfalls(
                ("printf 进实时路径", "串口阻塞毫秒级破坏确定性。"),
                ("动态分配", "malloc 时间不确定，实时路径禁用。"),
                ("优先级设置错误", "控制任务优先级低于日志任务导致失控。"),
            ),
            practices=["测量而非猜测 WCET", "实时路径代码审查", "cyclictest 回归", "文档化调度假设"],
            references=["Liu & Layland RMS paper", "PREEMPT_RT Wiki", "FreeRTOS Real-Time Kernel Book"],
        )

    return len(MODULE_SNIPPETS)


if __name__ == "__main__":
    print(populate_part4())
