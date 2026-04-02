---
name: org-heartbeat
version: 1.0.0
description: |
  AI 조직 에이전트의 핵심 하트비트 루프. 에이전트가 깨어나서 자신의 할당된 태스크를
  확인하고, 작업을 수행하고, 상태를 업데이트하는 전체 사이클을 수행한다.
  "heartbeat", "check in", "wake up", "내 할일 확인" 등의 요청에 트리거된다.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Org Heartbeat — Agent Wake-Up Loop

당신은 AI 조직의 에이전트입니다. 이 스킬은 하트비트 루프를 실행합니다.

## Prerequisites

조직 디렉토리를 찾습니다:

```bash
ORG_DIR="${ORG_COMPANY_DIR:-$(pwd)}"
```

에이전트 신원은 `ORG_AGENT_SLUG` 환경변수 또는 사용자 지정으로 결정됩니다.

## Heartbeat Procedure

### Step 1: Identity Check

자신이 누구인지 확인합니다.

1. `ORG_AGENT_SLUG` 환경변수 확인. 없으면 사용자에게 물어봅니다.
2. `agents/<slug>/AGENTS.md`를 읽어 역할, 지시사항, 스킬 목록 확인
3. `state/agents/<slug>.yaml`를 읽어 현재 상태 확인

상태가 `paused`이면 즉시 종료하고 사용자에게 알립니다:
> "에이전트 [name]은 현재 일시정지 상태입니다. 보드의 재개 승인이 필요합니다."

### Step 2: Budget Check

`state/budgets.yaml`에서 자신의 예산을 확인합니다.

```
사용률 = spentMonthlyCents / monthlyCents
```

- **80% 이상**: 경고 메시지 출력, critical 태스크만 수행
- **100% 이상**: 자동 일시정지. `state/agents/<slug>.yaml`의 status를 `paused`로 변경하고 종료

### Step 3: Scan Tasks

`state/tasks/` 디렉토리에서 자신에게 할당된 태스크를 스캔합니다.

```bash
# state/tasks/*.yaml에서 assignee가 자신인 태스크 찾기
grep -l "assignee: <slug>" state/tasks/*.yaml 2>/dev/null
```

우선순위:
1. `status: in_progress` (이미 진행 중인 작업 우선)
2. `status: todo` (priority: critical > high > medium > low)
3. `status: blocked` (새로운 해결 컨텍스트가 있을 때만)

태스크가 없으면 `idle` 상태를 보고하고 종료합니다.

### Step 4: Checkout

선택한 태스크 파일을 업데이트합니다:

```yaml
checkoutBy: <slug>
checkoutAt: <current ISO timestamp>
status: in_progress  # todo였을 경우
```

**중요**: 이미 `checkoutBy`가 다른 에이전트로 설정된 태스크는 건너뜁니다 (단일 담당자 모델).

### Step 5: Do The Work

에이전트의 AGENTS.md에 정의된 역할과 지시사항에 따라 실제 작업을 수행합니다.

- 엔지니어: 코드 작성, 테스트, 리뷰
- CTO: 기술 분해, 아키텍처 결정
- CEO: 전략 기획, 위임
- QA: 테스트 실행, 품질 검증

gstack이 설치된 환경에서는 에이전트의 스킬 목록에 있는 gstack 스킬 (`/review`, `/qa`, `/ship` 등)을 활용합니다.

### Step 6: Update Task

작업 완료 후 태스크 파일을 업데이트합니다:

```yaml
status: <new_status>  # in_review, done, blocked 등
updatedAt: <current ISO timestamp>
completedAt: <if done>
comments:
  - author: <slug>
    body: "<작업 요약>"
    at: <current ISO timestamp>
```

### Step 7: Log Activity

`state/activity.jsonl`에 활동을 추가합니다 (한 줄 JSON append):

```json
{"ts":"<ISO>","actor":"<slug>","action":"task.update","entity":"<task-id>","details":{"previousStatus":"todo","newStatus":"in_progress"}}
```

### Step 8: Update Agent State

`state/agents/<slug>.yaml`를 업데이트합니다:

```yaml
lastHeartbeatAt: <current ISO timestamp>
status: active
```

### Step 9: Next Task or Finish

아직 처리할 태스크가 있으면 Step 3으로 돌아갑니다.
없으면 하트비트 완료를 보고합니다.

## Activity Log Actions

표준 로그 액션:
- `task.checkout` — 태스크 체크아웃
- `task.update` — 상태 변경
- `task.comment` — 코멘트 추가
- `task.create` — 새 태스크 생성
- `task.delegate` — 태스크 위임
- `agent.heartbeat` — 하트비트 시작
- `agent.pause` — 에이전트 일시정지
- `agent.resume` — 에이전트 재개
- `approval.create` — 승인 요청 생성
- `approval.resolve` — 승인 처리

## Error Handling

- 파일이 없으면 초기 상태로 생성 (`bin/org init` 실행 안내)
- YAML 파싱 실패 시 사용자에게 파일 수정 요청
- 예상치 못한 상태 시 AskUserQuestion으로 사용자 판단 요청
