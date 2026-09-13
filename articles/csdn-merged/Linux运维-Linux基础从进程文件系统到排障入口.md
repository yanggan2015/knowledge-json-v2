# 登录就能干活？从 Shell、进程、文件系统到 /proc 排障入口讲透

SSH 登上生产机，磁盘满、服务起不来、网络 ping 通 curl 挂——若只会 `reboot`，每次故障都像摸黑。Linux 运维的基本盘不是背命令表，而是 **用户空间如何组织：Shell 解析命令 → 进程与信号 → FHS 与挂载 → systemd 拉服务 → 网络与日志 → /proc /sys 观测**。本文按这条线讲透 **装完系统后第一次排障该看哪**，锚点覆盖 `/proc`、`/sys`、`man 7 signal`、`ip`/`ss`、`journalctl`、`systemctl`；glibc 与 busybox 用户态差异点到为止，不深挖 libc 实现。

## 阅读地图

1. **第一层：Shell 与权限直觉**——解决「命令谁执行、权限为何 denied、环境变量从哪来」。
2. **第二层：进程、信号与资源**——解决「僵尸、D 状态、OOM、ulimit 怎么读」。
3. **第三层：FHS、挂载与设备**——解决「文件该放哪、mount 链、块设备从哪来」。
4. **第四层：systemd 与服务**——解决「unit 状态、依赖、开机顺序、失败为何重启不了」。
5. **第五层：网络与日志入口**——解决「ip/ss 看连接、journalctl 追日志、常见连通性分层」。
6. **第六层：/proc /sys 排障闭环**——解决「CPU/内存/内核参数/驱动状态从哪读」。

## 源码锚点（用户态与内核接口）

| 路径 / 手册 | 作用 |
|-------------|------|
| `/proc` | 进程与内核运行时伪文件系统 |
| `/sys` | sysfs：设备、驱动、内核对象 |
| `man 7 signal` | 信号语义与默认动作 |
| `man 5 proc` | `/proc` 各文件含义 |
| `man 5 systemd.unit` | unit 类型与依赖 |
| `fs/proc/`（内核） | procfs 实现 |
| `fs/sysfs/`（内核） | sysfs 实现 |
| `kernel/signal.c` | 信号投递 |
| `kernel/exit.c` | 进程退出、僵尸回收 |
| `systemd` unit 文件 | `/usr/lib/systemd/system/` |
| `glibc` | 完整 POSIX API、NSS、locale |
| `busybox` | 嵌入式裁剪命令与 applet |

---

## 调用链

### 从登录到一条命令执行

```mermaid
flowchart LR
    SSH[sshd] --> SHELL[登录 Shell bash]
    SHELL --> PATH[PATH 查可执行文件]
    PATH --> EXEC[execve 加载 ELF]
    EXEC --> GLIBC[glibc 或 musl]
    GLIBC --> SYSCALL[系统调用]
    SYSCALL --> KERN[内核 VFS / sched / net]
```

### 排障信息源

```mermaid
flowchart TB
    SYM[现象: 慢/挂/错] --> PROC[/proc: pid stat status fd]
    SYM --> SYS[/sys: block net class]
    SYM --> JOUR[journalctl / 文件日志]
    SYM --> SVC[systemctl status]
    SYM --> NET[ip ss ping curl]
    PROC --> ACT[动作: kill mount restart tune]
    SYS --> ACT
    JOUR --> ACT
    SVC --> ACT
    NET --> ACT
```

---

## 一、Shell 与权限直觉

### 1.1 Shell 在干什么

登录后默认 Shell（常见 `bash`）负责：

- **解析**：管道 `|`、重定向 `>`、子 shell `()`、环境变量 `$VAR`。
- **查找命令**：按 `$PATH` 顺序找可执行文件；**内置命令**（`cd`、`export`）不查 PATH。
- **启动程序**：最终 `execve()` 替换当前进程镜像。

```bash
echo $SHELL
echo $PATH
type -a ls
which -a python3
```

### 1.2 用户、组与权限位

```bash
id
ls -l /etc/shadow
```

| 字段 | 含义 |
|------|------|
| rwx r-x r-- | user / group / other |
| 目录 x | 进入目录权限 |
| setuid 位 | 执行时有效 UID 变为文件属主（如 `passwd`） |

