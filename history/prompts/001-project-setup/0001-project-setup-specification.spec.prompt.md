---
id: 0001
title: Project Setup Specification
stage: spec
date: 2026-03-20
surface: agent
model: claude-opus-4-5-20251101
feature: 001-project-setup
branch: 001-project-setup
user: abdullahshaikh6601
command: /sp.specify
labels: ["spec", "project-setup", "monorepo", "full-stack"]
links:
  spec: specs/001-project-setup/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-project-setup/spec.md
  - specs/001-project-setup/checklists/requirements.md
tests:
  - null
---

## Prompt

Create a specification for "Project Setup" - Initialize the Phase II Todo App monorepo.

## Overview
Scaffold a full-stack monorepo with Next.js frontend and FastAPI backend, connected to Neon PostgreSQL.

## Deliverables

### 1. Backend (/backend)
- FastAPI application with UV package manager
- pyproject.toml with dependencies: fastapi, uvicorn, sqlmodel, python-jose, python-dotenv, psycopg2-binary
- main.py with FastAPI app instance
- db.py with Neon PostgreSQL connection using SQLModel
- models.py with Task model (id, user_id, title, description, completed, created_at, updated_at)
- Health check endpoint: GET /health → {"status": "ok", "database": "connected"}
- CORS middleware configured for frontend origin
- .env.example with DATABASE_URL placeholder

### 2. Frontend (/frontend)
- Next.js 16+ with App Router (npx create-next-app@latest)
- TypeScript strict mode enabled
- CSS Modules for styling (no Tailwind)
- /lib/api.ts - API client with base URL from environment
- Basic landing page at / showing "Todo App - Phase II"
- app/page.module.css for page-specific styles
- .env.example with NEXT_PUBLIC_API_URL placeholder

### 3. Root Level
- docker-compose.yml running both frontend and backend
- README.md with setup instructions
- .gitignore covering node_modules, __pycache__, .env files

## Acceptance Criteria
- `cd backend && uv run uvicorn main:app --reload` starts on :8000
- `cd frontend && npm run dev` starts on :3000
- GET http://localhost:8000/health returns {"status": "ok", "database": "connected"}
- Frontend page loads and displays "Todo App - Phase II"
- No hardcoded secrets - all use environment variables
- docker-compose up runs both services together

## Response snapshot

Created specification for Project Setup feature with:

**3 User Stories:**
1. P1: Backend Health Verification - Start backend and verify database connection
2. P2: Frontend Landing Page - Start frontend and see landing page
3. P3: Full Stack Docker Orchestration - Run both services via Docker

**14 Functional Requirements:**
- FR-001 to FR-006: Backend (server start, health endpoint, DB connection, CORS, Task model)
- FR-007 to FR-011: Frontend (server start, landing page, CSS Modules, API client)
- FR-012 to FR-014: Infrastructure (Docker Compose, env examples, no hardcoded secrets)

**6 Success Criteria:**
- SC-001: Backend starts within 5 seconds
- SC-002: Frontend loads within 3 seconds
- SC-003: Health endpoint shows DB status
- SC-004: Both services run without port conflicts
- SC-005: Setup under 10 minutes with README
- SC-006: Zero hardcoded secrets

**Quality Checklist:** All items passed - no clarifications needed

## Outcome

- ✅ Impact: Created comprehensive specification for monorepo scaffolding
- 🧪 Tests: Defined in acceptance scenarios (backend health, frontend load, docker orchestration)
- 📁 Files: specs/001-project-setup/spec.md, specs/001-project-setup/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to generate implementation plan
- 🧠 Reflection: User provided complete requirements - no clarifications needed. Spec focuses on WHAT (functional outcomes) not HOW (implementation details)

## Evaluation notes (flywheel)

- Failure modes observed: None - user input was comprehensive
- Graders run and results (PASS/FAIL): Quality checklist PASS (all items checked)
- Prompt variant (if applicable): Standard /sp.specify command
- Next experiment (smallest change to try): N/A - specification complete
