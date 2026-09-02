# 每日 CSDN 主题合并发布（定时服务）

每天 **北京时间 08:00** 自动调用 Cursor `agent -p`：

**4 个主题包**（同模块多篇 chapter）→ **合并为 4 篇完整长文** → 发布 CSDN → 登记表 → `git push`。

> 不再「选 4 篇短 chapter 各发一篇」；而是保证每个知识点完整、篇幅足够。

## 合并策略

| 步骤 | 说明 |
|------|------|
| 聚类 | 如 `041~047-内存管理*` 属于同一主题包 |
| 合并 | 2～6 篇源 md → 1 篇 `articles/csdn-merged/*.md` |
| 图示 | 合并长文 **≥2 处 Mermaid**（调用链 + 架构/数据流） |
| 发布 | 每天 4 篇合并长文（CSDN 日额度） |
| 登记 | 成稿路径 + 备注列列出全部源 chapter |

## 文件

| 路径 | 作用 |
|------|------|
| `run.sh` | 入口：加锁、环境、`agent -p` |
| `PROMPT.md` | 正式日更提示词（4 主题包） |
| `PROMPT-TEST.md` | 测试提示词（1 主题包） |
| `csdn-daily-optimize.service` / `.timer` | systemd 用户单元 |
| `articles/csdn-merged/` | 合并成稿目录 |
| `articles/CSDN-DAILY-PUBLISHED.md` | 已发布登记表 |

## 测试单次发布

```bash
cd ~/knowledge-json-v2
PROMPT_FILE=scripts/daily-csdn/PROMPT-TEST.md \
DAILY_PUBLISH_COUNT=1 \
DISPLAY=:10 HEADLESS=0 \
bash scripts/daily-csdn/run.sh
```

## 正式日更

```bash
systemctl --user start csdn-daily-optimize.service
# 或
bash ~/knowledge-json-v2/scripts/daily-csdn/run.sh
```

## 注意

- CSDN 依赖本机浏览器登录态；`~/.config/csdn-daily.env` 配置 `DISPLAY`。
- 今日额度用尽时会存草稿；登记表仍追加源路径，避免重复合并。
