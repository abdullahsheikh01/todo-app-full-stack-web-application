"""JWT validation module for Better Auth integration.

This module provides authentication and authorization dependencies for FastAPI
routes, validating JWT tokens issued by Better Auth using JWKS.
"""

import os
from typing import Annotated

import httpx
import jwt
from cachetools import TTLCache
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")
security = HTTPBearer()

# Cache JWKS keys for 1 hour
jwks_cache: TTLCache[str, dict] = TTLCache(maxsize=1, ttl=3600)


async def get_jwks() -> dict:
    """Fetch and cache JWKS from Better Auth."""
    if "jwks" not in jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BETTER_AUTH_URL}/api/auth/jwks")
            response.raise_for_status()
            jwks_cache["jwks"] = response.json()
    return jwks_cache["jwks"]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Validate JWT and return user_id from the 'sub' claim.

    Args:
        credentials: Bearer token from Authorization header.

    Returns:
        User ID extracted from JWT 'sub' claim.

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing.
    """
    token = credentials.credentials

    try:
        # Get JWKS and find matching key
        jwks = await get_jwks()
        header = jwt.get_unverified_header(token)

        key = next(
            (k for k in jwks.get("keys", []) if k.get("kid") == header.get("kid")),
            None,
        )

        if not key:
            # Force refresh on key not found
            jwks_cache.clear()
            jwks = await get_jwks()
            key = next(
                (k for k in jwks.get("keys", []) if k.get("kid") == header.get("kid")),
                None,
            )
            if not key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        # Verify token with EdDSA public key
        public_key = jwt.algorithms.OKPAlgorithm.from_jwk(key)
        payload = jwt.decode(token, public_key, algorithms=["EdDSA"])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def authorize_user(
    user_id: Annotated[str, Path(description="User ID from URL")],
    current_user: str = Depends(get_current_user),
) -> str:
    """Verify the authenticated user matches the URL user_id.

    Args:
        user_id: User ID from the URL path.
        current_user: Authenticated user ID from JWT.

    Returns:
        The validated user_id.

    Raises:
        HTTPException: 403 if user_id doesn't match authenticated user.
    """
    if current_user != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )
    return user_id
