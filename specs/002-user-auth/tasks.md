# Tasks: User Authentication

**Input**: Design documents from `/specs/002-user-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/auth-api.yaml

**Tests**: Not explicitly requested in feature specification. Test tasks omitted.

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/` (FastAPI)
- **Frontend**: `frontend/` (Next.js)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure environment for auth feature

- [X] T001 Install backend auth dependencies: `cd backend && uv add PyJWT[crypto] httpx cachetools`
- [X] T002 [P] Install frontend auth dependencies: `cd frontend && npm install better-auth pg`
- [X] T003 [P] Add environment variables to backend/.env.example (BETTER_AUTH_URL)
- [X] T004 [P] Add environment variables to frontend/.env.local.example (DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, NEXT_PUBLIC_API_URL)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create Better Auth server configuration in frontend/lib/auth.ts
- [X] T006 Create Better Auth client configuration in frontend/lib/auth-client.ts
- [X] T007 Create auth API route handler in frontend/app/api/auth/[...all]/route.ts
- [X] T008 Generate Better Auth database schema: `cd frontend && npx @better-auth/cli migrate`
- [X] T009 Create JWT validation module with JWKS fetching in backend/security.py
- [X] T010 Update Task model to include user_id field in backend/models.py (pre-existing)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: New users can create accounts at /signup with email and password

**Independent Test**: Navigate to /signup, enter valid credentials (email, password, confirm password), verify account creation and redirect to main application

### Implementation for User Story 1

- [X] T011 [US1] Create signup page with form fields (name, email, password, confirm password) in frontend/app/signup/page.tsx
- [X] T012 [US1] Add client-side validation: email format, password min 8 chars, password match in frontend/app/signup/page.tsx
- [X] T013 [US1] Integrate Better Auth signUp.email() call on form submit in frontend/app/signup/page.tsx
- [X] T014 [US1] Add error handling for duplicate email (409) and display error message in frontend/app/signup/page.tsx
- [X] T015 [US1] Add success redirect to /dashboard after signup in frontend/app/signup/page.tsx
- [X] T016 [US1] Style signup page using CSS Modules in frontend/app/signup/page.module.css

**Checkpoint**: User Story 1 complete - users can register new accounts

---

## Phase 4: User Story 2 - Existing User Sign In (Priority: P1) 🎯 MVP

**Goal**: Registered users can sign in at /signin with email and password

**Independent Test**: Navigate to /signin with pre-existing account, enter valid credentials, verify authentication and redirect to main application

### Implementation for User Story 2

- [X] T017 [US2] Create signin page with form fields (email, password) in frontend/app/signin/page.tsx
- [X] T018 [US2] Add client-side validation: email format required in frontend/app/signin/page.tsx
- [X] T019 [US2] Integrate Better Auth signIn.email() call on form submit in frontend/app/signin/page.tsx
- [X] T020 [US2] Add generic error handling for invalid credentials (401) - do not reveal which field is wrong in frontend/app/signin/page.tsx
- [X] T021 [US2] Add success redirect to /dashboard (or callback URL) after signin in frontend/app/signin/page.tsx
- [X] T022 [US2] Style signin page using CSS Modules in frontend/app/signin/page.module.css
- [X] T023 [P] [US2] Add link to signup page for new users in frontend/app/signin/page.tsx
- [X] T024 [P] [US1] Add link to signin page for existing users in frontend/app/signup/page.tsx

**Checkpoint**: User Stories 1 & 2 complete - users can register and sign in (MVP achieved)

---

## Phase 5: User Story 3 - Sign Out (Priority: P2)

**Goal**: Authenticated users can sign out from anywhere in the application

**Independent Test**: Sign in, click sign out button, verify session cleared and redirect to /signin

### Implementation for User Story 3

- [X] T025 [US3] Create SignOutButton component with signOut() integration in frontend/components/SignOutButton.tsx
- [X] T026 [US3] Add redirect to /signin after successful sign out in frontend/components/SignOutButton.tsx
- [X] T027 [US3] Style SignOutButton using CSS Modules in frontend/components/SignOutButton.module.css
- [X] T028 [US3] Add SignOutButton to dashboard page (visible when authenticated) in frontend/app/(protected)/dashboard/page.tsx

**Checkpoint**: User Story 3 complete - users can sign out

---

## Phase 6: User Story 4 - Protected Routes (Priority: P2)

**Goal**: Unauthenticated users are redirected to /signin when accessing protected routes

**Independent Test**: Clear auth state, navigate directly to protected route (e.g., /), verify redirect to /signin with callback URL preserved

### Implementation for User Story 4

- [X] T029 [US4] Create proxy.ts for route protection in frontend/proxy.ts
- [X] T030 [US4] Implement cookie existence check for fast redirect in frontend/proxy.ts
- [X] T031 [US4] Configure matcher for protected routes (exclude /signin, /signup, /api/auth) in frontend/proxy.ts
- [X] T032 [US4] Add callbackUrl query parameter preservation for post-login redirect in frontend/proxy.ts
- [X] T033 [US4] Create protected route layout with server-side session validation in frontend/app/(protected)/layout.tsx
- [X] T034 [US4] Update signin page to handle callbackUrl redirect after authentication in frontend/app/signin/page.tsx
- [X] T035 [US4] Redirect authenticated users away from /signin and /signup to /dashboard in frontend/proxy.ts

