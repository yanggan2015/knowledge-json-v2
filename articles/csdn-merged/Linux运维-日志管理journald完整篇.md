# Linux 日志管理：journald 持久化、journalctl 与 rsyslog/logrotate

根分区被 `/var/log` 打满、重启丢日志、只读根写不进 journal，问题在 **Storage、RateLimit、转发链与轮转** 未对齐。本文按 journald 真实配置路径展开。

## 源码锚点

| 路径 / 手册 | 作用 |
|-------------|------|
| `man systemd-journald.service` | journald |
| `man journald.conf` | 主配置 |
| `man journalctl` | 查询 |
| `/etc/systemd/journald.conf` | 主配置 |
| `/etc/systemd/journald.conf.d/*.conf` | drop-in |
| `/var/log/journal/` | 持久存储 |
| `/run/log/journal/` | 非持久 |
| `/etc/logrotate.d/` | 轮转规则 |
| `/etc/rsyslog.d/` | rsyslog 片段 |
| `/dev/log` | syslog socket |

## 调用链

### 写入 journal

```mermaid
flowchart TD
    A[stdout/stderr] --> B[systemd/cgroup]
    C[syslog] --> D[/dev/log]
    D --> E[journald]
    B --> E
    E --> F{Storage}
    F -->|persistent| G[/var/log/journal/]
    F -->|volatile| H[/run/log/journal/]
```

### rsyslog + logrotate

```mermaid
flowchart LR
    J[journald] -->|ForwardToSyslog| R[rsyslog]
    R --> F[/var/log/messages]
    F --> L[logrotate]
    L --> F
```

## 重点知识

### journald.conf 核心

```ini
[Journal]
Storage=persistent
Compress=yes
SystemMaxUse=500M
SystemKeepFree=1G
RuntimeMaxUse=100M
MaxRetentionSec=1month
RateLimitIntervalSec=30s
RateLimitBurst=10000
ForwardToSyslog=yes
```

| Storage | 行为 |
|---------|------|
| auto | 有 /var/log/journal 则 persistent |
| persistent | 重启保留 |
| volatile | 仅 /run/log/journal |
| none | 不落盘 |

```bash
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal
sudo systemctl restart systemd-journald
journalctl --disk-usage
```

### journalctl 常用

```bash
journalctl -b
journalctl -b -1
journalctl --list-boots
journalctl -u nginx.service
journalctl -p err..emerg
journalctl -k
journalctl -f
journalctl --since '1 hour ago'
journalctl _COMM=sshd
journalctl _PID=1234
journalctl -o json-pretty
journalctl --verify
```

### RateLimit

洪水日志时出现 `Suppressed N messages`。

```ini
RateLimitIntervalSec=30s
RateLimitBurst=1000
```

service unit：`LogRateLimitIntervalSec=` `LogRateLimitBurst=`。

### 磁盘清理

```bash
journalctl --disk-usage
sudo journalctl --vacuum-size=200M
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-files=5
```

**勿**对 `/var/log/journal` 用 logrotate。

### rsyslog

```
*.info;mail.none;authpriv.none;cron.none    /var/log/messages
authpriv.*                                   /var/log/secure
cron.*                                       /var/log/cron
```

```bash
systemctl status rsyslog
logger -p user.notice 'test'
journalctl -t test -n 3
```

### logrotate

```
/var/log/nginx/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        invoke-rc.d nginx rotate >/dev/null 2>&1 || true
    endscript
}
```

```bash
logrotate -d /etc/logrotate.conf
logrotate -f /etc/logrotate.d/nginx
systemctl list-timers | grep logrotate
```

### 嵌入式只读根

| 策略 | 配置 |
|------|------|
| volatile | Storage=volatile; RuntimeMaxUse=32M |
| bind 可写分区 | mount --bind /data/log/journal /var/log/journal |
| 远程 | journal-remote / rsyslog @@central |

```bash
mount /dev/mmcblk0p2 /data
mkdir -p /data/log/journal
mount --bind /data/log/journal /var/log/journal
```

### 排障表

| 现象 | 查 | 处理 |
|------|----|------|
| 重启无历史 | list-boots | persistent |
| 盘满 | disk-usage | vacuum |
| 丢日志 | Suppressed | RateLimit/修源 |
| rsyslog 空 | status rsyslog | ForwardToSyslog |
| 只读根错 | dmesg | volatile/bind |

### syslog 优先级

| 级 | 名 | journalctl |
|----|-----|------------|
| 0 | emerg | `-p emerg` |
| 1 | alert | `-p alert` |
| 2 | crit | `-p crit` |
| 3 | err | `-p err` |
| 4 | warning | `-p warning` |
| 5 | notice | `-p notice` |
| 6 | info | `-p info` |
| 7 | debug | `-p debug` |

### 过滤 1：按 unit

```bash
journalctl _SYSTEMD_UNIT=ssh.service -n 20
```

### 过滤 2：按进程名

```bash
journalctl _COMM=nginx -n 20
```

### 过滤 3：按 UID

```bash
journalctl _UID=1000 -n 20
```

### 过滤 4：结构化 ID

```bash
journalctl MESSAGE_ID=... -n 20
```

### 过滤 5：正则 MESSAGE

```bash
journalctl --grep 'error|fail' -i -n 20
```

### 磁盘巡检 18

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 19

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 20

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 22

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 23

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 24

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 26

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 27

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 28

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 30

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 31

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 32

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 34

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 35

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 36

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 38

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 39

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 40

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 42

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 43

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 44

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 46

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 47

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 48

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 50

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 51

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 52

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 54

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 55

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 56

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 58

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 59

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 60

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 62

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 63

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 64

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 66

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 67

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 68

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 70

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 71

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 72

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 74

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 75

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 76

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 78

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 79

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

### 磁盘巡检 80

```bash
journalctl --disk-usage
df -h /var /run
du -sh /var/log/journal/* 2>/dev/null
du -sh /var/log/* | sort -h | tail -15
find /var/log -type f -size +100M -ls 2>/dev/null
ls -la /var/log/journal/
stat /etc/machine-id
systemctl show systemd-journald -p MemoryCurrent
grep -E '^Storage|^SystemMaxUse' /etc/systemd/journald.conf /etc/systemd/journald.conf.d/* 2>/dev/null
logrotate -d /etc/logrotate.conf 2>&1 | tail -5
journalctl -p err -b --no-pager | tail -10
```