**root 不是万能**：`CAP_SYS_ADMIN` 分区、`immutable` 属性、`SELinux`/`AppArmor` 仍可挡。

```bash
getfacl file
lsattr -d /path    #  immutable?
```

### 1.3 sudo 与 privilege

```bash
sudo -l
sudo -i    # root 登录 shell
sudo cmd   # 单命令
```

排障时区分 **「当前用户看不到」** 与 **「服务本身配置错」**：用 `sudo -u appuser -H bash` 复现应用视角。

### 1.4 环境变量与 systemd 差异

交互 Shell 读 `~/.bashrc`；**cron/systemd 服务默认干净环境**，常缺 `PATH` 或 `JAVA_HOME`。

```bash
systemctl show myapp -p Environment
cat /etc/systemd/system/myapp.service.d/override.conf
```

服务 unit 里显式：

```ini
[Service]
Environment=JAVA_HOME=/usr/lib/jvm/java-17
EnvironmentFile=-/etc/default/myapp
```

### 1.5 glibc vs busybox（直觉）

| | glibc 系发行版 | busybox 嵌入式 |
|--|----------------|----------------|
| 命令 | GNU coreutils | busybox applet |
| 脚本 | bash | ash/dash |
| 体积 | 大 | 小 |
| 排障 | 工具全 | 部分选项缺失 |

嵌入式上 `ps`/`top` 输出字段可能不同，**脚本别假设 GNU 扩展**。

---

## 二、进程、信号与资源

### 2.1 进程树

```bash
ps auxf
ps -eLo pid,ppid,tid,stat,comm
pstree -p
```

| STAT | 含义 |
|------|------|
| R | 运行或可运行 |
| S | 可中断睡眠 |
| D | 不可中断睡眠（常等 IO） |
| Z | 僵尸（已退出未 wait） |
| T | 停止（SIGSTOP） |

### 2.2 信号（man 7 signal）

常用：

| 信号 | 默认 | 运维用途 |
|------|------|----------|
| SIGTERM (15) | 终止 | `kill` 优雅停服务 |
| SIGKILL (9) | 终止 | 强杀，不可捕获 |
| SIGHUP (1) | 终止 | 重载配置（看程序） |
| SIGINT (2) | 终止 | Ctrl+C |
| SIGSTOP/SIGCONT | 停/继续 | 调试 |

```bash
kill -TERM $pid
kill -0 $pid && echo alive
systemctl kill -s HUP nginx
```

**僵尸**：子进程结束父进程未 `wait()`。查：

```bash
ps aux | awk '$8 ~ /Z/ {print}'
# 父进程是谁
ps -o ppid= -p <zombie_pid>
```

长期僵尸 → 修 **父进程**（常是 buggy 守护进程），不是 kill 僵尸本身。

### 2.3 /proc/PID 关键文件

```bash
PID=1234
ls /proc/$PID/
cat /proc/$PID/status    # Name, State, VmRSS, Cap
cat /proc/$PID/cmdline | tr '\0' ' '
cat /proc/$PID/environ | tr '\0' '\n' | head
ls -l /proc/$PID/fd
cat /proc/$PID/limits
cat /proc/$PID/cgroup
```

| 文件 | 内容 |
|------|------|
| `status` | 内存、UID、线程数 |
| `fd/` | 打开的文件/socket |
| `limits` | ulimit 实际上限 |
| `cgroup` | cgroup v1/v2 归属 |
| `stack` | 内核栈（需权限） |

### 2.4 负载、CPU 与内存

```bash
uptime
top
htop
vmstat 1
free -h
cat /proc/meminfo
cat /proc/loadavg
```

**load average** 含 **D 状态** 任务——load 高但 CPU 闲，先查 **IO/磁盘**。

### 2.5 OOM

```bash
dmesg | grep -i oom
journalctl -k | grep -i oom
cat /proc/sys/vm/overcommit_memory
```

OOM killer 选进程看 `oom_score`：

```bash
cat /proc/$PID/oom_score
```

### 2.6 ulimit 与 systemd Limit*

```bash
ulimit -a
cat /proc/$PID/limits
systemctl show myapp -p LimitNOFILE
```

