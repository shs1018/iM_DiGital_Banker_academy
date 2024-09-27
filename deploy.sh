#!/bin/bash

# 인자로 커밋 메시지가 전달되지 않으면 기본 메시지 "update" 사용
COMMIT_MESSAGE=${1:-"update"}

# git 명령어 실행
git add .
git commit -m "$COMMIT_MESSAGE"
git push