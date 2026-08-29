# 每日 CSDN 优选发布（定时服务）

每天 **本地时间 08:00** 自动调用 Cursor `agent -p`：在 `articles/` 选 4 篇最有吸引力的未发布文章 → 按质量标准优化并回写原文件 → 发布到 CSDN → 追加登记表 → `git push`。

## 文件

| 路径 | 作用 |
|------|------|
| `run.sh` | 入口：加锁、准备环境、调用 `agent -p` |
| `PROMPT.md` | 交给 Agent 的完整任务提示词 |
| `csdn-daily-optimize.service` / `.timer` | systemd 用户单元 |
| `install.sh` | 安装并启用 timer |
| `logs/` | 每次运行的文本日志 |
| `../articles/CSDN-DAILY-PUBLISHED.md` | 已发布登记表（只建一次，之后追加） |

## 安装

```bash
bash ~/knowledge-json-v2/scripts/daily-csdn/install.sh
```

可选：编辑 `~/.config/csdn-daily.env` 设置 `DISPLAY`、`AGENT_MODEL`、`CURSOR_API_KEY`。

## 常用命令

```bash
# 立即跑一次
systemctl --user start csdn-daily-optimize.service
# 或
bash ~/knowledge-json-v2/scripts/daily-csdn/run.sh

# 看下次触发时间
systemctl --user list-timers | grep csdn

# 看服务日志
journalctl --user -u csdn-daily-optimize.service -n 100 -f
ls -lt ~/knowledge-json-v2/scripts/daily-csdn/logs/
```

## 注意

- CSDN 发布依赖本机浏览器登录态（Chrome CDP / Firefox Cookie），定时触发时需 `DISPLAY` 可用。
- Agent 使用 `--force --sandbox disabled`，以便自动执行发布与 `git push`。
- 发文额度用尽时脚本会存草稿；登记表仍会追加，避免重复推同一篇。
