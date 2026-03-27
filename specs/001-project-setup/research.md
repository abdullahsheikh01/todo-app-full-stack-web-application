# Research: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-03-24
**Status**: Complete

## Research Questions

This section documents decisions made for technology choices and patterns.

---

### R1: FastAPI Project Structure with UV

**Decision**: Use UV as package manager with pyproject.toml for dependency management

**Rationale**:
- UV is the constitution-mandated package manager for backend
- pyproject.toml is the modern Python standard (PEP 517/518)
- UV provides fast, reliable dependency resolution
- Compatible with existing Python tooling

**Alternatives Considered**:
- pip + requirements.txt: Legacy approach, slower, less reproducible
- Poetry: Good but UV is constitution-specified
- Pipenv: Slower than UV, less modern

---

### R2: SQLModel for Database Operations

**Decision**: Use SQLModel for ORM with Neon PostgreSQL

**Rationale**:
- SQLModel is constitution-mandated (combines SQLAlchemy + Pydantic)
- Native type hints support (Principle V: Type Safety)
- Automatic Pydantic model generation for API responses
- Works seamlessly with FastAPI
- Supports async operations for future scalability

**Alternatives Considered**:
- Raw SQLAlchemy: More verbose, requires separate Pydantic models
- Tortoise ORM: Less mature, different paradigm
- Prisma Python: Not as integrated with FastAPI ecosystem

---

### R3: Neon PostgreSQL Connection Pooling

**Decision**: Use Neon's built-in connection pooling with psycopg2-binary

**Rationale**:
- Neon serverless requires connection pooling for efficiency
- psycopg2-binary is well-tested with SQLModel
- Neon provides pooled connection strings automatically
- Supports the stateless backend design (Principle III)

**Alternatives Considered**:
- asyncpg: Better async performance but requires different SQLModel setup
- psycopg3: Newer but less ecosystem support currently
- SQLAlchemy async: More complex configuration for setup phase

---

### R4: Next.js 16+ App Router Structure

**Decision**: Use Next.js App Router with server components by default

**Rationale**:
- Constitution specifies Next.js 16+ with App Router
- Server components provide better initial load performance
- CSS Modules are built-in (no additional dependencies)
- TypeScript strict mode is easily configurable

**Alternatives Considered**:
- Pages Router: Legacy approach in Next.js
- Remix: Different framework, not constitution-specified
- Astro: Not suited for interactive applications

---

### R5: CSS Modules for Styling

**Decision**: Use CSS Modules (built-in to Next.js) for component styling

**Rationale**:
- Constitution v1.1.0 specifies CSS Modules over Tailwind CSS
- Built-in to Next.js, no additional dependencies
- Provides scoped styling without naming conflicts
- Standard CSS syntax, familiar to most developers

**Alternatives Considered**:
- Tailwind CSS: Previously considered, removed in constitution amendment
- Styled Components: Requires additional dependency
- Emotion: CSS-in-JS overhead for simple setup

---

### R6: Docker Compose Configuration

**Decision**: Use Docker Compose v2 syntax with separate Dockerfiles per service

**Rationale**:
- Enables running full stack with single command
- Each service has its own optimized Dockerfile
- Supports environment variable injection
- Prepares for Phase IV Kubernetes deployment

**Alternatives Considered**:
- Single multi-stage Dockerfile: Less flexible for independent deployment
- Docker Swarm: Overkill for development environment
- Podman Compose: Less ecosystem support

---

### R7: Health Check Endpoint Design

**Decision**: GET /health returns JSON with server and database status

**Rationale**:
- Standard pattern for containerized applications
- Supports Kubernetes liveness/readiness probes (Phase IV)
- Database connectivity check confirms end-to-end setup
- Simple JSON response format per REST standards (Principle VI)

**Response Format**:
```json
{
  "status": "ok",
  "database": "connected"
}
```

**Error Format**:
```json
{
  "status": "ok",
  "database": "error: connection failed"
}
```

**Alternatives Considered**:
- Separate /health and /ready endpoints: Overkill for Phase II
- HTML health page: Not RESTful
- No health endpoint: Harder to verify setup

---

### R8: API Client Design (Frontend)

**Decision**: Create a typed API client in /lib/api.ts with fetch wrapper

**Rationale**:
- Centralizes backend communication
- Uses environment variable for base URL (FR-011)
- TypeScript types ensure type safety across frontend
- Simple fetch-based approach, no additional dependencies

**Alternatives Considered**:
- Axios: Additional dependency not needed for simple use case
- React Query: Too complex for setup phase
- SWR: Good but introduces caching complexity early

---

## Summary

All research questions resolved with decisions aligned to constitution principles:

| Question | Decision | Constitution Alignment |
|----------|----------|----------------------|
| R1 | UV + pyproject.toml | Technology Stack (Backend) |
| R2 | SQLModel ORM | Technology Stack, Principle V |
| R3 | Neon pooled connections | Principle III |
| R4 | Next.js App Router | Technology Stack (Frontend) |
| R5 | CSS Modules | Technology Stack v1.1.0 |
| R6 | Docker Compose v2 | Infrastructure |
| R7 | JSON health endpoint | Principle VI |
| R8 | Typed fetch client | Principle V |

**No NEEDS CLARIFICATION items remaining.**
