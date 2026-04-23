# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Todo App - Hackathon II: Spec-Driven Development & Cloud Native AI**

A 5-phase project evolving from a Python console app to a cloud-native AI chatbot:
- **Phase I**: In-Memory Python Console App (Basic CRUD)
- **Phase II**: Full-Stack Web App (Next.js + FastAPI + Neon DB)
- **Phase III**: AI Chatbot (OpenAI Agents SDK + MCP)
- **Phase IV**: Local Kubernetes (Minikube + Helm)
- **Phase V**: Cloud Deployment (Kafka + Dapr + DOKS)

## Spec-Driven Development Workflow

This project uses **SpecKit Plus** for spec-driven development. All code must originate from specifications.

**Workflow**: `/sp.specify` → `/sp.plan` → `/sp.tasks` → `/sp.implement`

**Core Rule**: No code without a spec. Refine the spec until Claude Code generates correct output.

### Key Commands
| Command | Purpose |
|---------|---------|
| `/sp.specify` | Create/update feature spec from natural language |
| `/sp.plan` | Generate implementation plan from spec |
| `/sp.tasks` | Break plan into actionable tasks |
| `/sp.implement` | Execute tasks from tasks.md |
| `/sp.clarify` | Identify underspecified areas (up to 5 questions) |
| `/sp.adr` | Document architectural decisions (requires consent) |
| `/sp.phr` | Record prompt history |

## Project Structure

```
todo-app/
├── .claude/commands/           # Agent skill definitions
├── .specify/
│   ├── memory/constitution.md  # Project principles
│   ├── templates/              # SDD artifact templates
│   └── scripts/bash/           # Automation scripts
├── specs/<feature>/            # Feature specs, plans, tasks
├── history/
│   ├── prompts/                # Prompt History Records
│   └── adr/                    # Architecture Decision Records
├── frontend/                   # Next.js app (Phase II+)
├── backend/                    # FastAPI server (Phase II+)
└── k8s/                        # Kubernetes manifests (Phase IV+)
```

## Technology Stack by Phase

### Phase I: Console App
- Python 3.13+, UV package manager
- In-memory data storage
- Basic CRUD: Add, Delete, Update, View, Mark Complete

### Phase II: Full-Stack Web
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth with JWT

### Phase III: AI Chatbot
- **UI**: OpenAI ChatKit
- **AI**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK for task operations
- **State**: Conversation persistence in database

### Phase IV-V: Cloud Native
- Docker, Minikube, Helm Charts
- Kafka for event-driven architecture
- Dapr for distributed runtime
- DigitalOcean Kubernetes (DOKS)

## Development Commands

### Phase I (Console)
```bash
uv run python src/main.py           # Run console app
uv run pytest                       # Run tests
```

### Phase II+ (Full-Stack)
```bash
# Frontend
cd frontend && npm install && npm run dev    # Dev server on :3000
cd frontend && npm run build                 # Production build
cd frontend && npm run lint                  # Lint check

# Backend
cd backend && uv run uvicorn main:app --reload --port 8000  # API server
cd backend && uv run pytest                                  # Run tests

# Both (Docker)
docker-compose up                   # Run full stack
docker-compose up --build           # Rebuild and run
```

### Phase IV+ (Kubernetes)
```bash
minikube start                      # Start local cluster
helm install todo ./k8s/charts      # Deploy with Helm
kubectl-ai "check pod status"       # AI-assisted kubectl
dapr init -k                        # Initialize Dapr on K8s
```

## API Endpoints (Phase II+)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| POST | `/api/{user_id}/chat` | Chat endpoint (Phase III) |

## MCP Tools (Phase III)

The MCP server exposes these tools for AI agent operations:
- `add_task` - Create new task
- `list_tasks` - Retrieve tasks (filterable by status)
- `complete_task` - Mark task complete
- `delete_task` - Remove task
- `update_task` - Modify task

## Code Patterns

### Backend (FastAPI)
```python
# Routes in routes/ directory
# Models in models.py using SQLModel
# Database connection in db.py
# All routes under /api/
# Use Pydantic for request/response validation
```

### Frontend (Next.js)
```typescript
// Use server components by default
// Client components only for interactivity ('use client')
// API calls through /lib/api.ts
// Components in /components, pages in /app
```

## Environment Variables

```bash
# Backend
DATABASE_URL=postgresql://...       # Neon connection string
BETTER_AUTH_SECRET=...              # JWT signing secret
OPENAI_API_KEY=...                  # For AI features

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...   # ChatKit domain key
```

## Core Development Rules

1. **Spec-First**: Always `/sp.specify` before coding
2. **PHR on Every Request**: Create Prompt History Record after each user interaction
3. **ADR by Consent**: Suggest ADRs for significant decisions, never auto-create
4. **Smallest Diff**: No unrelated refactoring or over-engineering
5. **Human as Tool**: Ask clarifying questions when requirements are ambiguous
6. **Reference Tasks**: All code must link to a task ID from tasks.md

## Artifact Routing

| Stage | Location |
|-------|----------|
| Constitution | `history/prompts/constitution/` |
| Feature work | `history/prompts/<feature-name>/` |
| General | `history/prompts/general/` |
| ADRs | `history/adr/` |
| Specs | `specs/<feature-name>/` |

## Constitution Reference

Project principles are defined in `.specify/memory/constitution.md`. This includes:
- Code quality standards
- Testing requirements
- Performance expectations
- Security guidelines
- Architecture patterns

## Active Technologies
- Python 3.13+ (backend), TypeScript strict mode (frontend) + FastAPI, uvicorn, SQLModel, python-jose, python-dotenv, psycopg2-binary (backend); Next.js 16+, CSS Modules (frontend) (001-project-setup)
- Python 3.13+ (backend), TypeScript strict mode (frontend) + FastAPI, PyJWT, httpx, cachetools (backend); Better Auth, Next.js 16+ (frontend) (002-user-auth)
- TypeScript (strict mode) with Next.js 16+ (App Router) + React 19+, Next.js 16+, Better Auth (client) (003-task-ui)
- N/A (frontend only; uses existing API client to communicate with backend) (003-task-ui)

## Recent Changes
- 001-project-setup: Added Python 3.13+ (backend), TypeScript strict mode (frontend) + FastAPI, uvicorn, SQLModel, python-jose, python-dotenv, psycopg2-binary (backend); Next.js 16+, CSS Modules (frontend)
