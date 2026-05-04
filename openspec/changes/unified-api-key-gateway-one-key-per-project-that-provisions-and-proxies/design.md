# Design: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Architecture
The first draft should be a complete local POC with a static frontend, a small backend API when useful, SQLite persistence, install/run docs, and deployment guidance.

## Data
Use SQLite locally. Document Neon and Supabase as production database options. Avoid paid APIs until explicitly approved.

## Auth
Use no auth for local POC unless required. Document Clerk and Firebase Auth integration points for production.

## Infra And DevOps
Prefer Vercel for frontend previews and AWS services for backend/infra when needed. Include Terraform placeholders and GitHub Actions checks.

## Risks
- The POC may prove interface feasibility without proving market demand.
- External integrations may need a second design pass.
- Deployment docs are scaffolding until real cloud accounts and project IDs are selected.
