#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 articles/ 下的 Markdown 教程生成 PPTX 与视频幻灯片（MP4）。

用法:
  python3 generate_ppt_from_article.py articles/React/chapters/001-*.md
"""

from __future__ import annotations

import argparse
import re
import subprocess
import textwrap
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
SLIDE_W, SLIDE_H = 1920, 1080
BG = (15, 23, 42)       # slate-900
ACCENT = (56, 189, 248) # sky-400
TEXT = (248, 250, 252)
SUBTEXT = (148, 163, 184)


@dataclass
class Slide:
    title: str
    bullets: list[str]
    subtitle: str = ""


def _clean_md(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def parse_article(path: Path) -> tuple[str, str, list[Slide]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = ""
    meta = ""
    if lines and lines[0].startswith("# "):
        title = _clean_md(lines[0][2:].strip())

    for line in lines[1:8]:
        if line.startswith("> "):
            meta += line[2:].strip() + " "

    slides: list[Slide] = []
    slides.append(Slide(title=title or path.stem, bullets=[], subtitle=meta.strip()))

    current_section = ""
    section_body: list[str] = []

    def flush_section():
        nonlocal current_section, section_body
        if not current_section:
            return
        body = "\n".join(section_body).strip()
        if not body:
            current_section = ""
            section_body = []
            return

        if current_section == "核心知识":
            concepts = re.findall(
                r"\*\*(\d+)\.\s*([^*]+)\*\*\s*\n+([^\n#*]+(?:\n(?!\*\*\d)[^\n#*]+)*)",
                body,
            )
            if concepts:
                for num, ctitle, cbody in concepts[:5]:
                    bullets = textwrap.wrap(_clean_md(cbody.strip()), width=42)
                    slides.append(
                        Slide(
                            title=f"核心知识 {num}：{_clean_md(ctitle)}",
                            bullets=bullets[:5],
                        )
                    )
            else:
                bullets = textwrap.wrap(_clean_md(body), width=42)
                slides.append(Slide(title=current_section, bullets=bullets[:6]))
        elif "```mermaid" in body:
            nodes = re.findall(r"\[([^\]]+)\]", body)
            bullets = [_clean_md(n) for n in nodes[:8]]
            slides.append(Slide(title="架构与流程", bullets=bullets or ["见 Mermaid 流程图"]))
        else:
            numbered = re.findall(r"^\d+\.\s+(.+)$", body, re.MULTILINE)
            if numbered:
                bullets = [_clean_md(x) for x in numbered[:6]]
            else:
                plain = re.sub(r"```[\s\S]*?```", "", body)
                plain = re.sub(r"^###\s+.+$", "", plain, flags=re.MULTILINE)
                bullets = textwrap.wrap(_clean_md(plain), width=42)[:6]
            slides.append(Slide(title=current_section, bullets=bullets))

        current_section = ""
        section_body = []

    for line in lines:
        if line.startswith("## "):
            flush_section()
            current_section = _clean_md(line[3:].strip())
            section_body = []
        elif line.startswith("---"):
            continue
        elif current_section:
            section_body.append(line)

    flush_section()

    # 收尾页
    if len(slides) > 1:
        slides.append(
            Slide(
                title="本章小结",
                bullets=[
                    "理解核心概念与协作边界",
                    "结合官方文档动手验证",
                    "关注性能、安全与可观测性",
                    "将要点沉淀为团队检查清单",
                ],
            )
        )

    return title, meta.strip(), slides[:14]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def render_slide_image(slide: Slide, index: int, out: Path) -> None:
    img = Image.new("RGB", (SLIDE_W, SLIDE_H), BG)
    draw = ImageDraw.Draw(img)

    # 顶部装饰条
    draw.rectangle([0, 0, SLIDE_W, 8], fill=ACCENT)

    title_font = _load_font(52)
    bullet_font = _load_font(34)
    sub_font = _load_font(28)

    y = 80
    if slide.subtitle:
        draw.text((80, y), slide.subtitle[:120], font=sub_font, fill=SUBTEXT)
        y += 50

    draw.text((80, y), slide.title[:60], font=title_font, fill=TEXT)
    y += 90

    for i, bullet in enumerate(slide.bullets):
        line = f"• {bullet}"
        draw.text((100, y), line[:80], font=bullet_font, fill=TEXT)
        y += 56
        if y > SLIDE_H - 120:
            break

    # 页码
    draw.text((SLIDE_W - 140, SLIDE_H - 60), f"{index:02d}", font=sub_font, fill=SUBTEXT)
    img.save(out)


def build_pptx(slides: list[Slide], out: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for slide in slides:
        s = prs.slides.add_slide(blank)
        # 背景色近似
        fill = s.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(15, 23, 42)

        box = s.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(12), Inches(1.2))
        tf = box.text_frame
        tf.text = slide.title
        p = tf.paragraphs[0]
        p.font.size = Pt(36)
        p.font.bold = True
        p.font.color.rgb = RGBColor(248, 250, 252)

        if slide.subtitle:
            sub = s.shapes.add_textbox(Inches(0.6), Inches(1.3), Inches(12), Inches(0.6))
            stf = sub.text_frame
            stf.text = slide.subtitle[:200]
            stf.paragraphs[0].font.size = Pt(18)
            stf.paragraphs[0].font.color.rgb = RGBColor(148, 163, 184)

        body = s.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.5), Inches(4.8))
        btf = body.text_frame
        btf.word_wrap = True
        for i, bullet in enumerate(slide.bullets):
            para = btf.paragraphs[0] if i == 0 else btf.add_paragraph()
            para.text = bullet
            para.level = 0
            para.font.size = Pt(22)
            para.font.color.rgb = RGBColor(226, 232, 240)

    prs.save(out)


def build_video(image_dir: Path, out: Path, duration: float = 5.0) -> None:
    images = sorted(image_dir.glob("slide_*.png"))
    if not images:
        raise RuntimeError("无幻灯片图片")

    list_file = image_dir / "ffmpeg_list.txt"
    lines = []
    for img in images:
        lines.append(f"file '{img.resolve()}'")
        lines.append(f"duration {duration}")
    lines.append(f"file '{images[-1].resolve()}'")
    list_file.write_text("\n".join(lines), encoding="utf-8")

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def main():
    parser = argparse.ArgumentParser(description="从 Markdown 教程生成 PPT 与视频")
    parser.add_argument("article", type=Path, help="文章 Markdown 路径")
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("ppt_output"))
    parser.add_argument("--seconds", type=float, default=5.0, help="每页停留秒数")
    args = parser.parse_args()

    article = args.article.resolve()
    if not article.exists():
        raise SystemExit(f"文件不存在: {article}")

    title, _, slides = parse_article(article)
    safe = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", title)[:40].strip("_")
    out_dir = args.output_dir.resolve() / safe
    out_dir.mkdir(parents=True, exist_ok=True)
    img_dir = out_dir / "slides"
    img_dir.mkdir(exist_ok=True)

    for i, slide in enumerate(slides, 1):
        render_slide_image(slide, i, img_dir / f"slide_{i:02d}.png")

    pptx_path = out_dir / f"{safe}.pptx"
    video_path = out_dir / f"{safe}_video.mp4"
    build_pptx(slides, pptx_path)
    build_video(img_dir, video_path, duration=args.seconds)

    print(f"文章: {article}")
    print(f"标题: {title}")
    print(f"幻灯片: {len(slides)} 页")
    print(f"PPTX: {pptx_path}")
    print(f"视频: {video_path}")
    print(f"预览图: {img_dir}")


if __name__ == "__main__":
    main()
