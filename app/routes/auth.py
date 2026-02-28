from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    Register a new user account with username, email, and password.
    The first registered user automatically becomes an admin. Subsequent users get the 'user' role.
    ---
    tags:
      - Authentication
    summary: Register a new user account
    description: Create a new user account with unique username and email. The first user registered automatically becomes admin. All subsequent users are assigned the 'user' role.
    parameters:
      - name: body
        in: body
        required: true
        description: User registration credentials
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              minLength: 3
              maxLength: 50
              example: "john_doe"
              description: Unique username (3-50 characters)
            email:
              type: string
              format: email
              example: "john@example.com"
              description: Valid email address
            password:
              type: string
              minLength: 6
              example: "SecurePass123"
              description: Password (minimum 6 characters)
    responses:
      201:
        description: User successfully registered
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User registered successfully"
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
                  example: "admin"
                  description: "Role assigned - 'admin' for first user, 'user' for others"
      400:
        description: Invalid input or user already exists
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username already exists"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    Authenticate user with username and password to receive JWT access token.
    Token is valid for 1 hour and must be included in Authorization header.
    ---
    tags:
      - Authentication
    summary: Authenticate user and receive JWT token
    description: Authenticate user credentials and receive JWT token valid for 1 hour. Include token as 'Bearer <token>' in Authorization header for subsequent requests.
    parameters:
      - name: body
        in: body
        required: true
        description: Login credentials
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "john_doe"
              description: Registered username
            password:
              type: string
              example: "SecurePass123"
              description: Account password
    responses:
      200:
        description: Login successful, JWT token returned
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login successful"
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
              description: JWT token (valid for 1 hour)
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
                role:
                  type: string
                  enum: [user, admin]
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid username or password"
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return AuthController.login()

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user profile
    Retrieve the authenticated user's complete profile information.
    ---
    tags:
      - Authentication
    summary: Get user profile
    description: Retrieve the current authenticated user's profile with all details (ID, username, email, role, creation date).
    security:
      - Bearer: []
    responses:
      200:
        description: User profile retrieved successfully
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
                  example: "2025-12-06T10:30:00"
      401:
        description: Unauthorized - missing or invalid token
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing Authorization Header"
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
    return AuthController.get_profile()
