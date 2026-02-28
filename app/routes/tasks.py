from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.task_controller import TaskController

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Retrieve all tasks with pagination and filtering
    Get a list of tasks belonging to the authenticated user (or all tasks if admin).
    Supports pagination and filtering by completion status.
    ---
    tags:
      - Tasks
    summary: List all tasks
    description: Retrieve paginated list of tasks for current user. Admin users see all tasks in system. Regular users see only their own tasks.
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number for pagination (must be >= 1)
        example: 1
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Number of tasks per page (must be >= 1)
        example: 10
      - name: completed
        in: query
        type: boolean
        description: Filter tasks by completion status (true/false)
        example: false
    responses:
      200:
        description: List of tasks retrieved successfully
        schema:
          type: object
          properties:
            tasks:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  title:
                    type: string
                    example: "Complete project"
                  description:
                    type: string
                    example: "Finish the task manager API"
                  completed:
                    type: boolean
                    example: false
                  user_id:
                    type: integer
                    example: 1
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
            pagination:
              type: object
              properties:
                page:
                  type: integer
                  example: 1
                per_page:
                  type: integer
                  example: 10
                total:
                  type: integer
                  example: 25
                pages:
                  type: integer
                  example: 3
      400:
        description: Invalid pagination parameters
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Page and per_page must be positive integers"
      401:
        description: Unauthorized - missing or invalid token
      404:
        description: User not found
      500:
        description: Internal server error
    """
    return TaskController.get_tasks()

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """
    Retrieve a specific task by ID
    Get detailed information about a single task. Users can only view their own tasks unless they are admins.
    ---
    tags:
      - Tasks
    summary: Get task by ID
    description: Retrieve a specific task. Users can only access their own tasks. Admin users can access any task.
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task ID
        example: 1
    responses:
      200:
        description: Task retrieved successfully
        schema:
          type: object
          properties:
            task:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                title:
                  type: string
                  example: "Complete project"
                description:
                  type: string
                  example: "Finish the task manager API"
                completed:
                  type: boolean
                  example: false
                user_id:
                  type: integer
                  example: 1
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
      404:
        description: Task not found
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized - missing or invalid token
      403:
        description: Forbidden - user cannot access this task
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Forbidden - you do not have permission to view this task"
      500:
        description: Internal server error
    """
    return TaskController.get_task(task_id)

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task
    Create a new task for the authenticated user. Only title is required, description and completed status are optional.
    ---
    tags:
      - Tasks
    summary: Create a new task
    description: Create a new task with required title and optional description and completion status.
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        description: Task details
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              minLength: 1
              maxLength: 200
              example: "Complete project"
              description: Task title (required, 1-200 characters)
            description:
              type: string
              maxLength: 1000
              example: "Finish the task manager API project"
              description: Task description (optional, max 1000 characters)
            completed:
              type: boolean
              default: false
              example: false
              description: Task completion status (optional, default false)
    responses:
      201:
        description: Task created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task created successfully"
            task:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                title:
                  type: string
                description:
                  type: string
                completed:
                  type: boolean
                user_id:
                  type: integer
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
      400:
        description: Invalid input - missing title
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required field: title"
      401:
        description: Unauthorized - missing or invalid token
      500:
        description: Internal server error
    """
    return TaskController.create_task()

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update a specific task
    Update one or more fields of a task. Users can only update their own tasks unless they are admins.
    ---
    tags:
      - Tasks
    summary: Update a task
    description: Update task details (title, description, or completion status). Users can only update their own tasks.
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task ID
        example: 1
      - name: body
        in: body
        required: true
        description: Task fields to update
        schema:
          type: object
          properties:
            title:
              type: string
              minLength: 1
              maxLength: 200
              example: "Updated title"
              description: New task title
            description:
              type: string
              maxLength: 1000
              example: "Updated description"
              description: New task description
            completed:
              type: boolean
              example: true
              description: New completion status
    responses:
      200:
        description: Task updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task updated successfully"
            task:
              type: object
              properties:
                id:
                  type: integer
                title:
                  type: string
                description:
                  type: string
                completed:
                  type: boolean
                user_id:
                  type: integer
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
      404:
        description: Task not found
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized - missing or invalid token
      403:
        description: Forbidden - user cannot update this task
        schema:
          type: object
          properties:
            error:
              type: string
      400:
        description: Invalid input
      500:
        description: Internal server error
    """
    return TaskController.update_task(task_id)

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a specific task
    Delete a task permanently. Users can only delete their own tasks unless they are admins.
    ---
    tags:
      - Tasks
    summary: Delete a task
    description: Permanently delete a task. Users can only delete their own tasks. Admin users can delete any task.
    security:
      - Bearer: []
    parameters:
      - name: task_id
        in: path
        type: integer
        required: true
        description: Task ID
        example: 1
    responses:
      200:
        description: Task deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task deleted successfully"
      404:
        description: Task not found
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized - missing or invalid token
      403:
        description: Forbidden - user cannot delete this task
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
    """
    return TaskController.delete_task(task_id)
