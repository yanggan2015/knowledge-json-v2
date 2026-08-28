# -*- coding: utf-8 -*-
"""文章深度完整性检测：交叉校验 JSON、文件、索引与链接"""

import json
import re
from pathlib import Path
from collections import Counter

from check_articles import check_domain, chapter_filename, ARTICLES_DIR, DOMAINS_DIR

def deep_check():
    errors = []
    warnings = []
    total_chapters_json = 0
    total_chapter_files = 0
    empty_files = []
    duplicate_ids = []

    json_files = sorted(DOMAINS_DIR.glob("*.json"))

    for jp in json_files:
        with open(jp, encoding="utf-8") as f:
            data = json.load(f)
        domain = data["domain"]
        chapters = data.get("chapters", [])
        total_chapters_json += len(chapters)

        domain_dir = ARTICLES_DIR / domain
        chapters_dir = domain_dir / "chapters"

        # ID 唯一性
        ids = [c.get("id") for c in chapters]
        dup = [k for k, v in Counter(ids).items() if v > 1]
        if dup:
            errors.append(f"{domain}: 重复章节 ID {dup}")

        expected_names = set()
        for c in chapters:
            fn = chapter_filename(c)
            expected_names.add(fn)
            fp = chapters_dir / fn
            if not fp.exists():
                errors.append(f"{domain}: 缺失章节文件 {fn}")
            elif fp.stat().st_size < 100:
                empty_files.append(str(fp))

        actual = set(p.name for p in chapters_dir.glob("*.md"))
        total_chapter_files += len(actual)

        extra = actual - expected_names
        if extra:
            warnings.append(f"{domain}: 多余文件 {len(extra)} 个")

        missing = expected_names - actual
        if missing:
            errors.append(f"{domain}: 未匹配文件 {len(missing)} 个")

        # README 链接校验
        readme = (domain_dir / "README.md").read_text(encoding="utf-8")
        link_pattern = re.compile(r'\]\((chapters/[^)]+)\)')
        for link in link_pattern.findall(readme):
            if not (domain_dir / link).exists():
                errors.append(f"{domain}: 损坏链接 {link}")

    # index.json 校验
    index_path = ARTICLES_DIR / "index.json"
    if index_path.exists():
        index = json.loads(index_path.read_text(encoding="utf-8"))
        if index.get("total_domains") != 100:
            errors.append(f"index total_domains != 100")
        if index.get("total_chapters") != total_chapters_json:
            errors.append(
                f"index chapters {index.get('total_chapters')} != json {total_chapters_json}"
            )
        for d in index.get("domains", []):
            name = d["name"]
            if not (ARTICLES_DIR / name / "README.md").exists():
                errors.append(f"index 指向缺失领域 {name}")
    else:
        errors.append("index.json 缺失")

    # 概述文章数量
    readme_count = len(list(ARTICLES_DIR.glob("*/README.md")))

    report = {
        "json_chapters": total_chapters_json,
        "chapter_files": total_chapter_files,
        "readme_count": readme_count,
        "total_articles": readme_count + total_chapter_files,
        "empty_files": empty_files,
        "errors": errors,
        "warnings": warnings,
        "passed": len(errors) == 0,
    }
    return report


if __name__ == "__main__":
    r = deep_check()
    print("=" * 60)
    print("深度完整性检测")
    print("=" * 60)
    print(f"JSON 章节总数: {r['json_chapters']}")
    print(f"章节文件数: {r['chapter_files']}")
    print(f"概述文章数: {r['readme_count']}")
    print(f"文章总计: {r['total_articles']}")
    print(f"空文件: {len(r['empty_files'])}")
    print(f"错误: {len(r['errors'])}")
    print(f"警告: {len(r['warnings'])}")

    if r["errors"]:
        print("\n错误列表:")
        for e in r["errors"][:30]:
            print(f"  - {e}")
    if r["warnings"]:
        print("\n警告列表 (前10):")
        for w in r["warnings"][:10]:
            print(f"  - {w}")

    out = ARTICLES_DIR / "deep_quality_report.json"
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告: {out}")

    if r["passed"]:
        print("\n✓ 深度检测全部通过")
    else:
        print("\n✗ 存在错误需修复")
        raise SystemExit(1)
