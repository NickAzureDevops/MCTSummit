# AI Study-Plan Generator — Constitution

## Core Principles

### I. Spec-First Development
Every feature or endpoint begins as a Speckit specification in `specs/`.
The spec is the single source of truth — implementation must match the spec contract.

### II. Test-Driven Validation
Tests are derived directly from the spec's acceptance scenarios and success criteria.
Red-Green-Refactor: write failing tests from the spec → implement → refactor.

### III. Automation via GitHub SDK
Pull request descriptions are kept in sync with the spec automatically via PyGithub.
CI pipelines enforce linting, type-checking, and test passage before merge.

### IV. Observability
Every response includes `X-Request-Id` for distributed tracing.
Structured logging is required for all upstream service calls.

### V. Data Integrity
Study plans are stored in memory for now. Swap to a real DB when ready.
All user-facing data must be validated with Pydantic v2 before storage.

### VI. Gamification
Each topic earns XP. Levels and badges are recalculated on every completion.
Progress is always visible to the learner.

### VII. Incremental Delivery
Start with basic plan generation and completion tracking (P1); add personalisation,
storage, and refinement as independently testable increments.

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI + Pydantic v2
- **Frontend**: Streamlit
- **AI Provider**: Azure AI Foundry (wire in when ready)
- **SDK**: PyGithub for PR automation
- **Spec tooling**: Speckit
- **CI**: GitHub Actions

## Development Workflow

1. Author or update the spec in `specs/`.
2. Generate or update tests in `tests/` to match the spec contract.
3. Implement in `src/` until tests pass.
4. Open a PR — CI runs lint, type-check, tests, and syncs the PR description with the spec.
5. Review, approve, merge.

## Governance

This constitution supersedes ad-hoc decisions.
Amendments require a PR with rationale and team approval.

**Version**: 0.3.0 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-02

---

## Non-Negotiable Principles for AI Study-Plan Generator (FastAPI / Streamlit / Postgres)

### I. Spec-First Development
- All features and endpoints begin with a Speckit specification in `specs/`.
- Specs define user stories, API contracts, and edge cases.
- Implementation must strictly follow the spec contract.

### II. UI Consistency (Streamlit)
- All user interfaces are built with Streamlit for rapid prototyping and consistency.
- Custom styling is minimized; focus is on usability and accessibility.
- Every UI must be responsive and accessible to all learners.

### III. API Contract Integrity (FastAPI)
- FastAPI endpoints validate input and output against the spec using Pydantic models.
- Error handling is explicit, structured, and user-friendly.
- All API responses are JSON, with clear error codes and trace IDs.

### V. Test-Driven Development
- Tests are written for every spec scenario before implementation.
- Unit and integration tests cover all critical paths.
- CI must pass all tests before merging.

### VI. Automation & CI/CD
- PRs are automatically updated with spec summaries and labels.
- GitHub Actions enforce linting, type-checking, and test coverage.
- Deployments are automated and reproducible.

### VII. Observability & Logging
- All API requests and errors are logged with trace IDs.
- Performance metrics and error rates are monitored.

### VIII. Incremental Delivery
- Features are delivered in small, testable increments.
- Each increment must be independently deployable and revertible.
