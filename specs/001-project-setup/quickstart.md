# Quickstart: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-03-27

## Prerequisites

Before starting, ensure you have:

- [ ] Node.js 18+ installed
- [ ] Python 3.13+ installed
- [ ] UV package manager installed (`pip install uv`)
- [ ] Docker and Docker Compose installed
- [ ] Access to a Neon PostgreSQL database with connection string

## Setup Steps

### 1. Clone and Navigate

```bash
cd todo-app-full-stack-web-application
```

### 2. Backend Setup

```bash
# Navigate to backend
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
# In a new terminal
curl http://localhost:8000/health

# Expected response:
# {"status": "ok", "database": "connected"}
```

### 4. Frontend Setup

```bash
# Navigate to frontend (from repo root)
cd frontend

# Create environment file
cp .env.example .env.local

# Edit .env.local if needed (defaults should work for local dev)
# NEXT_PUBLIC_API_URL=http://localhost:8000

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
# Find process
lsof -i :3000
# Kill it
kill -9 <PID>
```

### UV Not Found

**Solution**: Install UV package manager:
```bash
pip install uv
```

### Module Not Found (Backend)

**Solution**: Ensure dependencies are installed:
```bash
cd backend
uv sync
```
