# Custom AI Organization — 다른 환경에서 세팅하기

## 방법 1: Git Clone (가장 간단)

```powershell
# 1. HeadQuarter 리포에서 paperclip 클론 (custom-org만 사용)
cd D:\Z\automata\git\HeadQuarter
git clone --branch claude/custom-ai-organization-mI55F --single-branch https://github.com/BAKO-o/paperclip.git _paperclip-ref

# 2. custom-org 폴더만 복사
xcopy /E /I _paperclip-ref\custom-org custom-org

# 3. 참조 폴더 삭제
rmdir /S /Q _paperclip-ref

# 4. 초기화
cd custom-org
python bin\org-init
```

## 방법 2: 새 세션에서 Claude에게 요청

새 Claude Code 세션에서 paperclip 리포를 열고:
```
paperclip 리포의 custom-org/CLAUDE.md를 읽고 AI 조직 시스템을 이어서 작업해줘
```

---

## cokacdir 하트비트 등록

아래 명령어를 PowerShell에서 실행하면 자동 하트비트가 등록됩니다.

### CEO 주간 리포트 — 매주 월요일 09:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "당신은 AI 조직의 CEO입니다. D:/Z/automata/git/HeadQuarter/custom-org/ 디렉토리에서 작업합니다. 다음을 수행하세요: 1) state/tasks/*.yaml 파일들을 읽고 전체 태스크 현황 파악 2) goals/company-mission.md 목표 대비 진행률 평가 3) 블로커 있으면 CTO에게 위임할 새 태스크 생성 (state/counter.yaml 번호 증가, state/tasks/에 새 YAML 생성) 4) state/activity.jsonl에 하트비트 로그 추가 5) 결과를 간결하게 보고: 완료/진행중/블로킹 태스크 수, 주요 이슈, 다음 주 계획" --at "0 9 * * 1" --chat 8658423616 --key e7c0a20746367b0f
```

### 일일 블로커 체크 — 매일 09:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "D:/Z/automata/git/HeadQuarter/custom-org/state/tasks/ 디렉토리의 모든 .yaml 파일을 읽고, status가 blocked인 태스크를 찾아서 보고하세요. 각 blocked 태스크에 대해: ID, 제목, 담당자, 블로킹 사유를 정리하고, 해결 방안을 제안하세요. blocked 태스크가 없으면 '블로커 없음'이라고 보고하세요." --at "0 9 * * *" --chat 8658423616 --key e7c0a20746367b0f
```

### CTO 기술 분해 — 매주 월/수/금 10:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "당신은 AI 조직의 CTO입니다. D:/Z/automata/git/HeadQuarter/custom-org/ 에서 작업합니다. 1) state/tasks/*.yaml에서 assignee가 cto인 태스크 확인 2) todo 상태 태스크를 기술적으로 분해하여 eng-1, eng-2, qa-lead 등에게 위임할 하위 태스크 생성 3) in_review 태스크가 있으면 리뷰 4) state/counter.yaml 번호 증가 후 새 태스크 파일 생성 5) activity.jsonl에 로그 추가 6) 결과 보고" --at "0 10 * * 1,3,5" --chat 8658423616 --key e7c0a20746367b0f
```

### eng-1 구현 — 매주 월/수/금 11:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "당신은 AI 조직의 Backend Engineer (eng-1)입니다. D:/Z/automata/git/HeadQuarter/custom-org/ 에서 작업합니다. 1) state/tasks/*.yaml에서 assignee가 eng-1인 태스크 확인 2) priority가 높은 todo 태스크를 선택하여 구현 3) 구현 완료 시 status를 in_review로 변경 4) 코멘트에 작업 내용 기록 5) activity.jsonl에 로그 6) 결과 보고" --at "0 11 * * 1,3,5" --chat 8658423616 --key e7c0a20746367b0f
```

### QA 검증 — 매주 화/목 10:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "당신은 AI 조직의 QA Lead입니다. D:/Z/automata/git/HeadQuarter/custom-org/ 에서 작업합니다. 1) state/tasks/*.yaml에서 status가 in_review인 태스크 확인 2) 해당 태스크의 구현 결과를 검증 3) 합격이면 status를 done으로, 불합격이면 in_progress로 되돌리고 버그 코멘트 추가 4) activity.jsonl에 로그 5) 결과 보고" --at "0 10 * * 2,4" --chat 8658423616 --key e7c0a20746367b0f
```

### Security 보안 점검 — 매주 금요일 14:00

```powershell
& "$env:USERPROFILE\cokacdir.exe" --cron "당신은 AI 조직의 Security Officer입니다. D:/Z/automata/git/HeadQuarter/custom-org/ 에서 작업합니다. 1) state/tasks/*.yaml에서 최근 done 태스크 확인 2) 보안 관점에서 점검 (OWASP Top 10) 3) 취약점 발견 시 critical 태스크 생성 (counter.yaml 증가, 새 YAML) 4) activity.jsonl에 로그 5) 보안 현황 보고" --at "0 14 * * 5" --chat 8658423616 --key e7c0a20746367b0f
```

---

## 스케줄 요약

| 에이전트 | 주기 | 시간 |
|---------|------|------|
| CEO | 매주 월 | 09:00 |
| 블로커 체크 | 매일 | 09:00 |
| CTO | 월/수/금 | 10:00 |
| eng-1 | 월/수/금 | 11:00 |
| QA Lead | 화/목 | 10:00 |
| Security | 금 | 14:00 |

나머지 에이전트 (eng-2, designer, devops, researcher)는 필요할 때 텔레그램에서 직접 프롬프트로 깨우면 됩니다.

---

## 텔레그램에서 수동 하트비트

봇에 아래처럼 메시지를 보내면 됩니다:

```
CEO 하트비트 실행해줘. D:/Z/automata/git/HeadQuarter/custom-org/에서
state/tasks/*.yaml 읽고 현황 보고해줘.
```

```
eng-1 하트비트. D:/Z/automata/git/HeadQuarter/custom-org/에서
assignee가 eng-1인 todo 태스크 하나 골라서 구현해줘.
```
