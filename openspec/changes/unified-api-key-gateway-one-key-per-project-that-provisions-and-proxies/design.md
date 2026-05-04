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


## Implementation Plan
# Implementation Plan: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Goal
Create a working proof of concept that demonstrates the core value of `Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys` with the smallest credible interface.

## MVP
- Represent the idea as a concrete user workflow.
- Create one runnable local draft project.
- Include acceptance tests or manual verification steps.
- Document what the larger engineering crew should improve next.

## Approval Gate
Ask before spending money, publishing, deleting substantial work, or handing this to the 47-agent crew.

## POC Feasibility
Feasible if it can run locally using standard tooling and sample data.

## OpenSpec Change ID
`unified-api-key-gateway-one-key-per-project-that-provisions-and-proxies`

## Debate Context Used
Founder Board debate exists and was considered.

## Crew Implementation Notes
- Product Planner: MVP Workflow for Unified API Key Gateway:

1. **CLI-first Local Setup:**  
- Developer installs CLI tool per project.  
- CLI initializes a local encrypted JSON/YAML file storing third-party API keys (AES-256 encrypted).  

2. **Unified Key Generation:**  
- CLI generates a single unified API key per project (UUID or JWT-based).  
- This key proxies all API calls to third-party tools via a local proxy server.

3. **Proxy Server:**  
- Runs locally, intercepts calls authenticated with unified key.  
- Maps requests to stored third-party keys and forwards them securely.  
- Logs usage locally for audit trail.

4. **Key Provisioning & Rotation:**  
- CLI commands to add/remove third-party keys and rotate unified key.  
- Rotation invalidates old unified key, issues new one, updates proxy config.

5. **Slack Onboarding Bot (Optional MVP stretch):**  
- Basic Slack bot to generate unified keys and share CLI install instructions.

**Tradeoffs:**  
- Local-first avoids early cloud complexity and paid services but limits multi-user sync.  
- File-backed storage simplifies MVP but requires secure local backups.  
- No external deployment reduces risk but delays team-wide collaboration features.

**Next Steps:**  
- Build CLI + local proxy proof of concept within 1 week.  
- Validate with 5–30 person SaaS startups in accelerators.  
- Iterate based on security and usability feedback.
- POC Coder: POC Plan: CLI-first local unified API key gateway (file-backed)

1. Scope:
- Single project, local CLI tool
- Manage a single unified API key that proxies 2 example third-party APIs (e.g., GitHub, Stripe)
- Store third-party API keys encrypted in a local JSON file (AES-256)
- Proxy requests from CLI through unified key to third-party APIs
- Log usage events locally for audit trail

2. Implementation:
- CLI commands: `init` (create project key + encrypted store), `add-key` (add 3rd party API key), `proxy` (make proxied API call), `rotate` (rotate unified key)
- Use Node.js with `crypto` for encryption, `express` for local proxy server, and `commander` for CLI
- Unified key is a random token stored locally, required for proxy calls
- Proxy server decrypts stored keys, forwards requests with correct 3rd party key
- Log each proxy call with timestamp, endpoint, and response status

3. Tradeoffs:
- Local only, no multi-user or RBAC (simplifies MVP)
- No zero-knowledge encryption (operator trust assumed)
- No redundancy or failover (single-node POC)
- Minimal audit (local logs only)

4. Outcome:
- Demonstrates single unified key proxying multiple APIs
- Shows encrypted key storage and rotation
- Provides audit trail proof
- Ready for next step: multi-user, cloud deployment, RBAC

This POC can be built in <1 week with open-source libs, no paid services, proving core concept.
- Frontend Engineer: POC Interface Proposal for Unified API Key Gateway:

1. **Project Dashboard (Web UI)**
- List projects with unified API key status (active, pending rotation).
- Button: “Create New Project” → prompts for project name.
- Within each project: list integrated third-party tools, their key status, and usage logs (basic).
- Action buttons per tool: “Add API Key,” “Rotate Key,” “Remove Key.”

2. **Unified API Key Details**
- Show the single unified API key for the project with copy-to-clipboard.
- Display last rotation timestamp and next scheduled rotation.

3. **Onboarding Flow**
- Step 1: Create/select project.
- Step 2: Add third-party tools by selecting from a predefined list (e.g., Stripe, Twilio).
- Step 3: Input third-party API keys securely (masked input).
- Step 4: Confirm unified key provisioning.

