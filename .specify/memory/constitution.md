<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.1.0 (MINOR - Technology preference change)

Modified sections:
- Technology Stack > Frontend: Styling changed from Tailwind CSS → CSS Modules

Added sections: None

Removed sections: None

Templates requiring updates:
- ✅ plan-template.md - No changes required (styling is implementation detail)
- ✅ spec-template.md - No changes required
- ✅ tasks-template.md - No changes required
- ✅ phr-template.prompt.md - No changes required

Follow-up TODOs: None

---
Previous Sync Impact Report (v1.0.0):
Version change: 0.0.0 → 1.0.0 (MAJOR - Initial constitution creation)
Added: Core Principles (I-VIII), Technology Stack, API Design Standards,
       Security Requirements, Development Workflow, Governance
-->

# Todo App Phase II Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code MUST originate from specifications. The workflow is strictly enforced:
`/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement`

- No manual coding allowed outside the spec-driven workflow
- Refine specifications until Claude Code generates correct output
- Every feature starts with a specification document
- Code changes MUST reference a task ID from tasks.md

**Rationale**: This is the foundational hackathon requirement. SDD ensures
reproducibility, traceability, and AI-assisted development quality.

### II. Monorepo Architecture

The project uses a monorepo structure with clear separation of concerns:

```
/frontend    # Next.js 16+ application
/backend     # FastAPI application
/specs       # Feature specifications
/history     # PHRs and ADRs
/.specify    # SDD templates and scripts
```

- Frontend and backend are independently deployable
- Shared types/contracts documented in spec artifacts
- No circular dependencies between layers

**Rationale**: Enables clear ownership, independent testing, and aligned
deployment strategies while keeping related code together.

### III. Stateless Backend Design

The backend MUST be stateless and horizontally scalable:

- JWT tokens for authentication (no server-side sessions)
- No in-memory state between requests
- All state persisted in Neon PostgreSQL database
- Connection pooling for database efficiency

**Rationale**: Prepares for Phase IV/V Kubernetes deployment where pods can
scale independently without session affinity requirements.

### IV. User Data Isolation (NON-NEGOTIABLE)

Each user MUST only access their own data:

- All task operations scoped to authenticated user
- API routes use `/api/{user_id}/tasks` pattern
- Task ownership enforced on every database query
- Foreign key constraint: `tasks.user_id → users.id`
- No admin bypass or bulk user operations in Phase II

**Rationale**: Multi-tenancy security is foundational. Violations would
compromise user trust and data integrity.

### V. Type Safety

Type safety MUST be enforced across the entire stack:

- **Python**: Type hints required on all functions and methods
- **TypeScript**: Strict mode enabled, no `any` types without justification
- **API Contracts**: Pydantic models for request/response validation
- **Database**: SQLModel for typed ORM operations

**Rationale**: Type errors caught at compile/lint time reduce runtime bugs
and improve developer experience.

### VI. RESTful API Standards

All APIs MUST follow REST conventions:

- Proper HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove), PATCH (partial update)
- Consistent response format: `{"detail": "message"}` for errors
- Status codes: 200 (success), 201 (created), 204 (no content), 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error)
- All routes under `/api/` prefix
- Idempotent operations where semantically appropriate

**Rationale**: REST conventions enable predictable API behavior, easier
debugging, and better client integration.

### VII. Test-Driven Development

Testing follows Red-Green-Refactor when tests are requested:

- Write failing tests first, then implement
- Backend: pytest for API endpoint testing
- Test user isolation: User A cannot access User B's tasks
- Integration tests for critical user journeys
- No console.log or print statements in production code

**Rationale**: TDD catches bugs early and ensures code meets requirements
before integration.

### VIII. Smallest Viable Diff

Every change MUST be minimal and focused:

- No unrelated refactoring in the same commit
- No speculative features (YAGNI principle)
- One task = one logical change
- Avoid over-engineering abstractions

**Rationale**: Small diffs are easier to review, test, and roll back. They
reduce merge conflicts and speed up delivery.

## Technology Stack (Phase II)

### Frontend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | Next.js (App Router) | 16+ |
| Language | TypeScript | Strict mode |
| Styling | CSS Modules | Built-in |
| Package Manager | npm | Latest |
| Auth Client | Better Auth | Latest |

