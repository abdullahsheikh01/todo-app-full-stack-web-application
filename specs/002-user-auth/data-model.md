# Data Model: User Authentication

**Feature**: 002-user-auth
**Date**: 2026-04-02

## Entities

### User (Managed by Better Auth)

Better Auth automatically creates and manages the user table. The backend does not directly interact with this table but references user IDs in JWT tokens.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address |
| email_verified | BOOLEAN | DEFAULT FALSE | Email verification status |
| name | VARCHAR(255) | NULLABLE | User's display name |
| image | TEXT | NULLABLE | Profile image URL |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

### Session (Managed by Better Auth)

Better Auth manages sessions for token refresh and revocation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Session identifier |
| user_id | UUID | FK → user.id, NOT NULL | Owner of session |
| token | TEXT | UNIQUE, NOT NULL | Session token (hashed) |
| expires_at | TIMESTAMP | NOT NULL | Session expiration |
| ip_address | VARCHAR(45) | NULLABLE | Client IP |
| user_agent | TEXT | NULLABLE | Client user agent |
| created_at | TIMESTAMP | DEFAULT NOW() | Session creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last activity time |

### Account (Managed by Better Auth)

Links users to authentication providers (email/password or OAuth).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Account identifier |
| user_id | UUID | FK → user.id, NOT NULL | Associated user |
| account_id | VARCHAR(255) | NOT NULL | Provider's user ID |
| provider_id | VARCHAR(255) | NOT NULL | Provider name (e.g., "credential") |
| access_token | TEXT | NULLABLE | OAuth access token |
| refresh_token | TEXT | NULLABLE | OAuth refresh token |
| access_token_expires_at | TIMESTAMP | NULLABLE | Token expiration |
| password | TEXT | NULLABLE | Hashed password (for credential provider) |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update time |

**Composite Unique**: (provider_id, account_id)

### Task (Existing - Backend Managed)

Updated to enforce user ownership.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Task identifier |
| user_id | UUID | NOT NULL, INDEX | Task owner (from JWT sub claim) |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Task details |
| completed | BOOLEAN | DEFAULT FALSE, INDEX | Completion status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last modification |

**Note**: No foreign key constraint to user table since auth is managed separately. The user_id is validated via JWT.

---

## Entity Relationships

```
┌─────────────────┐         ┌─────────────────┐
│      User       │ 1    N  │     Session     │
│  (Better Auth)  │─────────│  (Better Auth)  │
└────────┬────────┘         └─────────────────┘
         │
         │ 1
         │
         │ N
┌────────┴────────┐         ┌─────────────────┐
│     Account     │         │      Task       │
│  (Better Auth)  │         │    (Backend)    │
└─────────────────┘         └─────────────────┘
                                    │
                                    │ user_id (logical ref)
                                    ▼
                            User.id from JWT
```

---

## Validation Rules

### User (Better Auth enforces)

- **email**: Valid email format, unique across all users
- **password**: Minimum 8 characters (configurable in Better Auth)

### Task (Backend enforces)

- **user_id**: Must match authenticated user's ID from JWT `sub` claim
- **title**: Required, 1-255 characters
- **description**: Optional, max 10,000 characters

---

## State Transitions

### User Authentication States

```
┌──────────┐    signup    ┌──────────────┐
│  Guest   │─────────────▶│ Authenticated│
└──────────┘              └──────┬───────┘
      ▲                          │
      │         signout          │
      └──────────────────────────┘

┌──────────────┐   token expired   ┌──────────┐
│ Authenticated│──────────────────▶│  Guest   │
└──────────────┘                   └──────────┘
```

### Session Lifecycle

```
signin
   │
   ▼
┌──────────┐
│  Active  │
└────┬─────┘
     │
     ├──── signout ────▶ Invalidated
     │
     └──── expiration ─▶ Expired
```

---

## Indexes

### User Table (Better Auth)

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| user_pkey | id | PRIMARY | Unique identifier |
| user_email_idx | email | UNIQUE | Login lookup |

### Session Table (Better Auth)

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| session_pkey | id | PRIMARY | Unique identifier |
| session_token_idx | token | UNIQUE | Token validation |
| session_user_id_idx | user_id | BTREE | User's sessions lookup |

### Task Table (Backend)

| Index | Columns | Type | Purpose |
|-------|---------|------|---------|
| task_pkey | id | PRIMARY | Unique identifier |
| task_user_id_idx | user_id | BTREE | User's tasks query |
| task_completed_idx | completed | BTREE | Filter by status |

---

## Database Migration Notes

### Better Auth Tables

Better Auth generates migrations automatically via CLI:

```bash
npx @better-auth/cli generate
```

This creates the user, session, account, and verification tables.

### Backend Task Table Update

Add user_id column to existing tasks table:

```sql
-- Migration: Add user_id to tasks
ALTER TABLE tasks ADD COLUMN user_id UUID NOT NULL;
CREATE INDEX idx_tasks_user_id ON tasks(user_id);

-- Note: Existing tasks without user_id will fail this migration
-- For fresh deployments, this is not an issue
```
