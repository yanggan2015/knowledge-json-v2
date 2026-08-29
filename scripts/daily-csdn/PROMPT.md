# 每日任务：优选 4 篇 → 优化 → 发布 CSDN → 回写 → git push

你是本仓库的自动化 Agent。请**严格按序**完成下列全部步骤，不要只规划不执行。

## 仓库与路径

- 工作目录：`~/knowledge-json-v2`
- 文章根目录：`~/knowledge-json-v2/articles/`（其下有多系列文件夹，如 `Linux内核/chapters/*.md`、`驱动开发/chapters/*.md` 等）
- 已发布登记表：`~/knowledge-json-v2/articles/CSDN-DAILY-PUBLISHED.md`
- 质量标准：`~/.agent/csdn-publish/QUALITY.md` 与 Cursor 规则 `csdn-article-quality`
- 发布脚本：`HEADLESS=0 bash ~/.agent/csdn-publish/publish.sh <md绝对路径>`

## 步骤 0：确认登记表存在

1. 若 `articles/CSDN-DAILY-PUBLISHED.md` **不存在**，按下列模板**新建一次**（含表头），然后继续：

```markdown
# CSDN 每日优化发布登记表

> 用途：记录已优化并发布到 CSDN 的文章，避免重复发布。
> 规则：本表只建一次；之后每次发布成功只追加行，禁止删改历史行。

## 已发布记录

| 日期 | 相对路径 | 标题 | CSDN状态 | articleId / URL | 备注 |
|------|----------|------|----------|-----------------|------|
```

2. 若已存在，**只读表头与已有行**，后续只追加，禁止清空或重写整表。

## 步骤 1：选出 4 篇「最有吸引力」且未发布的文章

1. 读取 `articles/CSDN-DAILY-PUBLISHED.md`，得到已发布的相对路径集合（表中「相对路径」列，相对 `articles/`）。
2. 在 `articles/` 下扫描各系列 `chapters/*.md`（跳过 `README.md`、`INDEX.md`、登记表自身、以及已在登记表中的路径）。
3. 从候选中选出 **恰好 4 篇** 最有吸引力的文章。吸引力优先看：
   - 标题具体、可检索、有痛点（非空泛「简介/浅谈」）
   - 题材偏嵌入式 / Linux 内核 / 驱动 / 实战排障（读者点击意愿高）
   - 正文已有一定骨架，优化后容易达标
4. 若不足 4 篇未发布候选，有几篇做几篇，并在最终汇报说明。

## 步骤 2：逐篇优化（直接改原文件）

对每一篇选中的 md：

1. 对照 `QUALITY.md` 九条硬门槛改写，结构必须含：**源码锚点 / 调用链 / 重点知识 / Checklist**。
2. **原地更新**原 md 文件（路径不变）。
3. 源码路径/符号必须真实；禁止编造 API；精简去水；知识面要闭环。
4. 不达标则继续改，直到自检通过，再进入发布。

## 步骤 3：发布到 CSDN

对每一篇优化通过的文章：

1. 再次确认该相对路径**不在**登记表中。
2. 执行：

```bash
HEADLESS=0 bash ~/.agent/csdn-publish/publish.sh "<文章绝对路径>"
```

3. 根据脚本输出如实判定（成功 / 草稿上限 / 需验证码等）。
4. **禁止**未跑脚本就声称已发布。

篇与篇之间若连续发布，间隔至少 20–60 秒（可用 `sleep`）。

## 步骤 4：追加登记表

每篇发布结果确定后，向 `articles/CSDN-DAILY-PUBLISHED.md` **追加一行**（不要改旧行）：

| 今日日期 YYYY-MM-DD | 相对路径如 `Linux内核/chapters/xxx.md` | 标题 | 已发布或草稿 | articleId 或完整 URL | 简短备注 |

草稿也要登记，避免明天重复推同一篇。

## 步骤 5：git 提交并 push

在 `~/knowledge-json-v2`：

1. `git status` / `git diff` 确认变更（优化后的 md + 登记表）。
2. 暂存相关文件并提交，提交说明示例：

```
daily: optimize and publish 4 CSDN articles

EOF
```

（用 HEREDOC 写 commit message；不要改 git config。）

3. **`git push` 到当前跟踪的远程分支**（需要网络权限时使用）。

## 最终汇报（必须）

用简短列表汇报：

- 选中的 4 篇路径与标题
- 每篇：优化要点一句话 + 发布结果（URL 或草稿链接或失败原因）
- 登记表是否已追加
- git commit hash 与 push 是否成功
