# Draft POC: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

This repository is generated from approved idea artifacts and should represent a runnable first draft for the approved use case.

    ## Use Case
    `api-key-gateway`

    ## What Is Included
    - Runnable backend API in `backend/`
    - Interactive frontend in `frontend/`
    - Local SQLite persistence
    - OpenSpec copied into `openspec/`
    - Terraform entrypoint in `infra/terraform/`
    - CI checks in `.github/workflows/poc-ci.yml`
    - Project docs in `docs/`

    ## Run Locally

    ```bash
    python3 backend/app.py
    ```

    Then open `http://localhost:8000`.

    ## Component Diagram

    ```mermaid
    flowchart LR
U["User"] --> F["Frontend\n(api-key-gateway)"]
F --> B["Backend API\nUnified API key gateway — one key per project th"]
B --> D[(SQLite Runtime DB)]
B --> X["External Services\n(Mock/Sandbox)"]
CI["GitHub Actions CI"] --> B
CI --> F
I["Terraform Infra"] -. deploy .-> F
I -. deploy .-> B

    ```

## Research

# Research Brief: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Raw Intent
Developers manage dozens of API keys across tools; one unified key per project reduces setup friction, centralizes credential management, and lets teams onboard new tools with a single click

## Track
This idea is on the `money` track, so the primary research lens is commercial opportunity.

## Working Hypothesis
Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys is worth exploring if it can produce a visible result within one week and a useful proof of concept within one focused session.

## Research Questions
- Who experiences this problem often enough to care?
- What painful alternative are they using today?
- What is the smallest demo that proves the idea?
- What would make this idea obviously not worth pursuing?
- What data, API, or permission would block implementation?

## Initial Recommendation
Continue to debate. The idea is strong enough for structured criticism, but not yet ready for full engineering crew handoff.

## Crew Additions
- Market Researcher: **Findings:**
1. **Narrowest ICP:** 5–30 person, VC-backed SaaS startups in accelerator programs, building integration-heavy products (e.g., workflow automation, SaaS aggregators) without dedicated DevOps/security staff.
2. **Current Alternatives & Willingness-to-Pay:** Teams use RapidAPI Teams, AWS Secrets Manager, or custom scripts. Willingness-to-pay is highest during rapid onboarding/offboarding, frequent API key rotation, and audit/compliance events.
3. **Entry Wedge:** Free tier for up to 3 APIs/project, promoted via dev-focused Slack/Discord communities and accelerator partnerships. Slack onboarding bot as a differentiator. Paid plans start at $49/mo/project for advanced audit and team features.

**Risks:**
- **Switching Friction:** Security/compliance concerns and existing vault integrations may slow adoption, especially for teams with ingrained workflows.
- **Perceived Redundancy:** If positioned as “just another secrets manager,” developers may not see enough differentiation to justify switching.

**Recommendation:**  
Target integration-heavy SaaS startups in accelerators with a free tier and Slack onboarding bot. Focus messaging on “single-key onboarding” and rapid key rotation to stand out from generic secrets managers.
- User Researcher: **Findings:**  
1. **Trigger:** Developers are prompted to manage multiple third-party API keys when starting new projects or onboarding teammates, especially during integration sprints or compliance reviews.  
2. **Current Workaround:** Teams juggle plaintext .env files, shared vaults (e.g., AWS Secrets Manager), or ad-hoc scripts. These methods are error-prone, slow, and create onboarding friction—especially when keys change or teammates join/leave.  
3. **Sharpest Pain Point:** The highest friction is during initial project setup and key rotation: copying, securing, and updating multiple keys across environments leads to mistakes, delays, and security lapses.

**Risks:**  
1. **Adoption Barrier:** If the unified gateway requires more initial setup than simply copying keys into .env files, developers may abandon it before seeing value.  
2. **Security Trust:** Users may hesitate to trust a new tool with all their API keys unless its local-only, minimal-permission model is obvious and auditable.

