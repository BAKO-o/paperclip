---
name: org-status
version: 1.0.0
description: |
  조직 상태 대시보드. 조직도, 태스크 보드, 예산 요약, 활동 피드를 생성한다.
  "조직 상태", "status", "대시보드", "현황 보여줘" 등에 트리거.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Org Status — Dashboard & Reporting

조직의 현재 상태를 종합적으로 보여주는 대시보드 스킬입니다.

## Dashboard Sections

### 1. Organization Chart

`agents/*/AGENTS.md`에서 에이전트 정보를 읽고, `state/agents/*.yaml`에서 런타임 상태를 결합하여 조직도를 생성합니다.

출력 형식:
```
=== Organization Chart ===

Board (Human)
└── CEO (active) — Chief Executive Officer
    └── CTO (active) — Chief Technology Officer
        ├── eng-1 (active) — Software Engineer
        ├── eng-2 (idle) — Software Engineer
        └── qa-lead (active) — QA Lead
```

각 에이전트 옆에 표시:
- `(active)` / `(paused)` / `(idle)` / `(error)` — 현재 상태
- 마지막 하트비트 시간 (있으면)

### 2. Task Board (Kanban)

`state/tasks/*.yaml`에서 모든 태스크를 읽어 상태별로 그룹화합니다.

출력 형식:
```
=== Task Board ===

BACKLOG (2)
  ORG-005 [low] Design landing page (unassigned)
  ORG-006 [medium] Write API docs (qa-lead)

TODO (3)
  ORG-003 [high] Set up monitoring (eng-2)
  ORG-004 [medium] Add unit tests (eng-1)
  ORG-007 [medium] Review security policy (qa-lead)

IN_PROGRESS (1)
  ORG-001 [critical] Implement auth system (eng-1) ← checkout by eng-1

IN_REVIEW (1)
  ORG-002 [high] Database migration (eng-2) → QA pending

DONE (5)
  ORG-010 ... ORG-014

BLOCKED (0)

CANCELLED (0)
```

### 3. Budget Summary

`state/budgets.yaml`에서 예산 현황을 읽습니다.

출력 형식:
```
=== Budget Summary (April 2026) ===

Company Total: $450.00 / $2,000.00 (22.5%)

Agent Budgets:
  CEO      $120.00 / $500.00  [████░░░░░░] 24.0%
  CTO       $85.00 / $400.00  [██░░░░░░░░] 21.3%
  eng-1    $130.00 / $300.00  [████░░░░░░] 43.3%
  eng-2     $65.00 / $300.00  [██░░░░░░░░] 21.7%
  qa-lead   $50.00 / $250.00  [██░░░░░░░░] 20.0%
```

80% 이상이면 경고, 100% 이상이면 위험 표시.

### 4. Activity Feed

`state/activity.jsonl`에서 최근 활동을 읽어 표시합니다.

출력 형식 (최근 10건):
```
=== Recent Activity ===

[2026-04-01 10:30] eng-1: task.update ORG-001 (todo → in_progress)
[2026-04-01 10:15] cto: task.create ORG-007 (assigned to qa-lead)
[2026-04-01 10:00] ceo: task.delegate ORG-003 (assigned to eng-2)
[2026-04-01 09:45] board: approval.resolve apr-001 (approved)
...
```

### 5. Blocked Work Summary

`status: blocked`인 태스크만 모아서 상세 표시:

```
=== Blocked Tasks ===

ORG-008 [high] Integration test failing (eng-2)
  Blocked since: 2026-04-01 09:00
  Last comment: "External API returns 500, waiting for fix"
  Assigned to: eng-2
```

### 6. Pending Approvals

`state/approvals/*.yaml`에서 `status: pending` 항목:

```
=== Pending Approvals ===

apr-002 [hire] CEO proposes hiring Designer Alpha
  Proposed: 2026-04-01 11:00
  Role: designer, Reports to: cto
  Budget: $150.00/month
```

## Output Options

기본적으로 전체 대시보드를 출력합니다. 특정 섹션만 요청할 수 있습니다:
- "태스크 보드만" → Task Board 섹션만
- "예산 현황" → Budget Summary 섹션만
- "활동 로그" → Activity Feed 섹션만
- "조직도" → Organization Chart 섹션만
