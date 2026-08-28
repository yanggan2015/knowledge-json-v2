#!/usr/bin/env bash
# 从 Markdown 教程生成竖屏框图 PPT + 带讲解 MP4
# 用法: ./run.sh "articles/React/chapters/001-*.md" [额外参数]
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"

ARTICLE="${1:-}"
if [[ -z "$ARTICLE" ]]; then
  echo "用法: $0 <markdown路径> [generate_ppt_from_article.py 参数...]"
  echo "示例: $0 articles/React/chapters/001-React基础核心概念与原理.md -o ppt_output --voice-preset duo"
  exit 1
fi
shift
python3 "$SCRIPT_DIR/generate_ppt_from_article.py" "$ARTICLE" -o ppt_output "$@"
