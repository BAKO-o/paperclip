# AWS EC2 Deployment Guide

## 전체 구조

```
┌─────────────────────────────────────────────┐
│  EC2 Instance                               │
│                                             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  cron         │    │  Dashboard       │   │
│  │  (30분마다)   │    │  (port 8080)     │   │
│  │              │    │                  │   │
│  │  org-heartbeat│    │  server.py       │   │
│  │  -run --all  │    │  (systemd)       │   │
│  └──────┬───────┘    └────────┬─────────┘   │
│         │                     │             │
│         ▼                     ▼             │
│  ┌──────────────────────────────────────┐   │
│  │  Claude Code CLI (claude -p)         │   │
│  │  ANTHROPIC_API_KEY로 Claude API 호출  │   │
│  └──────────────────────────────────────┘   │
│         │                                   │
│         ▼                                   │
│  ┌──────────────────────────────────────┐   │
│  │  state/ (YAML/JSONL files)           │   │
│  │  tasks, agents, activity, budgets    │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Quick Start

### 1. EC2 인스턴스 준비

```bash
# Ubuntu 22.04 or Amazon Linux 2023 권장
# t3.small 이상 (Claude Code CLI 실행에 메모리 필요)

# 보안 그룹에서 8080 포트 열기 (대시보드용)
```

### 2. 리포지토리 클론 & API 키 설정

```bash
git clone https://github.com/BAKO-o/paperclip.git
cd paperclip/custom-org

# API 키 설정 (필수)
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc
source ~/.bashrc
```

### 3. 원클릭 설치

```bash
bash deploy/setup-ec2.sh
```

이 스크립트가 자동으로:
- Node.js + Claude Code CLI 설치
- 조직 초기화 (`bin/org init`)
- cron 스케줄 설정 (30분마다 전체 에이전트 하트비트)
- 대시보드를 systemd 서비스로 등록 (자동 시작)

### 4. 확인

```bash
# 대시보드 접속
http://YOUR_EC2_IP:8080

# 수동 테스트
bin/org-heartbeat-run eng-1

# cron 확인
crontab -l

# 대시보드 상태
sudo systemctl status ai-org-dashboard

# 하트비트 로그
tail -f state/heartbeat-logs/cron.log
```

## Heartbeat Schedule 변경

```bash
# 10분마다
HEARTBEAT_CRON='*/10 * * * *' bash deploy/setup-ec2.sh

# 1시간마다
HEARTBEAT_CRON='0 * * * *' bash deploy/setup-ec2.sh

# 매일 오전 9시
HEARTBEAT_CRON='0 9 * * *' bash deploy/setup-ec2.sh

# 평일 30분마다 (업무시간)
HEARTBEAT_CRON='*/30 9-18 * * 1-5' bash deploy/setup-ec2.sh
```

## 수동 하트비트

```bash
# 특정 에이전트
bin/org-heartbeat-run ceo
bin/org-heartbeat-run eng-1

# 전체 순차 실행
bin/org-heartbeat-run --all

# 전체 병렬 실행
bin/org-heartbeat-run --all --parallel

# 모델 지정
bin/org-heartbeat-run --all --model claude-opus-4-6
```

## 비용 참고

| Schedule | 에이전트 | 월 하트비트 수 | 예상 비용* |
|----------|---------|--------------|----------|
| 30분마다 | 9명 | ~13,000 | 환경에 따라 다름 |
| 1시간마다 | 9명 | ~6,500 | 위의 ~50% |
| 평일 업무시간만 | 9명 | ~2,000 | 위의 ~15% |

*실제 비용은 태스크 복잡도, 모델, 토큰 사용량에 따라 달라집니다.

## Troubleshooting

```bash
# Claude Code 설치 확인
claude --version

# API 키 확인
echo $ANTHROPIC_API_KEY

# 대시보드 로그
sudo journalctl -u ai-org-dashboard -f

# 하트비트 로그
ls -la state/heartbeat-logs/
cat state/heartbeat-logs/cron.log
```
