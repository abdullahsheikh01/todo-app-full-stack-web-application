---
id: 0001
title: Phase II Constitution Creation
stage: constitution
date: 2026-03-20
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: abdullahshaikh6601
command: /sp.constitution
labels: ["constitution", "phase-ii", "sdd", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Create a constitution for Phase II of the Todo App Hackathon II - Full-Stack Web Application.

## Hackathon Context
This is Phase II of the "Evolution of Todo - Mastering Spec-Driven Development & Cloud Native AI" hackathon. The project progresses through 5 phases:
- Phase I: Python Console App (skipped - starting fresh)
- Phase II: Full-Stack Web Application ← WE ARE HERE
- Phase III: AI-Powered Chatbot (OpenAI Agents SDK + MCP)
- Phase IV: Local Kubernetes Deployment (Minikube + Helm)
- Phase V: Cloud Deployment (Kafka + Dapr + DigitalOcean)

Phase II must be built using Spec-Driven Development with Claude Code and SpecKit Plus. No manual coding allowed - refine specs until Claude generates correct output.

## Project Context
A multi-user Todo web application built using Spec-Driven Development. This is a greenfield project implementing basic task management with user authentication.

## Technology Stack (Non-Negotiable - Per Hackathon Requirements)
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Package Management: UV (backend), npm (frontend)

## Architecture Principles
1. Monorepo structure with /frontend and /backend directories
2. RESTful API design with /api/{user_id}/tasks pattern
3. Stateless backend - JWT tokens for authentication, no server sessions
4. User isolation - each user only sees their own tasks
5. Server components by default in Next.js, client components only when interactivity required

## Security Requirements
- JWT tokens shared between Better Auth (frontend) and FastAPI (backend) via BETTER_AUTH_SECRET
- All API endpoints require valid JWT in Authorization header
- Never hardcode secrets - use .env files
- Task ownership enforced on every operation
- Input validation on all endpoints using Pydantic

## Code Quality Standards
- Type hints required in Python code
- TypeScript strict mode in frontend
- API responses use consistent JSON structure
- Error handling with proper HTTP status codes (401, 403, 404, 500)
- No console.log or print statements in production code

## Database Principles
- SQLModel for all database operations
- Migrations tracked and reversible
- Foreign key constraints enforced (tasks.user_id -> users.id)
- Indexes on frequently queried columns (user_id, completed)

## API Endpoints (Per Hackathon Spec)
- GET /api/{user_id}/tasks - List all tasks
- POST /api/{user_id}/tasks - Create new task
- GET /api/{user_id}/tasks/{id} - Get task details
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
- PATCH /api/{user_id}/tasks/{id}/complete - Toggle completion

## API Design Rules
- All routes under /api/ prefix
- Use proper HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove), PATCH (partial update)
- Return appropriate status codes: 200 (success), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 404 (not found)
- Consistent error response format: {"detail": "error message"}

## Frontend Patterns
- API client abstraction in /lib/api.ts
- Reusable components in /components directory
- Pages and layouts in /app directory
- Tailwind CSS for styling, no inline styles
- Loading and error states for all async operations

## Testing Requirements
- Backend: pytest for API endpoint testing
- Frontend: Component tests where applicable
- Test user isolation (user A cannot access user B's tasks)

## Development Workflow
- Spec-driven: All features start with /sp.specify
- Small, incremental changes
- Feature branches for development
- Code must reference task IDs from tasks.md

## Performance Expectations
- API response time < 500ms for typical operations
- Frontend initial load optimized with Next.js SSR/SSG where appropriate
- Database queries optimized with proper indexes

## Core Features - Phase II Scope (Basic Level per Hackathon)
- User authentication (signup/signin) with Better Auth
- Add Task - Create new todo items
- Delete Task - Remove tasks from the list
- Update Task - Modify existing task details
- View Task List - Display all tasks
- Mark as Complete - Toggle task completion status
- Multi-user support with complete data isolation
- Responsive web UI
- Deployment to Vercel (frontend) and backend hosting

## Out of Scope for Phase II
- AI/chatbot features (Phase III)
- Kubernetes/Docker deployment (Phase IV)
- Event-driven architecture with Kafka/Dapr (Phase V)
- Intermediate features: Priorities, tags, categories, search, filter, sort
- Advanced features: Recurring tasks, due dates, reminders
- Bonus features: Voice commands, multi-language support

## Response snapshot

Created constitution v1.0.0 for Todo App Phase II with:

**8 Core Principles:**
1. Spec-Driven Development (NON-NEGOTIABLE) - SDD workflow enforced
2. Monorepo Architecture - /frontend, /backend, /specs, /history structure
3. Stateless Backend Design - JWT auth, no server sessions
4. User Data Isolation (NON-NEGOTIABLE) - Multi-tenant security
5. Type Safety - Python type hints, TypeScript strict mode
6. RESTful API Standards - Proper HTTP methods, status codes
7. Test-Driven Development - Red-Green-Refactor cycle
8. Smallest Viable Diff - YAGNI, minimal changes

**Additional Sections:**
- Technology Stack tables (Frontend, Backend, Database)
- API Design Standards with endpoint specifications
- Security Requirements (AuthN, AuthZ, Secrets, Input Validation)
- Development Workflow (SDD commands, PHR, ADR guidelines)
- Scope Boundaries (In/Out of scope for Phase II)
- Governance (Amendment process, versioning, compliance)

## Outcome

- ✅ Impact: Created foundational governance document for Phase II development
- 🧪 Tests: N/A (constitution document, not code)
- 📁 Files: .specify/memory/constitution.md created (v1.0.0)
- 🔁 Next prompts: /sp.specify to create first feature specification
- 🧠 Reflection: Constitution comprehensively covers hackathon requirements with 8 principles balancing SDD methodology, security, and code quality standards

## Evaluation notes (flywheel)

- Failure modes observed: None - template placeholders fully replaced
- Graders run and results (PASS/FAIL): Manual review PASS - all placeholders resolved
- Prompt variant (if applicable): Standard /sp.constitution command
- Next experiment (smallest change to try): N/A - initial constitution creation successful
