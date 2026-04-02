# Organization Templates

이 디렉토리에는 AI 조직을 확장하기 위한 템플릿이 있습니다.

## 사용 가능한 템플릿

| 템플릿 | 설명 |
|--------|------|
| `software-dev.md` | 소프트웨어 개발 전문 조직 (Designer, DevOps, Security, Researcher 추가) |

## 새 조직 만들기

기본 `custom-org`를 복사하여 새로운 조직을 만들 수 있습니다:

```bash
# 1. 복사
cp -r custom-org my-new-org

# 2. COMPANY.md 수정 (이름, 미션, 목표)
vi my-new-org/COMPANY.md

# 3. 에이전트 추가/수정
vi my-new-org/agents/<slug>/AGENTS.md

# 4. 초기화
cd my-new-org && bin/org init

# 5. 확인
bin/org status
```

## 에이전트 추가하기

기존 조직에 에이전트를 추가하려면:

```bash
# 1. 에이전트 디렉토리 생성
mkdir -p agents/<slug>

# 2. AGENTS.md 작성 (templates/software-dev.md 참고)
vi agents/<slug>/AGENTS.md

# 3. 초기화 재실행 (새 에이전트 상태 파일 생성)
bin/org init

# 4. 예산 추가 (수동)
vi state/budgets.yaml
```
