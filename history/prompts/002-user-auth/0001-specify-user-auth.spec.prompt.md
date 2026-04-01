---
id: "0001"
title: specify-user-auth
stage: spec
date: 2026-04-01
surface: cli
model: claude-opus-4-5-20251101
feature: 002-user-auth
branch: 002-user-auth
user: dell
command: /sp.specify
labels: [authentication, user-management, jwt, better-auth]
links:
  spec: specs/002-user-auth/spec.md
  ticket:
  adr:
  pr:
files:
  - specs/002-user-auth/spec.md
  - specs/002-user-auth/checklists/requirements.md
tests:
---

## Prompt

Create a specification for "User Authentication" - Implement signup/signin for Phase II Todo App.

## Overview
Add user authentication using Better Auth on the frontend with JWT token validation on the FastAPI backend.

## Deliverables

### 1. Frontend Authentication
- Better Auth integration with Next.js
- Signup page (/signup) - email, password, confirm password
- Signin page (/signin) - email, password
- Sign out functionality
- Protected routes - redirect unauthenticated users to /signin
- Store JWT token and attach to API requests via Authorization header
- Auth context/provider for global auth state

### 2. Backend JWT Validation
- JWT validation middleware using python-jose
- Decode and verify tokens signed with BETTER_AUTH_SECRET
- Extract user_id from token payload
- Protect all /api/{user_id}/* routes
- Return 401 Unauthorized for missing/invalid tokens
- Verify token's user_id matches URL's user_id (prevent accessing other users' data)

### 3. Database
- Users table managed by Better Auth (frontend)
- Backend only validates JWT, does not manage users directly

### 4. Environment Variables
- BETTER_AUTH_SECRET shared between frontend and backend
- BETTER_AUTH_URL for auth endpoints

## Response snapshot

Created feature branch `002-user-auth` and specification at `specs/002-user-auth/spec.md`. The specification includes:

- 5 prioritized user stories covering registration, sign in, sign out, protected routes, and authorization enforcement
- 15 functional requirements (FR-001 through FR-015)
- 7 measurable success criteria
- Edge cases for token expiration, invalid email, service unavailability, and multi-tab usage
- Key entities: User, Session/Token, Task
- Assumptions documenting reasonable defaults

Quality checklist at `specs/002-user-auth/checklists/requirements.md` - all items pass validation.

## Outcome

- Impact: Created complete user authentication specification ready for planning phase
- Tests: N/A (spec stage)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: /sp.clarify or /sp.plan
- Reflection: Spec written with technology-agnostic language focusing on user outcomes. Made informed defaults for password requirements (8 chars), no email verification, and Better Auth managing users.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual checklist - PASS (all 16 items)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
