# Custom AI Organization

Paperclip의 AI 조직 모델을 마크다운/YAML 파일 기반으로 경량 구현한 시스템.
DB 없이 파일만으로 AI 에이전트 팀을 운영할 수 있습니다.

## What is this?

[Paperclip](https://github.com/paperclipai/paperclip)은 AI 에이전트 조직을 운영하는 오케스트레이션 플랫폼입니다. PostgreSQL, Express 서버, React UI 등 무거운 인프라가 필요하지만, 이 프로젝트는 Paperclip의 핵심 개념을 **파일 기반**으로 구현합니다:

| Paperclip | Custom Org |
|-----------|-----------|
| PostgreSQL DB | YAML/JSONL 파일 (`state/`) |
| Express REST API | Bash CLI 스크립트 (`bin/org`) |
| React UI 대시보드 | 터미널 대시보드 (`bin/org status`) |
| Agent Adapters | Claude Code 스킬 |
| Heartbeat Service | `org-heartbeat` SKILL.md |

## Organization Chart

```
Board (Human)
└── CEO — Chief Executive Officer
    └── CTO — Chief Technology Officer
        ├── eng-1 — Software Engineer (Alpha)
        ├── eng-2 — Software Engineer (Beta)
        └── qa-lead — QA Lead
```

## Quick Start

```bash
# 1. 초기화
cd custom-org
bin/org init

# 2. 상태 확인
bin/org status

# 3. 태스크 생성
bin/org task create --title "첫 번째 태스크" --assignee ceo --priority high

# 4. 태스크 목록
bin/org task list

# 5. 에이전트 목록
bin/org agent list
```

## Claude Code Skills

이 조직은 5개의 조직 운영 스킬을 제공합니다:

| Skill | 설명 |
|-------|------|
| `/org-heartbeat` | 에이전트 하트비트 루프 — 태스크 확인, 작업, 상태 업데이트 |
| `/org-delegate` | 태스크 생성 및 위임 |
| `/org-board` | 보드(인간) 거버넌스 — 승인, 에이전트 관리 |
| `/org-status` | 조직 대시보드 — 조직도, 태스크 보드, 예산 |
| `/org-ceo` | CEO 전략 스킬 — 목표 리뷰, 전략 분해, 채용 제안 |

### gstack Integration

[gstack](https://github.com/garrytanlab/gstack) 스킬이 설치된 환경에서는 에이전트가 추가 스킬을 활용합니다:

| Agent | gstack Skills |
|-------|--------------|
| CEO | `/plan-ceo-review`, `/office-hours` |
| CTO | `/plan-eng-review`, `/plan-ceo-review` |
| eng-1 | `/review`, `/ship`, `/investigate` |
| eng-2 | `/review`, `/qa`, `/investigate` |
| qa-lead | `/qa`, `/qa-only`, `/design-review`, `/cso` |

## CLI Reference

```bash
# Task Management
bin/org task create --title "..." --assignee <slug> --priority <level>
bin/org task list [--status todo,in_progress] [--assignee <slug>]
bin/org task show <ID>
bin/org task update <ID> --status done --comment "완료"
bin/org task checkout <ID> --agent <slug>

# Agent Management
bin/org agent list
bin/org agent show <slug>
bin/org agent pause <slug>
bin/org agent resume <slug>

# Board Governance
bin/org board approvals
bin/org board approve <approval-id>
bin/org board reject <approval-id> --reason "..."

# Dashboard
bin/org status              # 전체 대시보드
bin/org status orgchart     # 조직도
bin/org status tasks        # 태스크 보드
bin/org status budget       # 예산 요약
bin/org status activity     # 최근 활동
```

## Extending the Organization

`templates/` 디렉토리에 확장 템플릿이 있습니다:

- `software-dev.md` — Designer, DevOps, Security, Researcher 추가

```bash
# 새 에이전트 추가
mkdir -p agents/designer
# templates/software-dev.md에서 AGENTS.md 복사/수정
bin/org init  # 상태 파일 자동 생성
```

## Architecture

```
custom-org/
├── COMPANY.md              # 회사 정의 (agentcompanies/v1)
├── agents/*/AGENTS.md      # 에이전트 정의
├── skills/*/SKILL.md       # Claude Code 스킬
├── state/                  # 런타임 상태 (파일 기반 DB)
│   ├── tasks/*.yaml        # 태스크 상태
│   ├── agents/*.yaml       # 에이전트 상태
│   ├── approvals/*.yaml    # 승인 요청
│   ├── activity.jsonl      # 활동 로그 (append-only)
│   └── budgets.yaml        # 예산 추적
├── bin/                    # CLI 스크립트
└── templates/              # 조직 확장 템플릿
```

## Specification

이 프로젝트는 [Agent Companies Specification](https://agentcompanies.io/specification) (`agentcompanies/v1`) 을 준수합니다.
