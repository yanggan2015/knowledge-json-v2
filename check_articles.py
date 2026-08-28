# -*- coding: utf-8 -*-
"""
文章完整性检测
校验每篇概述与章节是否结构完整、章节数量与 JSON 一致。
"""
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

DOMAINS_DIR = Path("domains")
ARTICLES_DIR = Path("articles")

# 章节文章必备结构
CHAPTER_REQUIRED_SECTIONS = [
    "## 导读",
    "## 核心概念",
    "## 架构与流程",
    "## 深度讲解",
    "### 本章小结",
]

CHAPTER_OPTIONAL_BUT_EXPECTED = [
    "### 常见误区",
    "### 最佳实践",
]

# 概述文章必备结构
OVERVIEW_REQUIRED_SECTIONS = [
    "## 领域概述",
    "## 前置知识",
    "## 章节索引",
]

MIN_CHAPTER_CHARS = 800
MIN_OVERVIEW_CHARS = 1500
MIN_Mermaid_BLOCKS = 1


def chapter_filename(chapter: dict) -> str:
    from article_generator.patterns import safe_filename
    from article_generator.sanitize import sanitize_text

    cid = chapter.get("id", "000")
    title = sanitize_text(chapter.get("title", "chapter"))
    safe = safe_filename(title, max_len=50)
    return f"{cid}-{safe}.md"


def check_chapter_file(path: Path, chapter: dict) -> list[str]:
    issues = []
    if not path.exists():
        return [f"文件缺失: {path.name}"]

    text = path.read_text(encoding="utf-8")
    title = chapter.get("title", "")

    if not text.startswith("# "):
        issues.append("缺少一级标题")

    if title and title not in text.split("\n")[0]:
        # 标题可能被 sanitize，只检查有标题行
        pass

    for sec in CHAPTER_REQUIRED_SECTIONS:
        if sec not in text:
            issues.append(f"缺少章节: {sec}")

    if text.count("```mermaid") < MIN_Mermaid_BLOCKS:
        issues.append("缺少 Mermaid 框图")

    if len(text) < MIN_CHAPTER_CHARS:
        issues.append(f"内容过短 ({len(text)} < {MIN_CHAPTER_CHARS} 字)")

    if "*章节 ID:" not in text and "章节 ID:" not in text:
        issues.append("缺少章节元数据脚注")

    if not re.search(r">\s*\*\*领域\*\*", text):
        issues.append("缺少元信息行（领域/模块/难度）")

    return issues


def check_overview_file(path: Path, domain_data: dict) -> list[str]:
    issues = []
    if not path.exists():
        return ["README.md 缺失"]

    text = path.read_text(encoding="utf-8")
    domain = domain_data.get("domain", "")

    if not text.startswith(f"# {domain}"):
        issues.append("概述标题与领域名不匹配")

    for sec in OVERVIEW_REQUIRED_SECTIONS:
        if sec not in text:
            issues.append(f"缺少章节: {sec}")

    if "```mermaid" not in text:
        issues.append("缺少学习路径 Mermaid 框图")

    if len(text) < MIN_OVERVIEW_CHARS:
        issues.append(f"内容过短 ({len(text)} < {MIN_OVERVIEW_CHARS} 字)")

    if "## 难度分布" not in text:
        issues.append("缺少难度分布表")

    return issues


def check_domain(json_path: Path) -> dict:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    domain = data["domain"]
    expected = data.get("total_chapters", len(data.get("chapters", [])))
    domain_dir = ARTICLES_DIR / domain
    readme = domain_dir / "README.md"
    chapters_dir = domain_dir / "chapters"

    result = {
        "domain": domain,
        "expected_chapters": expected,
        "issues": [],
        "chapter_issues": defaultdict(list),
    }

    result["issues"].extend(check_overview_file(readme, data))

    if not chapters_dir.is_dir():
        result["issues"].append("chapters/ 目录缺失")
        return result

    actual_files = list(chapters_dir.glob("*.md"))
    if len(actual_files) != expected:
        result["issues"].append(
            f"章节数量不符: 期望 {expected}, 实际 {len(actual_files)}"
        )

    for chapter in data.get("chapters", []):
        fname = chapter_filename(chapter)
        fpath = chapters_dir / fname
        cid = chapter.get("id", "")
        ch_issues = check_chapter_file(fpath, chapter)
        if ch_issues:
            result["chapter_issues"][cid] = ch_issues

        # 检查 ID 对应文件是否存在（按 id 前缀）
        if not fpath.exists():
            # 尝试按 id 前缀找
            alt = list(chapters_dir.glob(f"{cid}-*.md"))
            if not alt:
                result["chapter_issues"][cid].append(f"文件不存在: {fname}")

    return result


def run_check(verbose: bool = False) -> dict:
    json_files = sorted(DOMAINS_DIR.glob("*.json"))
    summary = {
        "total_domains": len(json_files),
        "domains_ok": 0,
        "domains_with_issues": 0,
        "total_chapter_issues": 0,
        "overview_issues": 0,
        "failed_domains": [],
        "failed_chapters_sample": [],
    }

    for jp in json_files:
        r = check_domain(jp)
        domain_issues = list(r["issues"])
        chapter_issue_count = len(r["chapter_issues"])

        if domain_issues or chapter_issue_count:
            summary["domains_with_issues"] += 1
            summary["overview_issues"] += len(domain_issues)
            summary["total_chapter_issues"] += chapter_issue_count
            summary["failed_domains"].append({
                "domain": r["domain"],
                "overview_issues": domain_issues,
                "chapter_issue_count": chapter_issue_count,
            })
            if verbose and domain_issues:
                print(f"[概述] {r['domain']}: {domain_issues}")
            if verbose and chapter_issue_count:
                for cid, issues in list(r["chapter_issues"].items())[:3]:
                    print(f"  [{cid}] {issues}")
        else:
            summary["domains_ok"] += 1

        # 抽样记录章节问题
        for cid, issues in r["chapter_issues"].items():
            if len(summary["failed_chapters_sample"]) < 20:
                summary["failed_chapters_sample"].append({
                    "domain": r["domain"],
                    "id": cid,
                    "issues": issues,
                })

    return summary


def main():
    print("=" * 60)
    print("文章完整性检测")
    print("=" * 60)

    if not ARTICLES_DIR.exists():
        print("错误: articles/ 目录不存在，请先运行 generate_articles.py")
        sys.exit(1)

    summary = run_check(verbose="--verbose" in sys.argv)

    print(f"领域总数: {summary['total_domains']}")
    print(f"完全通过: {summary['domains_ok']}")
    print(f"存在问题: {summary['domains_with_issues']}")
    print(f"概述问题数: {summary['overview_issues']}")
    print(f"有问题的章节数: {summary['total_chapter_issues']}")

    if summary["failed_chapters_sample"]:
        print("\n问题章节抽样:")
        for s in summary["failed_chapters_sample"][:10]:
            print(f"  {s['domain']} #{s['id']}: {s['issues']}")

    report_path = ARTICLES_DIR / "quality_report.json"
    report_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n报告已写入: {report_path}")

    if summary["domains_with_issues"] > 0:
        sys.exit(1)
    print("\n✓ 全部文章结构完整")
    sys.exit(0)


if __name__ == "__main__":
    main()