「Too many open files」→ 对齐 **服务 LimitNOFILE** 与 **应用配置**。

---

## 三、FHS、挂载与设备

### 3.1 FHS 要点

| 路径 | 用途 |
|------|------|
| `/` | 根 |
| `/etc` | 配置 |
| `/var` | 可变数据、日志、lib |
| `/usr` | 用户态程序与库 |
| `/opt` | 第三方大包 |
| `/tmp` | 临时 |
| `/home` | 用户家目录 |
| `/root` | root 家目录 |
| `/dev` | 设备节点 |
| `/proc` `/sys` | 内核接口 |

**配置改哪**：应用文档为准；包管理安装多在 `/etc` + `/usr/lib/systemd`。

### 3.2 挂载与 fstab

```bash
findmnt
mount | column -t
cat /etc/fstab
lsblk -f
blkid
```

`/etc/fstab` 字段：设备 UUID、挂载点、类型、选项、dump、fsck 顺序。**UUID 优于 /dev/sdX**（盘符会变）。

```bash
# 示例
UUID=xxxx  /data  xfs  defaults,noatime  0  2
```

### 3.3 块设备与 LVM

```bash
lsblk
pvs; vgs; lvs
df -hT
du -sh /var/*
```

**磁盘满** 分层：

1. `df -h` 哪个 mount 100%？
2. `du` 大目录？
3. 删了文件但空间未释？→ **进程仍持有 fd**：

```bash
lsof +L1 | grep deleted
# 或
ls -l /proc/*/fd 2>/dev/null | grep deleted
```

### 3.4 /dev 与设备节点

```bash
ls -l /dev/sda*
ls -l /dev/disk/by-uuid/
```

字符设备 vs 块设备；`mknod` 仅在特殊场景。

---

## 四、systemd 鸟瞰

### 4.1 unit 类型

| 类型 | 后缀 | 例子 |
|------|------|------|
| service | `.service` | nginx.service |
| socket | `.socket` | docker.socket |
| target | `.target` | multi-user.target |
| mount | `.mount` | var.mount |
| timer | `.timer` | 定时任务 |

### 4.2 状态与开机

```bash
systemctl status nginx
systemctl is-active nginx
systemctl is-enabled nginx
systemctl list-dependencies multi-user.target
systemctl list-units --failed
```

失败时：

```bash
journalctl -u nginx -b --no-pager -n 100
systemctl cat nginx
```

### 4.3 依赖与顺序

`After=` / `Before=` 是 **顺序**；`Requires=` / `Wants=` 是 **依赖**。`Requires` 失败会拖垮；`Wants` 弱依赖。

```ini
[Unit]
After=network-online.target
Wants=network-online.target
```

### 4.4 重启策略

```ini
[Service]
Restart=on-failure
RestartSec=5s
StartLimitBurst=3
StartLimitIntervalSec=60
```

**重启风暴**：看 `StartLimit` 与根本错误（端口占用、配置语法）。

### 4.5 target 与运行级别对照

| 传统 runlevel | systemd target |
|---------------|----------------|
| 3 | multi-user.target |
| 5 | graphical.target |
| 0 | poweroff.target |

```bash
systemctl get-default
systemctl isolate multi-user.target
```

---

## 五、网络基础命令

### 5.1 ip 替代 ifconfig/route

```bash
ip link
ip addr
ip route
ip neigh
ip -s link
```

配地址（临时）：

```bash
sudo ip addr add 192.168.1.10/24 dev eth0
sudo ip link set eth0 up
sudo ip route add default via 192.168.1.1
```

持久化：NetworkManager、`netplan`（Ubuntu）、`/etc/sysconfig/network-scripts`（RHEL 系）——**发行版不同文件不同**。

### 5.2 ss 看 socket

```bash
ss -tulpn
ss -tan state established
ss -o state established '( dport = :443 )'
```

| 场景 | 命令 |
|------|------|
| 端口是否在听 | `ss -tlnp \| grep :80` |
| 连接数过多 | `ss -s` |
| 进程占端口 | `-p` 需 root |

### 5.3 连通性分层

```bash
ping -c 3 8.8.8.8
ping -c 3 gateway
tracepath example.com
curl -v --connect-timeout 3 https://example.com
dig +short example.com
```