**Recommendation:**  
Ship a CLI-first, file-backed MVP:  
- `init` command creates a project and unified key.  
- `add-api` stores third-party keys locally (encrypted).  
- `proxy` command starts a local server for API calls.  
- Success = running a real integration (e.g., Stripe + SendGrid) through the proxy in <30 minutes.  
- Emphasize local-only, no cloud, no raw key exposure.
- Technical Scout: **Findings:**
1. **Minimal Architecture:** A local CLI tool can generate a unified project key, store third-party API keys encrypted in a local file, and run a lightweight local proxy (e.g., Flask/FastAPI) that maps unified key requests to real third-party APIs.  
2. **Mocking Needs:** For the POC, third-party API endpoints should be mocked (e.g., via httpbin or local stub servers) to avoid handling real credentials and rate limits. Key rotation/revocation logic can be implemented with simple file updates and simulated expiry.  
3. **Security Constraints:** Local encryption (e.g., using Fernet or OS keyring) is sufficient for POC, but real-world use will require hardened storage, audit logging, and secure key handling—these can be stubbed or logged to file for now.

**Risks:**
1. **Single Point of Failure:** The unified key and local proxy represent a critical security risk—if compromised, all downstream API keys are exposed.  
2. **Integration Fragility:** Real third-party API integrations may introduce unexpected auth flows (OAuth, JWT, etc.) that are non-trivial to generalize; POC should mock these flows.

**Recommendation:**  
Build the MVP with a local CLI, encrypted file storage, and a mock proxy server. Mock all third-party APIs and key rotation. Defer real integrations and advanced security until after demo validation.

---

## Debate

# Founder Board Debate: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## Advocate
This idea deserves a POC because it addresses a repeated attention and execution problem. If the workflow becomes habitual, it can compound into more shipped projects.

## Skeptic
The risk is overbuilding agent theater before proving that capture, prioritization, and handoff actually change behavior. The system must stay small and runnable.

## Builder
The first useful version should be CLI-first, local-first, and file-backed. It should create artifacts that another agent crew can immediately read.

## Strategist
Prioritize revenue path, buyer clarity, and MVP speed.

## Synthesis
Proceed to planning if the POC can be implemented without paid services, external deployment, or fragile integrations.

## Research Context Used
Research brief exists and was considered.

## Crew Positions
- Advocate: Targeted Research Follow-ups:
Q1. What specific features or guarantees would convince integration-heavy SaaS teams to switch from existing secrets managers to a unified API key gateway?
A1. - **Centralized API key proxying:** Guarantees no direct exposure of third-party keys to developers, reducing leak risk beyond standard secrets managers.  
- **Single unified key per project:** Simplifies onboarding/offboarding by rotating one key instead of many, reducing human error and operational overhead.  
- **Automated provisioning & rotation:** Built-in workflows for key lifecycle management surpass manual or script-based rotation in speed and reliability.  
- **Audit trail & compliance:** Detailed logs of API key usage and access events tailored for integration-heavy SaaS needs, impro

Q2. How can the unified API key gateway mitigate the security and liability risks of becoming a single point of failure for all third-party API keys?
A2. - **Mitigation via architectural design:**
  - Use strong encryption (e.g., AES-256) for stored keys, with keys encrypted at rest and in transit.
  - Implement zero-knowledge or client-side encryption so the gateway operator cannot access raw keys.
- **Access controls and auditing:**
  - Role-based access control (RBAC) limits who can retrieve or rotate keys.
  - Detailed audit logs track all key usage and access attempts to detect anomalies.
- **Redundancy and failover:**
  - Distribute key storage across multiple secure nodes to avoid single hardware failure.
  - Provide backup and recovery

Round 1 - Opening Statement:
This idea deserves a POC now because it directly targets a validated pain point among integration-heavy SaaS startups—centralizing and simplifying API key management, which is currently time-consuming, error-prone, and a security risk. Existing tools like AWS Secrets Manager or RapidAPI Teams either lack seamless onboarding or require complex integrations that small teams struggle to set up and maintain.

A POC can be delivered in a week: a CLI tool that generates a unified project key, stores third-party keys locally, and proxies API requests. This immediately demonstrates three high-value outcomes:
1. **Instant Developer Onboarding:** New tools require no manual secret wrangling—one key per project, one command, instant productivity.
2. **Security Differentiation:** Keys are never exposed to clients; rotation and revocation happen centrally, reducing breach risk.
3. **Clear Buyer Signal:** Accelerator-backed SaaS teams can try it free, revealing real usage and willingness-to-pay data.

