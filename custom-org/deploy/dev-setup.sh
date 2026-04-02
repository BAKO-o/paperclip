#!/usr/bin/env bash
# dev-setup.sh — 로컬 개발 환경 초기화
#
# 이 스크립트를 실행하면:
#   1. 필수 도구 확인 (Python 3, Node.js, Claude Code)
#   2. .env 파일 생성 가이드
#   3. 디렉토리 구조 초기화
#   4. 로컬 서버 기동 옵션 제공
#
# Usage:
#   bash deploy/dev-setup.sh
#   bash deploy/dev-setup.sh --start  # 설정 후 서버 자동 시작

set -euo pipefail

ORG_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DASHBOARD_PORT="${DASHBOARD_PORT:-8080}"
AUTO_START=false

# ── 옵션 파싱 ──
for arg in "$@"; do
  case "$arg" in
    --start) AUTO_START=true ;;
    *) echo "Unknown option: $arg"; exit 1 ;;
  esac
done

echo "══════════════════════════════════════════════════"
echo "  Custom AI Organization — 로컬 개발 환경 설정"
echo "══════════════════════════════════════════════════"
echo "  ORG_DIR: $ORG_DIR"
echo ""

# ── Step 1: Python 3 확인 ──
echo "[1/4] Python 3 확인..."
if ! command -v python3 &>/dev/null; then
  echo "  ERROR: python3가 설치되지 않았습니다."
  echo "  설치: https://python.org/downloads"
  exit 1
fi
PYTHON_VER=$(python3 --version 2>&1)
echo "  OK: $PYTHON_VER"

# ── Step 2: Node.js 확인 ──
echo "[2/4] Node.js 확인..."
if ! command -v node &>/dev/null; then
  echo "  ERROR: Node.js가 설치되지 않았습니다."
  echo "  설치: https://nodejs.org (v20+ 권장)"
  exit 1
fi
NODE_VER=$(node --version 2>&1)
echo "  OK: Node.js $NODE_VER"

# Claude Code CLI 확인
if ! command -v claude &>/dev/null; then
  echo "  Claude Code CLI 미설치 — 설치 중..."
  npm install -g @anthropic-ai/claude-code
  echo "  OK: Claude Code 설치 완료"
else
  echo "  OK: Claude Code $(claude --version 2>/dev/null | head -1 || echo 'found')"
fi

# ── Step 3: 환경변수 확인 ──
echo "[3/4] 환경변수 확인..."

# .env 파일 로드 (존재하는 경우)
if [ -f "$ORG_DIR/.env" ]; then
  # shellcheck disable=SC1091
  set -a
  source "$ORG_DIR/.env"
  set +a
  echo "  .env 로드 완료"
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo ""
  echo "  ⚠️  ANTHROPIC_API_KEY가 설정되지 않았습니다."
  echo ""
  echo "  방법 1: .env 파일 생성"
  echo "    cp $ORG_DIR/.env.example $ORG_DIR/.env"
  echo "    # .env 파일에 ANTHROPIC_API_KEY=sk-ant-... 입력"
  echo ""
  echo "  방법 2: 환경변수 직접 설정"
  echo "    export ANTHROPIC_API_KEY=sk-ant-..."
  echo ""
  echo "  설정 후 이 스크립트를 다시 실행하세요."
  exit 1
fi
echo "  OK: ANTHROPIC_API_KEY 설정됨"

# ── Step 4: 디렉토리 구조 초기화 ──
echo "[4/4] 디렉토리 구조 확인..."
mkdir -p "$ORG_DIR/state/heartbeat-logs"

# 필수 파일 확인
MISSING=0
for f in COMPANY.md .org-config.yaml state/activity.jsonl; do
  if [ ! -f "$ORG_DIR/$f" ]; then
    echo "  WARN: $f 없음"
    MISSING=$((MISSING + 1))
  fi
done

if [ $MISSING -gt 0 ]; then
  echo "  일부 파일이 누락되었습니다. 'bin/org init'으로 초기화하세요."
else
  echo "  OK: 조직 구조 정상"
fi

echo ""
echo "══════════════════════════════════════════════════"
echo "  개발 환경 준비 완료!"
echo ""
echo "  다음 명령어로 시작:"
echo "    make dev              # 대시보드 서버 (http://localhost:$DASHBOARD_PORT)"
echo "    make status           # 조직 상태 확인"
echo "    make heartbeat A=cto  # CTO 하트비트 실행"
echo "    make heartbeat-all    # 전체 에이전트 하트비트"
echo "══════════════════════════════════════════════════"

# ── 자동 시작 ──
if [ "$AUTO_START" = "true" ]; then
  echo ""
  echo "  서버 시작 중... (Ctrl+C로 종료)"
  echo ""
  export ORG_COMPANY_DIR="$ORG_DIR"
  exec python3 "$ORG_DIR/server.py" --port "$DASHBOARD_PORT"
fi
