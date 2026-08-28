---
name: article-ppt-video
description: "从 Markdown 教程文章生成框图风格 PPTX、竖屏/横屏幻灯片视频，以及 edge-tts 中文讲解配音。在用户要求把文章做成 PPT、视频课、带旁白的手机竖屏讲解时使用。"
---

# 文章 → 框图 PPT → 带讲解视频

本仓库已实现完整流水线：`generate_ppt_from_article.py`。其他 Agent 按本 Skill 操作即可复现。

## 流水线概览

```
Markdown 文章
    → 解析章节（## 标题、核心知识、Mermaid）
    → Slide 数据结构（框图节点 + 连线）
    → Pillow 绘制每页 PNG（渐变背景 + 彩色圆角框 + 箭头）
    → python-pptx 将 PNG 嵌入 PPTX
    → edge-tts 为每页生成讲解 MP3
    → ffmpeg 按配音时长合成无声视频 + 混流得到 MP4
```

**关键依赖**（需预先安装）：

```bash
pip install python-pptx pillow edge-tts
# 系统需有 ffmpeg、ffprobe；中文渲染需字体，如 wqy-microhei
```

## 执行步骤（Agent 必须实际运行）

1. 确认文章路径存在（通常为 `articles/<领域>/chapters/*.md`）。
2. 生成竖屏带讲解视频（默认 1080×1920，适合手机）：

```bash
python3 generate_ppt_from_article.py "articles/React/chapters/001-*.md" -o ppt_output
```

3. 输出目录结构：

```
ppt_output/<标题>/
  slides/slide_01.png ...     # 每页幻灯片图
  audio/slide_01.mp3 ...      # 每页讲解音频
  <标题>_竖屏.pptx
  <标题>_竖屏_讲解.mp4
```

4. 将演示视频复制到 artifacts 供用户预览：

```bash
cp -r ppt_output/<标题> /opt/cursor/artifacts/ppt-demo/
```

5. 在回复中用 `<video src="/opt/cursor/artifacts/...mp4" controls></video>` 展示。

## 声音如何调节

使用 **edge-tts** 的 `rate` / `volume` / `pitch` 参数（相对字符串）：

| 参数 | 含义 | 示例 |
|------|------|------|
| `--voice` | 单个发音人 | `zh-CN-XiaoxiaoNeural` |
| `--voices` | 多个发音人（逗号分隔，按页轮换） | `zh-CN-XiaoxiaoNeural,zh-CN-YunxiNeural` |
| `--voice-preset` | 预设组合 | `duo`（女+男）、`female`、`male`、`mix`、`dialect` |
| `--voice-mode` | 多发音人策略 | `rotate` 按页轮换 / `single` 固定第一个 / `by_kind` 按版式 |
| `--rate` | 语速 | `+15%` 更快 |
| `--volume` | 音量 | `+20%` 更响 |
| `--pitch` | 音调 | `+5Hz` |

列出预设与中文语音：`python3 generate_ppt_from_article.py --list-voices`

示例：男女声轮换讲解：

```bash
python3 generate_ppt_from_article.py "articles/..." --voice-preset duo
# 或
python3 generate_ppt_from_article.py "articles/..." \
  --voices zh-CN-XiaoxiaoNeural,zh-CN-YunxiNeural --voice-mode rotate
```

无配音仅幻灯片视频：

```bash
python3 generate_ppt_from_article.py "articles/..." --no-voice --seconds 5
```

横屏 16:9：

```bash
python3 generate_ppt_from_article.py "articles/..." --landscape
```

## 幻灯片版式（框图为主）

解析器将内容映射为以下 `kind`：

| kind | 视觉 |
|------|------|
| `title` | 封面 + 元信息标签 |
| `cards` | 2×2 或竖排卡片（核心知识） |
| `flow` | 横向流程框 + 箭头（Mermaid LR） |
| `pipeline` | 纵向步骤管道 |
| `layers` | 分层架构条 |
| `hub` | 中心主题 + 辐射/竖列要点 |

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
| 视频过长 | 缩短 `narration_for` 文案，或提高 `--rate +20%` |
| 页数过多 | 在 `parse_article` 中限制 `body_slides[:10]` |

## 扩展方向

- 页间淡入淡出：ffmpeg `xfade` 滤镜
- 背景音乐：混流第二条音轨并降低音量
- 更精美配图：对封面调用 `GenerateImage` 作背景，再 Pillow 叠加文字

## 参考文件

- 主脚本：`generate_ppt_from_article.py`
- 用户说明：`docs/article-to-ppt-video.md`
