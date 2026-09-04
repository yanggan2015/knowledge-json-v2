# CSDN 每日优化发布登记表

> 用途：记录已优化并发布到 CSDN 的文章，避免重复发布。  
> 规则：本表只建一次；之后每次发布成功只追加行，禁止删改历史行。  
> Agent：发布前必须读取本表；发布成功后追加一行。

## 已发布记录

| 日期 | 相对路径 | 标题 | CSDN状态 | articleId / URL | 备注 |
|------|----------|------|----------|-----------------|------|
| 2026-08-29 | `Linux内核/chapters/024-进程管理与调度的源码级分析.md` | CFS 调度源码：从 schedule() 到 pick_next_entity 的 vruntime 公平 | 已发布 | 164173051 / https://mp.csdn.net/mp_blog/creation/success/164173051 | 首次定时流程实测 |
| 2026-08-29 | `Linux内核/chapters/044-内存管理的源码级分析.md` | 缺页与 page cache：从 handle_mm_fault 到 do_swap_page 的源码路径 | 已发布 | 164173074 / https://mp.csdn.net/mp_blog/creation/success/164173074 | 首次定时流程实测 |
| 2026-08-29 | `Linux内核/chapters/084-同步机制的源码级分析.md` | RCU 读多写少：从 rcu_read_lock 到 call_rcu 的宽限期 | 已发布 | 164173084 / https://mp.csdn.net/mp_blog/creation/success/164173084 | 首次定时流程实测 |
| 2026-08-29 | `Linux内核/chapters/064-中断与时间的源码级分析.md` | softirq 与 tasklet：从 irq_exit 到 __do_softirq 的下半部路径 | 已发布 | 164173096 / https://mp.csdn.net/mp_blog/creation/success/164173096 | 首次定时流程实测 |
| 2026-08-30 | `驱动开发/chapters/044-平台设备驱动的源码级分析.md` | platform 驱动匹配：从 platform_driver_register 到 probe 的 DT 绑定 | 已发布 | 164192498 / https://mp.csdn.net/mp_blog/creation/success/164192498 | 日更优化发布 |
| 2026-08-30 | `驱动开发/chapters/014-字符设备驱动的源码级分析.md` | 字符设备注册：从 cdev_add 到 chrdev_open 的 VFS 路径 | 已发布 | 164192507 / https://mp.csdn.net/mp_blog/creation/success/164192507 | 日更优化发布 |
| 2026-08-30 | `驱动开发/chapters/084-中断与定时的源码级分析.md` | 驱动中断与定时：从 request_threaded_irq 到 hrtimer 回调 | 已发布 | 164192521 / https://mp.csdn.net/mp_blog/creation/success/164192521 | 日更优化发布 |
| 2026-08-30 | `Linux系统编程/chapters/076-IO多路复用的源码级分析.md` | epoll 源码路径：从 epoll_ctl 到 ep_poll 的就绪唤醒 | 已发布 | 164192541 / https://mp.csdn.net/mp_blog/creation/success/164192541 | 日更优化发布 |
| 2026-08-30 | `Linux内核/chapters/004-内核基础与启动的源码级分析.md` | 内核启动链：从 start_kernel 到 kernel_init 的 initcall 路径 | 已发布 | 164203640 / https://mp.csdn.net/mp_blog/creation/success/164203640 | 日更优化发布 |
| 2026-08-30 | `驱动开发/chapters/004-驱动模型基础的源码级分析.md` | 驱动模型匹配：从 driver_register 到 bus->match/probe 的绑定路径 | 已发布 | 164203651 / https://mp.csdn.net/mp_blog/creation/success/164203651 | 日更优化发布 |
| 2026-08-30 | `驱动开发/chapters/024-块设备驱动的源码级分析.md` | 块设备 I/O：从 submit_bio 到 blk_mq queue_rq 的请求路径 | 已发布 | 164203688 / https://mp.csdn.net/mp_blog/creation/success/164203688 | 日更优化发布 |
| 2026-09-01 | `Linux内核/chapters/104-文件系统VFS的源码级分析.md` | VFS 打开路径：从 path_openat 到 inode->i_fop 的统一抽象 | 已发布 | 164287192 / https://mp.csdn.net/mp_blog/creation/success/164287192 | 日更优化发布 |
| 2026-09-01 | `Linux内核/chapters/124-网络协议栈的源码级分析.md` | TCP 发包路径：从 sock_sendmsg 到网卡 NAPI 的 sk_buff 旅程 | 已发布 | 164287218 / https://mp.csdn.net/mp_blog/creation/success/164287218 | 日更优化发布 |
| 2026-09-01 | `驱动开发/chapters/054-PCI设备驱动的源码级分析.md` | PCI 驱动绑定：从 pci_register_driver 到 probe 的 ID 表匹配 | 已发布 | 164287252 / https://mp.csdn.net/mp_blog/creation/success/164287252 | 日更优化发布 |
| 2026-09-01 | `驱动开发/chapters/064-USB设备驱动的源码级分析.md` | USB 接口驱动：从 usb_register_driver 到 URB 提交的绑定路径 | 已发布 | 164287279 / https://mp.csdn.net/mp_blog/creation/success/164287279 | 日更优化发布 |
| 2026-09-01 | `csdn-merged/Linux内核-内存管理完整篇.md` | Linux 内核内存管理完整篇：伙伴系统、SLUB、缺页、page cache 与 OOM 实战 | 已发布 | 164289252 / https://mp.csdn.net/mp_blog/creation/success/164289252 | 合并源：041,042,043,045,046,047（内存管理系列） |
| 2026-09-02 | `csdn-merged/Linux内核-中断处理从硬件到GIC完整篇.md` | 一篇搞懂 Linux 中断：从引脚、GIC 到 softirq 的完整链路 | 已发布 | 164302997 / https://mp.csdn.net/mp_blog/creation/success/164302997 | 硬件原理+GICv2/v3+IRQ子系统+softirq |
| 2026-09-02 | `csdn-merged/Linux内核-进程管理与调度完整篇.md` | Linux 进程调度完整篇：从 task_struct、fork 到 CFS/实时类与排障 | 已发布 | 164323124 / https://mp.csdn.net/mp_blog/creation/success/164323124 | 合并源：Linux内核/chapters/021,022,023,025,026,027-进程管理与调度* |
| 2026-09-02 | `csdn-merged/Linux内核-同步机制完整篇.md` | Linux 内核同步机制完整篇：spinlock、mutex、rwsem、RCU 选型与死锁排查 | 已发布 | 164323251 / https://mp.csdn.net/mp_blog/creation/success/164323251 | 合并源：Linux内核/chapters/081,082,083,085,086,087-同步机制* |
| 2026-09-02 | `csdn-merged/驱动开发-网络设备驱动完整篇.md` | 网卡驱动完整篇：从 net_device、NAPI 到收发包与排障 | 已发布 | 164323301 / https://mp.csdn.net/mp_blog/creation/success/164323301 | 合并源：驱动开发/chapters/031,032,033,034,035,036-网络设备驱动* |
| 2026-09-02 | `csdn-merged/驱动开发-输入子系统完整篇.md` | Linux 输入子系统完整篇：从 input_dev、evdev 到按键/触控上报 | 已发布 | 164323347 / https://mp.csdn.net/mp_blog/creation/success/164323347 | 合并源：驱动开发/chapters/071,072,073,074,075,076-输入子系统* |
| 2026-09-03 | `csdn-merged/Linux内核-文件系统VFS完整篇.md` | Linux VFS 完整篇：从 path_openat、dentry/inode 到 page cache 与挂载排障 | 已发布 | 164358459 / https://mp.csdn.net/mp_blog/creation/success/164358459 | 合并源：Linux内核/chapters/101,102,103,105,106,107-文件系统VFS* |
| 2026-09-03 | `csdn-merged/Linux内核-设备驱动模型完整篇.md` | Linux 设备驱动模型完整篇：bus/device/driver、sysfs、延迟 probe 与绑定排障 | 已发布 | 164358509 / https://mp.csdn.net/mp_blog/creation/success/164358509 | 合并源：Linux内核/chapters/141,142,143,144,145,146-设备驱动模型* |
| 2026-09-03 | `csdn-merged/Linux内核-系统调用与IPC完整篇.md` | Linux 系统调用与 IPC 完整篇：从 syscall 入口、VDSO 到 pipe/shm/futex 选型 | 已发布 | 164358548 / https://mp.csdn.net/mp_blog/creation/success/164358548 | 合并源：Linux内核/chapters/161,162,163,164,165,166-系统调用与IPC* |
| 2026-09-03 | `csdn-merged/Linux内核-性能调优与追踪完整篇.md` | Linux 性能调优与追踪完整篇：ftrace、perf、eBPF 从采样到落地验证 | 已发布 | 164358582 / https://mp.csdn.net/mp_blog/creation/success/164358582 | 合并源：Linux内核/chapters/181,182,183,184,185,186-性能调优与追踪* |
