# Research: Task Management UI

**Feature**: 003-task-ui
**Date**: 2026-04-23

## Overview

This document captures research findings and technical decisions for the Task Management UI feature. Since the backend API and API client are already implemented, this research focuses on frontend patterns and component design.

---

## R1: Server vs Client Components in Next.js App Router

### Decision
Use a **hybrid approach**: Server component for the dashboard page (authentication check), with a client component wrapper for task state management.

### Rationale
- Server components cannot use hooks (useState, useEffect) required for task fetching and UI state
- The existing dashboard page uses `auth.api.getSession()` server-side, which is correct for auth
- Task operations require client-side state management for loading states, optimistic updates, and error handling

### Alternatives Considered
1. **Full server component with actions**: Would require form actions and server-side mutations; more complex and doesn't support real-time UI feedback
2. **Full client component**: Would lose server-side session validation benefits

### Pattern
```
page.tsx (Server) → validates session → renders DashboardClient
DashboardClient.tsx (Client) → manages task state → renders UI components
```

---

## R2: Modal Implementation Strategy

### Decision
Use **native HTML `<dialog>` element** with CSS Modules styling.

### Rationale
- Native `<dialog>` has built-in accessibility (focus trapping, backdrop, Escape key)
- No additional dependencies required
- Consistent with project's minimal-dependency approach
- Works with CSS Modules styling system

### Alternatives Considered
1. **Headless UI / Radix**: Adds dependencies, over-engineering for simple modals
2. **Custom portal with div**: Requires manual accessibility implementation

### Pattern
```typescript
const dialogRef = useRef<HTMLDialogElement>(null);
dialogRef.current?.showModal(); // Open
dialogRef.current?.close();     // Close
```

---

## R3: Task List Filtering Strategy

### Decision
Use **client-side filtering** with local state.

### Rationale
- API already fetches all user tasks (no pagination in Phase II scope)
- Instant filter response (< 500ms requirement easily met)
- Simpler implementation than API-based filtering
- No additional network requests

### Alternatives Considered
1. **API-based filtering**: Uses `listTasks(userId, completed)` parameter; adds latency, unnecessary for small lists

### Pattern
```typescript
const filteredTasks = useMemo(() => {
  if (filter === 'all') return tasks;
  if (filter === 'active') return tasks.filter(t => !t.completed);
  return tasks.filter(t => t.completed);
}, [tasks, filter]);
```

---

## R4: Error Handling Pattern

### Decision
Use **inline error messages** with retry capability.

### Rationale
- Consistent with existing signin/signup error pattern
- No toast library dependency required
- Clear user feedback near the action point

### Alternatives Considered
1. **Toast notifications**: Requires additional library or custom implementation
2. **Global error boundary**: Too coarse for individual operation failures

### Pattern
```typescript
const [error, setError] = useState<string | null>(null);
// On error: setError("Failed to create task. Please try again.");
// In JSX: {error && <p className={styles.error}>{error}</p>}
```

---

## R5: Form Validation Approach

### Decision
Use **HTML5 native validation** with `required` attribute plus client-side check.

### Rationale
- Matches existing auth forms pattern
- Simple, no dependencies
- Prevents form submission with empty required fields
- Works without JavaScript for basic validation

### Pattern
```tsx
<input required ... />
// Plus explicit check before submission:
if (!title.trim()) { setError("Title is required"); return; }
```

---

## R6: CSS Modules Organization

### Decision
**Component-scoped CSS Modules** with shared CSS variables from page scope.

### Rationale
- Each component gets its own `.module.css` file for isolation
- CSS variables defined at page level are inherited
- Consistent with existing `SignOutButton.module.css` pattern

### Structure
```
components/tasks/
├── TaskList.tsx
├── TaskList.module.css
├── TaskItem.tsx
├── TaskItem.module.css
...
```

---

## R7: Refetch Strategy After Mutations

### Decision
Use **simple refetch** after each mutation.

### Rationale
- Straightforward to implement
- Guarantees data consistency with server
- Acceptable latency for Phase II scope
- Optimistic updates marked as optional in spec

### Alternatives Considered
1. **Optimistic updates**: More complex state management, potential for race conditions
2. **React Query / SWR**: Adds dependency, over-engineering for this scope

### Pattern
```typescript
const fetchTasks = async () => { /* ... */ };
const handleCreate = async (task: TaskCreate) => {
  await api.createTask(userId, task);
  await fetchTasks(); // Refetch to sync
};
```

---

## R8: Loading State Management

### Decision
Use **multiple loading states** for granular feedback.

### Rationale
- Different operations should show loading in their respective UI areas
- Initial load shows full-page loader
- Individual operations show button/checkbox loading states

### State Structure
```typescript
const [loading, setLoading] = useState(true);        // Initial fetch
const [creating, setCreating] = useState(false);     // Add form
const [togglingId, setTogglingId] = useState<string | null>(null); // Which task
```

---

## Summary

| Area | Decision | Key Benefit |
|------|----------|-------------|
| Components | Hybrid server/client | Auth on server, state on client |
| Modals | Native `<dialog>` | Zero dependencies, accessible |
| Filtering | Client-side | Instant response |
| Errors | Inline messages | Consistent with auth pages |
| Validation | HTML5 + JS check | Simple, no dependencies |
| CSS | Component-scoped modules | Isolation + shared variables |
| Mutations | Refetch after | Data consistency |
| Loading | Granular states | Clear user feedback |
