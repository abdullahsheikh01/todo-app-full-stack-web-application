# Quickstart: User Authentication

**Feature**: 002-user-auth
**Prerequisites**: Node.js 18+, Python 3.13+, Neon PostgreSQL database

## 1. Environment Setup

### Frontend (.env.local)

```bash
# Create frontend/.env.local
DATABASE_URL=postgresql://user:password@host:5432/dbname  # Neon connection
BETTER_AUTH_SECRET=your-32-character-secret-key-here       # Generate: openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)

```bash
# Create backend/.env
DATABASE_URL=postgresql://user:password@host:5432/dbname  # Same Neon connection
BETTER_AUTH_URL=http://localhost:3000                     # For JWKS endpoint
```

## 2. Install Dependencies

### Frontend

```bash
cd frontend
npm install better-auth pg
```

### Backend

```bash
cd backend
uv add PyJWT[crypto] httpx cachetools
```

## 3. Configure Better Auth (Frontend)

### Create `lib/auth.ts`

```typescript
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

### Create `lib/auth-client.ts`

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### Create `app/api/auth/[...all]/route.ts`

```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

## 4. Generate Database Schema

```bash
cd frontend
npx @better-auth/cli generate
```

This creates the `user`, `session`, `account`, and `verification` tables.

## 5. Configure JWT Validation (Backend)

### Create `backend/security.py`

```python
import os
import jwt
import httpx
from cachetools import TTLCache
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
security = HTTPBearer()
jwks_cache = TTLCache(maxsize=1, ttl=3600)

async def get_jwks() -> dict:
    """Fetch and cache JWKS from Better Auth."""
    if "jwks" not in jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BETTER_AUTH_URL}/api/auth/jwks")
            response.raise_for_status()
            jwks_cache["jwks"] = response.json()
    return jwks_cache["jwks"]

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Validate JWT and return user_id."""
    token = credentials.credentials

    try:
        # Get JWKS and find matching key
        jwks = await get_jwks()
        header = jwt.get_unverified_header(token)

        key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
        if not key:
            jwks_cache.clear()
            jwks = await get_jwks()
            key = next((k for k in jwks["keys"] if k["kid"] == header.get("kid")), None)
            if not key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )

        # Verify token
        public_key = jwt.algorithms.OKPAlgorithm.from_jwk(key)
        payload = jwt.decode(token, public_key, algorithms=["EdDSA"])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
```

## 6. Protect API Routes (Backend)

### Update `backend/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, status
from uuid import UUID
from security import get_current_user

app = FastAPI()

@app.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: UUID,
    current_user: str = Depends(get_current_user)
):
    # Authorization: ensure token user matches URL user
    if current_user != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )

    # Fetch and return tasks
    return {"tasks": []}
```

## 7. Create Auth Pages (Frontend)

### Signup Page (`app/signup/page.tsx`)

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth-client";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    const { error } = await signUp.email({ email, password, name: email });
    if (error) {
      setError(error.message || "Signup failed");
    } else {
      router.push("/");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
      {error && <p>{error}</p>}
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

### Signin Page (`app/signin/page.tsx`)

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth-client";

export default function SigninPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const { error } = await signIn.email({ email, password });
    if (error) {
      setError("Invalid credentials");
    } else {
      router.push("/");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      {error && <p>{error}</p>}
      <button type="submit">Sign In</button>
    </form>
  );
}
```

## 8. Route Protection (Frontend)

### Create `proxy.ts` (Next.js 16 middleware)

```typescript
import { getSessionCookie } from "better-auth/cookies";
import { NextRequest, NextResponse } from "next/server";

export async function proxy(request: NextRequest) {
  const sessionCookie = getSessionCookie(request);
  const isAuthPage = request.nextUrl.pathname.startsWith("/signin") ||
                     request.nextUrl.pathname.startsWith("/signup");

  // Redirect unauthenticated users to signin
  if (!sessionCookie && !isAuthPage && request.nextUrl.pathname !== "/") {
    const signinUrl = new URL("/signin", request.url);
    signinUrl.searchParams.set("callbackUrl", request.nextUrl.pathname);
    return NextResponse.redirect(signinUrl);
  }

  // Redirect authenticated users away from auth pages
  if (sessionCookie && isAuthPage) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

## 9. Verify Setup

### Start Services

```bash
# Terminal 1: Frontend
cd frontend && npm run dev

# Terminal 2: Backend
cd backend && uv run uvicorn main:app --reload --port 8000
```

### Test Flow

1. Navigate to http://localhost:3000/signup
2. Create a new account
3. Verify redirect to main application
4. Sign out and verify redirect to /signin
5. Sign in and verify access to protected routes
6. Test API authorization by accessing /api/{user_id}/tasks

## Common Issues

| Issue | Solution |
|-------|----------|
| JWKS fetch fails | Ensure `BETTER_AUTH_URL` is correct and frontend is running |
| Token validation fails | Check that EdDSA algorithm is used (not HS256) |
| 403 on API calls | Verify user_id in URL matches authenticated user |
| Session not persisting | Check cookie settings and CORS configuration |
