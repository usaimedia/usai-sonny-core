#!/usr/bin/env bash
set -euo pipefail
echo "This script helps prepare and push the repo to GitHub and create ECR repo placeholders."
if [ "$#" -lt 2 ]; then
  echo "Usage: ./setup.sh <GITHUB_ORG> <AWS_ACCOUNT_ID>"
  exit 1
fi
GITHUB_ORG="$1"
AWS_ACCOUNT_ID="$2"
REPO="usai-sonny-core"

# Create GitHub repo (will prompt via gh)
gh repo create ${GITHUB_ORG}/${REPO} --private --source=. --remote=origin --push || true

# Create ECR repo (if you have AWS cli configured)
aws ecr describe-repositories --repository-names usai-sonny-core --region us-east-1 >/dev/null 2>&1 || \
aws ecr create-repository --repository-name usai-sonny-core --region us-east-1

echo "Set these GitHub secrets in your repo:"
echo "  AWS_ACCOUNT_ID (value: $AWS_ACCOUNT_ID)"
echo "  GHA_ROLE_ARN (value: arn:aws:iam::${AWS_ACCOUNT_ID}:role/github-actions-oidc-role-production)"
echo "  SLACK_WEBHOOK (value: https://hooks.slack.com/services/TEMP/PLACE/HOLDER)"
echo ""
echo "Then merge a small change to 'main' to trigger GitHub Actions."
