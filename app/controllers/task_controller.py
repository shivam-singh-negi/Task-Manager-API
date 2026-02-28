from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity
from app.models import db, Task, User

class TaskController:
    @staticmethod
    def check_user_authorization(task, user_id):
        """Check if user is authorized to modify the task"""
        user = User.query.get(user_id)
        if not user:
            return False, None
        
        # Admin can modify any task, users can only modify their own
        if user.is_admin():
            return True, user
        
        return task.user_id == user_id, user

    @staticmethod
    def get_tasks():
        try:
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            completed = request.args.get('completed', None, type=lambda x: x.lower() == 'true' if x else None)
            
            if page < 1 or per_page < 1:
                return jsonify({'error': 'Page and per_page must be positive integers'}), 400
            
            query = Task.query
            if not user.is_admin():
                query = query.filter_by(user_id=user_id)
            
            if completed is not None:
                query = query.filter_by(completed=completed)
            
            paginated_tasks = query.order_by(Task.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'tasks': [task.to_dict() for task in paginated_tasks.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated_tasks.total,
                    'pages': paginated_tasks.pages
                }
            }), 200
        except Exception as e:
            current_app.logger.error(f'Error retrieving tasks for user {user_id}: {str(e)}')
            return jsonify({'error': f'Failed to retrieve tasks: {str(e)}'}), 500

    @staticmethod
    def get_task(task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            authorized, user = TaskController.check_user_authorization(task, user_id)
            if not authorized:
                return jsonify({'error': 'Forbidden - you do not have permission to view this task'}), 403
            
            return jsonify({'task': task.to_dict()}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve task: {str(e)}'}), 500

    @staticmethod
    def create_task():
        try:
            user_id = int(get_jwt_identity())
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            title = data.get('title')
            if not title or len(title.strip()) < 1:
                return jsonify({'error': 'Missing required field: title'}), 400
            
            if len(title) > 255:
                return jsonify({'error': 'Title must be 255 characters or less'}), 400
            
            description = data.get('description', '')
            if len(description) > 1000:
                return jsonify({'error': 'Description must be 1000 characters or less'}), 400
            
            completed = data.get('completed', False)
            task = Task(title=title, description=description, completed=completed, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            
            current_app.logger.info(f'Task created by user {user_id}: {task.id}')
            
            return jsonify({
                'message': 'Task created successfully',
                'task': task.to_dict()
            }), 201
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error creating task for user {user_id}: {str(e)}')
            return jsonify({'error': f'Failed to create task: {str(e)}'}), 500

    @staticmethod
    def update_task(task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            authorized, user = TaskController.check_user_authorization(task, user_id)
            if not authorized:
                return jsonify({'error': 'Forbidden - you do not have permission to update this task'}), 403
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            if 'title' in data:
                title = data['title']
                if not title or len(title.strip()) < 1:
                    return jsonify({'error': 'Title cannot be empty or whitespace only'}), 400
                if len(title) > 255:
                    return jsonify({'error': 'Title must be 255 characters or less'}), 400
                task.title = title
            
            if 'description' in data:
                description = data['description']
                if len(description) > 1000:
                    return jsonify({'error': 'Description must be 1000 characters or less'}), 400
                task.description = description
            
            if 'completed' in data:
                task.completed = data['completed']
            
            db.session.commit()
            current_app.logger.info(f'Task {task_id} updated by user {user_id}')
            return jsonify({
                'message': 'Task updated successfully',
                'task': task.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update task: {str(e)}'}), 500

    @staticmethod
    def delete_task(task_id):
        try:
            user_id = int(get_jwt_identity())
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            authorized, user = TaskController.check_user_authorization(task, user_id)
            if not authorized:
                return jsonify({'error': 'Forbidden - you do not have permission to delete this task'}), 403
            
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete task: {str(e)}'}), 500
