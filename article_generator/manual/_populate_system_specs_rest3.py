#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Populate remaining domains part 3: 汇编语言 through 实时系统."""

import sys
sys.path.insert(0, "/workspace/article_generator/manual")
from _system_module_specs import _add, _concepts, _pitfalls, MODULE_SNIPPETS


def populate_part3():
    # ===== 汇编语言 (10) =====
    D = "汇编语言"
    asm = {
        "汇编基础": ("汇编是机器指令助记符表示，与具体 ISA 绑定。理解寄存器、标志位与内存模型是阅读反汇编的基础。", [
            ("指令与操作码", "mov add 等助记符对应二进制操作码，汇编器翻译为机器码。"),
            ("寄存器", "通用寄存器存操作数，PC 程序计数器，FLAGS 条件标志。"),
            ("内存模型", "线性地址空间，字节编址，小端/大端序影响多字节存取。"),
            ("汇编器", "GAS/NASM 语法差异，产生 ELF 目标文件。"),
            ("链接脚本", "控制段布局与入口 _start。"),
        ]),
        "数据传送与运算": ("mov 传送数据，算术指令 add/sub/imul 修改标志位。lea 计算地址不访存，常用于快速算术。", [
            ("mov 限制", "x86 不能 mem to mem，需经寄存器中转。"),
            ("标志位", "ZF SF CF OF 用于后续条件跳转。"),
            ("扩展运算", "mul/imul 乘；div/idiv 除，隐含 rax/rdx。"),
            ("位运算", "and or xor not shl shr 用于掩码与快速乘除 2^n。"),
            ("cmp/test", "减法/与仅设标志不写回，配合 jcc 分支。"),
        ]),
        "流程控制": ("jmp 无条件跳转，jcc 条件跳转根据标志位。cmp+je/jne 实现 if，loop 指令递减 rcx。", [
            ("条件码", "je相等 jg大于 jl小于，有符号与无符号比较指令不同。"),
            ("跳转范围", "短跳转 8 位偏移，近跳转 32 位。"),
            ("if-else", "cmp→条件跳转 else 分支→jmp 汇合。"),
            ("switch", "跳转表 jmp [table+rax*8] 或 if-else 链。"),
            ("循环", "dec rcx jnz 或 cmp+jcc 顶部测试。"),
        ]),
        "子程序与栈": ("call 压返回地址跳转，ret 弹出返回。调用约定规定参数与保存寄存器责任。", [
            ("栈生长", "x86 栈向低地址生长，rsp 指向栈顶。"),
            ("栈帧", "rbp 帧指针链，局部变量负偏移，参数正偏移。"),
            ("cdecl", "调用者清栈，参数右到左压栈。"),
            ("x86_64 System V", "前 6 整参 rdi rsi rdx rcx r8 r9，余下栈传。"),
            ("叶子函数", "不调其他函数可省略帧指针 -fomit-frame-pointer。"),
        ]),
        "寻址方式": ("立即、寄存器、直接、寄存器间接、基址变址。x86 复杂寻址 [base+index*scale+disp]。", [
            ("立即寻址", "操作数在指令中，快但位数有限。"),
            ("寄存器间接", "[rax] 指向内存，需对齐访问。"),
            ("变址", "数组 base+index*element_size。"),
            ("RIP 相对", "x86_64 位置无关代码 PIC 访问全局。"),
            ("段寄存器", "x86 分段 fs gs 线程局部。"),
        ]),
        "中断与系统调用": ("int 软中断进入内核，syscall 指令快速入口。用户态通过寄存器传参。", [
            ("中断向量", "IDT 表项含处理函数地址与特权级。"),
            ("syscall", "x86_64 rax 号参数 rdi rsi rdx r10 r8 r9。"),
            ("内核态切换", "换栈、保存用户寄存器、启用内核页表。"),
            ("iret", "从中断返回用户态恢复上下文。"),
            ("vDSO", "gettimeofday 用户态映射无需 syscall。"),
        ]),
        "宏与伪指令": ("宏汇编重复代码块，伪指令 .data .text .global 控制段与符号。", [
            ("%macro", "NASM 带参宏，展开多次避免函数调用开销。"),
            ("equ", "符号常量不占存储。"),
            ("db dw dd dq", "定义字节字双字字数据。"),
            (".section", "ELF .text .data .bss .rodata 段。"),
            (".align", "对齐边界，cache line 与 SIMD 需要。"),
        ]),
        "x86_64汇编": ("64 位扩展 16 个通用寄存器，r8-r15。REX 前缀扩展编码，red zone 128 字节栈下空间。", [
            ("寄存器扩展", "rax-eax-ax-al 部分访问，写 32 位清零高 32。"),
            ("调用约定", "Windows x64 前 4 参 rcx rdx r8 r9，与 Linux 不同。"),
            ("red zone", "叶子函数可不调整 rsp 的 128 字节。"),
            ("SSE/AVX", "xmm ymm 向量寄存器 SIMD 运算。"),
            ("PIE", "位置无关可执行 ASLR 友好。"),
        ]),
        "ARM汇编": ("ARM AArch64 32 个 64 位寄存器 x0-x30，sp 单独。load/store 架构，条件码可选。", [
            ("AAPCS64", "x0-x7 参数，x0 返回值，x29 帧指针 x30 LR。"),
            ("load/store", "ldr/str 访存，不支持 mem 运算。"),
            ("条件执行", "A32 条件码；A64 用显式分支。"),
            ("Thumb", "A32 16/32 位混合省代码密度。"),
            ("SVC", "supervisor call 系统调用入口。"),
        ]),
        "汇编优化": ("手写汇编或内联 asm 优化热点。注意流水线、对齐与避免部分寄存器依赖。", [
            ("循环展开", "减分支开销，增寄存器压力。"),
            ("SIMD", "SSE AVX NEON 并行处理向量数据。"),
            ("内联汇编", "gcc __attribute__((asm)) 约束输入输出。"),
            ("对齐", "movdqa 需 16 字节对齐否则 fault。"),
            ("微架构", "Intel 手册查 latency/throughput 调度指令。"),
        ]),
    }
    for mod, (intro, concepts) in asm.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 通过汇编指令直接操控 CPU 寄存器与内存，经汇编器与链接器生成可执行代码。",
            internals="Intel/ARM 手册定义编码与行为；反汇编 objdump -d 对照源码。",
            workflow="Compiler Explorer 对比 C 与汇编；GDB disassemble 单步。",
            performance="热点函数内联 SIMD；避免错误推测分支；对齐数据。",
            security="栈溢出覆盖返回地址是经典漏洞，启用 NX 与 stack canary 防御。",
            case_study="memcpy SIMD 版本较通用 C 实现带宽提升数倍。",
            configuration="gcc -S 输出汇编；-masm=intel 语法；CFLAGS -march=native。",
            debugging="GDB break *addr；寄存器 info registers；单步 si/ni。",
            comparison="GAS Intel vs AT&T 语法：操作数顺序相反。",
            pitfalls=_pitfalls(
                ("调用约定错误", "参数寄存器用错导致崩溃或数据错。"),
                ("clobber 未声明", "内联 asm 破坏编译器假设的寄存器。"),
                ("栈对齐", "x86_64 调用前 rsp 16 字节对齐。"),
            ),
            practices=["先写 C 再优化看汇编", "遵守 ABI 文档", "用 intrinsics 代替手写 asm", "验证各优化级别输出"],
            references=["Intel SDM Volume 2", "ARM Architecture Reference Manual", "System V AMD64 ABI"],
        )

    # ===== 嵌入式系统 (10) =====
    D = "嵌入式系统"
    emb = {
        "嵌入式概述": ("嵌入式系统专用于特定任务，资源受限、实时性与可靠性要求高。MCU 与 MPU 选型决定软件栈复杂度。", [
            ("MCU vs MPU", "MCU 单片机无 MMU 跑 RTOS；MPU 如 Cortex-A 跑 Linux。"),
            ("交叉开发", "宿主机编译目标机运行，gdbserver 远程调试。"),
            ("Bootloader", "U-Boot 初始化硬件加载内核或应用。"),
            ("HAL", "硬件抽象层隔离寄存器操作与业务逻辑。"),
            ("看门狗", "超时复位防程序跑飞，需定期喂狗。"),
        ]),
        "嵌入式处理器": ("ARM Cortex-M 微控制器与 Cortex-A 应用处理器主导市场。时钟、复位与电源域由 RCC 配置。", [
            ("Cortex-M", "Thumb 指令，NVIC 嵌套中断，适合控制。"),
            ("存储器映射", "Flash 代码 SRAM 数据，外设寄存器固定地址。"),
            ("时钟树", "PLL 倍频，分频给 CPU/AHB/APB 总线。"),
            ("复位向量", "0 地址 SP 与 Reset_Handler 入口。"),
            ("FPU", "Cortex-M4F 硬件浮点，需编译 -mfpu。"),
        ]),
        "嵌入式操作系统": ("FreeRTOS、Zephyr、RT-Thread 提供任务调度与同步。裸机 super loop 适合极简应用。", [
            ("任务", "独立栈与优先级，抢占式调度。"),
            ("队列", "任务间传数据，阻塞发送接收。"),
            ("信号量", "资源计数与互斥，二值信号量作锁。"),
            ("定时器", "软件定时器回调，硬件 timer 驱动 tick。"),
            ("空闲钩子", "idle 任务进低功耗 WFI。"),
        ]),
        "设备驱动开发": ("嵌入式驱动直接操作寄存器，按参考手册配置 GPIO、UART、SPI、I2C。", [
            ("寄存器位域", "读-modify-写 注意原子性与竞态。"),
            ("GPIO", "输入输出模式，上拉下拉，速度驱动能力。"),
            ("UART", "波特率分频，帧格式 8N1，环形缓冲收发。"),
            ("DMA", "外设到内存自动搬运，减 CPU 中断频率。"),
            ("中断优先级", "NVIC 分组，高优先级可抢占低。"),
        ]),
        "外设接口": ("SPI 全双工主从，I2C 两线多主从，CAN 总线车载。时序与电气特性需对照手册。", [
            ("SPI", "CLK MOSI MISO CS，模式 0-3 CPOL CPHA。"),
            ("I2C", "开漏上拉，起始停止条件，7/10 位地址。"),
            ("CAN", "差分总线，仲裁 ID，错误帧与 ACK。"),
            ("ADC/DAC", "采样率分辨率，参考电压，DMA 连续采样。"),
            ("PWM", "定时器比较输出占空比，电机与 LED 调光。"),
        ]),
        "实时系统": ("硬实时错过截止即失效；软实时可容忍偶尔超时。WCET 分析保证可调度性。", [
            ("截止期", "任务必须在 D 内完成，相对释放时刻。"),
            ("抖动", "实际响应时间与最坏情况差，越小越确定。"),
            ("优先级倒置", "低优先级持锁阻塞高优先级，继承协议缓解。"),
            ("RMS", "速率单调，周期短优先级高，可调度利用率上界。"),
            ("EDF", "最早截止期优先，动态优先级，利用率可达 100%。"),
        ]),
        "嵌入式网络": ("LwIP 轻量 TCP/IP，MQTT CoAP 物联网协议。以太网 PHY 与 MAC 驱动集成。", [
            ("LwIP", "裸机或 RTOS，零拷贝 pbuf，内存池配置。"),
            ("MQTT", "发布订阅，QoS 0/1/2，轻量适合窄带。"),
            ("以太网", "RMII/MII 接 PHY，MAC 驱动 DMA 收发。"),
            ("Wi-Fi 模块", "AT 指令或 SDIO 协议栈在模块内。"),
            ("TLS mbed", "嵌入式加密库，证书链校验。"),
        ]),
        "低功耗设计": ("动态调频 DVS 与睡眠模式降功耗。测量各模式电流，优化唤醒频率与时长。", [
            ("睡眠模式", "Stop Standby 关时钟与外设，RAM 保持与否。"),
            ("WFI/WFE", "等待中断/事件指令进低功耗。"),
            ("外设门控", "不用外设关时钟减漏电。"),
            ("DVFS", "负载低降频降压，高负载升频。"),
            ("能量采集", "太阳能振动供电，超低功耗设计。"),
        ]),
        "嵌入式调试": ("JTAG/SWD 边界扫描，逻辑分析仪抓时序。Semihosting 通过调试器 I/O。", [
            ("SWD", "两线 Serial Wire Debug，Cortex-M 常用。"),
            ("OpenOCD", "开源调试服务器，GDB 远程 target remote。"),
            ("逻辑分析仪", "多通道数字采样，解析 SPI I2C 协议。"),
            ("Trace", "ETM 指令 trace，分析实时行为。"),
            ("断言与日志", "UART 打印或 RTT 缓冲输出。"),
        ]),
        "嵌入式安全": ("安全启动验证固件签名，TrustZone 隔离安全世界。侧信道与故障注入需硬件对策。", [
            ("Secure Boot", "ROM 校验 bootloader 签名链。"),
            ("TrustZone", "安全与非安全世界，SMC 切换。"),
            ("加密存储", "Flash 加密，密钥存 OTP/eFuse。"),
            ("调试口", "生产关闭 JTAG 防读取固件。"),
            ("OTA", "签名差分升级，回滚防砖。"),
        ]),
    }
    for mod, (intro, concepts) in emb.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 在资源受限环境下通过直接硬件控制或 RTOS 抽象完成任务调度与外设访问。",
            internals="参考 STM32/NXP 等 Reference Manual 寄存器定义；启动文件 vector table。",
            workflow="CubeMX 生成初始化→HAL 驱动→应用逻辑→示波器/逻辑分析仪验证时序。",
            performance="中断尽量短；DMA 批量传输；低功耗模式平衡响应与电量。",
            security="最小功能固件；关闭调试口；加密通信与安全启动。",
            case_study="温湿度传感器 I2C 读数异常，示波器发现上拉电阻不足导致上升沿过慢。",
            configuration="FreeRTOSConfig.h 堆栈与 tick；设备树或 CubeMX 引脚时钟。",
            debugging="OpenOCD+GDB 断点；SWO ITM 打印；逻辑分析仪协议解码。",
            comparison="裸机简单确定；RTOS 适合多任务复杂系统。",
            pitfalls=_pitfalls(
                ("堆栈溢出", "任务栈设太小 HardFault，需 configCHECK_FOR_STACK_OVERFLOW。"),
                ("中断里阻塞", "ISR 调用阻塞 API 导致系统挂死。"),
                ("未初始化时钟", "外设访问前必须使能 GPIO 与总线时钟。"),
            ),
            practices=["阅读数据手册电气特性", "原理图与代码对照引脚", "WCET 估算关键路径", "量产前关调试口"],
            references=["ARM Cortex-M Programming Manual", "FreeRTOS Documentation", "STM32 Reference Manual"],
        )

    # ===== 驱动开发 (10) =====
    D = "驱动开发"
    drv = {
        "驱动模型基础": ("Linux 驱动遵循 bus-device-driver 模型，platform/PCI/USB 总线匹配 probe 初始化设备。", [
            ("struct device", "设备核心结构，kobject 与 sysfs 关联。"),
            ("struct device_driver", "驱动注册 name 与 of_match_table。"),
            ("probe/remove", "匹配成功初始化与卸载清理生命周期。"),
            ("module_init", "insmod 注册驱动，module_exit 注销。"),
            ("GPL 符号", "EXPORT_SYMBOL 导出供其他模块使用。"),
        ]),
        "字符设备驱动": ("字符设备按字节流访问，file_operations 实现 open/read/write/ioctl。", [
            ("register_chrdev", "分配主设备号，或 alloc_chrdev_region 动态。"),
            ("cdev", "字符设备抽象，cdev_add 关联 file_operations。"),
            ("copy_to_user", "内核到用户安全拷贝，不可直接解引用用户指针。"),
            ("ioctl", "设备控制命令，_IO/_IOR/_IOW 宏定义命令号。"),
            ("poll", "select/poll 等待可读可写，wait_queue。"),
        ]),
        "块设备驱动": ("块设备按扇区随机访问，请求队列与 bio 提交，文件系统在其上构建。", [
            ("gendisk", "块设备表示，分区表与 capacity。"),
            ("request_queue", "I/O 调度器合并请求，make_request_fn 或 blk-mq。"),
            ("bio", "块 I/O 描述，bio_for_each_segment 遍历段。"),
            ("blk-mq", "多队列块层，每 CPU 或硬件队列，减锁争用。"),
            ("分区", "add_partition 逻辑划分设备。"),
        ]),
        "网络设备驱动": ("net_device 表示网卡，ndo_start_xmit 发送，NAPI poll 接收。", [
            ("net_device", "注册 register_netdev，私有数据 netdev_priv。"),
            ("sk_buff", "分配 alloc_skb，dev_kfree_skb 释放。"),
            ("NAPI", "napi_schedule 软中断批量收包。"),
            ("ethtool", "驱动实现 get_settings 等诊断接口。"),
            ("MAC 地址", "dev_addr 六字节，本地管理位。"),
        ]),
        "平台设备驱动": ("platform_device 无即插即用，设备树或板文件声明资源。", [
            ("platform_driver", "driver.of_match_table 匹配 compatible。"),
            ("资源获取", "platform_get_resource IORESOURCE_MEM/IRQ。"),
            ("devm_ioremap", "映射物理地址到虚拟，devres 自动释放。"),
            ("设备树", "DTB 编译 dtc，内核启动解析。"),
            ("defer probe", "EPROBE_DEFER 等待依赖驱动加载。"),
        ]),
        "PCI设备驱动": ("PCI 配置空间枚举，pci_register_driver 匹配 vendor/device ID。", [
            ("配置空间", "BAR 寄存器映射 I/O 内存，pci_enable_device。"),
            ("DMA", "pci_alloc_consistent 或 dma_alloc_coherent。"),
            ("MSI-X", "多消息中断，pci_enable_msix 减共享中断。"),
            ("热插拔", "pci_register_driver 支持动态插拔。"),
            ("IOMMU", "DMA 地址转换与隔离，防恶意设备。"),
        ]),
        "USB设备驱动": ("USB 主机控制器调度传输，usb_driver 匹配 interface，URB 异步传输。", [
            ("USB 描述符", "设备配置接口端点层次，枚举过程。"),
            ("URB", "usb_submit_urb 异步，完成回调处理。"),
            ("控制传输", "端点 0 标准请求 GET_DESCRIPTOR。"),
            ("bulk/interrupt", "大流量与定时小包，isochronous 等时音视频。"),
            ("usbmon", "抓 USB 流量调试。"),
        ]),
        "输入子系统": ("input 核心统一键盘鼠标触摸，input_register_device 上报事件。", [
            ("input_event", "EV_KEY EV_REL EV_ABS 类型与 code value。"),
            ("evdev", "字符接口 /dev/input/eventX 用户态读取。"),
            ("设备树", "gpio-keys 等绑定定义按键。"),
            ("多点触摸", "ABS_MT_SLOT ABS_MT_POSITION 协议 B。"),
            ("power key", "INPUT_PROP_BUTTON 电源键上报。"),
        ]),
        "中断与定时": ("request_irq 注册中断，hrtimer 高精度定时，tasklet 底半部。", [
            ("IRQF_SHARED", "共享中断线多设备。"),
            ("threaded_irq", "handler 内核线程执行减硬中断时间。"),
            ("hrtimer", "hrtimer_init 纳秒定时回调。"),
            ("tasklet", "TASKLET_SOFTIRQ 上下文不可睡眠。"),
            ("workqueue", "可睡眠上下文延迟工作。"),
        ]),
        "驱动调试": ("dynamic_debug 控制 pr_debug，ftrace 跟踪，sysfs 属性读写寄存器。", [
            ("printk", "KERN_INFO 等级，dmesg 查看。"),
            ("debugfs", "调试文件系统，仅开发内核启用。"),
            ("ftrace", "function_graph 跟踪调用链。"),
            ("kmemleak", "检测内核内存泄漏。"),
            ("硬件辅助", "逻辑分析仪与 JTAG 对照软件行为。"),
        ]),
    }
    for mod, (intro, concepts) in drv.items():
        _add(D, mod, intro=intro, concepts=_concepts(*concepts),
            mechanism=f"{mod} 驱动在 probe 中申请资源、注册设备节点，中断或轮询处理硬件事件并向上层提交数据。",
            internals="Documentation/driver-api 与 LDD3 示例；阅读同类主线驱动源码。",
            workflow="设备树/模块参数配置→insmod→sysfs 验证→应用读写测试→压力与异常测试。",
            performance="NAPI 与 DMA；中断合并；per-CPU 统计减锁。",
            security="ioctl 权限检查；用户缓冲区 copy_from_user；IOMMU 隔离 DMA。",
            case_study="新网卡驱动 RX 丢包，调大 ring buffer 并开启 NAPI weight 后恢复。",
            configuration="modprobe 参数；udev rules；设备树 overlay。",
            debugging="echo file +p > /sys/kernel/debug/dynamic_debug/control；lspci -vvv。",
            comparison="字符设备简单流式；块设备扇区；网络设备 sk_buff 路径。",
            pitfalls=_pitfalls(
                ("probe 未检查返回值", " devm 函数失败未 return 导致后续空指针。"),
                ("中断上下文睡眠", "ISR 中 malloc 或 mutex_lock 崩溃。"),
                ("竞态卸载", "模块卸载时仍有 URB 或 work 未完成。"),
            ),
            practices=["用 devres 管理资源", "参考同类上游驱动", "checkpatch 风格", "文档化 sysfs 接口"],
            references=["Linux Device Drivers 3e", "Kernel driver-api documentation", "USB/PCI 规范"],
        )

    return len(MODULE_SNIPPETS)


if __name__ == "__main__":
    print(populate_part3())
