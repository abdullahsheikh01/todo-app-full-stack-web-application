# Implementation Plan: User Authentication

**Branch**: `002-user-auth` | **Date**: 2026-04-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-user-auth/spec.md`

## Summary

Implement user authentication for Phase II Todo App using Better Auth on the Next.js frontend for signup/signin flows, with JWT token validation on the FastAPI backend. Better Auth uses EdDSA (Ed25519) for token signing, requiring JWKS-based validation on the backend. All task API endpoints will be protected, ensuring users can only access their own data.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript strict mode (frontend)
**Primary Dependencies**: FastAPI, PyJWT, httpx, cachetools (backend); Better Auth, Next.js 16+ (frontend)
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Web (Linux server deployment)
**Project Type**: Web application (frontend + backend monorepo)
**Performance Goals**: API response < 500ms, auth flows < 60s signup / < 30s signin
**Constraints**: Stateless backend, JWT-based auth (no server sessions)
**Scale/Scope**: Multi-user with complete data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Feature originated from `/sp.specify` |
| II. Monorepo Architecture | PASS | Frontend/backend separation maintained |
| III. Stateless Backend Design | PASS | JWT tokens, no server-side sessions |
| IV. User Data Isolation | PASS | Authorization enforces user_id match |
| V. Type Safety | PASS | TypeScript strict, Python type hints |
| VI. RESTful API Standards | PASS | Proper HTTP methods and status codes |
| VII. Test-Driven Development | PASS | Tests planned for auth flows |
| VIII. Smallest Viable Diff | PASS | Focused on auth only, no extras |

**Gate Result**: PASS - All constitution principles satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/002-user-auth/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Technology research and decisions
├── data-model.md        # Entity definitions and schemas
├── quickstart.md        # Developer setup guide
├── contracts/
│   └── auth-api.yaml    # OpenAPI specification
└── checklists/
    └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
backend/
├── security.py          # NEW: JWT validation, auth dependency
├── main.py              # UPDATE: Add auth dependency to routes
├── models.py            # UPDATE: Add user_id to Task model
└── tests/
    └── test_auth.py     # NEW: Auth middleware tests

frontend/
├── lib/
│   ├── auth.ts          # NEW: Better Auth server config
│   └── auth-client.ts   # NEW: Better Auth client
├── app/
│   ├── api/auth/[...all]/
│   │   └── route.ts     # NEW: Auth API handler
│   ├── signup/
│   │   └── page.tsx     # NEW: Signup page
│   ├── signin/
│   │   └── page.tsx     # NEW: Signin page
│   └── (protected)/     # Protected route group
│       └── layout.tsx   # NEW: Auth check wrapper
├── components/
│   └── SignOutButton.tsx # NEW: Sign out component
└── proxy.ts             # NEW: Route protection middleware
```

**Structure Decision**: Web application structure with frontend (Next.js) and backend (FastAPI) in monorepo. Auth logic split between frontend (user management via Better Auth) and backend (token validation via JWKS).

## Key Design Decisions

### 1. JWT Algorithm: EdDSA (Ed25519)

Better Auth uses EdDSA by default (not configurable to HS256 per GitHub Issue #7245). Backend must validate tokens using public keys from JWKS endpoint.

**Impact**: Cannot use shared secret validation; must fetch and cache public keys.

### 2. Token Storage: HttpOnly Cookies

Better Auth stores tokens in HttpOnly cookies for XSS protection. Frontend automatically includes cookies in requests.

**Impact**: May need CORS credentials configuration for cross-origin API calls.

### 3. User Management: Frontend Only

Better Auth manages user table, sessions, and accounts. Backend only validates JWT `sub` claim for user_id.

**Impact**: Backend has no direct user table access; authorization based solely on JWT payload.

### 4. Route Protection: Two-Layer Approach

1. **Proxy (fast)**: Cookie existence check for quick redirects
2. **Page (secure)**: Database session validation for security

**Impact**: Balance between UX (fast redirects) and security (validated access).

## Implementation Phases

### Phase 1: Backend JWT Validation

1. Create `security.py` with JWKS fetching and caching
2. Implement `get_current_user` dependency for token validation
3. Add auth dependency to all `/api/{user_id}/*` routes
4. Return 401 for invalid/expired tokens, 403 for user_id mismatch
5. Update Task model to include user_id field
6. Write tests for auth middleware

### Phase 2: Frontend Better Auth Setup

1. Install and configure Better Auth with PostgreSQL
2. Create auth.ts server configuration
3. Create auth-client.ts for React hooks
4. Set up API route handler at `/api/auth/[...all]`
5. Generate database schema with Better Auth CLI

### Phase 3: Auth UI Pages

1. Create signup page with form validation
2. Create signin page with error handling
3. Implement sign out button component
4. Add auth state context/provider

### Phase 4: Route Protection

1. Create proxy.ts for middleware-level redirects
2. Implement protected route layout
3. Add callback URL preservation for post-login redirect
4. Test protected route access

### Phase 5: Integration Testing

1. End-to-end signup flow
2. End-to-end signin flow
3. Token expiration handling
4. Cross-user access prevention (403 tests)
5. Session persistence across page refresh

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| better-auth | latest | Frontend auth framework |
| pg | latest | PostgreSQL driver for Better Auth |
| PyJWT[crypto] | latest | JWT decoding with Ed25519 support |
| httpx | latest | Async HTTP client for JWKS fetch |
| cachetools | latest | TTL cache for JWKS keys |

## Environment Variables

| Variable | Required By | Purpose |
|----------|-------------|---------|
| `DATABASE_URL` | Frontend + Backend | Neon PostgreSQL connection |
| `BETTER_AUTH_SECRET` | Frontend | Encryption key for Better Auth |
| `BETTER_AUTH_URL` | Frontend + Backend | Base URL for auth endpoints |
| `NEXT_PUBLIC_API_URL` | Frontend | FastAPI backend URL |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| JWKS endpoint unavailable | Low | High | Cache keys with TTL, retry on failure |
| Token expiration during use | Medium | Low | Frontend detects 401, redirects to signin |
| EdDSA library compatibility | Low | Medium | PyJWT with cryptography backend confirmed |
| CORS issues with cookies | Medium | Medium | Configure credentials and allowed origins |

## Complexity Tracking

No constitution violations requiring justification. Design follows all principles.

## Related Artifacts

- **Research**: [research.md](./research.md) - Technology decisions and alternatives
- **Data Model**: [data-model.md](./data-model.md) - Entity schemas
- **API Contract**: [contracts/auth-api.yaml](./contracts/auth-api.yaml) - OpenAPI spec
- **Quickstart**: [quickstart.md](./quickstart.md) - Developer setup guide