| 层 | 失败含义 |
|----|----------|
| L2 | 链路 down、网线/VLAN |
| L3 | 无路由、IP 错 |
| DNS | 能 ping IP 不能 ping 域名 |
| TCP | 防火墙、服务未 listen |
| TLS/应用 | 证书、HTTP 502 |

### 5.4 防火墙入口

```bash
# nftables
sudo nft list ruleset
# 或 firewalld
sudo firewall-cmd --list-all
# 传统 iptables
sudo iptables -L -n -v
```

「本机 curl localhost 通、外部不通」→ 听地址 `0.0.0.0` vs `127.0.0.1` + 防火墙。

### 5.5 /proc/net

```bash
cat /proc/net/tcp
cat /proc/net/dev
sysctl net.ipv4.ip_forward
```

---

## 六、日志入口

### 6.1 journalctl

```bash
journalctl -b                  # 本次启动
journalctl -u nginx -f
journalctl -p err -b
journalctl --since "1 hour ago"
journalctl -k                  # 内核
journalctl _PID=1234
```

持久化 journal 需 `/var/log/journal` 存在且 `Storage=persistent`（`journald.conf`）。

### 6.2 传统文本日志

```bash
ls /var/log/
tail -F /var/log/messages      # RHEL 系
tail -F /var/log/syslog        # Debian 系
tail -F /var/log/nginx/error.log
```

应用日志路径在 **unit 的 StandardOutput** 或应用 config。

### 6.3 rsyslog / 转发

`/etc/rsyslog.conf` 决定内核与应用日志落盘与转发。**排障先本地 `-f` 跟 unit**，再查集中日志延迟。

---

## 七、/proc 系统级观测

### 7.1 CPU

```bash
lscpu
cat /proc/cpuinfo
grep . /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 2>/dev/null
mpstat -P ALL 1
```

### 7.2 内存

```bash
cat /proc/meminfo
slabtop
grep -i dirty /proc/meminfo
```

### 7.3 内核命令行与版本

```bash
cat /proc/cmdline
uname -r
cat /proc/version
```

### 7.4 模块

```bash
lsmod
modinfo e1000
cat /proc/modules
```

### 7.5  sysctl

```bash
sysctl -a | grep ip_forward
sysctl -w net.ipv4.ip_forward=1   # 临时
# 永久 /etc/sysctl.d/*.conf
```

### 7.6 进程级汇总脚本（示例）

```bash
# 内存占用 Top 10
ps aux --sort=-%mem | head -11
# 按线程看 CPU
ps -eLo pid,tid,pcpu,comm --sort=-pcpu | head -20
```

---

## 八、/sys 与设备驱动

### 8.1 布局直觉

```bash
ls /sys/block/
ls /sys/class/net/
ls /sys/devices/pci0000:00/
```

| 路径 | 内容 |
|------|------|
| `/sys/class/net/eth0` | 网卡属性 |
| `/sys/block/sda` | 块设备 |
| `/sys/fs/cgroup` | cgroup 层次 |

### 8.2 udev 与持久命名

```bash
udevadm info -a -n /dev/sda | head
ls /dev/disk/by-id/
```

### 8.3 调设备参数

```bash
cat /sys/class/net/eth0/speed
cat /sys/block/sda/queue/scheduler
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler
```

**重启丢失** → 写 udev rule 或 tuned/profile。

---

## 九、「装完系统不会排障」闭环案例

### 9.1 案例 A：Web 502

```bash
systemctl status myapp
journalctl -u myapp -n 50 --no-pager
ss -tlnp | grep :8080
curl -v http://127.0.0.1:8080/
```

路径：**服务活吗 → 端口听吗 → 本机 curl → 上游 nginx 配置**。

### 9.2 案例 B：SSH 能登，业务端口不通

```bash
ss -tlnp | grep :443
sudo nft list ruleset | grep 443
sudo iptables -L INPUT -n -v
ip addr
```

路径：**listen 地址 → 防火墙 → 云安全组**（云上要控制台）。

### 9.3 案例 C：机器「卡死」但能 ping

```bash
uptime
vmstat 1 5
dmesg | tail -30
cat /proc/loadavg
ps aux | awk '$8 ~ /D/'
```

高 load + 大量 **D** → 存储或 NFS 挂住；**别急着 reboot**，先隔离存储。

