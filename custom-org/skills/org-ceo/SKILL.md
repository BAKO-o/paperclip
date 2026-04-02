---
name: org-ceo
version: 1.0.0
description: |
  CEO 전용 전략 스킬. 목표 리뷰, 전략적 태스크 분해, 채용 제안, 보드 커뮤니케이션을
  수행한다. CEO 에이전트가 전략적 결정을 내릴 때 사용.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
benefits-from:
  - plan-ceo-review
  - office-hours
---

# Org CEO — Strategic Planning & Governance

CEO 에이전트의 전략적 역할을 수행하는 스킬입니다.

## Strategic Planning

### Goal Review

1. `goals/` 디렉토리의 모든 목표 파일을 읽습니다
2. 각 목표의 달성 상태를 평가합니다:
   - 연결된 태스크들의 상태 확인 (`state/tasks/`에서 `goalSlug` 매칭)
   - 완료율 = done 태스크 / 전체 태스크
3. 목표 상태 업데이트가 필요하면 목표 파일 수정

### Strategic Decomposition

큰 목표를 프로젝트와 태스크로 분해합니다:

1. 목표 분석 → 필요한 프로젝트 식별
2. 프로젝트별 마일스톤 정의
3. CTO에게 위임할 기술 태스크 생성 (`/org-delegate` 활용)
4. 전략적 결정이 필요한 경우 보드 승인 요청

### Board Communication

보드(인간)에게 보고할 내용을 작성합니다:

**상태 보고서** (생성 경로: `state/board-updates/`):
```yaml
date: <current date>
author: ceo
type: status-report
summary: |
  <조직 현황 요약>
highlights:
  - <주요 성과 1>
  - <주요 성과 2>
concerns:
  - <우려 사항>
nextSteps:
  - <다음 단계>
```

## Hiring Proposals

새로운 에이전트가 필요할 때 채용 제안을 생성합니다.

### Proposal Creation

`state/approvals/` 디렉토리에 승인 요청 파일 생성:

```yaml
id: apr-<NNN>
type: hire
status: pending
proposedBy: ceo
proposal:
  agentSlug: <new-agent-slug>
  agentName: <Agent Name>
  role: <role>
  title: <title>
  reportsTo: <manager-slug>
  budgetMonthlyCents: <amount>
  rationale: |
    <채용 필요성 설명>
  capabilities: |
    <필요 역량>
createdAt: <current ISO timestamp>
resolvedAt: null
resolvedBy: null
comments: []
```

### Post-Approval

보드 승인 후:
1. 새 에이전트 디렉토리 생성 (`agents/<slug>/AGENTS.md`)
2. `state/agents/<slug>.yaml` 초기화
3. `state/budgets.yaml`에 예산 항목 추가
4. 환영 태스크 생성 (온보딩)

## Strategy Approval

대규모 전략 변경 시:

1. 전략 제안서 작성
2. `state/approvals/`에 `type: strategy` 승인 요청 생성
3. 보드 승인 대기
4. 승인 후 실행 계획 수립 및 위임

## gstack Integration

gstack이 설치된 환경에서:
- `/plan-ceo-review` — 10-star 제품 관점의 전략 리뷰, 4가지 스코프 모드
- `/office-hours` — 제품 진단, 디자인 문서 생성, 아이디어 브레인스토밍

이 스킬들은 CEO의 전략적 사고를 보강합니다. 전략 분해 전에 `/office-hours`로 아이디어를 정리하고, `/plan-ceo-review`로 스코프를 결정하는 것을 권장합니다.
