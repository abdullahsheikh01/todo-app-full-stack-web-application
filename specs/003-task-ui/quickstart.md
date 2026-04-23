# Quickstart: Task Management UI

**Feature**: 003-task-ui
**Date**: 2026-04-23

## Prerequisites

- Node.js 18+ installed
- Backend server running on `http://localhost:8000`
- Neon database configured and accessible
- A user account created (via /signup)

## Quick Setup

### 1. Start the Backend

```bash
cd backend
uv run uvicorn main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/health` should return `{"status":"healthy","database":"connected"}`

### 2. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

### 3. Test the Feature

1. Navigate to `http://localhost:3000/signin`
2. Sign in with your account
3. You'll be redirected to `/dashboard`
4. Create, edit, complete, and delete tasks

## Development Workflow

### File Locations

```
frontend/
├── app/(protected)/dashboard/
│   ├── page.tsx              # Server component (auth)
│   ├── page.module.css       # Dashboard styles
│   └── DashboardClient.tsx   # Client component (state)
└── components/tasks/
    ├── TaskList.tsx
    ├── TaskItem.tsx
    ├── AddTaskForm.tsx
    ├── EditTaskModal.tsx
    └── DeleteConfirmDialog.tsx
```

### Making Changes

1. **Components**: Edit files in `frontend/components/tasks/`
2. **Dashboard Layout**: Edit `frontend/app/(protected)/dashboard/page.module.css`
3. **API Calls**: Use functions from `frontend/lib/api.ts`

### Hot Reload

Next.js dev server automatically reloads on file changes. No manual restart needed.

## Testing Checklist

### Manual Testing Steps

- [ ] Dashboard loads and shows task list (or empty state)
- [ ] Can create a task with title only
- [ ] Can create a task with title and description
- [ ] Cannot submit empty title (validation)
- [ ] Can toggle task completion via checkbox
- [ ] Completed tasks show strikethrough/muted style
- [ ] Filter tabs work (All / Active / Completed)
- [ ] Can open edit modal and modify task
- [ ] Can cancel edit without saving
- [ ] Delete confirmation shows task title
- [ ] Can confirm delete to remove task
- [ ] Can cancel delete to keep task
- [ ] Error messages show on API failure
- [ ] Loading states appear during operations
- [ ] UI is usable on mobile (320px width)

### API Endpoints Used

| Action | Method | Endpoint |
|--------|--------|----------|
| List tasks | GET | `/api/{userId}/tasks` |
| Create task | POST | `/api/{userId}/tasks` |
| Update task | PUT | `/api/{userId}/tasks/{taskId}` |
| Delete task | DELETE | `/api/{userId}/tasks/{taskId}` |
| Toggle complete | PATCH | `/api/{userId}/tasks/{taskId}/complete` |

## Troubleshooting

### "Failed to load tasks"

- Check backend is running: `curl http://localhost:8000/health`
- Verify DATABASE_URL is set in backend `.env`
- Check browser console for detailed error

### "Unauthorized" redirect to signin

- Session may have expired
- Sign out and sign in again
- Check BETTER_AUTH_SECRET matches in frontend and backend

### Styles not applying

- Ensure CSS module imports use correct paths
- Check for typos in className references
- Verify `.module.css` file exists alongside component

### Modal not opening

- Check `dialogRef.current` is not null
- Ensure `useRef` is initialized correctly
- Verify `showModal()` is called (not `show()`)

## Environment Variables

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-here
```

### Backend (.env)

```bash
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=your-secret-here  # Same as frontend
```