Action: Build and demo a CLI/local proxy—no cloud infra, no paid services—showing single-key to multi-API proxying. Get direct user feedback and refine fast. This unlocks fast iteration and real-world validation.

Round 2 - Rebuttal:
I appreciate the rigor from both Skeptic and Builder. Skeptic correctly flags switching friction and security as real risks; Builder, meanwhile, shows how a POC can prove or disprove core value with minimal investment.

However, Skeptic’s call for interviews before building is overly cautious given our rapid prototype mandate. Per Strategist and Builder, we have a clear ICP, market entry wedge, and the ability to deliver a CLI-first, local POC that runs in a single session—no infra, no sensitive data risk.

Builder’s approach is actionable: two CLI commands, a simple proxy, and a demo that rotates API keys. This is the least risky way to pressure-test both the onboarding promise and real security concerns—without asking teams to migrate anything yet.

**Action:** Support Builder’s POC plan and Strategist’s prioritization:  
- Build the CLI/local proxy demo for 2 APIs.  
- Immediately demo to 3–5 ICP teams as Strategist suggests, measuring “I’d switch now” reactions and specific blockers.  
- Use those reactions to refine messaging or pivot—before further investment.

In short: build, demo, learn, decide. This is the smallest, fastest, and most outcome-driven way forward.
- Skeptic: Targeted Research Follow-ups:
Q1. What specific features or guarantees would convince integration-heavy SaaS teams to switch from existing secrets managers to a unified API key gateway?
A1. - **Centralized API key proxying:** Guarantees no direct exposure of third-party keys to developers, reducing leak risk beyond standard secrets managers.  
- **Single unified key per project:** Simplifies onboarding/offboarding by rotating one key instead of many, reducing human error and operational overhead.  
- **Automated provisioning & rotation:** Built-in workflows for key lifecycle management surpass manual or script-based rotation in speed and reliability.  
- **Audit trail & compliance:** Detailed logs of API key usage and access events tailored for integration-heavy SaaS needs, impro

Q2. How can the unified API key gateway mitigate the security and liability risks of becoming a single point of failure for all third-party API keys?
A2. - **Mitigation via architectural design:**
  - Use strong encryption (e.g., AES-256) for stored keys, with keys encrypted at rest and in transit.
  - Implement zero-knowledge or client-side encryption so the gateway operator cannot access raw keys.
- **Access controls and auditing:**
  - Role-based access control (RBAC) limits who can retrieve or rotate keys.
  - Detailed audit logs track all key usage and access attempts to detect anomalies.
- **Redundancy and failover:**
  - Distribute key storage across multiple secure nodes to avoid single hardware failure.
  - Provide backup and recovery

Round 1 - Opening Statement:
Let’s stress-test the assumptions and risks:

**1. Switching Friction Underestimated:**  
You’re assuming integration-heavy SaaS startups will switch, but most already use AWS Secrets Manager, Vault, or custom scripts tightly woven into their CI/CD and compliance processes. The cost (time, risk, retraining) to migrate—even for a “free tier”—is high unless your solution is 10x better. Quantify: How many teams have actually abandoned their existing secrets manager in the last year? If <10%, your wedge is weak.

**2. Security/Liability Risk:**  
Centralizing all third-party API keys behind a single proxy creates a massive single point of failure. A breach here could expose every integrated service. You must demonstrate airtight local security and have a clear liability/disaster plan. Quantify: What’s your plan for incident response, and how fast can you revoke/rotate all keys if compromised?

**3. Opportunity Cost:**  
You’re targeting a niche (5–30 person SaaS teams in accelerators). Is this market big enough to justify the build? What’s the TAM, and how many would pay $49/mo? If you spend a month here, what higher-leverage problems are you ignoring?

**Action:**  
Before further build, run 5 interviews with target users: ask what would make them switch and what would stop them. Quantify switching pain and security concerns. If you can’t get strong “I’d switch today” signals, pause.

