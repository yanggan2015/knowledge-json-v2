# 每日任务：主题合并 → 产出 4 篇完整长文 → 发布 CSDN → 登记 → git push

你是本仓库的自动化 Agent。请**严格按序**完成下列全部步骤，不要只规划不执行。

## 核心策略（必读）

**CSDN 每日额度：4 篇。** 不要直接把 4 个零散 chapter 各发一篇——它们往往篇幅过小、知识点割裂。

正确做法：

1. 在 `articles/` 下按**同一知识点/同一模块**聚类（例如 `Linux内核/chapters/041~047` 都属于「内存管理」）。
2. 将 **2～6 篇**同源 md **合并重写**为 **1 篇完整长文**，保证该知识点从概念→机制→源码→配置→排障→Checklist **闭环**。
3. 每天产出并发布 **恰好 4 篇**这样的合并长文（=CSDN 额度打满）。
4. 合并后的成稿写入 `articles/csdn-merged/<系列>-<主题>.md`（单文件对应 CSDN 一篇）。

**篇幅与质量**：合并文建议 **2500～6000 字**（信息密度优先，不注水）；必须含 **源码锚点 / 调用链 / 重点知识 / Checklist**；**有必要处用 Mermaid 框图**（合并长文 ≥2 处，至少 1 处在调用链）；对照 `~/.agent/csdn-publish/QUALITY.md` 九条硬门槛。

## 仓库与路径

- 工作目录：`~/knowledge-json-v2`
- 文章源：`~/knowledge-json-v2/articles/<系列>/chapters/*.md`
- 合并成稿目录：`~/knowledge-json-v2/articles/csdn-merged/`（不存在则创建）
- 已发布登记表：`~/knowledge-json-v2/articles/CSDN-DAILY-PUBLISHED.md`
- 质量标准：`~/.agent/csdn-publish/QUALITY.md`
- 发布脚本：`HEADLESS=0 bash ~/.agent/csdn-publish/publish.sh <成稿绝对路径>`

## 步骤 0：确认登记表

1. 若 `articles/CSDN-DAILY-PUBLISHED.md` 不存在，按模板**新建一次**（含表头）。
2. 已存在则**只读**；发布成功后**只追加行**，禁止删改历史。

登记表列：`| 日期 | 相对路径 | 标题 | CSDN状态 | articleId / URL | 备注 |`

- **相对路径**：写合并成稿路径，如 `csdn-merged/Linux内核-内存管理完整篇.md`
- **备注**：列出**已合并的源 chapter 相对路径**（逗号分隔），避免日后重复合并发布

## 步骤 1：规划 4 个「主题包」

1. 读取登记表，收集已发布的成稿路径 + 备注中的源 chapter 路径。
2. 扫描 `articles/*/chapters/*.md`，按目录名/文件名前缀聚类（如 `041-内存管理…`～`047-内存管理…` 为一包）。
3. 选出 **4 个**未发布过的主题包。优先级：
   - 嵌入式 / Linux 内核 / 驱动 / 系统编程
   - 标题可检索、有痛点
   - 源 chapter ≥2 篇且尚未在登记表「备注」中出现
4. 若 `DAILY_PUBLISH_COUNT` 环境变量已设置（如测试 `=1`），则只处理对应篇数并在汇报说明。

## 步骤 2：逐包合并重写

对每个主题包：

1. 读取该包全部源 md，提取真实知识点（去重、去模板水词）。
2. 写一篇**新结构**的合并长文，写入 `articles/csdn-merged/<系列>-<主题>.md`。
3. 结构必须含：导语、源码锚点（真实路径+短代码）、**调用链（含 Mermaid flowchart）**、重点知识（分小节）、Checklist（≥5 条）。
4. **Mermaid**：合并长文至少 **2 处**——① 主调用链/分支（`flowchart TD`）；② 模块分层或数据流（`flowchart TB/LR`）。节点标签与源码锚点一致，禁止编造调用关系。
5. **可选**：在源 chapter 文件末尾追加一行 `> 已合并至 csdn-merged/xxx.md（YYYY-MM-DD）`，便于追溯；**不要**删除源文件。
6. 自检不达标则继续改，直到通过再发布。

## 步骤 3：发布到 CSDN

对每个合并成稿：

1. 确认成稿路径与源 chapter 均不在登记表中。
2. 执行：

```bash
HEADLESS=0 bash ~/.agent/csdn-publish/publish.sh "<成稿绝对路径>"
```

3. 根据脚本输出判定：已发布 / 草稿（额度用尽）/ 需验证码 / 失败。
4. **禁止**未跑脚本就声称已发布。篇间间隔 20–60 秒。

## 步骤 4：追加登记表

每篇发布后追加一行；备注必须含源 chapter 列表。

## 步骤 5：git commit & push

在 `~/knowledge-json-v2` 暂存：`csdn-merged/` 新成稿、登记表、可选源文件追溯注释；提交并 `git push`（push 失败时用 `gh auth token` + `GIT_ASKPASS` 重试，不改 git config）。

## 最终汇报

- 4 个主题包：成稿路径、标题、合并了哪些源 chapter
- 每篇：合并要点 + 发布结果（URL / 草稿 / 失败原因）
- 登记表与 git 状态
