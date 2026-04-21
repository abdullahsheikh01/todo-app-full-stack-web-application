# Todo App

A modern, full-stack task management application built with Next.js 16, FastAPI, and PostgreSQL. Features secure user authentication, protected routes, and a clean responsive UI.

![Next.js](https://img.shields.io/badge/Next.js-16+-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?style=flat-square&logo=postgresql)
![TypeScript](https://img.shields.io/badge/TypeScript-Strict-3178C6?style=flat-square&logo=typescript)
![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python)

## Features

- **User Authentication** - Secure signup/signin with Better Auth
- **Protected Routes** - JWT-based route protection with session validation
- **Task Management** - Full CRUD operations for personal tasks
- **Authorization** - Users can only access their own data
- **Responsive Design** - Clean UI with CSS Modules and dark mode support
- **Type Safety** - TypeScript (frontend) + Python type hints (backend)

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 16, TypeScript, CSS Modules |
| **Backend** | FastAPI, SQLModel, PyJWT |
| **Database** | Neon Serverless PostgreSQL |
| **Auth** | Better Auth (frontend), JWKS validation (backend) |

## Project Structure

```
todo-app/
├── backend/                 # FastAPI server
│   ├── main.py              # API endpoints with auth
│   ├── security.py          # JWT validation (JWKS)
│   ├── models.py            # SQLModel entities
│   └── db.py                # Database connection
├── frontend/                # Next.js application
│   ├── app/
│   │   ├── (protected)/     # Auth-required routes
│   │   │   └── dashboard/   # User dashboard
│   │   ├── signin/          # Sign in page
│   │   ├── signup/          # Sign up page
│   │   └── api/auth/        # Better Auth endpoints
│   ├── components/          # React components
│   ├── lib/
│   │   ├── auth.ts          # Better Auth server config
│   │   ├── auth-client.ts   # Better Auth client
│   │   └── api.ts           # API client
│   └── proxy.ts             # Route protection middleware
├── specs/                   # Feature specifications
└── docker-compose.yml       # Container orchestration
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.12+
- [UV](https://github.com/astral-sh/uv) package manager
- [Neon](https://neon.tech) PostgreSQL database

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/todo-app-full-stack-web-application.git
cd todo-app-full-stack-web-application
```

### 2. Backend Setup

```bash
cd backend

# Create environment file
cp .env.example .env

# Edit .env with your credentials:
# DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
# BETTER_AUTH_URL=http://localhost:3000

# Install dependencies
uv sync

# Start the server
uv run uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Create environment file
cp .env.example .env.local

# Edit .env.local with your credentials:
# DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
# BETTER_AUTH_SECRET=your-32-char-secret
# BETTER_AUTH_URL=http://localhost:3000
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# Install dependencies
npm install

# Generate auth database tables
npx @better-auth/cli migrate

# Start the dev server
npm run dev
```

### 4. Verify Setup

- **Backend**: http://localhost:8000/health
- **Frontend**: http://localhost:3000

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with DB status |

### Protected (requires JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List user's tasks |
| POST | `/api/{user_id}/tasks` | Create a task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Authentication Flow

```
┌─────────────┐     signup/signin     ┌─────────────┐
│   Browser   │ ──────────────────►   │ Better Auth │
└─────────────┘                       └──────┬──────┘
       │                                     │
       │  JWT in HttpOnly cookie             │ Creates user
       │ ◄───────────────────────────────────┘
       │
       │  API request + JWT
       ▼
┌─────────────┐     validate JWT      ┌─────────────┐
│   FastAPI   │ ◄────────────────────►│    JWKS     │
└─────────────┘                       └─────────────┘
```

## Environment Variables

### Backend (`backend/.env`)

```bash
DATABASE_URL=postgresql://...      # Neon connection string
BETTER_AUTH_URL=http://localhost:3000  # Frontend URL for JWKS
```

### Frontend (`frontend/.env.local`)

```bash
DATABASE_URL=postgresql://...      # Same Neon connection
BETTER_AUTH_SECRET=...             # 32+ char secret
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

## Docker

Run the full stack with Docker:

```bash
docker-compose up --build
```

## Development Workflow

This project uses **Spec-Driven Development** with SpecKit Plus:

1. `/sp.specify` - Define feature requirements
2. `/sp.plan` - Create implementation plan
3. `/sp.tasks` - Generate actionable tasks
4. `/sp.implement` - Execute implementation

See `specs/` directory for feature documentation.

## Project Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| **I** | Console App (Python) | - |
| **II** | Full-Stack Web App | Current |
| **III** | AI Chatbot (OpenAI Agents) | Planned |
| **IV** | Local Kubernetes | Planned |
| **V** | Cloud Deployment (DOKS) | Planned |

## License

MIT

---

Built with [Claude Code](https://claude.ai/code)