Round 2 - Rebuttal:
Builder, your CLI-first, local-only MVP is the right scope for a POC, but it risks missing the real-world switching friction I flagged earlier. Strategist, you’re right that the pain is real and the wedge is plausible, but both of you underweight the **opportunity cost**: even a fast POC is wasted if the “single-key” story doesn’t break through entrenched workflows.

**Actionable critique:**
- **Builder:** Add a “migration simulation” step—import a sample AWS Secrets Manager or Vault config and measure how much manual work is required to switch. If it’s >30 minutes or breaks CI/CD, that’s a red flag.
- **Strategist:** Instruct the demo to explicitly ask users: “What, if anything, would stop you from replacing your current secrets manager with this?” Quantify blockers, not just positive signals.

**Revised stance:** Proceed with the POC, but only if you commit to measuring switching pain and blockers as rigorously as onboarding speed. If >50% of target users say migration is too risky or laborious, kill or pivot the project before investing further.
- Builder: Targeted Research Follow-ups:
Q1. What specific features or guarantees would convince integration-heavy SaaS teams to switch from existing secrets managers to a unified API key gateway?
A1. - **Centralized API key proxying:** Guarantees no direct exposure of third-party keys to developers, reducing leak risk beyond standard secrets managers.  
- **Single unified key per project:** Simplifies onboarding/offboarding by rotating one key instead of many, reducing human error and operational overhead.  
- **Automated provisioning & rotation:** Built-in workflows for key lifecycle management surpass manual or script-based rotation in speed and reliability.  
- **Audit trail & compliance:** Detailed logs of API key usage and access events tailored for integration-heavy SaaS needs, impro

Q2. How can the unified API key gateway mitigate the security and liability risks of becoming a single point of failure for all third-party API keys?
A2. - **Mitigation via architectural design:**
  - Use strong encryption (e.g., AES-256) for stored keys, with keys encrypted at rest and in transit.
  - Implement zero-knowledge or client-side encryption so the gateway operator cannot access raw keys.
- **Access controls and auditing:**
  - Role-based access control (RBAC) limits who can retrieve or rotate keys.
  - Detailed audit logs track all key usage and access attempts to detect anomalies.
- **Redundancy and failover:**
  - Distribute key storage across multiple secure nodes to avoid single hardware failure.
  - Provide backup and recovery

Round 1 - Opening Statement:
**Smallest Credible Build Path (Actionable)**

**1. CLI-First, Local-Only MVP**
- **User runs a CLI command** to:  
  - Initialize a project (creates a config file, e.g., `api-gateway.yaml`).
  - Add two third-party API keys (e.g., for Stripe and SendGrid) via CLI prompts.
  - Generate a single “unified” project API key (random string, stored locally).

**2. Minimal Local Proxy**
- **Run a local proxy server** (Python FastAPI or Node Express, single file).
  - Accepts requests with the unified key in the header.
  - Routes requests to the correct third-party API using stored keys.
  - Logs all requests to a local file for audit.

**3. Key Rotation/Revocation**
- **CLI command** to rotate or revoke third-party keys (updates config and proxy behavior).

**4. Manual Verification**
- Demo:  
  - Make a request to the proxy with the unified key.
  - See it successfully call both third-party APIs.
  - Rotate a key and verify old key fails.

**No cloud, no external infra, no Slack bot.**  
**Total: 2 CLI commands + 1 proxy script + 1 config file.**  
This proves the core value in one session.

Round 2 - Rebuttal:
**Rebuttal (Builder):**

Referencing both **Skeptic** and **Advocate**:

I support Advocate’s push for a CLI/local proxy POC, as it is the fastest, lowest-risk way to test real demand and gather feedback. However, Skeptic is right to flag switching friction and security/liability as existential risks. Most teams will not migrate unless the POC clearly outperforms secrets managers on onboarding speed and security.

