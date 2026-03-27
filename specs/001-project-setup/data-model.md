# Data Model: Project Setup

**Feature**: 001-project-setup
**Date**: 2026-03-24
**Status**: Complete

## Entities

### Task

The Task entity represents a todo item belonging to a user. This model is defined in the setup phase to establish the database schema foundation for all subsequent features.

**Purpose**: Store user-specific todo items with completion tracking

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Auto-generated | Unique identifier for the task |
| user_id | UUID | Foreign Key → users.id, Indexed, Required | Owner of the task |
| title | String | Required, Max 255 chars | Task title/summary |
| description | String | Optional, Max 2000 chars | Detailed task description |
| completed | Boolean | Default: false, Indexed | Completion status |
| created_at | DateTime | Auto-set on create | Timestamp of creation |
| updated_at | DateTime | Auto-set on update | Timestamp of last modification |

**Relationships**:
- Belongs to User (many-to-one via user_id FK)

**Indexes**:
- Primary: id
- Foreign Key: user_id (for user isolation queries)
- Status: completed (for filtered list views)

**Validation Rules**:
- title: Non-empty, trimmed whitespace, max 255 characters
- description: Optional, max 2000 characters if provided
- user_id: Must reference valid user (enforced by FK constraint)

**State Transitions**:
```
[Created] → completed=false
    ↓
[Toggle Complete] → completed=true
    ↓
[Toggle Complete] → completed=false
    ↓
[Deleted] → removed from database
```

---

## Database Schema (SQL Reference)

```sql
-- Note: Actual implementation uses SQLModel, this is reference only

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

---

## SQLModel Implementation Reference

```python
# Reference for implementation - actual code goes in backend/models.py
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Notes

- The User entity is not created in this setup phase; it will be added in the authentication feature
- The user_id foreign key references a users table that will be created later
- For setup phase, the Task model is defined but the FK constraint may be deferred until User model exists
- All timestamps use UTC timezone for consistency
