import { NextRequest, NextResponse } from "next/server";

// Routes accessible without authentication
const PUBLIC_ROUTES = ["/", "/signin", "/signup"];

// Auth pages that authenticated users should be redirected away from
const AUTH_ROUTES = ["/signin", "/signup"];

// Protected routes that require authentication
const PROTECTED_ROUTES = ["/dashboard"];

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for session cookie (Better Auth sets this)
  const sessionCookie = request.cookies.get("better-auth.session_token");
  const isAuthenticated = !!sessionCookie;

  // Allow API routes and static files
  if (
    pathname.startsWith("/api") ||
    pathname.startsWith("/_next") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }

  // Redirect authenticated users away from auth pages to dashboard
  if (isAuthenticated && AUTH_ROUTES.some((route) => pathname.startsWith(route))) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Redirect unauthenticated users to signin for protected routes
  const isProtectedRoute = PROTECTED_ROUTES.some((route) => pathname.startsWith(route));
  if (!isAuthenticated && isProtectedRoute) {
    const signinUrl = new URL("/signin", request.url);
    signinUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(signinUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