4. **Security & Audit View**
- Show recent access logs: who used the unified key and when.
- Role-based access controls: simple toggle (Admin/User).

**Tradeoffs:**
- Web UI only (no CLI) for rapid iteration and demo.
- Minimal integrations (start with 2–3 tools) to prove concept.
- No backend persistence yet; use local JSON files to simulate data.
- Focus on usability, not full security (encryption, RBAC) in POC.

This interface enables a quick, visible demo of unified key management and onboarding benefits within a week.
- Backend Engineer: **API Definition for POC:**

- **POST /projects**  
  Create a project with a unified API key (UUID). Returns project ID and unified key.

- **POST /projects/{projectId}/keys**  
  Add third-party API key metadata (service name, encrypted key blob). Returns key ID.

- **GET /projects/{projectId}/proxy/{serviceName}/request**  
  Proxy a request to the third-party API using stored key. Accepts method, path, headers, body. Returns proxied response.

- **POST /projects/{projectId}/keys/{keyId}/rotate**  
  Rotate a third-party API key (replace encrypted blob). Returns success status.

- **GET /projects/{projectId}/audit-logs**  
  Fetch audit logs of key usage and rotations.

**Local Persistence:**

- File-backed JSON/YAML store per project, encrypted at rest with a local master key (e.g., AES-256).  
- Store: project metadata, unified key, encrypted third-party keys, audit logs.  
- CLI-first: local file sync, no external DB or paid services.

**Tradeoffs:**

- **Security vs Simplicity:** Local encryption reduces exposure but shifts key management responsibility to user.  
- **No external deployment:** Limits scalability and multi-user collaboration but accelerates POC delivery and demo.  
- **Proxy scope limited:** Proxy only core API calls, no full SDK support to keep POC lightweight.

**Action:**  
Implement CLI tool managing encrypted local files, exposing above REST endpoints locally for integration tests and demos.
- Auth Engineer: For local POC, adopt a CLI-first, local-first, file-backed auth posture:

- Generate a single unified API key per project stored encrypted locally (e.g., AES-256).
- Proxy third-party API keys via local agent reading from encrypted config files.
- No external dependencies or paid services; no network calls beyond proxied APIs.
- Minimal RBAC: local user only; audit logs written to local files.
- Rotation and provisioning simulated via CLI commands updating local encrypted files.

Tradeoffs:  
+ Fast MVP, easy iteration, no infra cost or cloud risk.  
- No multi-user support, no centralized audit, no high availability.  
- Security limited to local machine trust boundary.

For production handoff, evolve to a cloud-hosted gateway with:  
- Strong encryption at rest and in transit, zero-knowledge encryption if feasible.  
- RBAC and team management integrated with identity providers (SSO/OAuth).  
- Centralized audit logs and alerting.  
- Redundancy and failover for availability.  
- API proxying with rate limiting and usage monitoring.

Tradeoffs:  
+ Enterprise-grade security, compliance, multi-user support, and scalability.  
- Higher complexity, cost, and operational overhead.

Action: Build local CLI POC with encrypted file storage and proxy logic. Plan cloud gateway architecture in parallel for smooth production handoff.
- Database Engineer: For a local-first, deployable unified API key gateway POC, choose SQLite as the default database:

- **Why SQLite?**  
  - Zero-config, file-backed, and embeddable—perfect for CLI-first, local use.  
  - ACID-compliant with strong reliability guarantees.  
  - Supports encryption extensions (e.g., SQLCipher) for AES-256 at rest.  
  - Easy to bundle and deploy without external dependencies.

- **Schema basics:**  
  - Tables for projects, unified keys, third-party keys, audit logs.  
  - Indexed by project ID and key ID for fast lookup.

- **Tradeoffs:**  
  - Not ideal for high concurrency or distributed multi-node setups—acceptable for MVP local use.  
  - Limited built-in access control; enforce RBAC in application layer.  
  - Backup is file-copy based; recommend automated encrypted backups.

- **Next steps:**  
  - Implement key encryption before storage.  
  - Build CLI commands to create projects, add third-party keys, rotate unified keys, and query audit logs.  
  - Design export/import for easy handoff to future distributed vault or cloud DB.

SQLite balances simplicity, security, and deployability for a rapid POC without paid services or fragile integrations.
- Infra Engineer: **Deployment Shape for Unified API Key Gateway**

