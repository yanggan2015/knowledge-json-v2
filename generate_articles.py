# -*- coding: utf-8 -*-
"""
领域知识库文章生成器
从 domains/*.json 生成 Markdown 教程文章
每个领域一个文件夹：articles/<领域名>/
  - README.md          领域概述
  - chapters/          各章节文章
"""
import json
import os
import re
import sys
import time
from pathlib import Path

from article_generator import generate_chapter_article, generate_overview_article
from article_generator.patterns import safe_filename
from article_generator.sanitize import sanitize_text

DOMAINS_DIR = Path("domains")
OUTPUT_DIR = Path("articles")


def chapter_filename(chapter: dict) -> str:
    cid = chapter.get("id", "000")
    title = sanitize_text(chapter.get("title", "chapter"))
    safe = safe_filename(title, max_len=50)
    return f"{cid}-{safe}.md"


def generate_domain(domain_path: Path, verbose: bool = True) -> dict:
    """生成单个领域的全部文章"""
    with open(domain_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    domain = data["domain"]
    out_dir = OUTPUT_DIR / domain
    chapters_dir = out_dir / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    # 概述文章
    overview = generate_overview_article(data)
    overview_path = out_dir / "README.md"
    overview_path.write_text(overview, encoding="utf-8")

    # 章节文章
    count = 0
    for chapter in data.get("chapters", []):
        article = generate_chapter_article(chapter, data)
        fname = chapter_filename(chapter)
        (chapters_dir / fname).write_text(article, encoding="utf-8")
        count += 1

    if verbose:
        print(f"  ✓ {domain}: 概述 + {count} 章节")

    return {"domain": domain, "chapters": count, "path": str(out_dir)}


def generate_all(domains_dir: Path = DOMAINS_DIR, output_dir: Path = OUTPUT_DIR) -> list:
    """生成全部领域文章"""
    global OUTPUT_DIR
    OUTPUT_DIR = output_dir
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    json_files = sorted(domains_dir.glob("*.json"))
    results = []
    start = time.time()

    print(f"开始生成 {len(json_files)} 个领域的教程文章...")
    print("=" * 60)

    for i, path in enumerate(json_files, 1):
        try:
            result = generate_domain(path)
            results.append(result)
        except Exception as e:
            print(f"  ✗ {path.name}: {e}")
            results.append({"domain": path.stem, "error": str(e)})

        if i % 10 == 0:
            print(f"  ... 已完成 {i}/{len(json_files)}")

    elapsed = time.time() - start
    total_chapters = sum(r.get("chapters", 0) for r in results)
    errors = sum(1 for r in results if "error" in r)

    print("=" * 60)
    print(f"生成完成！")
    print(f"  领域数: {len(results)}")
    print(f"  章节文章: {total_chapters}")
    print(f"  概述文章: {len(results) - errors}")
    print(f"  失败: {errors}")
    print(f"  耗时: {elapsed:.1f}s")
    print(f"  输出目录: {output_dir.absolute()}")

    # 生成总索引
    index = {
        "total_domains": len(results),
        "total_chapters": total_chapters,
        "domains": [
            {
                "name": r["domain"],
                "chapters": r.get("chapters", 0),
                "path": r.get("path", ""),
                "overview": f"articles/{r['domain']}/README.md",
            }
            for r in results if "error" not in r
        ],
    }
    index_path = output_dir / "index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  索引文件: {index_path}")

    return results


def generate_single(domain_name: str) -> dict:
    """生成单个领域"""
    path = DOMAINS_DIR / f"{domain_name}.json"
    if not path.exists():
        raise FileNotFoundError(f"领域文件不存在: {path}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return generate_domain(path)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        name = sys.argv[1]
        generate_single(name)
    else:
        generate_all()