### Backend

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | FastAPI | Latest |
| Language | Python | 3.13+ |
| ORM | SQLModel | Latest |
| Package Manager | UV | Latest |
| Auth | JWT (Better Auth compatible) | N/A |

### Database

| Component | Technology |
|-----------|------------|
| Provider | Neon Serverless PostgreSQL |
| Connection | Pooled connections via Neon |
| Migrations | SQLModel/Alembic |

### Environment Variables

```bash
# Backend (.env)
DATABASE_URL=postgresql://...       # Neon connection string
BETTER_AUTH_SECRET=...              # JWT signing secret (shared)

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...              # Same secret as backend
```

## API Design Standards

### Endpoints (Phase II Scope)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all user tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### Request/Response Contracts

- All requests require `Authorization: Bearer <jwt>` header
- JSON request bodies validated via Pydantic
- Successful responses return appropriate status code + JSON body
- Error responses: `{"detail": "Error description"}`

### Database Schema

```
users
├── id (UUID, PK)
├── email (unique, indexed)
├── password_hash
└── created_at

tasks
├── id (UUID, PK)
├── user_id (FK → users.id, indexed)
├── title (required)
├── description (optional)
├── completed (boolean, indexed, default: false)
├── created_at
└── updated_at
```

## Security Requirements

### Authentication

- Better Auth handles signup/signin flows on frontend
- JWT tokens signed with `BETTER_AUTH_SECRET`
- Backend validates JWT on every protected route
- Token expiration enforced (refresh token strategy TBD)

### Authorization

- User can only access resources where `resource.user_id == jwt.user_id`
- 403 Forbidden returned for ownership violations
- No privilege escalation paths in Phase II

### Secrets Management

- NEVER hardcode secrets in source code
- Use `.env` files (gitignored) for local development
- Environment variables for deployment
- Document required secrets in README without values

### Input Validation

- All user inputs validated via Pydantic models
- SQL injection prevented via SQLModel parameterized queries
- XSS prevented via React's default escaping

## Development Workflow

### SDD Command Sequence

1. `/sp.specify` - Create feature specification
2. `/sp.clarify` - Resolve ambiguities (if needed)
3. `/sp.plan` - Generate implementation plan
4. `/sp.tasks` - Break into actionable tasks
5. `/sp.implement` - Execute tasks from tasks.md

### PHR Requirements

- Create Prompt History Record after every user interaction
- Route to appropriate directory under `history/prompts/`
- Never truncate user prompts in records

### ADR Guidelines

- Suggest ADR when architecturally significant decisions detected
- Never auto-create; require explicit user consent
- Store in `history/adr/` directory

### Performance Expectations

- API response time: < 500ms for typical operations
- Database queries: < 100ms with proper indexes
- Frontend initial load: Optimized with Next.js SSR/SSG
- Indexes required: `user_id`, `completed` on tasks table

## Scope Boundaries

### In Scope (Phase II)

- User authentication (signup/signin) with Better Auth
- Add Task - Create new todo items
- Delete Task - Remove tasks from the list
- Update Task - Modify existing task details
- View Task List - Display all tasks
- Mark as Complete - Toggle task completion status
- Multi-user support with complete data isolation
- Responsive web UI
- Deployment preparation for Vercel (frontend)

### Out of Scope (Future Phases)

- AI/chatbot features (Phase III)
- Docker/Kubernetes deployment (Phase IV)
- Kafka/Dapr event-driven architecture (Phase V)
- Priorities, tags, categories, search, filter, sort
- Recurring tasks, due dates, reminders
- Voice commands, multi-language support

## Governance

### Amendment Process

1. Propose change via `/sp.constitution` command with rationale
2. Document version bump rationale (MAJOR/MINOR/PATCH)
3. Update dependent templates if principles change
4. Create PHR documenting the amendment

### Version Policy

- **MAJOR**: Backward-incompatible principle changes
- **MINOR**: New principles or significant expansions
- **PATCH**: Clarifications, typo fixes, non-semantic changes

### Compliance Review

- All PRs/reviews MUST verify constitution compliance
- Constitution supersedes ad-hoc decisions
- Complexity deviations MUST be justified in ADRs

**Version**: 1.1.0 | **Ratified**: 2026-03-20 | **Last Amended**: 2026-03-20
