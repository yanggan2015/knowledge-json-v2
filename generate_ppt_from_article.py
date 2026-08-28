#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Markdown 教程生成以框图为主的精美 PPTX 与视频幻灯片。

用法:
  python3 generate_ppt_from_article.py articles/React/chapters/001-*.md -o ppt_output
"""

from __future__ import annotations

import argparse
import math
import re
import subprocess
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
W, H = 1920, 1080

# 深色科技风配色
C_BG_TOP = (12, 18, 35)
C_BG_BOT = (28, 38, 58)
C_TITLE = (248, 250, 252)
C_SUB = (148, 163, 184)
C_LINE = (71, 85, 105)
PALETTE = [
    (56, 189, 248),   # sky
    (52, 211, 153),   # emerald
    (167, 139, 250),  # violet
    (251, 191, 36),   # amber
    (244, 114, 182),  # pink
    (94, 234, 212),   # teal
]


@dataclass
class Node:
    label: str
    detail: str = ""
    color_idx: int = 0


@dataclass
class Slide:
    title: str
    kind: str  # title | flow | layers | cards | pipeline | hub | summary
    nodes: List[Node] = field(default_factory=list)
    edges: List[Tuple[int, int]] = field(default_factory=list)
    subtitle: str = ""
    caption: str = ""


def _clean(text: str) -> str:
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    return text.strip()


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


def _gradient_bg() -> Image.Image:
    img = Image.new("RGB", (W, H))
    for y in range(H):
        t = y / H
        r = int(C_BG_TOP[0] + (C_BG_BOT[0] - C_BG_TOP[0]) * t)
        g = int(C_BG_TOP[1] + (C_BG_BOT[1] - C_BG_TOP[1]) * t)
        b = int(C_BG_TOP[2] + (C_BG_BOT[2] - C_BG_TOP[2]) * t)
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=(r, g, b))
    return img


def _draw_glow_orbs(draw: ImageDraw.ImageDraw) -> None:
    for cx, cy, rad, col in [(220, 200, 180, (30, 58, 90)), (1680, 320, 240, (40, 50, 80)), (1500, 820, 160, (35, 55, 75))]:
        draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=col, width=2)


def _rounded_box(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int, int, int],
    fill: Tuple[int, int, int],
    outline: Tuple[int, int, int],
    radius: int = 20,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def _text_centered(
    draw: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    title: str,
    detail: str = "",
    title_font: ImageFont.FreeTypeFont | None = None,
    detail_font: ImageFont.FreeTypeFont | None = None,
    color: Tuple[int, int, int] = C_TITLE,
) -> None:
    title_font = title_font or _font(28)
    detail_font = detail_font or _font(22)
    x1, y1, x2, y2 = box
    tw = x2 - x1
    lines = textwrap.wrap(title, width=max(8, tw // 28))
    detail_lines = textwrap.wrap(detail, width=max(10, tw // 24))[:3] if detail else []
    total_h = len(lines) * 34 + len(detail_lines) * 28 + (10 if detail_lines else 0)
    y = y1 + (y2 - y1 - total_h) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        tw_line = bbox[2] - bbox[0]
        draw.text((x1 + (tw - tw_line) // 2, y), line, font=title_font, fill=color)
        y += 34
    if detail_lines:
        y += 6
        for line in detail_lines:
            bbox = draw.textbbox((0, 0), line, font=detail_font)
            tw_line = bbox[2] - bbox[0]
            draw.text((x1 + (tw - tw_line) // 2, y), line, font=detail_font, fill=C_SUB)
            y += 28


def _arrow(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, color: Tuple[int, int, int]) -> None:
    draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    ang = math.atan2(y2 - y1, x2 - x1)
    sz = 12
    p1 = (x2 - sz * math.cos(ang - 0.4), y2 - sz * math.sin(ang - 0.4))
    p2 = (x2 - sz * math.cos(ang + 0.4), y2 - sz * math.sin(ang + 0.4))
    draw.polygon([(x2, y2), p1, p2], fill=color)


def _header(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "", page: int = 0) -> int:
    draw.rectangle([0, 0, W, 6], fill=PALETTE[0])
    draw.text((72, 42), title[:48], font=_font(44), fill=C_TITLE)
    if subtitle:
        draw.text((72, 98), subtitle[:100], font=_font(24), fill=C_SUB)
    if page:
        draw.text((W - 100, H - 50), f"{page:02d}", font=_font(24), fill=C_SUB)
    return 150 if subtitle else 130


def parse_mermaid(body: str) -> Tuple[List[Node], List[Tuple[int, int]], str]:
    """解析 flowchart / graph 为节点与边"""
    nodes_map: dict[str, int] = {}
    nodes: List[Node] = []
    edges: List[Tuple[int, int]] = []
    direction = "LR"
    if re.search(r"flowchart\s+TD|graph\s+TB|flowchart\s+TB", body):
        direction = "TB"

    for m in re.finditer(r"(\w+)\s*\[([^\]]+)\]", body):
        nid, label = m.group(1), _clean(m.group(2))
        if nid not in nodes_map:
            nodes_map[nid] = len(nodes)
            nodes.append(Node(label=label, color_idx=len(nodes) % len(PALETTE)))

    for m in re.finditer(r"(\w+)\s*-->\s*(\w+)", body):
        a, b = m.group(1), m.group(2)
        if a in nodes_map and b in nodes_map:
            edges.append((nodes_map[a], nodes_map[b]))

    # subgraph 标签作层名
    layers = re.findall(r"subgraph\s+([^\n{]+)", body)
    layer_hint = layers[0].strip() if layers else ""
    return nodes, edges, direction


SKIP_SECTIONS = frozenset({"延伸学习", "巩固建议", "常见误区与纠正", "最佳实践", "延伸阅读"})


def parse_article(path: Path) -> tuple[str, str, List[Slide]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = _clean(lines[0][2:]) if lines and lines[0].startswith("# ") else path.stem
    meta = " ".join(_clean(l[2:]) for l in lines[1:8] if l.startswith("> "))

    slides: List[Slide] = [
        Slide(title=title, kind="title", subtitle=meta, caption="教程章节 · 框图导读")
    ]

    current = ""
    body_lines: List[str] = []

    def flush():
        nonlocal current, body_lines
        if not current:
            return
        if current in SKIP_SECTIONS:
            current, body_lines = "", []
            return
        body = "\n".join(body_lines).strip()
        if not body:
            current, body_lines = "", []
            return
        body = re.sub(r"^###\s+.+$", "", body, flags=re.MULTILINE)

        if current == "核心知识":
            concepts = re.findall(
                r"\*\*(\d+)\.\s*([^*]+)\*\*\s*\n+([^\n#*]+(?:\n(?!\*\*\d)[^\n#*]+)*)",
                body,
            )
            if concepts:
                nodes = [
                    Node(label=_clean(ct), detail=_clean(cb)[:80], color_idx=i)
                    for i, (_, ct, cb) in enumerate(concepts[:4])
                ]
                slides.append(Slide(title="核心知识图谱", kind="cards", nodes=nodes, caption=current))
                # 关系页：概念之间的逻辑链
                if len(nodes) >= 3:
                    slides.append(
                        Slide(
                            title="核心概念关系",
                            kind="flow",
                            nodes=nodes[:5],
                            edges=[(i, i + 1) for i in range(min(4, len(nodes) - 1))],
                            caption="概念递进关系",
                        )
                    )
            else:
                plain = _clean(re.sub(r"```[\s\S]*?```", "", body))
                slides.append(
                    Slide(
                        title=current,
                        kind="cards",
                        nodes=[Node(label=plain[:40], detail=plain[40:120], color_idx=0)],
                    )
                )
        elif "```mermaid" in body:
            mermaid = re.search(r"```mermaid\s*([\s\S]*?)```", body)
            m_body = mermaid.group(1) if mermaid else body
            nodes, edges, direction = parse_mermaid(m_body)
            if "subgraph" in m_body:
                slides.append(
                    Slide(title="架构分层", kind="layers", nodes=nodes, edges=edges, caption=current)
                )
            else:
                kind = "flow" if direction == "LR" else "pipeline"
                slides.append(
                    Slide(title="流程框图", kind=kind, nodes=nodes, edges=edges, caption=current)
                )
        else:
            numbered = [_clean(x) for x in re.findall(r"^\d+\.\s+(.+)$", body, re.MULTILINE)]
            if numbered:
                nodes = [Node(label=f"步骤 {i+1}", detail=t[:70], color_idx=i) for i, t in enumerate(numbered[:5])]
                slides.append(
                    Slide(
                        title=current,
                        kind="pipeline",
                        nodes=nodes,
                        edges=[(i, i + 1) for i in range(len(nodes) - 1)],
                    )
                )
            else:
                plain = _clean(re.sub(r"```[\s\S]*?```", "", body))
                chunks = textwrap.wrap(plain, width=36)[:4]
                nodes = [Node(label=c[:36], color_idx=i) for i, c in enumerate(chunks)]
                slides.append(Slide(title=current, kind="cards", nodes=nodes))

        current, body_lines = "", []

    for line in lines:
        if line.startswith("## "):
            flush()
            current = _clean(line[3:])
            body_lines = []
        elif line.startswith("---"):
            continue
        elif current:
            body_lines.append(line)
    flush()

    hub = Slide(
        title="本章要点回顾",
        kind="hub",
        nodes=[
            Node("概念模型", color_idx=0),
            Node("流程机制", color_idx=1),
            Node("工程实践", color_idx=2),
            Node("性能安全", color_idx=3),
            Node("持续学习", color_idx=4),
        ],
        caption="围绕本章主题的系统化掌握路径",
    )
    core = slides[0]
    body_slides = slides[1:]
    if len(body_slides) > 10:
        body_slides = body_slides[:10]
    slides = [core] + body_slides + [hub]
    return title, meta, slides


def _node_box_size(n: int, horizontal: bool) -> Tuple[int, int, int, int]:
    margin = 72
    top = 160
    if horizontal:
        gap = 48
        box_w = min(280, (W - 2 * margin - gap * (n - 1)) // max(n, 1))
        box_h = 140
        total_w = n * box_w + (n - 1) * gap
        start_x = (W - total_w) // 2
        return box_w, box_h, start_x, gap
    gap = 36
    box_w = 520
    box_h = 100
    start_x = (W - box_w) // 2
    return box_w, box_h, start_x, gap


def _draw_node(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int], node: Node) -> None:
    color = PALETTE[node.color_idx % len(PALETTE)]
    inner = (tuple(max(0, c - 80) for c in color))
    _rounded_box(draw, box, fill=(inner[0] // 4 + 20, inner[1] // 4 + 28, inner[2] // 4 + 45), outline=color, radius=18, width=3)
    _text_centered(draw, box, node.label, node.detail, _font(26), _font(20), C_TITLE)


def render_title(slide: Slide, img: Image.Image, page: int) -> None:
    draw = ImageDraw.Draw(img)
    _draw_glow_orbs(draw)
    draw.rectangle([0, 0, W, 6], fill=PALETTE[0])
    # 装饰框
    _rounded_box(draw, (120, 200, W - 120, H - 200), fill=(22, 32, 50), outline=PALETTE[0], radius=32, width=2)
    draw.text((200, 280), slide.title, font=_font(64), fill=C_TITLE)
    if slide.subtitle:
        draw.text((200, 400), slide.subtitle[:90], font=_font(26), fill=C_SUB)
    if slide.caption:
        _rounded_box(draw, (200, 500, 520, 560), fill=(56, 189, 248), outline=PALETTE[0], radius=12)
        draw.text((220, 515), slide.caption, font=_font(24), fill=C_TITLE)
    # 底部标签
    tags = re.findall(r"[^｜|]+", slide.subtitle or "")
    x = 200
    for i, tag in enumerate(tags[:4]):
        tag = tag.strip()
        if not tag:
            continue
        bw = min(280, len(tag) * 18 + 40)
        _rounded_box(draw, (x, 620, x + bw, 680), fill=(30, 45, 68), outline=PALETTE[(i + 1) % len(PALETTE)], radius=10)
        draw.text((x + 16, 638), tag[:20], font=_font(22), fill=C_TITLE)
        x += bw + 20
    draw.text((W - 100, H - 50), f"{page:02d}", font=_font(24), fill=C_SUB)


def render_flow(slide: Slide, img: Image.Image, page: int, vertical: bool = False) -> None:
    draw = ImageDraw.Draw(img)
    top = _header(draw, slide.title, slide.caption, page)
    nodes = slide.nodes[:6]
    n = len(nodes)
    if not n:
        return
    box_w, box_h, start_x, gap = _node_box_size(n, not vertical)
    positions: List[Tuple[int, int, int, int]] = []
    if vertical:
        y = top + 40
        for i in range(n):
            positions.append((start_x, y, start_x + box_w, y + box_h))
            y += box_h + gap
    else:
        x = start_x
        y = top + 80
        for i in range(n):
            positions.append((x, y, x + box_w, y + box_h))
            x += box_w + gap

    for i, node in enumerate(nodes):
        _draw_node(draw, positions[i], node)

    edge_list = slide.edges or [(i, i + 1) for i in range(n - 1)]
    for a, b in edge_list:
        if a >= len(positions) or b >= len(positions):
            continue
        ax = (positions[a][0] + positions[a][2]) // 2
        ay = (positions[a][1] + positions[a][3]) // 2
        bx = (positions[b][0] + positions[b][2]) // 2
        by = (positions[b][1] + positions[b][3]) // 2
        if vertical:
            _arrow(draw, ax, positions[a][3], bx, positions[b][1], PALETTE[0])
        else:
            _arrow(draw, positions[a][2], ay, positions[b][0], by, PALETTE[0])


def render_cards(slide: Slide, img: Image.Image, page: int) -> None:
    draw = ImageDraw.Draw(img)
    top = _header(draw, slide.title, slide.caption, page)
    nodes = slide.nodes[:4]
    cols = 2 if len(nodes) > 1 else 1
    rows = math.ceil(len(nodes) / cols)
    pad = 48
    cw = (W - 2 * 72 - pad) // cols
    ch = min(220, (H - top - 100 - pad * (rows - 1)) // max(rows, 1))
    for i, node in enumerate(nodes):
        row, col = divmod(i, cols)
        x1 = 72 + col * (cw + pad)
        y1 = top + 30 + row * (ch + pad)
        _draw_node(draw, (x1, y1, x1 + cw, y1 + ch), node)


def render_layers(slide: Slide, img: Image.Image, page: int) -> None:
    draw = ImageDraw.Draw(img)
    top = _header(draw, slide.title, slide.caption, page)
    nodes = slide.nodes[:8]
    layer_h = min(110, (H - top - 80) // max(len(nodes), 1))
    for i, node in enumerate(nodes):
        y1 = top + 20 + i * (layer_h + 16)
        margin = 80 + i * 30
        _rounded_box(draw, (margin, y1, W - margin, y1 + layer_h), fill=(25, 35, 55), outline=PALETTE[i % len(PALETTE)], radius=14, width=2)
        draw.text((margin + 24, y1 + 16), node.label[:50], font=_font(28), fill=C_TITLE)
        if node.detail:
            draw.text((margin + 24, y1 + 56), node.detail[:60], font=_font(20), fill=C_SUB)
    # 层间箭头
    for i in range(len(nodes) - 1):
        y1 = top + 20 + i * (layer_h + 16) + layer_h
        y2 = y1 + 16
        _arrow(draw, W // 2, y1, W // 2, y2 + 20, PALETTE[0])


def render_hub(slide: Slide, img: Image.Image, page: int) -> None:
    draw = ImageDraw.Draw(img)
    top = _header(draw, slide.title, slide.caption, page)
    cx, cy = W // 2, top + 280
    _rounded_box(draw, (cx - 120, cy - 60, cx + 120, cy + 60), fill=(56, 189, 248), outline=PALETTE[0], radius=24, width=3)
    draw.text((cx - 80, cy - 18), slide.title[:12], font=_font(30), fill=C_TITLE)
    satellites = slide.nodes[:5]
    radius = 280
    for i, node in enumerate(satellites):
        ang = -math.pi / 2 + 2 * math.pi * i / len(satellites)
        sx = int(cx + radius * math.cos(ang))
        sy = int(cy + radius * math.sin(ang))
        bw, bh = 200, 90
        box = (sx - bw // 2, sy - bh // 2, sx + bw // 2, sy + bh // 2)
        _draw_node(draw, box, node)
        _arrow(draw, cx + 100 * math.cos(ang), cy + 50 * math.sin(ang), sx - (bw // 2 - 10) * math.cos(ang), sy - (bh // 2 - 10) * math.sin(ang), PALETTE[i % len(PALETTE)])


def render_slide(slide: Slide, page: int, out: Path) -> None:
    img = _gradient_bg()
    kind = slide.kind
    if kind == "title":
        render_title(slide, img, page)
    elif kind in ("flow", "pipeline"):
        render_flow(slide, img, page, vertical=kind == "pipeline")
    elif kind == "cards":
        render_cards(slide, img, page)
    elif kind == "layers":
        render_layers(slide, img, page)
    elif kind == "hub":
        render_hub(slide, img, page)
    else:
        render_cards(slide, img, page)
    img.save(out)


def build_pptx(image_paths: List[Path], out: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    for p in image_paths:
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(str(p.resolve()), 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(out)


def build_video(image_dir: Path, out: Path, duration: float) -> None:
    images = sorted(image_dir.glob("slide_*.png"))
    list_file = image_dir / "ffmpeg_list.txt"
    lines = []
    for img in images:
        lines.append(f"file '{img.resolve()}'")
        lines.append(f"duration {duration}")
    lines.append(f"file '{images[-1].resolve()}'")
    list_file.write_text("\n".join(lines), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(out),
        ],
        check=True,
        capture_output=True,
    )


def main():
    parser = argparse.ArgumentParser(description="从 Markdown 生成框图风格 PPT/视频")
    parser.add_argument("article", type=Path)
    parser.add_argument("-o", "--output-dir", type=Path, default=Path("ppt_output"))
    parser.add_argument("--seconds", type=float, default=4.5)
    args = parser.parse_args()

    article = args.article.resolve()
    title, _, slides = parse_article(article)
    safe = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", title)[:40].strip("_")
    out_dir = args.output_dir.resolve() / safe
    img_dir = out_dir / "slides"
    img_dir.mkdir(parents=True, exist_ok=True)

    paths: List[Path] = []
    for i, slide in enumerate(slides, 1):
        p = img_dir / f"slide_{i:02d}.png"
        render_slide(slide, i, p)
        paths.append(p)

    pptx_path = out_dir / f"{safe}.pptx"
    video_path = out_dir / f"{safe}_video.mp4"
    build_pptx(paths, pptx_path)
    build_video(img_dir, video_path, args.seconds)

    print(f"标题: {title}")
    print(f"幻灯片: {len(slides)} 页（框图为主）")
    print(f"PPTX: {pptx_path}")
    print(f"视频: {video_path}")


if __name__ == "__main__":
    main()
