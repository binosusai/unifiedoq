# Spec: Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys

## ADDED Requirements

### Requirement: Runnable local proof of concept
The system SHALL include a local proof of concept that demonstrates the core idea with frontend, backend when needed, and local persistence without requiring paid services by default.

#### Scenario: User runs the POC
- **WHEN** the user follows the instructions in `poc_report.md`
- **THEN** the POC runs locally or clearly explains missing prerequisites

### Requirement: External POC workspace
Generated POC source code SHALL live outside the Ideate agent factory folder.

#### Scenario: POC is generated
- **WHEN** the user runs `idea poc`
- **THEN** the POC is written under the workspace-level `pocs/` folder

### Requirement: Deployment-ready documentation
The system SHALL include documentation for local setup and production deployment options.

#### Scenario: User reviews deployment path
- **WHEN** the user reads the generated POC `docs/deployment.md`
- **THEN** they can identify Vercel, AWS, Terraform, auth, database, and GitHub Actions next steps

### Requirement: Engineering handoff
The system SHALL provide enough context for a larger agent crew to continue implementation.

#### Scenario: Engineering crew receives the folder
- **WHEN** the crew reads `handoff.md`
- **THEN** it can identify mission, inputs, guardrails, and next tasks
