# 从 Markdown 文章生成框图 PPT 与讲解视频

一篇短文，说明本仓库如何把教程文章变成 **PPTX**、**竖屏幻灯片视频**，以及 **带中文旁白** 的成片。

---

## 一、整体思路

传统 PPT 是「一页页文字」。这里的做法是：

1. **读 Markdown**：按 `## 章节` 切块，抽出核心知识条目、Mermaid 流程图、编号步骤。
2. **变成框图**：每块内容对应一种版式（卡片网格、横向流程、纵向管道、分层条、中心辐射）。
3. **画成图片**：用 Python Pillow 在固定分辨率画布上绘制（默认 **1080×1920 竖屏**）。
4. **打包 PPT**：用 `python-pptx` 把每张 PNG 全页贴进幻灯片。
5. **生成旁白**：用微软 Edge 在线 TTS（`edge-tts`）把每页要讲的话合成 MP3。
6. **合成视频**：`ffmpeg` 让每张图停留「旁白时长」，再与音频混流成 MP4。

所以：**PPT 和视频共用同一套幻灯片图片**；视频比 PPT 多了「按页配音 + 时间轴」。

---

## 二、怎么用

```bash
pip install -r .cursor/skills/article-ppt-video/requirements.txt
# 系统需安装 ffmpeg、fonts-wqy-microhei（见下方环境搭建）

python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py \
  "articles/React/chapters/001-React基础核心概念与原理.md" \
  -o ppt_output
```

或使用同目录一键脚本：

```bash
.cursor/skills/article-ppt-video/run.sh \
  "articles/React/chapters/001-React基础核心概念与原理.md" \
  --voice-preset duo
```

默认产出：

- `*_竖屏.pptx` — 可用 PowerPoint / WPS 打开
- `*_竖屏_讲解.mp4` — 带讲解的竖屏视频
- `slides/` — 每页 PNG
- `audio/` — 每页 MP3

---

## 三、发音人多种选择

支持 **单个**、**多个轮换**、**预设组合** 三种方式：

```bash
# 查看预设与全部中文语音
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py --list-voices

# 预设：女声 duo=女+男轮换 mix=四人轮换 dialect=方言
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py "articles/..." --voice-preset duo

# 自定义多个发音人（按页轮换）
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py "articles/..." \
  --voices zh-CN-XiaoxiaoNeural,zh-CN-YunxiNeural,zh-CN-XiaoyiNeural

# 按版式分配：封面用第一个，流程类用第二个，其余轮换
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py "articles/..." --voice-preset duo --voice-mode by_kind
```

| 预设 | 包含发音人 |
|------|------------|
| `female` | 晓晓、晓伊（女声） |
| `male` | 云希、云健、云扬（男声） |
| `duo` | 晓晓 + 云希（推荐对谈感） |
| `mix` | 4 种音色轮换 |
| `dialect` | 东北、陕西方言女声 |

每页实际使用的发音人会写入 `audio/voices_used.txt`。

语速/音量/音调仍可调：

| 参数 | 作用 | 示例 |
|------|------|------|
| `--voice` | 单个发音人 | `zh-CN-YunxiNeural` |
| `--rate` | 语速 | `+12%` |
| `--volume` | 音量 | `+18%` |
| `--pitch` | 音调 | `+5Hz` |

每页讲什么由脚本里的 `narration_for()` 根据框图标题和节点自动生成；若要完全自定义，可在代码里给 `Slide.narration` 写字段。

---

## 四、为什么视频会有声音？

流程是：

```
每页 Slide → 生成讲解文本 → edge-tts → slide_01.mp3 ...
所有 MP3 拼接 → narration.mp3
所有 PNG 按音频时长轮播 → silent.mp4
ffmpeg 混流 → 最终 MP4（画面 + 旁白）
```

每页停留时间 = **该页 MP3 时长 + 0.4 秒**，避免话没讲完就切页。

---

## 五、竖屏与横屏

| 模式 | 分辨率 | 参数 |
|------|--------|------|
| 竖屏（默认，适合手机） | 1080×1920 | 不加参数 |
| 横屏（适合投影） | 1920×1080 | `--landscape` |

竖屏下流程图、卡片会自动改为 **纵向排列**，方便单手滑动观看。

---

## 六、环境搭建

完整步骤见 Skill 目录下的 README：

```
.cursor/skills/article-ppt-video/README.md
```

简要命令：

```bash
sudo apt-get install -y ffmpeg fonts-wqy-microhei
pip install -r .cursor/skills/article-ppt-video/requirements.txt
```

## 七、给其他 AI Agent

仓库内已添加 Skill（**脚本与 Skill 同目录**）：

```
.cursor/skills/article-ppt-video/
  SKILL.md
  generate_ppt_from_article.py
  README.md
  requirements.txt
  run.sh
```

其他 Cursor / Cloud Agent 读到 `SKILL.md` 后，应按其中步骤安装依赖、运行脚本，并把成片放到 artifacts 用 `<video>` 展示给用户。

框图布局会尽量**铺满标题下方内容区**（竖屏纵向等分、网格卡片），避免仅顶部或左侧一小块、其余留白。

---

## 八、局限与后续

- 当前为 **程序化框图**，不是设计师级模板；美观度来自统一配色与圆角卡片。
- 旁白偏「念要点」，时长随内容自动变长；可用 `--rate` 加速或改短 `narration_for` 文案。
- 尚未支持：页间转场动画、背景音乐、真人音色克隆。

如需增强，可在 `.cursor/skills/article-ppt-video/generate_ppt_from_article.py` 的 `render_*` 函数中改视觉，或在 ffmpeg 步骤加滤镜与第二条音轨。
