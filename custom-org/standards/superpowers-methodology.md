# Organization Development Standards — superpowers Methodology

이 문서는 **모든 에이전트**가 반드시 따라야 하는 개발 방법론입니다.
[superpowers](https://github.com/obra/superpowers) 프레임워크에서 채택한 규율을 정의합니다.

---

## 1. The Iron Laws (절대 원칙)

### 코드 전에 설계 (Design Before Code)
> "Do NOT write code until design is approved"

- 아무리 "간단한" 작업이라도 설계 승인 후 구현
- 2~3가지 접근법을 제안하고 선택받은 후 시작
- 설계 문서: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`

### 테스트 먼저 (Test-Driven Development)
> "Production code must never exist without a failing test written first"

- **RED**: 실패하는 테스트 작성
- **GREEN**: 테스트를 통과하는 최소 코드 구현
- **REFACTOR**: 테스트 통과를 유지하면서 코드 정리
- 테스트가 즉시 통과하면 → 무언가 잘못된 것

### 근본 원인 먼저 (Root Cause First)
> "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"

1. 에러 메시지를 주의 깊게 읽기
2. 일관되게 재현
3. 진단 증거 수집
4. 가설 수립 → 최소 변경으로 검증
5. 3번 수정 실패 시 → 아키텍처 자체를 의심

### 검증 없이 완료 선언 금지 (Verify Before Completion)
> "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"

1. 증명할 수 있는 명령어 식별
2. 실제로 실행 (과거 결과 재사용 금지)
3. 출력과 exit code 모두 확인
4. "아마 될 거야", "작동해야 해" 같은 표현 금지

---

## 2. Development Workflow (개발 워크플로우)

모든 작업은 이 순서를 따릅니다:

```
1. BRAINSTORMING (설계)
   → 컨텍스트 탐색 → 질문 → 2-3개 접근법 제안 → 승인

2. WRITING-PLANS (계획)
   → 2-5분 단위 원자적 태스크로 분해
   → 각 스텝은 테스트 가능해야 함
   → 모호한 표현 ("TBD", "나중에 추가") 금지

3. EXECUTING-PLANS (실행)
   → 계획을 순서대로 실행
   → 블로커 발생 시 즉시 중단 & 질문
   → 추측하지 말고 확인

4. CODE REVIEW (리뷰)
   → 작업 완료 후 반드시 코드 리뷰
   → "간단한 변경"이라도 리뷰 생략 금지
   → 리뷰 피드백은 기술적으로만 응답 (빈말 금지)

5. VERIFICATION (검증)
   → 신선한 검증 증거로 완료 확인
   → 테스트 통과, 빌드 성공, 린트 통과 모두 실행
```

---

## 3. Anti-Patterns (금지 행동)

### 절대 하지 말 것
- 테스트 없이 코드 작성
- 에러 메시지를 읽지 않고 수정 시도
- "잘 될 거야"라고 가정하고 완료 선언
- 한 번에 여러 문제를 동시에 수정
- "이왕 하는 김에" 요청받지 않은 코드 정리
- 근본 원인 파악 없이 증상만 패치
- 코드 리뷰 피드백에 "좋은 지적이세요!" 같은 빈말

### 위험 신호 (Red Flags)
- 코드가 테스트보다 먼저 존재
- 테스트가 즉시 통과
- 3번 연속 수정 실패
- "아마", "~해야 하는데" 같은 표현 사용
- 과거 테스트 결과를 인용 (새로 실행하지 않음)

---

## 4. Code Review Standards (코드 리뷰 기준)

### 리뷰 요청 시 (Requesting)
- 커밋 해시 제공
- 변경 범위 명시
- Critical → Important → Minor 순서로 처리

### 리뷰 수신 시 (Receiving)
- 전체 피드백을 끝까지 읽기
- 요구사항을 자신의 언어로 재진술
- 코드베이스에서 검증 후 평가
- 기술적으로만 응답 — "고쳤습니다" (빈말 금지)
- 피드백이 모호하면 작업 완전 중단 후 질문

### 정당한 반박 사유
- 피드백이 기존 기능을 깨뜨리는 경우
- 피드백에 컨텍스트가 부족한 경우
- YAGNI 원칙에 위배되는 경우
- 아키텍처와 충돌하는 경우

---

## 5. Subagent Development (서브에이전트 개발)

복잡한 작업은 서브에이전트에 위임합니다:

1. 태스크별 전용 서브에이전트 생성 (신선한 컨텍스트)
2. **2단계 리뷰**: 스펙 준수 리뷰 → 코드 품질 리뷰
3. 리뷰 단계를 절대 생략하지 않음
4. 미해결 이슈가 있으면 다음으로 진행하지 않음

---

## 6. Git Worktrees (격리된 작업 공간)

병렬 개발 시:
- `.gitignore`에 포함된 디렉토리에만 워크트리 생성
- 프로젝트 타입 자동 감지 → 의존성 설치
- 베이스라인 테스트 통과 확인 후 작업 시작

---

*이 문서는 superpowers v12.0 기반으로 작성되었습니다.*
*Reference: https://github.com/obra/superpowers*
