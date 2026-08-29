#!/usr/bin/env bash
# 安装用户级 systemd timer：每天本地时间 08:00 执行
set -euo pipefail

REPO="${REPO:-$HOME/knowledge-json-v2}"
SRC="$REPO/scripts/daily-csdn"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
ENV_FILE="$HOME/.config/csdn-daily.env"

chmod +x "$SRC/run.sh" "$SRC/install.sh"

mkdir -p "$UNIT_DIR" "$(dirname "$ENV_FILE")"

cp -f "$SRC/csdn-daily-optimize.service" "$UNIT_DIR/"
cp -f "$SRC/csdn-daily-optimize.timer" "$UNIT_DIR/"

# 写入/合并 DISPLAY 等环境（已有文件则不覆盖，只提示）
if [[ ! -f "$ENV_FILE" ]]; then
  cat >"$ENV_FILE" <<EOF
# CSDN 每日任务环境（可按需修改）
DISPLAY=${DISPLAY:-:0}
XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}
# 可选：指定模型，例如 AGENT_MODEL=composer-2.5
# AGENT_MODEL=
# 可选：若 agent 需 API Key
# CURSOR_API_KEY=
EOF
  echo "[install] 已创建 $ENV_FILE"
else
  echo "[install] 保留已有 $ENV_FILE"
fi

systemctl --user daemon-reload
systemctl --user enable --now csdn-daily-optimize.timer

# 未登录也能触发 timer（浏览器发布仍建议保持图形会话/DISPLAY 可用）
if command -v loginctl >/dev/null 2>&1; then
  if [[ "$(loginctl show-user "$USER" -p Linger --value 2>/dev/null || true)" != "yes" ]]; then
    echo "[install] 尝试开启 linger（可能需要密码）…"
    loginctl enable-linger "$USER" 2>/dev/null || \
      echo "[install] 请手动执行: sudo loginctl enable-linger $USER"
  fi
fi

echo
echo "[install] 已启用定时器。状态："
systemctl --user list-timers --all | grep -E 'csdn-daily|NEXT' || true
systemctl --user status csdn-daily-optimize.timer --no-pager || true
echo
echo "手动试跑一次："
echo "  systemctl --user start csdn-daily-optimize.service"
echo "  # 或直接: $SRC/run.sh"
echo "查看日志："
echo "  journalctl --user -u csdn-daily-optimize.service -f"
echo "  ls -lt $SRC/logs/"