**Revision:**  
Let’s tighten the build path to directly address Skeptic’s concerns:
- **Explicitly demo security:** The POC should not just proxy keys, but also show that raw third-party keys are never exposed in logs or responses. Add a CLI audit command to verify this.
- **Switching friction test:** After demoing, run a 10-minute “migration simulation” with 1–2 target users. If they can’t see a clear time savings or security win, pause further build.
- **Incident response:** Include a CLI command to “revoke all keys” and demonstrate immediate cut-off in the proxy.

**Action:**  
Build the CLI/proxy POC as described, but require hands-on user validation and explicit security demonstration before scaling. This balances Advocate’s speed with Skeptic’s realism.
- Strategist: Targeted Research Follow-ups:
Q1. What specific features or guarantees would convince integration-heavy SaaS teams to switch from existing secrets managers to a unified API key gateway?
A1. - **Centralized API key proxying:** Guarantees no direct exposure of third-party keys to developers, reducing leak risk beyond standard secrets managers.  
- **Single unified key per project:** Simplifies onboarding/offboarding by rotating one key instead of many, reducing human error and operational overhead.  
- **Automated provisioning & rotation:** Built-in workflows for key lifecycle management surpass manual or script-based rotation in speed and reliability.  
- **Audit trail & compliance:** Detailed logs of API key usage and access events tailored for integration-heavy SaaS needs, impro

Q2. How can the unified API key gateway mitigate the security and liability risks of becoming a single point of failure for all third-party API keys?
A2. - **Mitigation via architectural design:**
  - Use strong encryption (e.g., AES-256) for stored keys, with keys encrypted at rest and in transit.
  - Implement zero-knowledge or client-side encryption so the gateway operator cannot access raw keys.
- **Access controls and auditing:**
  - Role-based access control (RBAC) limits who can retrieve or rotate keys.
  - Detailed audit logs track all key usage and access attempts to detect anomalies.
- **Redundancy and failover:**
  - Distribute key storage across multiple secure nodes to avoid single hardware failure.
  - Provide backup and recovery

Round 1 - Opening Statement:
**Ranking the Unified API Key Gateway Idea**

**1. Focus (Clarity, Buyer, Use Case):**  
High. The target is clear: 5–30 person integration-heavy SaaS startups, especially in accelerators, lacking dedicated DevOps. The pain (API key sprawl, onboarding friction) is real and recurring.

**2. Money Potential:**  
Medium-High. Willingness-to-pay is validated for onboarding/offboarding, key rotation, and compliance. Entry wedge (free tier, Slack bot) is credible. However, the market is niche and faces competition from secrets managers and API platforms, so differentiation is critical.

**3. Timing (Speed to Impact):**  
High. A CLI-first, local POC can be built in a week, demonstrating core value fast. Early feedback is achievable without infra spend.

**Prioritization:**  
**Proceed.** This idea is focused, has a plausible path to revenue, and can be validated quickly. The main risk is differentiation—ensure messaging and demo highlight “single-key onboarding” and rapid key rotation, not just secrets storage.  
**Action:** Build and demo the POC to 3–5 target teams. Collect feedback on onboarding speed and perceived value vs. existing tools before scaling.

Round 2 - Rebuttal:
**Rebuttal and Revised Stance**

Referencing both the **Skeptic** and **Builder**:

1. **On Switching Friction (Skeptic):**  
I agree that switching from entrenched secrets managers is a major hurdle. However, the Builder’s proposed CLI-first, local-only MVP minimizes this risk: it doesn’t require teams to abandon their current setup—just to try a parallel, low-friction workflow. This “sidecar” approach lets us test value without demanding a risky migration.

2. **On Security/Liability (Skeptic):**  
Your concerns are valid. The MVP must clearly demonstrate that keys are never exposed and that rotation/revocation is instant and auditable. Builder’s plan (local storage, no cloud, audit logs) directly addresses this. We should add a simple “breach simulation” in the demo to show rapid incident response.

3. **On Speed and Focus (Builder):**  
I support Builder’s minimal, CLI-driven approach—this is the fastest way to surface real objections and validate the “single-key onboarding” wedge.

**Revised Action:**  
Proceed with the MVP, but require that user interviews (per Skeptic) and a breach/rotation demo are completed before further investment. This balances speed with risk mitigation and market validation.

---

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
