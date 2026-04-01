# Software Development Organization Template

이 템플릿을 사용하면 소프트웨어 개발에 특화된 AI 조직을 추가로 만들 수 있습니다.

## 추가 에이전트 (기본 5명 + 확장)

### Designer
```yaml
# agents/designer/AGENTS.md
---
slug: designer
name: Designer
title: UI/UX Designer
reportsTo: cto
skills:
  - org-heartbeat
  - org-delegate
  - design-review
  - design-consultation
capabilities: |
  UI/UX 디자인, 와이어프레임, 디자인 시스템, 프로토타이핑
budget:
  monthlyCents: 20000
---
```

### DevOps Engineer
```yaml
# agents/devops/AGENTS.md
---
slug: devops
name: DevOps Engineer
title: DevOps Engineer
reportsTo: cto
skills:
  - org-heartbeat
  - ship
  - land-and-deploy
  - canary
  - setup-deploy
capabilities: |
  CI/CD, 인프라, 모니터링, 배포, 컨테이너화
budget:
  monthlyCents: 25000
---
```

### Security Officer
```yaml
# agents/security/AGENTS.md
---
slug: security
name: Security Officer
title: Chief Security Officer
reportsTo: cto
skills:
  - org-heartbeat
  - cso
  - careful
  - guard
capabilities: |
  보안 감사, OWASP Top 10, STRIDE 위협 모델링, 취약점 분석
budget:
  monthlyCents: 20000
---
```

### Researcher
```yaml
# agents/researcher/AGENTS.md
---
slug: researcher
name: Researcher
title: Technical Researcher
reportsTo: ceo
skills:
  - org-heartbeat
  - org-delegate
  - office-hours
capabilities: |
  기술 리서치, 벤치마킹, 경쟁 분석, 기술 문서 작성
budget:
  monthlyCents: 15000
---
```

## 확장 방법

1. 위 템플릿에서 필요한 에이전트를 선택
2. `agents/<slug>/AGENTS.md` 파일 생성
3. `bin/org init` 실행하여 상태 파일 자동 생성
4. `state/budgets.yaml`에 예산 항목 추가

## 전문 조직 워크플로우

### 소프트웨어 개발 파이프라인
```
Office Hours (아이디어)
  → CEO Review (전략)
    → CTO Eng Review (아키텍처)
      → Engineer (구현)
        → Review (코드 리뷰)
          → QA (테스트)
            → Security (보안 감사)
              → DevOps (배포)
                → Canary (모니터링)
                  → Retro (회고)
```

### 디자인 중심 파이프라인
```
Office Hours → Design Consultation → Design Review → Implementation → QA → Ship
```

### 리서치 중심 파이프라인
```
Office Hours → Research → CEO Review → Engineering Plan → Implementation → Ship
```
