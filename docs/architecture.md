# Architecture

## POC Goal
    Demonstrate `Unified API key gateway — one key per project that provisions and proxies all third-party tool API keys` with a simple browser workflow and a local backend API.

    ## Use Case Classification
    `api-key-gateway`

    ## Components
    - `frontend/`: static HTML/CSS/JavaScript
    - `backend/`: Python stdlib HTTP API
    - `poc.sqlite3`: local runtime database, ignored by git
    - `infra/`: Terraform placeholders for production resources
    - `.github/workflows/`: CI checks

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

    ## Request Flow
    ```mermaid
    sequenceDiagram
participant User
participant Frontend
participant Backend
participant DB as SQLite

User->>Frontend: Enter input and submit
Frontend->>Backend: POST /api/run
Backend->>DB: Persist run and recommendation
DB-->>Backend: Stored row id
Backend-->>Frontend: JSON recommendation
Frontend-->>User: Render next action
    ```

    ## Production Upgrade Path
    Replace SQLite with Neon or Supabase Postgres, add Clerk or Firebase Auth, deploy frontend to Vercel, and deploy backend to AWS.
