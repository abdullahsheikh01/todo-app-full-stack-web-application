# Tasks: Project Setup

**Input**: Design documents from `/specs/001-project-setup/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: No tests requested for setup phase (per constitution: TDD N/A for setup)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend directory structure at backend/
- [ ] T002 Create frontend directory structure at frontend/
- [ ] T003 [P] Create root .gitignore with node_modules, __pycache__, .env, .next patterns
- [ ] T004 [P] Create root README.md with project overview and setup instructions

**Checkpoint**: Basic directory structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create backend/pyproject.toml with dependencies (fastapi, uvicorn, sqlmodel, python-jose, python-dotenv, psycopg2-binary)
- [ ] T006 [P] Create backend/.env.example with DATABASE_URL placeholder
- [ ] T007 Create backend/db.py with Neon PostgreSQL connection using SQLModel
- [ ] T008 Create backend/models.py with Task model (id, user_id, title, description, completed, created_at, updated_at)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Backend Health Verification (Priority: P1) 🎯 MVP

**Goal**: Start the backend server and verify it connects to the database

**Independent Test**: Run `uv run uvicorn main:app --reload --port 8000` and call `GET /health`

### Implementation for User Story 1

- [ ] T009 [US1] Create backend/main.py with FastAPI app instance and CORS middleware for localhost:3000
- [ ] T010 [US1] Implement GET /health endpoint in backend/main.py returning {"status": "ok", "database": "connected|error"}
- [ ] T011 [US1] Add database connectivity check to health endpoint using db.py connection

**Checkpoint**: Backend starts on :8000, GET /health returns database status

---

## Phase 4: User Story 2 - Frontend Landing Page (Priority: P2)

**Goal**: Start the frontend application and see the landing page

**Independent Test**: Run `npm run dev` and navigate to http://localhost:3000

### Implementation for User Story 2

- [ ] T012 [US2] Initialize Next.js 16+ project in frontend/ with App Router and TypeScript strict mode
- [ ] T013 [US2] Create frontend/.env.example with NEXT_PUBLIC_API_URL=http://localhost:8000
- [ ] T014 [US2] Create frontend/app/layout.tsx with root layout structure
- [ ] T015 [P] [US2] Create frontend/app/page.module.css with landing page styles
- [ ] T016 [US2] Create frontend/app/page.tsx displaying "Todo App - Phase II" with CSS Modules
- [ ] T017 [US2] Create frontend/lib/api.ts with typed fetch client using NEXT_PUBLIC_API_URL

**Checkpoint**: Frontend starts on :3000, landing page displays "Todo App - Phase II"

---

## Phase 5: User Story 3 - Full Stack Docker Orchestration (Priority: P3)

**Goal**: Run both frontend and backend together using Docker

**Independent Test**: Run `docker-compose up` and verify both services are accessible

### Implementation for User Story 3

- [ ] T018 [P] [US3] Create backend/Dockerfile with Python 3.13+ and UV setup
- [ ] T019 [P] [US3] Create frontend/Dockerfile with Node.js and npm setup
- [ ] T020 [US3] Create root docker-compose.yml orchestrating both services with environment variables

**Checkpoint**: docker-compose up runs both services, frontend loads, health endpoint responds

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T021 Update root README.md with complete setup instructions per quickstart.md
- [ ] T022 Validate all acceptance criteria from spec.md
- [ ] T023 Run quickstart.md verification checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP delivery
- **User Story 2 (Phase 4)**: Depends on Foundational - Can run parallel to US1
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion (needs both Dockerfiles)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Backend only - no dependencies on other stories
- **User Story 2 (P2)**: Frontend only - can run parallel to US1
- **User Story 3 (P3)**: Requires US1 and US2 complete (needs both services to containerize)

### Within Each User Story

- Setup files before application code
- Core functionality before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T003, T004 can run in parallel (different files)
- T006 can run parallel to T005
- T015 can run parallel to T014
- T018, T019 can run in parallel (different Dockerfiles)
- US1 and US2 can run in parallel after Foundational phase

---

## Parallel Example: Setup Phase

```bash
# Launch setup tasks together:
Task: "Create root .gitignore"
Task: "Create root README.md"
```

## Parallel Example: User Story 2

```bash
# After T014 (layout.tsx):
Task: "Create frontend/app/page.module.css"
Task: "Create frontend/app/page.tsx"  # Can start after layout exists
```

## Parallel Example: User Story 3

```bash
# Launch Dockerfile tasks together:
Task: "Create backend/Dockerfile"
Task: "Create frontend/Dockerfile"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: `curl http://localhost:8000/health` returns database status
5. Backend MVP ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Backend health works (MVP!)
3. Add User Story 2 → Frontend landing page works
4. Add User Story 3 → Full stack Docker works
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Backend)
   - Developer B: User Story 2 (Frontend)
3. Both complete → Developer A or B: User Story 3 (Docker)

---

## Summary

| Phase | Tasks | Parallel | Story |
|-------|-------|----------|-------|
| Setup | 4 | 2 | - |
| Foundational | 4 | 1 | - |
| US1: Backend Health | 3 | 0 | P1 |
| US2: Frontend Landing | 6 | 1 | P2 |
| US3: Docker | 3 | 2 | P3 |
| Polish | 3 | 0 | - |
| **Total** | **23** | **6** | **3 stories** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
