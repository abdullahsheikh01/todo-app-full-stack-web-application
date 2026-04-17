# Research: User Authentication

**Feature**: 002-user-auth
**Date**: 2026-04-02
**Status**: Complete

## Executive Summary

This research resolves technical decisions for implementing user authentication with Better Auth (frontend) and JWT validation (FastAPI backend). A critical finding is that Better Auth uses **EdDSA (Ed25519)** signing by default, not HS256, which impacts the backend validation approach.

---

## Research Item 1: Better Auth JWT Signing Algorithm

### Decision

Use **EdDSA (Ed25519)** for JWT signing with JWKS-based validation on the backend.

### Rationale

- Better Auth uses EdDSA by default and does not support HS256 configuration (see [GitHub Issue #7245](https://github.com/better-auth/better-auth/issues/7245))
- EdDSA is recommended by security experts as the most secure option: "EdDSA > ECDSA > RSASSA-PSS > RSASSA-PKCS1-v1_5" ([WorkOS](https://workos.com/blog/hmac-vs-rsa-vs-ecdsa-which-algorithm-should-you-use-to-sign-jwts))
- EdDSA provides faster verification and stronger security properties than HS256
- Better Auth exposes public keys via `/api/auth/jwks` endpoint for asymmetric verification

### Alternatives Considered

| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| HS256 (shared secret) | Simple, fast | Better Auth doesn't support it (Issue #7245) | Not technically feasible |
| RS256 (RSA) | Widely supported | Larger keys, slower | EdDSA is better performance/security |
| EdDSA (chosen) | Best security, fast, Better Auth default | Requires JWKS validation | N/A - selected |

### Implementation Impact

- Backend must fetch public keys from JWKS endpoint (`/api/auth/jwks`)
- `BETTER_AUTH_SECRET` is used for encryption, not JWT signing
- Use `PyJWT` with `cryptography` backend for Ed25519 support (python-jose has limited EdDSA support)

---

## Research Item 2: Backend JWT Validation Approach

### Decision

Use **JWKS-based validation** with key caching and `PyJWT` library.

### Rationale

- Asymmetric verification (public key) is more secure for distributed systems
- JWKS endpoint allows key rotation without backend changes
- PyJWT has better Ed25519/EdDSA support than python-jose
- Caching public keys reduces latency (refresh on verification failure)

### Alternatives Considered

| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| Shared secret (HS256) | Simple implementation | Not supported by Better Auth | Infeasible |
| Hardcoded public key | No network call | Cannot rotate keys | Maintenance burden |
| JWKS with caching (chosen) | Secure, supports rotation | Initial complexity | N/A - selected |

### Implementation Pattern

```python
# Install: pip install PyJWT[crypto] httpx cachetools

import jwt
import httpx
from cachetools import TTLCache

jwks_cache = TTLCache(maxsize=1, ttl=3600)  # Cache JWKS for 1 hour

async def get_jwks():
    if "jwks" not in jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BETTER_AUTH_URL}/api/auth/jwks")
            jwks_cache["jwks"] = response.json()
    return jwks_cache["jwks"]

async def verify_token(token: str) -> dict:
    jwks = await get_jwks()
    header = jwt.get_unverified_header(token)

    # Find matching key by kid
    key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
    if not key:
        jwks_cache.clear()  # Force refresh on key not found
        jwks = await get_jwks()
        key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)

    public_key = jwt.algorithms.OKPAlgorithm.from_jwk(key)
    payload = jwt.decode(token, public_key, algorithms=["EdDSA"])
    return payload
```

---

## Research Item 3: Token Storage Strategy

### Decision

Use **HttpOnly cookies** (Better Auth default) with secure flags.

### Rationale

- HttpOnly cookies are not accessible via JavaScript (XSS protection)
- Better Auth manages token storage automatically
- SameSite=Lax prevents CSRF while allowing navigation
- Tokens automatically sent with requests (no manual header attachment)

### Alternatives Considered

| Option | Pros | Cons | Rejected Because |
|--------|------|------|------------------|
| localStorage | Accessible for custom headers | XSS vulnerable | Security risk |
| sessionStorage | Per-tab isolation | XSS vulnerable, lost on close | Security risk, poor UX |
| HttpOnly cookies (chosen) | XSS protection, auto-sent | Requires cookie config | N/A - selected |

### Implementation Note

Better Auth stores tokens in HttpOnly cookies. The frontend auth client automatically handles:
- Setting cookies on signin/signup
- Clearing cookies on signout
- Refreshing tokens before expiration

For API requests to FastAPI backend, extract the token from cookies and forward via Authorization header if needed, or configure CORS to allow credentials.

---

## Research Item 4: Better Auth + Next.js 16 Integration

### Decision

Use **Better Auth with PostgreSQL adapter** and Next.js 16 proxy (middleware).

### Key Configuration Files

| File | Purpose |
|------|---------|
| `lib/auth.ts` | Better Auth server configuration |
| `lib/auth-client.ts` | Frontend auth client |
| `app/api/auth/[...all]/route.ts` | Auth API route handler |
| `proxy.ts` | Next.js 16 route protection |

### Better Auth Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL,
});
```

### JWT Token Payload Structure

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "iss": "http://localhost:3000",
  "aud": "http://localhost:3000",
  "exp": 1743667200,
  "iat": 1743667100,
  "kid": "key-id"
}
```

- `sub` (subject) contains the user ID
- `exp` is Unix timestamp for expiration
- `kid` identifies which key to use for verification

---

## Research Item 5: Route Protection Strategy

### Decision

Use **proxy-based redirect for UX** + **server-side validation for security**.

### Rationale

- Proxy (middleware) provides fast UX redirects without database calls
- Server-side validation in protected pages ensures security
- Two-layer approach balances performance and security

### Implementation

**Proxy (fast redirect):**
```typescript
// proxy.ts
import { getSessionCookie } from "better-auth/cookies";

export async function proxy(request: NextRequest) {
  const sessionCookie = getSessionCookie(request);
  if (request.nextUrl.pathname.startsWith("/app") && !sessionCookie) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }
  return NextResponse.next();
}
```

**Protected Page (secure validation):**
```typescript
// app/app/page.tsx
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function AppPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) redirect("/signin");
  return <div>Welcome, {session.user.email}</div>;
}
```

---

## Research Item 6: 401 vs 403 Error Handling

### Decision

Follow HTTP semantics: **401 for authentication failures**, **403 for authorization failures**.

### Rationale

| Status | Meaning | Use Case |
|--------|---------|----------|
| 401 Unauthorized | Authentication required/failed | Missing token, invalid token, expired token |
| 403 Forbidden | Authenticated but not authorized | User accessing another user's data |

### Implementation

```python
# 401: Authentication failed (in dependency)
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# 403: Authorization failed (in route handler)
if current_user.id != user_id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Forbidden"
    )
```

---

## Research Item 7: Database Schema

### Decision

Let **Better Auth manage user schema**, backend only reads user_id from JWT.

### Rationale

- Better Auth auto-generates user, session, account, verification tables
- Backend does not need direct user table access
- Tasks table references user_id via foreign key
- Maintains separation of concerns (auth handled by frontend stack)

### Schema Impact

```sql
-- Better Auth creates (frontend manages):
CREATE TABLE "user" (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  email_verified BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Backend manages:
CREATE TABLE tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,  -- References user.id conceptually (no FK needed if auth separate)
  title VARCHAR NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

---

## Environment Variables

| Variable | Purpose | Used By |
|----------|---------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection | Frontend (Better Auth) + Backend |
| `BETTER_AUTH_SECRET` | Encryption key for Better Auth | Frontend only |
| `BETTER_AUTH_URL` | Base URL for auth endpoints | Frontend + Backend (JWKS fetch) |
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL | Frontend |

---

## Sources

- [Better Auth Installation](https://better-auth.com/docs/installation)
- [Better Auth Next.js Integration](https://better-auth.com/docs/integrations/next)
- [Better Auth JWT Plugin](https://better-auth.com/docs/plugins/jwt)
- [GitHub Issue #7245 - Allow HS256 JWTs](https://github.com/better-auth/better-auth/issues/7245)
- [HMAC vs RSA vs ECDSA - WorkOS](https://workos.com/blog/hmac-vs-rsa-vs-ecdsa-which-algorithm-should-you-use-to-sign-jwts)
- [JWTs: Which Signing Algorithm - Scott Brady](https://www.scottbrady.io/jose/jwts-which-signing-algorithm-should-i-use)
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [PyJWT Documentation](https://pyjwt.readthedocs.io/en/latest/)
