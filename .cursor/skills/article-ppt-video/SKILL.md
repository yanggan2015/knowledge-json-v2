---
name: article-ppt-video
description: "从 Markdown 教程文章生成框图风格 PPTX、竖屏/横屏幻灯片视频，以及 edge-tts 中文讲解配音。在用户要求把文章做成 PPT、视频课、带旁白的手机竖屏讲解时使用。"
---

# 文章 → 框图 PPT → 带讲解视频

**脚本与 Skill 同目录**，路径：

```
.cursor/skills/article-ppt-video/
  generate_ppt_from_article.py   # 主脚本
  requirements.txt
  run.sh
  README.md                      # 环境搭建（必读）
  SKILL.md                       # 本文件
```

其他 Agent 应先读 `README.md` 完成环境搭建，再运行脚本。

## 环境搭建（Agent 必须确认）

```bash
# 系统
sudo apt-get install -y ffmpeg fonts-wqy-microhei

# Python（在仓库根目录）
pip install -r .cursor/skills/article-ppt-video/requirements.txt

# 验证
ffmpeg -version && python3 -c "import pptx, PIL, edge_tts"
```

中文字体路径：`/usr/share/fonts/truetype/wqy/wqy-microhei.ttc`（脚本内 `FONT_PATH`）。

## 流水线概览

```
Markdown 文章
    → 解析章节（## 标题、核心知识、Mermaid）
    → Slide 数据结构（框图节点 + 连线）
    → Pillow 绘制每页 PNG（渐变背景 + 彩色圆角框 + 箭头，内容区铺满画面）
    → python-pptx 将 PNG 嵌入 PPTX
    → edge-tts 为每页生成讲解 MP3
    → ffmpeg 按配音时长合成无声视频 + 混流得到 MP4
```

## 执行步骤（Agent 必须实际运行）

1. 确认文章路径存在（通常为 `articles/<领域>/chapters/*.md`）。
2. 在**仓库根目录**生成竖屏带讲解视频（默认 1080×1920）：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py \
  "articles/React/chapters/001-React基础核心概念与原理.md" \
  -o ppt_output \
  --voice-preset duo
```

或使用同目录 `run.sh`：

```bash
.cursor/skills/article-ppt-video/run.sh "articles/..." --voice-preset duo
```

3. 输出目录结构：

```
ppt_output/<标题>/
  slides/slide_01.png ...
  audio/slide_01.mp3 ...
  <标题>_竖屏.pptx
  <标题>_竖屏_讲解.mp4
```

4. 将演示视频复制到 artifacts 供用户预览：

```bash
cp -r ppt_output/<标题> /opt/cursor/artifacts/ppt-demo/
```

5. 在回复中用 `<video src="/opt/cursor/artifacts/...mp4" controls></video>` 展示。

## 声音如何调节

使用 **edge-tts** 的 `rate` / `volume` / `pitch` 参数：

| 参数 | 含义 | 示例 |
|------|------|------|
| `--voice` | 单个发音人 | `zh-CN-XiaoxiaoNeural` |
| `--voices` | 多个发音人（逗号分隔） | `zh-CN-XiaoxiaoNeural,zh-CN-YunxiNeural` |
| `--voice-preset` | 预设组合 | `duo`（女+男）、`female`、`male`、`mix`、`dialect` |
| `--voice-mode` | 多发音人策略 | `rotate` / `single` / `by_kind` |
| `--rate` | 语速 | `+15%` |
| `--volume` | 音量 | `+20%` |
| `--pitch` | 音调 | `+5Hz` |

列出预设与中文语音：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py --list-voices
```

无配音仅幻灯片视频：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py "articles/..." --no-voice --seconds 5
```

横屏 16:9：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py "articles/..." --landscape
```

## 幻灯片版式（框图为主）

| kind | 视觉 |
|------|------|
| `title` | 封面大卡片铺满主区域 |
| `cards` | 网格卡片（核心知识） |
| `flow` | 流程框 + 箭头（竖屏纵向铺满） |
| `pipeline` | 纵向步骤管道 |
| `layers` | 分层架构条（等分高度） |
| `hub` | 中心主题 + 下方要点列表 |

布局由 `_content_area`、`_layout_boxes_vertical`、`_layout_grid` 等函数计算，**尽量占满标题下方至页脚之间的区域**，避免框图仅出现在顶部或左侧。

讲解文案由 `narration_for(slide)` 自动生成；可在 `Slide.narration` 字段写入自定义旁白。

## ffmpeg 合成原理

1. **无声视频**：concat demuxer，每张 PNG 按 `duration` 停留（= 配音时长 + 0.4s 缓冲）。
2. **音频**：concat 合并各页 MP3。
3. **混流**：`ffmpeg -i silent.mp4 -i narration.mp3 -c:v copy -c:a aac -shortest out.mp4`

## 常见问题

| 问题 | 处理 |
|------|------|
| 中文乱码/方块 | 安装 `fonts-wqy-microhei`，或改 `FONT_PATH` |
| edge-tts 写入失败 | 先输出到 `/workspace/ppt_output`，再 cp 到 artifacts |
| 视频过长 | 缩短 `narration_for` 文案，或 `--rate +20%` |
| 框图留白过多 | 调整 `_content_area` / `_layout_*` 或对应 `render_*` |
| 页数过多 | 在 `parse_article` 中限制 `body_slides[:10]` |

## 参考文件

- 主脚本：`.cursor/skills/article-ppt-video/generate_ppt_from_article.py`
- 环境搭建：`.cursor/skills/article-ppt-video/README.md`
- 用户说明：`docs/article-to-ppt-video.md`
