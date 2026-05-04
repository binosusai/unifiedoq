# DevOps

## Default Strategy
Use the shared platform library whenever this project fits the standard POC architecture.

## Shared Library
`/home/runner/work/ideate/platform`

## Shared Rules
Start with `PROJECT_RULES.md`, then use the detailed rule files in `/home/runner/work/ideate/platform/rules`.

## GitHub Organization Target
Later, move the platform folder to a repository such as `your-org/platform`.
Each POC/product repo can then call reusable workflows:

```yaml
jobs:
  ci:
    uses: your-org/platform/.github/workflows/python-poc-ci.yml@main
    with:
      backend_path: backend/app.py
```

## Terraform Modules
Keep `infra/terraform/main.tf` small and call shared modules for standard Vercel, AWS, and database resources.

## Local Overrides
Add local workflows or Terraform modules only when this project has a different architecture than the shared templates support.
