# Implementation Plan: Task Management UI

**Branch**: `003-task-ui` | **Date**: 2026-04-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-task-ui/spec.md`

## Summary

Build frontend UI components for task management on the dashboard page. The backend API is complete and the API client (`lib/api.ts`) is ready. This feature adds 5 React components (TaskList, TaskItem, AddTaskForm, EditTaskModal, DeleteConfirmDialog), enhances the dashboard page to fetch/display tasks, and implements filtering, CRUD operations, and responsive CSS Modules styling.

## Technical Context

**Language/Version**: TypeScript (strict mode) with Next.js 16+ (App Router)
**Primary Dependencies**: React 19+, Next.js 16+, Better Auth (client)
**Storage**: N/A (frontend only; uses existing API client to communicate with backend)
**Testing**: Manual testing (no test framework specified for frontend)
**Target Platform**: Web browsers (desktop and mobile, min 320px width)
**Project Type**: Web application (monorepo: frontend + backend)
**Performance Goals**: Task list loads < 2s, interactions respond < 1s, filter updates < 500ms
**Constraints**: CSS Modules only (no Tailwind), consistent with existing auth page styling
**Scale/Scope**: Single user dashboard, no pagination required for Phase II

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | PASS | Feature has spec.md, following workflow |
| II. Monorepo Architecture | PASS | Changes confined to /frontend |
| III. Stateless Backend Design | N/A | Frontend-only changes |
| IV. User Data Isolation | PASS | API client uses user_id from session |
| V. Type Safety | PASS | TypeScript strict mode, Task interface exists |
| VI. RESTful API Standards | N/A | Using existing API client |
| VII. Test-Driven Development | PASS | Manual testing acceptable for UI |
| VIII. Smallest Viable Diff | PASS | Focused on UI components only |

**Gate Result**: PASS - No violations, proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/003-task-ui/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - frontend only)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   └── (protected)/
│       └── dashboard/
│           ├── page.tsx           # Enhanced with task fetching (exists)
│           ├── page.module.css    # Dashboard layout styles (exists)
│           └── DashboardClient.tsx # New client component for state
├── components/
│   ├── tasks/
│   │   ├── TaskList.tsx           # New: Task list with filtering
│   │   ├── TaskList.module.css    # New: TaskList styles
│   │   ├── TaskItem.tsx           # New: Single task display
│   │   ├── TaskItem.module.css    # New: TaskItem styles
│   │   ├── AddTaskForm.tsx        # New: Create task form
│   │   ├── AddTaskForm.module.css # New: AddTaskForm styles
│   │   ├── EditTaskModal.tsx      # New: Edit modal dialog
│   │   ├── EditTaskModal.module.css # New: EditTaskModal styles
│   │   ├── DeleteConfirmDialog.tsx  # New: Delete confirmation
│   │   └── DeleteConfirmDialog.module.css # New: Dialog styles
│   └── SignOutButton.tsx          # Existing
└── lib/
    ├── api.ts                     # Existing API client
    └── auth-client.ts             # Existing auth client
```

**Structure Decision**: Web application option selected. All new components placed under `frontend/components/tasks/` following the component co-location pattern. Dashboard page uses a client component wrapper for state management.

## Complexity Tracking

> No violations - table not required.

## Component Architecture

### State Flow

```
Dashboard (Server Component)
    ↓ passes session
DashboardClient (Client Component)
    ├── manages: tasks[], loading, error, filter, editingTask, deletingTask
    ├── fetches tasks on mount via api.listTasks()
    └── renders:
        ├── AddTaskForm → onSubmit → createTask() → refetch
        ├── TaskList
        │   └── TaskItem (for each task)
        │       ├── checkbox → toggleTaskComplete() → refetch
        │       ├── edit btn → setEditingTask(task)
        │       └── delete btn → setDeletingTask(task)
        ├── EditTaskModal (when editingTask) → updateTask() → refetch
        └── DeleteConfirmDialog (when deletingTask) → deleteTask() → refetch
```

### Component Props

| Component | Props |
|-----------|-------|
| DashboardClient | `session: Session` |
| TaskList | `tasks: Task[], filter: FilterType, onFilterChange, onToggle, onEdit, onDelete` |
| TaskItem | `task: Task, onToggle, onEdit, onDelete` |
| AddTaskForm | `onSubmit: (task: TaskCreate) => Promise<void>` |
| EditTaskModal | `task: Task \| null, onSave, onClose` |
| DeleteConfirmDialog | `task: Task \| null, onConfirm, onClose` |

### Filter Type

```typescript
type FilterType = 'all' | 'active' | 'completed';
```

## Styling Strategy

### CSS Variables (from existing auth pages)

```css
--background: #fafafa / #0a0a0a (dark)
--foreground: #fff / #111 (dark)
--text-primary: #000 / #ededed (dark)
--text-secondary: #666 / #999 (dark)
--accent: #0070f3 / #3291ff (dark)
--border: #ddd / #333 (dark)
--error: #e00 / #ff6b6b (dark)
```

### New Additions

```css
--success: #00a854 / #52c41a (dark)  /* For completed tasks */
--completed-text: #999 / #666 (dark)  /* Muted text for completed */
```

### Responsive Breakpoints

- Mobile: < 640px (single column, full-width inputs)
- Desktop: >= 640px (comfortable spacing)
