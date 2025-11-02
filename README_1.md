# USAI Sonny — Ready GitHub Project (upload this folder)

This is a ready-to-upload GitHub project for the AI Sonny core minimal starter.  
Upload the *contents* of this folder (not the folder itself) to the GitHub repo https://github.com/usaimedia/usai-sonny-core.

## Quick start (local dev)
1. Build and run locally:
   ```bash
   docker build -t usai-sonny:dev .
   docker run -p 9000:9000 usai-sonny:dev
   ```
2. Check health: `curl http://localhost:9000/health`

## GitHub / AWS Deploy (high-level)
1. Run: `./setup.sh usaimedia <YOUR_AWS_ACCOUNT_ID>`
2. Add GitHub Secrets: `AWS_ACCOUNT_ID`, `GHA_ROLE_ARN`, `SLACK_WEBHOOK`
3. Merge to `main` — the workflow `.github/workflows/deploy.yml` will build and push to ECR and deploy to EKS.

## Notes
- Replace the Slack webhook secret with your real webhook in GitHub Secrets (do not commit it).
- The k8s manifest references an ECR image using your AWS account id; the workflow tags the pushed image with the SHA.
- This starter is intentionally minimal — production additions include persistent queues (Redis), S3 storage, and real verification/LLM adapters.
