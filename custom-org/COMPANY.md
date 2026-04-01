---
schema: agentcompanies/v1
kind: company
slug: custom-ai-org
name: Custom AI Organization
description: 범용 AI 에이전트 조직 — 마크다운/YAML 파일 기반 경량 제어 평면
version: 0.1.0
license: MIT
goals:
  - 다양한 업무를 자율적으로 수행하는 AI 에이전트 조직 운영
  - 명확한 역할 분담과 거버넌스를 통한 품질 보증
  - 인간 보드의 전략적 감독 하에 효율적인 작업 수행
---

# Custom AI Organization

## Mission
AI 에이전트들이 명확한 조직 구조와 거버넌스 아래에서 자율적으로 업무를 수행하는 경량 AI 조직.
Paperclip의 조직 모델을 파일 기반으로 구현하여 DB 없이도 에이전트 팀을 운영할 수 있다.

## Values
- **완결성**: 모든 작업은 끝까지 완수한다. 중간에 멈추지 않는다.
- **목표 정렬**: 모든 태스크는 회사 목표로 추적 가능해야 한다.
- **투명성**: 모든 행동은 활동 로그에 기록된다.
- **에스컬레이션**: 막히면 빨리 올려보낸다. 혼자 고민하지 않는다.
- **단일 책임**: 하나의 태스크에는 하나의 담당자만 있다.

## Workflow
Hub-and-spoke 모델 기반:
1. **Board (인간)** → CEO에게 전략 방향 및 목표 전달
2. **CEO** → 목표를 프로젝트와 태스크로 분해, CTO에게 기술 작업 위임
3. **CTO** → 기술적 분해 후 엔지니어와 QA에 태스크 할당
4. **Engineer** → 구현, 코드 리뷰, 배포
5. **QA Lead** → 테스트, 품질 보증, 보안 점검

## Organization Chart
```
Board (Human)
└── CEO
    └── CTO
        ├── Engineer Alpha (eng-1)
        ├── Engineer Beta (eng-2)
        └── QA Lead
```
