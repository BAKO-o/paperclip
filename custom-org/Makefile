# Custom AI Organization — Developer Task Runner
# Usage: make <target>

ORG_DIR := $(shell pwd)
DASHBOARD_PORT ?= 8080
MODEL ?= claude-sonnet-4-6

.PHONY: help setup dev server status heartbeat heartbeat-all lint check clean

help:
	@echo "Custom AI Organization — 개발 명령어"
	@echo ""
	@echo "  make setup          로컬 개발 환경 초기화"
	@echo "  make dev            대시보드 서버 실행 (포트 $(DASHBOARD_PORT))"
	@echo "  make server         make dev 별칭"
	@echo "  make status         조직 상태 요약 출력"
	@echo "  make heartbeat A=<slug>  특정 에이전트 하트비트 실행"
	@echo "  make heartbeat-all  전체 활성 에이전트 하트비트 순차 실행"
	@echo "  make lint           코드 린트 (yamllint, shellcheck, flake8)"
	@echo "  make check          조직 구조 유효성 검사"
	@echo "  make clean          로그 파일 정리"

setup:
	@echo "==> 개발 환경 초기화..."
	@if [ -z "$$ANTHROPIC_API_KEY" ]; then \
		echo "ERROR: ANTHROPIC_API_KEY가 설정되지 않았습니다."; \
		echo "  cp .env.example .env 후 .env에 키를 입력하고 source .env 하세요."; \
		exit 1; \
	fi
	@command -v python3 >/dev/null || (echo "ERROR: python3 필요"; exit 1)
	@command -v node >/dev/null || (echo "ERROR: Node.js 필요 (https://nodejs.org)"; exit 1)
	@command -v claude >/dev/null || npm install -g @anthropic-ai/claude-code
	@mkdir -p state/heartbeat-logs
	@echo "==> 환경 초기화 완료. 'make dev'로 서버를 시작하세요."

dev server:
	@echo "==> 대시보드 서버 시작: http://localhost:$(DASHBOARD_PORT)"
	ORG_COMPANY_DIR=$(ORG_DIR) python3 server.py --port $(DASHBOARD_PORT)

status:
	@ORG_COMPANY_DIR=$(ORG_DIR) bin/org status

heartbeat:
	@if [ -z "$(A)" ]; then echo "Usage: make heartbeat A=<agent-slug>"; exit 1; fi
	@ORG_COMPANY_DIR=$(ORG_DIR) HEARTBEAT_MODEL=$(MODEL) bin/org-heartbeat-run $(A)

heartbeat-all:
	@ORG_COMPANY_DIR=$(ORG_DIR) HEARTBEAT_MODEL=$(MODEL) bin/org-heartbeat-run --all

lint:
	@echo "==> YAML 린트..."
	@if command -v yamllint >/dev/null; then \
		find . -name "*.yaml" -not -path "./.git/*" | head -50 | xargs yamllint -d relaxed; \
	else echo "  yamllint 미설치 — pip install yamllint"; fi
	@echo "==> Shell 스크립트 린트..."
	@if command -v shellcheck >/dev/null; then \
		find bin deploy -name "*.sh" -o -type f -name "org*" 2>/dev/null | xargs shellcheck 2>/dev/null || true; \
	else echo "  shellcheck 미설치 — apt install shellcheck"; fi
	@echo "==> Python 린트..."
	@python3 -m py_compile server.py && echo "  server.py: OK"
	@if command -v flake8 >/dev/null; then flake8 server.py --max-line-length=120; \
	else echo "  flake8 미설치 — pip install flake8"; fi

check:
	@echo "==> 조직 구조 검사..."
	@test -f COMPANY.md || (echo "FAIL: COMPANY.md 없음"; exit 1)
	@test -f .org-config.yaml || (echo "FAIL: .org-config.yaml 없음"; exit 1)
	@test -d state/agents || (echo "FAIL: state/agents 없음"; exit 1)
	@test -d state/tasks || (echo "FAIL: state/tasks 없음"; exit 1)
	@test -f state/activity.jsonl || (echo "FAIL: state/activity.jsonl 없음"; exit 1)
	@echo "  구조 검사: OK"
	@python3 -c "import json; [json.loads(l) for l in open('state/activity.jsonl') if l.strip()]" \
		&& echo "  activity.jsonl: OK" || echo "  WARN: activity.jsonl 파싱 오류"

clean:
	@echo "==> 30일 이상 된 하트비트 로그 삭제..."
	@find state/heartbeat-logs -name "*.log" -mtime +30 -delete 2>/dev/null || true
	@echo "  정리 완료."
