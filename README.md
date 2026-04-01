# Todo App - Phase II

A full-stack web application with Next.js frontend and FastAPI backend, connected to Neon PostgreSQL.

## Project Structure

```
todo-app/
├── backend/              # FastAPI server (Python 3.13+)
│   ├── main.py           # Application entry point
│   ├── db.py             # Database connection
│   ├── models.py         # SQLModel entities
│   └── Dockerfile        # Container configuration
├── frontend/             # Next.js application (TypeScript)
│   ├── app/              # App Router pages
│   ├── lib/api.ts        # API client utility
│   └── Dockerfile        # Container configuration
├── specs/                # Feature specifications
├── docker-compose.yml    # Full stack orchestration
└── README.md
```

## Prerequisites

- Node.js 18+
- Python 3.12+
- UV package manager (`pip install uv`)
- Docker and Docker Compose (optional)
- Neon PostgreSQL database with connection string

## Quick Start

### 1. Clone and Navigate

```bash
cd todo-app-full-stack-web-application
```

### 2. Backend Setup

```bash
cd backend

# Create environment file
cp .env.example .env

# Edit .env and add your Neon DATABASE_URL
# DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Install dependencies
uv sync

# Start the backend server
uv run uvicorn main:app --reload --port 8000
```

### 3. Verify Backend

```bash
curl http://localhost:8000/health

# Expected response:
# {"status": "ok", "database": "connected"}
```

### 4. Frontend Setup

```bash
cd frontend

# Create environment file
cp .env.example .env.local

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 5. Verify Frontend

Open http://localhost:3000 in your browser.

Expected: Landing page displaying "Todo App - Phase II"

### 6. Docker (Optional)

Run both services together:

```bash
# From repo root
docker-compose up

# Or rebuild and run
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check with database status |

## Environment Variables

### Backend (`backend/.env`)

```bash
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

### Frontend (`frontend/.env.local`)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Verification Checklist

- [ ] Backend starts on port 8000
- [ ] GET /health returns `{"status": "ok", "database": "connected"}`
- [ ] Frontend starts on port 3000
- [ ] Landing page shows "Todo App - Phase II"
- [ ] No hardcoded secrets in any files
- [ ] docker-compose up runs both services (optional)

## Troubleshooting

### Database Connection Failed

```
{"status": "ok", "database": "error: connection failed"}
```

**Solution**: Verify your DATABASE_URL in backend/.env:
- Check credentials are correct
- Ensure `?sslmode=require` is appended for Neon
- Verify your IP is allowed in Neon dashboard

### Port Already in Use

```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution**: Kill the process using the port:
```bash
lsof -i :3000
kill -9 <PID>
```

### UV Not Found

**Solution**: Install UV package manager:
```bash
pip install uv
```

## Development

This project follows Spec-Driven Development. See `specs/` for feature specifications.

### Workflow

1. `/sp.specify` - Create feature specification
2. `/sp.plan` - Generate implementation plan
3. `/sp.tasks` - Break into actionable tasks
4. `/sp.implement` - Execute tasks
