#!/usr/bin/env bash
# 每日 8:00：调用 Cursor Agent 优选 4 篇 → 优化 → 发布 CSDN → 回写 → git push
set -euo pipefail

REPO="${REPO:-$HOME/knowledge-json-v2}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="${PROMPT_FILE:-$SCRIPT_DIR/PROMPT.md}"
LOG_DIR="${LOG_DIR:-$SCRIPT_DIR/logs}"
AGENT_BIN="${AGENT_BIN:-$(command -v agent || true)}"
LOCK_FILE="${LOCK_FILE:-$SCRIPT_DIR/.run.lock}"
DATE_TAG="$(date +%Y%m%d-%H%M%S)"
LOG_FILE="$LOG_DIR/daily-$DATE_TAG.log"

mkdir -p "$LOG_DIR"
cd "$REPO"

# 避免重叠执行
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[daily-csdn] 已有实例在跑，退出" | tee -a "$LOG_FILE"
  exit 0
fi

# GUI / 浏览器发布所需环境（systemd 下常缺失）
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
export LANG="${LANG:-zh_CN.UTF-8}"
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:$PATH"

# Chrome CDP / CSDN 发布默认
export HEADLESS="${HEADLESS:-0}"
export CSDN_BROWSER="${CSDN_BROWSER:-chrome}"
export CSDN_CDP_PORT="${CSDN_CDP_PORT:-9222}"

if [[ ! -x "$AGENT_BIN" ]]; then
  echo "[daily-csdn] 找不到 agent 可执行文件: $AGENT_BIN" | tee -a "$LOG_FILE"
  exit 1
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "[daily-csdn] 找不到提示词: $PROMPT_FILE" | tee -a "$LOG_FILE"
  exit 1
fi

# 登记表若不存在则创建一次
REGISTRY="$REPO/articles/CSDN-DAILY-PUBLISHED.md"
if [[ ! -f "$REGISTRY" ]]; then
  cat >"$REGISTRY" <<'EOF'
# CSDN 每日优化发布登记表

> 用途：记录已优化并发布到 CSDN 的文章，避免重复发布。
> 规则：本表只建一次；之后每次发布成功只追加行，禁止删改历史行。

## 已发布记录

| 日期 | 相对路径 | 标题 | CSDN状态 | articleId / URL | 备注 |
|------|----------|------|----------|-----------------|------|
EOF
  echo "[daily-csdn] 已初始化登记表: $REGISTRY" | tee -a "$LOG_FILE"
fi

PROMPT="$(cat "$PROMPT_FILE")"
PROMPT+=$'\n\n'"今天日期：$(date +%Y-%m-%d)。请开始执行，不要只输出计划。"

echo "[daily-csdn] $(date -Is) 开始" | tee -a "$LOG_FILE"
echo "[daily-csdn] REPO=$REPO" | tee -a "$LOG_FILE"
echo "[daily-csdn] agent=$AGENT_BIN" | tee -a "$LOG_FILE"
echo "[daily-csdn] DISPLAY=$DISPLAY" | tee -a "$LOG_FILE"

# --print：非交互；--force：自动批准工具/命令；--sandbox disabled：允许浏览器与 git push
set +e
"$AGENT_BIN" -p \
  --force \
  --trust \
  --sandbox disabled \
  --workspace "$REPO" \
  ${AGENT_MODEL:+--model "$AGENT_MODEL"} \
  "$PROMPT" 2>&1 | tee -a "$LOG_FILE"
RC=${PIPESTATUS[0]}
set -e

echo "[daily-csdn] $(date -Is) 结束 exit=$RC" | tee -a "$LOG_FILE"
# 保留最近 30 天日志
find "$LOG_DIR" -name 'daily-*.log' -mtime +30 -delete 2>/dev/null || true
exit "$RC"