**Checkpoint**: User Story 4 complete - routes are protected

---

## Phase 7: User Story 5 - Authorization Enforcement (Priority: P2)

**Goal**: Backend validates JWT and ensures users can only access their own data

**Independent Test**: Authenticate as User A, attempt to access User B's tasks via API, verify 403 Forbidden response

### Implementation for User Story 5

- [X] T036 [US5] Implement get_current_user dependency with JWKS validation in backend/security.py
- [X] T037 [US5] Add JWKS caching with TTL (1 hour) and cache invalidation on key miss in backend/security.py
- [X] T038 [US5] Implement user_id extraction from JWT 'sub' claim in backend/security.py
- [X] T039 [US5] Add 401 Unauthorized response for missing/invalid/expired tokens in backend/security.py
- [X] T040 [US5] Create authorize_user dependency to compare token user_id with URL user_id in backend/security.py
- [X] T041 [US5] Add 403 Forbidden response for user_id mismatch in backend/security.py
- [X] T042 [US5] Add auth dependency to GET /api/{user_id}/tasks endpoint in backend/main.py
- [X] T043 [US5] Add auth dependency to POST /api/{user_id}/tasks endpoint in backend/main.py
- [X] T044 [US5] Add auth dependency to GET /api/{user_id}/tasks/{task_id} endpoint in backend/main.py
- [X] T045 [US5] Add auth dependency to PUT /api/{user_id}/tasks/{task_id} endpoint in backend/main.py
- [X] T046 [US5] Add auth dependency to DELETE /api/{user_id}/tasks/{task_id} endpoint in backend/main.py
- [X] T047 [US5] Add auth dependency to PATCH /api/{user_id}/tasks/{task_id}/complete endpoint in backend/main.py
- [X] T048 [US5] Update frontend API client with credentials and 401 handling in frontend/lib/api.ts

**Checkpoint**: User Story 5 complete - backend authorization enforced

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T049 [P] Add auth state context/provider in frontend/app/providers.tsx
- [X] T050 [P] Create loading states for auth operations (signup, signin, signout) in frontend components
- [X] T051 [P] Add CORS configuration for credentials (cookies) in backend/main.py (pre-existing)
- [X] T052 Handle 401 responses in frontend API client - redirect to /signin in frontend/lib/api.ts
- [X] T053 Add user name/email display in dashboard header when authenticated in frontend/app/(protected)/dashboard/page.tsx
- [X] T054 Run quickstart.md validation - test full auth flow end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Depends on Foundational - No dependencies on other stories (can parallel with US1)
- **User Story 3 (P2)**: Depends on Foundational - Requires auth state from US1/US2 to test
- **User Story 4 (P2)**: Depends on Foundational - Requires US1/US2 for signin redirect
- **User Story 5 (P2)**: Depends on Foundational - Independent of frontend stories

### Within Each User Story

- Models/config before services
- Core implementation before styling
- Story complete before moving to next priority

### Parallel Opportunities

- T001-T004: All setup tasks can run in parallel
- T005-T010: Foundational tasks have dependencies (T005→T006→T007, T009→T010)
- US1 and US2 can run in parallel after Foundational
- US3, US4, US5 can run in parallel after US1/US2
- T023 and T024 can run in parallel (cross-linking signup/signin)
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# These must be sequential (dependencies):
T005 → T006 → T007 → T008 (Better Auth setup chain)
T009 → T010 (Backend security chain)

# But the two chains can run in parallel:
Chain 1: T005, T006, T007, T008
Chain 2: T009, T010
```

## Parallel Example: User Stories 1 & 2

```bash
# After Foundational phase, both can start simultaneously:
Developer A: T011-T016 (US1: Signup)
Developer B: T017-T022 (US2: Signin)

# Then cross-link when both complete:
T023, T024 (add navigation links)
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Signup)
4. Complete Phase 4: User Story 2 (Signin)
5. **STOP and VALIDATE**: Test signup/signin flow independently
6. Deploy/demo if ready - this is the MVP!

### Full Feature Delivery

1. Complete MVP (US1 + US2)
2. Add User Story 3 (Sign Out) → Validate
3. Add User Story 4 (Protected Routes) → Validate
4. Add User Story 5 (Authorization) → Validate
5. Complete Polish phase
6. Full feature complete

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Signup)
   - Developer B: User Story 2 (Signin)
3. After US1/US2:
   - Developer A: User Story 3 (Sign Out) + User Story 4 (Protected Routes)
   - Developer B: User Story 5 (Authorization)
4. Polish phase together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- US1 and US2 together form the MVP
- Backend (US5) can be developed independently of frontend stories
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
