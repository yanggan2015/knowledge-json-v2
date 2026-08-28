# 文章 → 框图 PPT → 带讲解视频

将 Markdown 教程解析为**框图风格幻灯片**（PPTX + PNG），并用 edge-tts 生成**中文讲解配音**，最终合成**竖屏 MP4**（默认 1080×1920，适合手机观看）。

本目录包含完整可运行脚本与 Cursor Skill，**脚本与 Skill 同目录**，便于 Agent 直接调用。

## 目录结构

```
.cursor/skills/article-ppt-video/
├── SKILL.md                      # Cursor Agent 操作说明
├── README.md                     # 本文件（环境搭建与用户指南）
├── requirements.txt              # Python 依赖
├── run.sh                        # 一键生成（从仓库根目录解析文章路径）
└── generate_ppt_from_article.py  # 主脚本
```

## 一、环境搭建

### 1. 系统依赖（Linux / Debian / Ubuntu）

```bash
# ffmpeg（视频合成，需 ffprobe）
sudo apt-get update
sudo apt-get install -y ffmpeg

# 中文字体（框图文字渲染，避免方块/乱码）
sudo apt-get install -y fonts-wqy-microhei
```

字体默认路径：`/usr/share/fonts/truetype/wqy/wqy-microhei.ttc`  
若路径不同，请修改 `generate_ppt_from_article.py` 中的 `FONT_PATH`。

### 2. Python 依赖

```bash
cd /path/to/knowledge-json-v2
pip install -r .cursor/skills/article-ppt-video/requirements.txt
```

或手动安装：

```bash
pip install python-pptx pillow edge-tts
```

### 3. 验证环境

```bash
ffmpeg -version
ffprobe -version
python3 -c "import pptx, PIL, edge_tts; print('OK')"
test -f /usr/share/fonts/truetype/wqy/wqy-microhei.ttc && echo "字体 OK"
```

列出可用中文发音人：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py --list-voices
```

## 二、快速使用

在**仓库根目录**执行（推荐）：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py \
  "articles/React/chapters/001-React基础核心概念与原理.md" \
  -o ppt_output \
  --voice-preset duo
```

或使用 `run.sh`：

```bash
chmod +x .cursor/skills/article-ppt-video/run.sh
.cursor/skills/article-ppt-video/run.sh \
  "articles/React/chapters/001-React基础核心概念与原理.md" \
  --voice-preset duo
```

### 输出目录

```
ppt_output/<文章标题>/
  slides/slide_01.png ...       # 每页框图
  audio/slide_01.mp3 ...        # 每页讲解
  audio/voices_used.txt         # 每页使用的发音人
  <标题>_竖屏.pptx
  <标题>_竖屏_讲解.mp4
```

## 三、常用参数

| 参数 | 说明 |
|------|------|
| `-o ppt_output` | 输出根目录 |
| `--landscape` | 横屏 1920×1080（默认竖屏） |
| `--no-voice` | 不生成配音，用 `--seconds` 控制每页时长 |
| `--voice` | 单个发音人，如 `zh-CN-XiaoxiaoNeural` |
| `--voices` | 多个发音人逗号分隔，按页轮换 |
| `--voice-preset` | `female` / `male` / `duo` / `mix` / `dialect` |
| `--voice-mode` | `rotate` / `single` / `by_kind` |
| `--rate` / `--volume` / `--pitch` | edge-tts 语速、音量、音调 |

示例：无配音仅幻灯片视频：

```bash
python3 .cursor/skills/article-ppt-video/generate_ppt_from_article.py \
  "articles/..." --no-voice --seconds 5
```

## 四、框图布局说明

脚本按内容类型自动选择版式（`cards` / `flow` / `pipeline` / `layers` / `hub`），并在**标题下方的内容区**内均匀分布节点框：

- 竖屏下流程与管道默认**纵向铺满**可用高度
- 卡片使用网格（竖屏多列时 1～2 列）填满区域
- 分层与 hub 版式按节点数量**等分垂直空间**，避免框图挤在顶部或左侧、其余留白

若需微调视觉效果，编辑 `generate_ppt_from_article.py` 中的 `render_*` 与 `_layout_*` 函数。

## 五、给 Cursor / Cloud Agent

阅读同目录 `SKILL.md`，按步骤安装依赖、运行脚本，并将成片复制到 artifacts 供用户预览。

更完整的用户向说明见：`docs/article-to-ppt-video.md`。
