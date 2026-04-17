---
id: "0002"
title: plan-user-auth-implementation
stage: plan
date: 2026-04-02
surface: cli
model: claude-opus-4-5-20251101
feature: 002-user-auth
branch: 002-user-auth
user: dell
command: /sp.plan
labels: [authentication, jwt, better-auth, fastapi, nextjs, planning]
links:
  spec: specs/002-user-auth/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/002-user-auth/plan.md
  - specs/002-user-auth/research.md
  - specs/002-user-auth/data-model.md
  - specs/002-user-auth/quickstart.md
  - specs/002-user-auth/contracts/auth-api.yaml
tests:
---

## Prompt

/sp.plan

Execute the implementation planning workflow for 002-user-auth feature based on the spec.md specification.

## Response snapshot

Generated complete implementation plan for User Authentication feature:

**Phase 0 - Research:**
- Discovered Better Auth uses EdDSA (Ed25519) by default, not HS256
- Determined JWKS-based validation required for backend
- Researched token storage (HttpOnly cookies) and route protection patterns

**Phase 1 - Design Artifacts:**
- `research.md`: 7 research items covering JWT algorithm, validation approach, token storage, Better Auth integration, route protection, error handling, and database schema
- `data-model.md`: Entity definitions for User, Session, Account (Better Auth managed) and Task (backend managed)
- `contracts/auth-api.yaml`: OpenAPI 3.1 specification for auth and task endpoints
- `quickstart.md`: Developer setup guide with code snippets

**Plan Summary:**
- 5 implementation phases: Backend JWT Validation → Frontend Better Auth Setup → Auth UI Pages → Route Protection → Integration Testing
- All 8 constitution principles satisfied (PASS)
- Key design decisions documented (EdDSA, HttpOnly cookies, two-layer route protection)
- Risk assessment with mitigations

## Outcome

- Impact: Complete implementation plan ready for task generation
- Tests: N/A (plan stage)
- Files: 5 files created (plan.md, research.md, data-model.md, quickstart.md, auth-api.yaml)
- Next prompts: /sp.tasks
- Reflection: Critical finding that Better Auth uses EdDSA not HS256 changed the backend validation approach from shared-secret to JWKS-based. This was discovered during research phase and properly documented.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check - PASS (all 8 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
