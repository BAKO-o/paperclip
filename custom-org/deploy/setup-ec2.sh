#!/usr/bin/env bash
# EC2 Setup Script — Custom AI Organization Heartbeat
#
# 이 스크립트를 EC2 인스턴스에서 실행하면:
# 1. 필요한 도구 설치 (Node.js, Claude Code)
# 2. 조직 파일 동기화
# 3. cron 스케줄 설정
# 4. 대시보드 서버를 systemd 서비스로 등록
#
# Usage: bash setup-ec2.sh
#
# Prerequisites:
#   - EC2 instance (Ubuntu/Amazon Linux)
#   - ANTHROPIC_API_KEY 환경변수 설정
#   - 이 리포지토리가 클론되어 있어야 함

set -euo pipefail

# ── Config ──
ORG_DIR="${ORG_COMPANY_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
CRON_SCHEDULE="${HEARTBEAT_CRON:-*/30 * * * *}"  # 기본: 30분마다
DASHBOARD_PORT="${DASHBOARD_PORT:-8080}"

echo "═══════════════════════════════════════════════"
echo "  Custom AI Organization — EC2 Setup"
echo "═══════════════════════════════════════════════"
echo "  ORG_DIR: $ORG_DIR"
echo "  Cron: $CRON_SCHEDULE"
echo "  Dashboard port: $DASHBOARD_PORT"
echo ""

# ── Step 1: Check prerequisites ──
echo "[1/5] Checking prerequisites..."

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "ERROR: ANTHROPIC_API_KEY is not set."
  echo ""
  echo "Add to ~/.bashrc or /etc/environment:"
  echo "  export ANTHROPIC_API_KEY=sk-ant-..."
  exit 1
fi

# ── Step 2: Install Claude Code if needed ──
echo "[2/5] Checking Claude Code CLI..."

if ! command -v claude &>/dev/null; then
  echo "  Installing Claude Code..."
  if command -v npm &>/dev/null; then
    npm install -g @anthropic-ai/claude-code
  else
    echo "  Installing Node.js first..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - 2>/dev/null || true
    sudo apt-get install -y nodejs 2>/dev/null || sudo yum install -y nodejs 2>/dev/null
    npm install -g @anthropic-ai/claude-code
  fi
  echo "  Claude Code installed: $(claude --version)"
else
  echo "  Claude Code already installed: $(claude --version 2>/dev/null || echo 'found')"
fi

# ── Step 3: Initialize org ──
echo "[3/5] Initializing organization..."
chmod +x "$ORG_DIR"/bin/*
"$ORG_DIR/bin/org" init

# ── Step 4: Setup cron ──
echo "[4/5] Setting up cron schedule ($CRON_SCHEDULE)..."

CRON_CMD="cd $ORG_DIR && ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY ORG_COMPANY_DIR=$ORG_DIR bin/org-heartbeat-run --all >> state/heartbeat-logs/cron.log 2>&1"

# Remove old cron entries for this org
crontab -l 2>/dev/null | grep -v "org-heartbeat-run" | crontab - 2>/dev/null || true

# Add new cron entry
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $CRON_CMD") | crontab -

echo "  Cron installed. Current schedule:"
crontab -l | grep "org-heartbeat-run" || echo "  (none)"

# ── Step 5: Setup dashboard as systemd service ──
echo "[5/5] Setting up dashboard service..."

sudo tee /etc/systemd/system/ai-org-dashboard.service > /dev/null <<EOF
[Unit]
Description=Custom AI Organization Dashboard
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=$ORG_DIR
ExecStart=/usr/bin/python3 $ORG_DIR/server.py --port $DASHBOARD_PORT
Restart=always
RestartSec=5
Environment=ORG_COMPANY_DIR=$ORG_DIR

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable ai-org-dashboard
sudo systemctl start ai-org-dashboard

echo ""
echo "═══════════════════════════════════════════════"
echo "  Setup Complete!"
echo "═══════════════════════════════════════════════"
echo ""
echo "  Dashboard: http://$(curl -s ifconfig.me 2>/dev/null || echo 'YOUR_IP'):$DASHBOARD_PORT"
echo ""
echo "  Cron schedule: $CRON_SCHEDULE"
echo "  = Agents wake up every 30 minutes"
echo ""
echo "  Commands:"
echo "    bin/org-heartbeat-run eng-1       # 수동 하트비트 (특정 에이전트)"
echo "    bin/org-heartbeat-run --all       # 수동 하트비트 (전체)"
echo "    sudo systemctl status ai-org-dashboard  # 대시보드 상태"
echo "    crontab -l                        # cron 확인"
echo "    tail -f state/heartbeat-logs/cron.log   # 하트비트 로그"
echo ""
echo "  Cron schedule 변경:"
echo "    HEARTBEAT_CRON='0 * * * *' bash deploy/setup-ec2.sh  # 1시간마다"
echo "    HEARTBEAT_CRON='*/10 * * * *' bash deploy/setup-ec2.sh  # 10분마다"
echo ""
