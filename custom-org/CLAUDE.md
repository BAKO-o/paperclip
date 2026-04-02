# CLAUDE.md — Custom AI Organization (custom-org/)

이 파일은 새 세션에서 AI 조직 시스템을 이어서 작업하기 위한 컨텍스트입니다.

## Project Overview

`custom-org/` 폴더에 Paperclip의 AI 조직 모델을 마크다운/YAML 파일 기반으로 경량 구현한 시스템이 있습니다.
PostgreSQL, Express 서버 없이 **파일만으로** AI 에이전트 팀을 운영합니다.

## Architecture

```
custom-org/
├── COMPANY.md                    # 회사 정의 (agentcompanies/v1 스펙)
├── .org-config.yaml              # 런타임 설정 (거버넌스, 예산)
├── agents/                       # 9명 에이전트 정의
│   ├── ceo/AGENTS.md             # CEO — 전략, 위임 (reports to: board)
│   ├── cto/AGENTS.md             # CTO — 기술 분해, 방법론 시행 (reports to: ceo)
│   ├── eng-1/AGENTS.md           # Backend Engineer (reports to: cto)
│   ├── eng-2/AGENTS.md           # Frontend Engineer (reports to: cto)
│   ├── qa-lead/AGENTS.md         # QA Lead (reports to: cto)
│   ├── designer/AGENTS.md        # UI/UX Designer (reports to: cto)
│   ├── devops/AGENTS.md          # DevOps Engineer (reports to: cto)
│   ├── security/AGENTS.md        # CSO (reports to: cto)
│   └── researcher/AGENTS.md      # Researcher (reports to: ceo)
├── standards/                    # 공통 규율
│   ├── superpowers-methodology.md  # Iron Laws (TDD, 근본원인, 검증)
│   └── tool-ownership.md          # 도구 소유권 매트릭스
├── skills/                       # 5개 조직 운영 스킬 (SKILL.md)
│   ├── org-heartbeat/            # 에이전트 하트비트 루프
│   ├── org-delegate/             # 태스크 생성/위임
│   ├── org-board/                # 보드(인간) 거버넌스
│   ├── org-status/               # 대시보드
│   └── org-ceo/                  # CEO 전략 스킬
├── state/                        # 런타임 상태 (파일 기반 DB)
│   ├── tasks/*.yaml              # 태스크별 상태
│   ├── agents/*.yaml             # 에이전트별 상태
│   ├── approvals/*.yaml          # 승인 대기
│   ├── activity.jsonl            # 활동 로그 (append-only)
│   ├── budgets.yaml              # 예산 추적
│   └── counter.yaml              # 태스크 번호 카운터
├── bin/                          # CLI 스크립트
│   ├── org                       # 메인 CLI (task/agent/board/status/heartbeat/chart)
│   ├── org-chart                 # 조직도 (컬러 ASCII)
│   └── org-heartbeat-run         # 에이전트 하트비트 실행 (claude -p)
├── server.py                     # 웹 대시보드 (python3 server.py --port 8080)
├── dashboard.html                # 대시보드 UI
├── deploy/                       # EC2 배포 스크립트
└── templates/                    # 조직 확장 템플릿
```

## Key Commands

```bash
cd custom-org

# 조직도 (라이브 상태)
bin/org chart

# 태스크 관리
bin/org task list
bin/org task create --title "..." --assignee ceo --priority high
bin/org task update ORG-001 --status done --comment "완료"

# 에이전트 하트비트 (수동 실행 — Max 구독 내)
bin/org heartbeat ceo          # 특정 에이전트
bin/org heartbeat --all        # 전체 순차
bin/org heartbeat --all --parallel  # 전체 병렬

# 에이전트/보드 관리
bin/org agent list
bin/org agent pause eng-1
bin/org board approvals
bin/org board approve apr-001

# 대시보드
python3 server.py --port 8080
```

## Agent Training (4 Tool Ecosystems)

각 에이전트는 4개 도구 생태계에서 역할별 도구를 할당받았습니다:

| 도구 | 성격 | 위치 |
|------|------|------|
| **gstack** | 실행 도구 (review, qa, ship, cso) | /home/user/gstack |
| **bkit** | PDCA 워크플로우 엔진 | github.com/popup-studio-ai/bkit-claude-code |
| **claude-forge** | 통합 환경 (40 commands, 11 agents) | github.com/sangrokjung/claude-forge |
| **superpowers** | 행동 규율 (Iron Laws) | github.com/obra/superpowers |

도구 중복 제거 완료 — `standards/tool-ownership.md`에 단일 오너 정의.

## Development Branch

모든 작업은 `claude/custom-ai-organization-mI55F` 브랜치에서 진행합니다.

```bash
git checkout claude/custom-ai-organization-mI55F
```

## gstack은 별도 클론 필요 없음

gstack 리포지토리(`/home/user/gstack`)는 **참조용**입니다:
- 에이전트 AGENTS.md에 gstack 스킬 이름만 기록되어 있음
- 실제로 gstack 스킬을 실행하려면 Claude Code 환경에 gstack이 설치되어야 함
- 분석/수정 작업에서는 gstack 리포지토리를 불러올 필요 없음
- 에이전트 하트비트 실행 시에만 gstack 설치 환경 필요

## Current State

- 9명 에이전트, 전원 active
- 완료 태스크 4개, blocked 1개 (ORG-004), critical 보안 태스크 1개 (ORG-006)
- `bin/org task list`로 최신 상태 확인
