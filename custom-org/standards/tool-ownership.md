# Tool Ownership & Selection Guide

각 도구의 **단일 오너**를 정의하고, 중복 도구 간 선택 기준을 명시합니다.

---

## Tool Selection Rules

### Code Review — 오너: 담당 엔지니어 (self-review) + qa-lead (gate)
| 상황 | 도구 |
|------|------|
| 구현 후 셀프 리뷰 | gstack `/review` |
| 아키텍처 수준 리뷰 | CTO가 직접 수행 |
| 최종 품질 게이트 | qa-lead가 `verification-engine` |
| ~~bkit `code-review`~~ | `/review`로 통합 |
| ~~forge `/code-review`~~ | `/review`로 통합 |

### QA/Testing — 오너: qa-lead
| 상황 | 도구 |
|------|------|
| 브라우저 기반 QA | gstack `/qa` (primary) |
| 리포트만 (수정 없음) | gstack `/qa-only` |
| 테스트 커버리지 분석 | forge `/test-coverage` |
| 로그 기반 패턴 분석 | bkit `zero-script-qa` |
| ~~forge `/e2e`~~ | `/qa`로 통합 |

### Deployment — 오너: devops
| 상황 | 도구 |
|------|------|
| 릴리즈 (테스트→푸시→PR) | gstack `/ship` |
| PR 머지→배포→헬스체크 | gstack `/land-and-deploy` |
| 배포 후 모니터링 | gstack `/canary` |
| 초기 배포 설정 | gstack `/setup-deploy` |
| 롤백 | bkit `rollback` |
| ~~forge `/commit-push-pr`~~ | `/ship`으로 통합 |

### Security — 오너: security
| 상황 | 도구 |
|------|------|
| 보안 감사 (OWASP+STRIDE) | gstack `/cso` (primary) |
| 보안 컴플라이언스 | forge `/security-compliance` |
| 파괴적 명령 방지 | gstack `/careful`, `/guard` |
| ~~forge `/security-review`~~ | `/cso`로 통합 |

### Design — 오너: designer
| 상황 | 도구 |
|------|------|
| 디자인 시스템 구축 | gstack `/design-consultation` |
| 라이브 사이트 감사 | gstack `/design-review` |
| AI 슬롭 탐지 | gstack `/plan-design-review` |
| 목업/프로토타입 | bkit `phase-3-mockup` |

### TDD — 모든 엔지니어 공통
| 방법론 | 도구 |
|--------|------|
| 행동 규율 | superpowers `test-driven-development` (standards 참조) |
| 실행 도구 | forge `/tdd` (엔지니어만 사용) |

---

## Methodology Enforcement — 오너: CTO

CTO는 아래 Iron Laws 준수를 감시합니다:
1. 설계 승인 없이 코드 작성 금지
2. 테스트 없이 코드 존재 금지
3. 근본 원인 파악 없이 수정 금지
4. 검증 없이 완료 선언 금지

위반 시 태스크를 `blocked`로 되돌리고 코멘트에 위반 사항을 기록합니다.
