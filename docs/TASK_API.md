# Task Management API Documentation

This document describes the REST API endpoints for task management functionality in the orga-ai application.

## Authentication

All task endpoints require authentication using a Bearer token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Base URL

All endpoints are prefixed with `/tasks`

## Endpoints

### 1. GET /tasks - List Tasks

Retrieve all tasks for the authenticated user with optional filtering, pagination, and sorting.

**Query Parameters:**
- `status` (optional): Filter by task status (`pending`, `in_progress`, `completed`, `cancelled`)
- `priority` (optional): Filter by priority (0=none, 1=low, 2=medium, 3=high, 4=urgent)
- `due_date_from` (optional): Filter tasks due from this date (YYYY-MM-DD format)
- `due_date_to` (optional): Filter tasks due until this date (YYYY-MM-DD format)
- `parent_task_id` (optional): Filter by parent task ID (for subtasks)
- `category_id` (optional): Filter by category ID
- `search` (optional): Search in title and description
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Number of items per page (default: 20, max: 100)
- `sort_by` (optional): Field to sort by (default: `created_at`)
- `sort_order` (optional): Sort order (`asc` or `desc`, default: `desc`)

**Example Request:**
```bash
GET /tasks?status=pending&priority=3&page=1&page_size=10&sort_by=due_date&sort_order=asc
```

**Response:**
```json
{
  "tasks": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "title": "Task Title",
      "description": "Task Description",
      "due_date": "2024-01-15",
      "due_time": "14:30:00",
      "status": "pending",
      "priority": 3,
      "completion_percentage": 0,
      "estimated_duration": 120,
      "actual_duration": null,
      "parent_task_id": null,
      "category_id": "uuid",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z",
      "completed_at": null
    }
  ],
  "total": 25,
  "page": 1,
  "page_size": 10,
  "total_pages": 3
}
```

### 2. GET /tasks/{id} - Get Task by ID

Retrieve a specific task by its ID.

**Path Parameters:**
- `id`: UUID of the task

**Example Request:**
```bash
GET /tasks/123e4567-e89b-12d3-a456-426614174000
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "uuid",
  "title": "Task Title",
  "description": "Task Description",
  "due_date": "2024-01-15",
  "due_time": "14:30:00",
  "status": "pending",
  "priority": 3,
  "completion_percentage": 0,
  "estimated_duration": 120,
  "actual_duration": null,
  "parent_task_id": null,
  "category_id": "uuid",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z",
  "completed_at": null
}
```

### 3. POST /tasks - Create Task

Create a new task.

**Request Body:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2024-01-15",
  "due_time": "14:30:00",
  "status": "pending",
  "priority": 2,
  "completion_percentage": 0,
  "estimated_duration": 120,
  "parent_task_id": null,
  "category_id": "uuid"
}
```

**Required Fields:**
- `title`: Task title (1-500 characters)

**Response:** Returns the created task object (same format as GET /tasks/{id})

### 4. PUT /tasks/{id} - Update Task

Update an existing task completely. At least one field must be provided.

**Path Parameters:**
- `id`: UUID of the task to update

**Request Body:** Same format as POST, but all fields are optional

**Response:** Returns the updated task object

### 5. PATCH /tasks/{id} - Partial Update

Partially update an existing task. Only provided fields will be updated.

**Path Parameters:**
- `id`: UUID of the task to update

**Request Body:** Any subset of the task fields

**Example Request:**
```json
{
  "status": "completed",
  "completion_percentage": 100
}
```

**Response:** Returns the updated task object

### 6. DELETE /tasks/{id} - Delete Task

Delete a task (soft delete).

**Path Parameters:**
- `id`: UUID of the task to delete

**Response:**
```json
{
  "message": "Task deleted successfully",
  "deleted_task_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Invalid authentication credentials",
  "error_code": "UNAUTHORIZED"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Access forbidden",
  "error_code": "FORBIDDEN"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Task with ID {id} not found",
  "error_code": "TASK_NOT_FOUND"
}
```

### 422 Validation Error
```json
{
  "success": false,
  "message": "Validation error message",
  "error_code": "VALIDATION_ERROR",
  "details": {
    "field": "error details"
  }
}
```

## Task Status Values

- `pending`: Task is not yet started
- `in_progress`: Task is currently being worked on
- `completed`: Task has been completed
- `cancelled`: Task has been cancelled

## Priority Values

- `0`: None
- `1`: Low
- `2`: Medium
- `3`: High
- `4`: Urgent

## Notes

- All timestamps are in ISO 8601 format
- Task deletion is soft delete (sets `deleted_at` timestamp)
- Subtasks are not automatically deleted when parent task is deleted
- When a task status is changed to `completed`, the `completed_at` timestamp is automatically set
- When a task status is changed from `completed` to another status, the `completed_at` timestamp is cleared
