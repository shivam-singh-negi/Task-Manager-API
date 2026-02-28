from flask import Blueprint
from app.controllers.admin_controller import AdminController
from app.utils import require_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_all_users():
    """
    Get all users in the system
    Retrieve a paginated list of all users with optional filtering by role. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: List all users (Admin only)
    description: Retrieve all system users with pagination and optional role filtering. Only accessible to admin users.
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
        description: Number of users per page (must be >= 1)
        example: 10
      - name: role
        in: query
        type: string
        enum: ['user', 'admin']
        description: Filter by user role
        example: "user"
    responses:
      200:
        description: List of all users retrieved successfully
        schema:
          type: object
          properties:
            users:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  username:
                    type: string
                    example: "john_doe"
                  email:
                    type: string
                    example: "john@example.com"
                  role:
                    type: string
                    enum: [user, admin]
                    example: "user"
                  created_at:
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
                  example: 50
                pages:
                  type: integer
                  example: 5
      403:
        description: Admin privileges required
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Admin privileges required"
      500:
        description: Internal server error
    """
    return AdminController.get_all_users()

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """
    Get a specific user by ID
    Retrieve detailed information about a specific user. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: Get user by ID (Admin only)
    description: Retrieve detailed information about a specific user by ID. Only accessible to admin users.
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
        example: 1
    responses:
      200:
        description: User retrieved successfully
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                username:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john@example.com"
                role:
                  type: string
                  enum: [user, admin]
                  example: "user"
                created_at:
                  type: string
                  format: date-time
                updated_at:
                  type: string
                  format: date-time
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "User not found"
      403:
        description: Admin privileges required
      500:
        description: Internal server error
    """
    return AdminController.get_user(user_id)

@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@require_admin
def change_user_role(user_id):
    """
    Change a user's role
    Change the role of a specific user between 'user' and 'admin'. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: Change user role (Admin only)
    description: Change a user's role between 'user' and 'admin'. Only accessible to admin users.
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
        example: 5
      - name: body
        in: body
        required: true
        description: New role for the user
        schema:
          type: object
          required:
            - role
          properties:
            role:
              type: string
              enum: ['admin', 'user']
              example: 'admin'
              description: New role for the user
    responses:
      200:
        description: Role changed successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User role changed to admin"
            user:
              type: object
              properties:
                id:
                  type: integer
                  example: 5
                username:
                  type: string
                email:
                  type: string
                role:
                  type: string
                  enum: [user, admin]
                  example: "admin"
      400:
        description: Invalid role or missing required field
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid role. Must be 'admin' or 'user'"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Admin privileges required
      500:
        description: Internal server error
    """
    return AdminController.change_user_role(user_id)

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """
    Delete a user account
    Permanently delete a user account and all associated data. Admin only endpoint. Cannot delete your own account.
    ---
    tags:
      - Admin
    summary: Delete a user (Admin only)
    description: Permanently delete a user account. Users cannot delete their own account. Only accessible to admin users.
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
        example: 5
    responses:
      200:
        description: User deleted successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User deleted successfully"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Admin privileges required or cannot delete own account
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Cannot delete your own account"
      500:
        description: Internal server error
    """
    return AdminController.delete_user(user_id)

@admin_bp.route('/tasks', methods=['GET'])
@require_admin
def get_all_tasks():
    """
    Get all tasks in the system
    Retrieve a paginated list of all tasks across all users. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: List all tasks in system (Admin only)
    description: Retrieve all tasks created by any user with pagination and optional filtering. Only accessible to admin users.
    security:
      - Bearer: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Page number for pagination (must be >= 1)
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Number of tasks per page (must be >= 1)
      - name: completed
        in: query
        type: boolean
        description: Filter by completion status (true/false)
      - name: user_id
        in: query
        type: integer
        description: Filter tasks by user ID
    responses:
      200:
        description: List of all tasks retrieved successfully
        schema:
          type: object
          properties:
            tasks:
              type: array
              items:
                type: object
            pagination:
              type: object
      400:
        description: Invalid pagination parameters or user not found
      403:
        description: Admin privileges required
      500:
        description: Internal server error
    """
    return AdminController.get_all_tasks()

@admin_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@require_admin
def delete_task(task_id):
    """
    Delete any task in the system
    Permanently delete any task regardless of owner. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: Delete any task (Admin only)
    description: Permanently delete any task in the system. Only accessible to admin users.
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
      403:
        description: Admin privileges required
      500:
        description: Internal server error
    """
    return AdminController.delete_task(task_id)

@admin_bp.route('/stats', methods=['GET'])
@require_admin
def get_system_stats():
    """
    Get system statistics
    Retrieve comprehensive system statistics including user counts, task counts, and completion rates. Admin only endpoint.
    ---
    tags:
      - Admin
    summary: Get system statistics (Admin only)
    description: Retrieve system-wide statistics including total users, tasks, completion rates, and role distribution. Only accessible to admin users.
    security:
      - Bearer: []
    responses:
      200:
        description: System statistics retrieved successfully
        schema:
          type: object
          properties:
            stats:
              type: object
              properties:
                total_users:
                  type: integer
                  example: 50
                  description: Total number of users in system
                total_tasks:
                  type: integer
                  example: 150
                  description: Total number of tasks in system
                completed_tasks:
                  type: integer
                  example: 85
                  description: Number of completed tasks
                incomplete_tasks:
                  type: integer
                  example: 65
                  description: Number of incomplete tasks
                admin_users:
                  type: integer
                  example: 3
                  description: Number of admin users
                regular_users:
                  type: integer
                  example: 47
                  description: Number of regular users
                completion_rate:
                  type: string
                  example: "56.7%"
                  description: Overall task completion rate
      403:
        description: Admin privileges required
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
    """
    return AdminController.get_system_stats()