1. **AWS Infrastructure:**
   - Use **AWS Lambda** for API proxying and key rotation logic (serverless, scales on demand).
   - Store encrypted keys in **AWS Secrets Manager** or **DynamoDB with KMS encryption** for durability and auditability.
   - Use **API Gateway** to expose the unified key endpoint with throttling and RBAC via Cognito or IAM.
   - Enable CloudWatch Logs for audit trails and anomaly detection.

2. **Vercel Frontend:**
   - Host the developer dashboard and onboarding Slack bot UI on Vercel for fast global delivery.
   - Use Vercel Serverless Functions for lightweight API calls (e.g., onboarding flows).

3. **Terraform:**
   - Define all AWS resources (Lambda, API Gateway, Secrets Manager, IAM roles) and Vercel project config in Terraform for reproducible, version-controlled infra.
   - Use Terraform modules to separate concerns (API, storage, frontend).

**Tradeoffs:**
- Serverless reduces ops overhead but may increase cold start latency; mitigate with provisioned concurrency.
- AWS Secrets Manager adds cost but simplifies secure key storage and rotation.
- Vercel is ideal for frontend speed but adds a second platform to manage.
- Terraform adds initial complexity but ensures infra consistency and easier scaling.

**Actionables:**
- Prototype Lambda + API Gateway proxy with DynamoDB encrypted storage.
- Deploy minimal Vercel frontend for onboarding.
- Write Terraform modules for core infra.
- Implement RBAC and audit logging from day one.
- DevOps Engineer: **GitHub Automation & Checks:**

- **CI Workflow:** On PRs and pushes to main, run:
  - Linting & formatting (e.g., ESLint, Prettier)
  - Unit & integration tests (mock key provisioning)
  - Security scans (e.g., secret scanning, dependency checks)
  - Build artifact generation (CLI tool + config schema)
- **Pre-merge Checks:** Require passing CI, code review, and signed commits.
- **Branch Protection:** Enforce status checks and restrict force pushes.

**Deployment Notes:**

- Deploy CLI-first, local-first POC as a GitHub Release artifact.
- No external paid services or cloud deployment initially; keep all state file-backed and local.
- Document manual deployment steps for future server/proxy hosting.
- Use semantic versioning; tag releases for easy rollback.

**Tradeoffs:**

- **Pros:** Fast MVP, minimal external dependencies, easy contributor onboarding.
- **Cons:** No centralized hosted service limits demo scope; manual deployment may slow iteration.
- **Mitigation:** Automate release publishing and artifact generation to speed iteration.

**Actionables:**

1. Define GitHub Actions YAML with above checks.
2. Add secret scanning and dependency audit steps.
3. Prepare release workflow to publish CLI binaries.
4. Document local usage and manual deployment in README.
- OpenSpec Writer: Implementation Requirements:

1. **Unified Key Generation & Proxying:**  
   - Generate one project-level API key that proxies requests to third-party APIs.  
   - Proxy layer must authenticate requests, inject correct third-party keys, and forward responses transparently.

2. **Secure Key Storage & Encryption:**  
   - Store third-party keys encrypted with AES-256 at rest and TLS in transit.  
   - Implement zero-knowledge encryption or client-side encryption to prevent operator access to raw keys.

3. **Access Control & Auditing:**  
   - Role-based access control (RBAC) for key retrieval, rotation, and proxy usage.  
   - Maintain detailed audit logs of all key usage and access attempts.

4. **CLI-First, Local-First MVP:**  
   - Provide CLI tool to create/manage unified keys and local file-backed config for offline use.  
   - Generate artifacts consumable by other agents or services.

5. **Automated Provisioning & Rotation:**  
   - Support automated lifecycle management workflows for third-party keys.

Acceptance Checks:

- Unified key proxies requests correctly with no direct exposure of third-party keys.  
- Keys are encrypted at rest and in transit; operator cannot decrypt raw keys.  
- RBAC enforced; audit logs capture all relevant events.  
- CLI tool creates and manages keys and config files locally without external dependencies.  
- Demo completes within one focused session, proving core concept without paid services or fragile integrations.

Tradeoffs:

- Zero-knowledge encryption increases complexity but improves security and trust.  
- Local-first CLI MVP limits immediate cloud scalability but accelerates POC delivery.  
- Proxying adds latency; optimize for minimal overhead in MVP.