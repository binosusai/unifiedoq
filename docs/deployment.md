# Deployment

## Recommended POC Deployment
- Frontend: Vercel
- Backend: AWS Lambda + API Gateway, ECS Fargate, or App Runner
- Database: Neon Postgres or Supabase Postgres
- Auth: Clerk for SaaS, Firebase Auth when the Firebase ecosystem is preferred
- Infra: shared Terraform modules from `/home/runner/work/ideate/platform/terraform-modules`
- DevOps: shared GitHub Actions from `/home/runner/work/ideate/platform/github-actions`

## Vercel
Deploy `frontend/` as the static site. Configure API routing once the backend target URL exists.

## AWS
Convert `backend/app.py` to Lambda/API Gateway or containerize it for App Runner/ECS.

## Terraform
Use `infra/terraform/main.tf` as the project entrypoint. It should call shared platform modules by default.

## When To Use Local Infra
Create local project-specific modules only when this POC needs an unusual architecture, special compliance, custom AWS topology, streaming/queues/workers, mobile/desktop distribution, or provider-specific resources not covered by the platform library.

## Environment Variables
Configure secrets in Vercel, AWS, Clerk, Firebase, Neon, or Supabase dashboards. Do not commit `.env`.

## Shared Rules
Follow `PROJECT_RULES.md` and the platform rules in `/home/runner/work/ideate/platform/rules`.
