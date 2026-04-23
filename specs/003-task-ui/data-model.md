# Data Model: Task Management UI

**Feature**: 003-task-ui
**Date**: 2026-04-23

## Overview

This document defines the TypeScript interfaces and state structures for the Task Management UI components. Since this is a frontend feature, it references existing API types and defines new UI-specific types.

---

## Existing Types (from lib/api.ts)

These types already exist and will be imported:

```typescript
// Task entity returned from API
interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

// Payload for creating a task
interface TaskCreate {
  title: string;
  description?: string | null;
}

// Payload for updating a task
interface TaskUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}
```

---

## New Types (to be created)

### Filter Types

```typescript
// Filter options for task list
type FilterType = 'all' | 'active' | 'completed';

// Filter tab configuration
interface FilterTab {
  value: FilterType;
  label: string;
}

const FILTER_TABS: FilterTab[] = [
  { value: 'all', label: 'All' },
  { value: 'active', label: 'Active' },
  { value: 'completed', label: 'Completed' },
];
```

### Session Types

```typescript
// User session from Better Auth (simplified)
interface User {
  id: string;
  name: string | null;
  email: string;
}

interface Session {
  user: User;
}
```

---

## Component State Structures

### DashboardClient State

```typescript
interface DashboardState {
  // Task data
  tasks: Task[];

  // Loading states
  loading: boolean;           // Initial fetch
  creating: boolean;          // Add form submission

  // Error state
  error: string | null;

  // Filter state
  filter: FilterType;

  // Modal states
  editingTask: Task | null;   // Task being edited (null = modal closed)
  deletingTask: Task | null;  // Task being deleted (null = dialog closed)
}
```

### AddTaskForm State

```typescript
interface AddTaskFormState {
  title: string;
  description: string;
  isSubmitting: boolean;
  error: string | null;
}
```

### EditTaskModal State

```typescript
interface EditTaskModalState {
  title: string;
  description: string;
  isSubmitting: boolean;
  error: string | null;
}
```

### TaskItem State

```typescript
interface TaskItemState {
  isToggling: boolean;  // Checkbox loading state
}
```

---

## Component Props Interfaces

### TaskList Props

```typescript
interface TaskListProps {
  tasks: Task[];
  filter: FilterType;
  onFilterChange: (filter: FilterType) => void;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}
```

### TaskItem Props

```typescript
interface TaskItemProps {
  task: Task;
  onToggle: (taskId: string) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}
```

### AddTaskForm Props

```typescript
interface AddTaskFormProps {
  onSubmit: (task: TaskCreate) => Promise<void>;
}
```

### EditTaskModal Props

```typescript
interface EditTaskModalProps {
  task: Task | null;  // null = closed
  onSave: (taskId: string, updates: TaskUpdate) => Promise<void>;
  onClose: () => void;
}
```

### DeleteConfirmDialog Props

```typescript
interface DeleteConfirmDialogProps {
  task: Task | null;  // null = closed
  onConfirm: (taskId: string) => Promise<void>;
  onClose: () => void;
}
```

---

## State Transitions

### Task Lifecycle in UI

```
[No Tasks]
    ↓ user adds task
[Task Created] → displayed in list (completed: false)
    ↓ user clicks checkbox
[Task Toggled] → visual update (strikethrough if completed)
    ↓ user clicks edit
[Task Editing] → modal opens with current values
    ↓ user saves
[Task Updated] → list refreshes with new values
    ↓ user clicks delete
[Confirm Delete] → dialog shows task title
    ↓ user confirms
[Task Deleted] → removed from list
```

### Filter State Transitions

```
[All] ← default
  ↓↑
[Active] ← shows only completed: false
  ↓↑
[Completed] ← shows only completed: true
```

---

## Validation Rules

### AddTaskForm

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Required, non-empty after trim | "Title is required" |
| description | Optional | N/A |

### EditTaskModal

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Required, non-empty after trim | "Title is required" |
| description | Optional | N/A |

---

## Empty States

| Scenario | Message |
|----------|---------|
| No tasks at all | "No tasks yet. Create your first task!" |
| No active tasks (filter: active) | "No active tasks. All caught up!" |
| No completed tasks (filter: completed) | "No completed tasks yet." |

---

## Error Messages

| Operation | Error Message |
|-----------|---------------|
| Fetch tasks failed | "Failed to load tasks. Please try again." |
| Create task failed | "Failed to create task. Please try again." |
| Update task failed | "Failed to update task. Please try again." |
| Delete task failed | "Failed to delete task. Please try again." |
| Toggle completion failed | "Failed to update task. Please try again." |