### 9.4 案例 D：磁盘满

```bash
df -h
du -xhd1 /var | sort -h
journalctl --disk-usage
lsof +L1 | grep deleted
```

### 9.5 案例 E：CPU 100% 不知谁

```bash
top -H -p $(pgrep -d, myapp)
perf top -p $pid    # 若可装 perf
strace -cp $pid     #  syscall 占比（短暂）
cat /proc/$pid/stack
```

---

## 十、常用维护命令（非堆砌，带场景）

### 10.1 包管理（发行版相关）

```bash
# Debian/Ubuntu
apt search nginx
apt install -y nginx
apt show nginx

# RHEL/Fedora
dnf install -y nginx
rpm -ql nginx
```

### 10.2 定时任务

```bash
systemctl list-timers
crontab -l
ls /etc/cron.d/
```

systemd timer 优先于 cron 新部署（依赖清晰、日志进 journal）。

### 10.3 用户与登录

```bash
getent passwd appuser
last -a | head
who
w
```

### 10.4 时间

```bash
timedatectl
chronyc tracking    # 若 chrony
```

证书/API 故障常是 **时钟漂移**。

---

## 十一、安全与最小暴露（运维基本盘）

```bash
ss -tlnp    # 少开 0.0.0.0 端口
sudo grep PermitRootLogin /etc/ssh/sshd_config
sudo systemctl status sshd
```

生产：**密钥登录**、**sudo 审计**、**自动安全更新策略** 按公司基线。

---

## 十二、排障思维：先边界再深挖

1. **复现**：最小命令、是否稳定。
2. **分层**：硬件/网络/OS/配置/应用。
3. **对比**：同类正常节点 diff 配置。
4. **变更**：最近发布、内核、挂载、证书。
5. **记录**：命令输出贴 ticket，便于交接。

```mermaid
flowchart LR
    R[复现] --> L[分层]
    L --> C[对比正常机]
    C --> CH[查最近变更]
    CH --> F[修复 + 文档]
```

---

## 十三、/proc 与 /sys 对照表

| 需求 | /proc | /sys |
|------|-------|------|
| 进程内存 | `/proc/PID/status` | — |
| 打开文件 | `/proc/PID/fd` | — |
| CPU 信息 | `/proc/cpuinfo` | `/sys/devices/system/cpu/` |
| 网卡统计 | `/proc/net/dev` | `/sys/class/net/` |
| 块设备队列 | — | `/sys/block/*/queue/` |
| 内核参数 | `/proc/sys/` | 部分重复 |
| cgroup | `/proc/PID/cgroup` | `/sys/fs/cgroup/` |

`/proc/sys` 与 `sysctl` 互通；`/sys` 更偏 **kobject 设备模型**。

---

## 十四、与后续运维专题的衔接

| 本文 | 延伸 |
|------|------|
| systemd 基础 | systemd 服务管理完整篇 |
| journalctl | 日志管理 journald 完整篇 |
| 磁盘 df/du | 磁盘与文件系统管理完整篇 |
| ip/ss | 网络配置完整篇 |
| 性能 top/vmstat | 性能监控完整篇 |

---

## 十五、命令闭环：新机器验收 10 条

```bash
hostnamectl; uname -r
timedatectl
free -h; df -hT
ip -br addr; ip route
ss -tulpn
systemctl list-units --failed
journalctl -p err -b --no-pager | tail -20
cat /proc/cmdline
getenforce 2>/dev/null || aa-status 2>/dev/null | head
last -a | head -5
```

验收通过再谈业务部署，避免 **带病上线**。

---

## 十六、小结

Linux 运维基本盘是 **Shell 权限 → 进程信号 → FHS 挂载 → systemd → 网络日志 → /proc /sys**。排障时 **先 systemctl/journalctl 定服务，再 ss/ip 定网络，再 /proc/PID 定资源，再 df/du 定磁盘**；僵尸修父进程，磁盘满查 deleted fd，load 高看 D 状态与 IO。命令要挂在 **场景链** 上记，而不是 alphabet soup。

合并自 `articles/Linux运维/chapters/001～006`（Linux 基础系列）；发行版路径差异处以 RHEL/Debian 双系举例，以目标系统手册为准。
