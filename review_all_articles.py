# -*- coding: utf-8 -*-
"""
全量文章质量审阅（非抽样）
遍历 articles/ 下每一篇 Markdown，检查结构、禁用的模板话术与最低信息量。
记录全部未通过项，不按数量截断。
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ARTICLES = Path("articles")

CHAPTER_SECTIONS = [
    "## 导读",
    "## 核心知识",
    "## 架构与流程",
    "## 技术详解",
]

OVERVIEW_SECTIONS = [
    "## 领域定位",
    "## 学习目标",
    "## 学习路径",
    "## 章节索引",
]

# 旧版模板化空话 — 出现即判为需优化
BANNED_PHRASES = [
    "职责单一、接口稳定、可观测",
    "落地时需明确验收标准与回滚方案",
    "在 React基础 语境下，这一点直接影响",
    "本章详细讲解",
    "将其固化为团队规范或 CI 检查项，而非个人习惯",
    "连接业务需求与底层运行时",
    "行业标准工具链 等主流工具与框架",
    "每个知识点作为独立章节，包含原理讲解",
]

MIN_CHAPTER_CHARS = 1500
MIN_OVERVIEW_CHARS = 2000


def review_file(path: Path) -> list[str]:
    issues = []
    text = path.read_text(encoding="utf-8")
    name = path.name
    is_overview = name == "README.md"

    if not text.startswith("# "):
        issues.append("缺少一级标题")

    required = OVERVIEW_SECTIONS if is_overview else CHAPTER_SECTIONS
    for sec in required:
        if sec not in text:
            issues.append(f"缺少 {sec}")

    if "```mermaid" not in text:
        issues.append("缺少 Mermaid 框图")

    min_chars = MIN_OVERVIEW_CHARS if is_overview else MIN_CHAPTER_CHARS
    if len(text) < min_chars:
        issues.append(f"字数不足 ({len(text)} 字，要求 ≥{min_chars})")

    for phrase in BANNED_PHRASES:
        if phrase in text:
            issues.append(f"含旧模板话术: {phrase[:40]}...")

    # 章节：核心知识区应有编号条目（勿在 ### 子标题处截断）
    if not is_overview and "## 核心知识" in text:
        after = text.split("## 核心知识", 1)[1]
        next_h2 = re.search(r"\n## [^#]", after)
        block = after[:next_h2.start()] if next_h2 else after
        if "**1." not in block and "**" not in block[:800]:
            issues.append("核心知识区缺少结构化条目")

    return issues


def review_all() -> dict:
    results = {
        "total_files": 0,
        "passed": 0,
        "failed": 0,
        "overview_total": 0,
        "overview_failed": 0,
        "chapter_total": 0,
        "chapter_failed": 0,
        "issue_summary": {},
        "failures": [],
    }
    issue_counter: Counter = Counter()

    for readme in sorted(ARTICLES.glob("*/README.md")):
        results["total_files"] += 1
        results["overview_total"] += 1
        issues = review_file(readme)
        if issues:
            results["failed"] += 1
            results["overview_failed"] += 1
            for i in issues:
                issue_counter[i.split("(")[0].split(":")[0].strip()] += 1
            results["failures"].append({"path": str(readme), "issues": issues})
        else:
            results["passed"] += 1

    for chapter in sorted(ARTICLES.glob("*/chapters/*.md")):
        results["total_files"] += 1
        results["chapter_total"] += 1
        issues = review_file(chapter)
        if issues:
            results["failed"] += 1
            results["chapter_failed"] += 1
            for i in issues:
                issue_counter[i.split("(")[0].split(":")[0].strip()] += 1
            results["failures"].append({"path": str(chapter), "issues": issues})
        else:
            results["passed"] += 1

    results["pass_rate"] = (
        f"{results['passed'] * 100 // max(results['total_files'], 1)}%"
    )
    results["issue_summary"] = dict(issue_counter.most_common())
    return results


def main():
    if not ARTICLES.exists():
        print("articles/ 不存在，请先运行 generate_articles.py")
        sys.exit(1)

    report = review_all()
    out = ARTICLES / "full_review_report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 仅路径列表，便于脚本处理
    paths_out = ARTICLES / "full_review_failures.txt"
    paths_out.write_text(
        "\n".join(f["path"] for f in report["failures"]),
        encoding="utf-8",
    )

    print("=" * 60)
    print("全量文章审阅（非抽样）")
    print("=" * 60)
    print(f"文件总数: {report['total_files']}")
    print(f"通过: {report['passed']}")
    print(f"未通过: {report['failed']}")
    print(f"通过率: {report['pass_rate']}")
    print(f"概述: {report['overview_total']} 篇, 未通过 {report['overview_failed']}")
    print(f"章节: {report['chapter_total']} 篇, 未通过 {report['chapter_failed']}")
    print(f"未通过记录数: {len(report['failures'])}（无截断）")
    print(f"报告: {out}")
    print(f"失败路径列表: {paths_out}")

    if report["issue_summary"]:
        print("\n问题类型汇总:")
        for kind, count in list(report["issue_summary"].items())[:15]:
            print(f"  {kind}: {count}")

    if report["failures"]:
        print("\n未通过文件（前 20）:")
        for f in report["failures"][:20]:
            print(f"  {f['path']}")
            for i in f["issues"]:
                print(f"    - {i}")

    if report["failed"] > 0:
        sys.exit(1)
    print("\n✓ 全部 10100 篇文章通过全量审阅")
    sys.exit(0)


if __name__ == "__main__":
    main()
