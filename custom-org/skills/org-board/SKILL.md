---
name: org-board
version: 1.0.0
description: |
  인간 보드(Human Board)를 위한 거버넌스 스킬. 승인/거부, 에이전트 관리,
  예산 변경, 조직 전체 제어를 수행한다. "승인", "거부", "에이전트 일시정지",
  "보드 액션", "조직 관리" 등에 트리거.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Org Board — Human Governance Controls

당신은 AI 조직의 보드(인간 운영자)를 보조합니다. 이 스킬은 조직에 대한 모든 거버넌스 작업을 수행합니다.

## Available Actions

### 1. Pending Approvals Review

`state/approvals/` 디렉토리에서 `status: pending`인 승인 요청을 확인합니다.

```bash
grep -l "status: pending" state/approvals/*.yaml 2>/dev/null
```

각 승인 요청의 내용을 요약하여 보드에 제시합니다:
- 요청 유형 (hire / strategy / budget-override)
- 제안자 (어느 에이전트가 요청했는지)
- 제안 내용
- 연관 태스크

### 2. Approve / Reject

승인:
```yaml
status: approved
resolvedAt: <current ISO timestamp>
resolvedBy: board
```

거부:
```yaml
status: rejected
resolvedAt: <current ISO timestamp>
resolvedBy: board
comments:
  - author: board
    body: "<거부 사유>"
    at: <current ISO timestamp>
```

활동 로그에 기록:
```json
{"ts":"<ISO>","actor":"board","action":"approval.resolve","entity":"apr-001","details":{"decision":"approved"}}
```

### 3. Agent Management

**일시정지**: `state/agents/<slug>.yaml`의 `status`를 `paused`로 변경
```json
{"ts":"<ISO>","actor":"board","action":"agent.pause","entity":"eng-1","details":{"reason":"manual"}}
```

**재개**: `status`를 `active`로 변경
```json
{"ts":"<ISO>","actor":"board","action":"agent.resume","entity":"eng-1","details":{}}
```

**상태 확인**: 모든 에이전트의 현재 상태, 마지막 하트비트, 예산 사용량 표시

### 4. Budget Management

`state/budgets.yaml`에서 예산을 조정합니다.

- 에이전트별 월 예산 변경
- 전체 조직 예산 변경
- 예산 리셋 (월초)

### 5. Direct Task Management

보드는 어떤 태스크든 직접 관리할 수 있습니다:
- 태스크 생성 (`createdBy: board`)
- 태스크 재할당 (`assignee` 변경)
- 태스크 취소 (`status: cancelled`)
- 우선순위 변경

### 6. Hiring (via Approval)

CEO가 제출한 채용 승인을 검토합니다.

승인 시:
1. 승인 파일 업데이트
2. 새 에이전트 디렉토리 생성 (`agents/<new-slug>/AGENTS.md`)
3. `state/agents/<new-slug>.yaml` 초기화
4. `state/budgets.yaml`에 예산 항목 추가

## Governance Principles

- 보드는 조직의 최고 권한을 가집니다
- 모든 보드 액션은 `state/activity.jsonl`에 기록됩니다
- 에이전트는 보드의 결정을 거부할 수 없습니다
- 보드는 어떤 에이전트의 어떤 태스크든 수정할 수 있습니다
