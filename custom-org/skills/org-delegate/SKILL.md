---
name: org-delegate
version: 1.0.0
description: |
  태스크 생성 및 위임 스킬. 새로운 태스크를 만들고, 조직도에 따라 적절한
  에이전트에게 할당한다. "태스크 만들어줘", "이 작업 위임해", "할일 추가" 등에 트리거.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Org Delegate — Task Creation & Delegation

조직 내에서 태스크를 생성하고 위임하는 스킬입니다.

## Task Creation Procedure

### Step 1: Read Counter

`state/counter.yaml`에서 다음 번호를 읽습니다:

```yaml
prefix: ORG
next: 42
```

### Step 2: Create Task File

`state/tasks/<PREFIX>-<NNN>.yaml` 파일을 생성합니다:

```yaml
id: ORG-042
title: "<태스크 제목>"
description: |
  <태스크 상세 설명>
status: todo
priority: medium        # critical|high|medium|low
assignee: <agent-slug>  # 할당할 에이전트
createdBy: <self-slug>  # 생성한 에이전트
parentId: null           # 상위 태스크 ID (있으면)
goalSlug: null           # 연결된 목표 slug (있으면)
projectSlug: null        # 연결된 프로젝트 slug (있으면)
checkoutBy: null
checkoutAt: null
createdAt: <current ISO timestamp>
updatedAt: <current ISO timestamp>
completedAt: null
comments: []
```

### Step 3: Increment Counter

`state/counter.yaml`의 `next`를 1 증가시킵니다.

### Step 4: Log Activity

`state/activity.jsonl`에 기록:

```json
{"ts":"<ISO>","actor":"<self>","action":"task.create","entity":"ORG-042","details":{"assignee":"<slug>","priority":"medium"}}
```

## Delegation Rules

### Org Chart Enforcement

에이전트는 자신의 **직속 부하**에게만 태스크를 위임할 수 있습니다.

조직도 (`agents/*/AGENTS.md`의 `reportsTo` 필드로 결정):
```
CEO → CTO → eng-1, eng-2, qa-lead
```

- CEO는 CTO에게만 위임 가능
- CTO는 eng-1, eng-2, qa-lead에게 위임 가능
- 엔지니어/QA는 자신에게만 태스크 생성 가능 (하위 조직 없음)
- **월권 위임 금지**: CEO가 직접 eng-1에게 위임하지 않음 (CTO를 거침)

### Goal Alignment

모든 태스크는 가능한 한 `goalSlug`를 설정해야 합니다.
`goals/` 디렉토리에서 활성 목표 목록을 확인합니다.

### Parent Task

분해된 태스크는 `parentId`로 상위 태스크를 참조합니다.
이를 통해 작업 추적이 가능합니다.

## Bulk Creation

여러 태스크를 한 번에 생성할 때:
1. 카운터를 한 번에 필요한 만큼 증가
2. 각 태스크 파일을 순차 생성
3. 활동 로그에 각각 기록
