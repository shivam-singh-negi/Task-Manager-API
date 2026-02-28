from flask_sqlalchemy import SQLAlchemy

# Initialize database
db = SQLAlchemy()

# Import models here to ensure they are registered with SQLAlchemy
# Importing after db initialization to avoid circular dependencies
from .user import User, UserRole
from .task import Task
