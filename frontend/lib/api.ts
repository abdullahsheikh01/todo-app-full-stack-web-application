const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface HealthResponse {
  status: string;
  database: string;
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string | null;
}

export interface TaskUpdate {
  title?: string;
  description?: string | null;
  completed?: boolean;
}

export interface ApiError {
  detail: string;
}

async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    credentials: "include", // Include cookies for CORS
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  // Handle 401 - redirect to signin
  if (response.status === 401) {
    if (typeof window !== "undefined") {
      window.location.href = "/signin";
    }
    throw new Error("Unauthorized");
  }

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.detail || "An error occurred");
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

export async function getHealth(): Promise<HealthResponse> {
  return fetchApi<HealthResponse>("/health");
}

// Task API functions
export async function listTasks(
  userId: string,
  completed?: boolean
): Promise<Task[]> {
  const params = new URLSearchParams();
  if (completed !== undefined) {
    params.set("completed", String(completed));
  }
  const queryString = params.toString();
  const endpoint = `/api/${userId}/tasks${queryString ? `?${queryString}` : ""}`;
  return fetchApi<Task[]>(endpoint);
}

export async function createTask(
  userId: string,
  task: TaskCreate
): Promise<Task> {
  return fetchApi<Task>(`/api/${userId}/tasks`, {
    method: "POST",
    body: JSON.stringify(task),
  });
}

export async function getTask(userId: string, taskId: string): Promise<Task> {
  return fetchApi<Task>(`/api/${userId}/tasks/${taskId}`);
}

export async function updateTask(
  userId: string,
  taskId: string,
  task: TaskUpdate
): Promise<Task> {
  return fetchApi<Task>(`/api/${userId}/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(task),
  });
}

export async function deleteTask(
  userId: string,
  taskId: string
): Promise<void> {
  return fetchApi<void>(`/api/${userId}/tasks/${taskId}`, {
    method: "DELETE",
  });
}

export async function toggleTaskComplete(
  userId: string,
  taskId: string
): Promise<Task> {
  return fetchApi<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
    method: "PATCH",
  });
}

export const api = {
  getHealth,
  listTasks,
  createTask,
  getTask,
  updateTask,
  deleteTask,
  toggleTaskComplete,
};
