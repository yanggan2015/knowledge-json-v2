# Linux 日志管理：journald、rsyslog 与 logrotate

「服务挂了但日志没有」、磁盘被日志写满、容器里找不到 journal，根因通常是 **存储后端、持久化目录、速率限制与轮转策略** 没对齐。

## 源码锚点

| 路径 / 手册 | 作用 |
|-------------|------|
| `man journalctl` | 查询 journal |
| `man journald.conf` | 持久化、大小上限 |
| `/etc/systemd/journald.conf` | 主配置 |
| `man rsyslogd` | 传统 syslog |
| `man logrotate` | 文本日志轮转 |

## 调用链

```mermaid
flowchart LR
    A[进程 stdout/stderr/sd_journal] --> B[journald]
    B --> C[(volatile 或 persistent)]
    B --> D[转发 rsyslog 可选]
    D --> E[/var/log/*.log]
    E --> F[logrotate]
```

## 重点知识

### 持久化

```bash
# /var/log/journal 存在且 Storage=persistent 时重启可查
mkdir -p /var/log/journal
systemctl restart systemd-journald
journalctl --disk-usage
```

`SystemMaxUse=` / `RuntimeMaxUse=` 防止日志吃光盘。

### 常用查询

```bash
journalctl -u nginx -b --no-pager
journalctl -p err..alert --since "1 hour ago"
journalctl -k -b   # 内核环缓
journalctl -f -u myapp
```

### 与 rsyslog

不少发行版 journald 仍转发到 rsyslog，文本文件继续给老脚本用。改一处前先确认应用写的是 journal、syslog 还是自己的文件。

### logrotate

```bash
cat /etc/logrotate.d/*
logrotate -d /etc/logrotate.conf   # 演练
```

关注 `daily/weekly`、`rotate`、`compress`、`copytruncate` vs `create`。

### 嵌入式

只读根把 journal 指到可写分区；必要时 `Storage=volatile` 保寿命，关关键故障抓 `/tmp` 环形缓冲。
