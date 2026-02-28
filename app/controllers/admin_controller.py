from flask import jsonify, request, current_app
from flask_jwt_extended import get_jwt_identity
from app.models import db, Task, User, UserRole

class AdminController:
    @staticmethod
    def get_all_users():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            role = request.args.get('role', None, type=str)
            
            if page < 1 or per_page < 1:
                return jsonify({'error': 'Page and per_page must be positive integers'}), 400
            
            query = User.query
            if role:
                if role not in [UserRole.ADMIN.value, UserRole.USER.value]:
                    return jsonify({'error': f'Invalid role. Must be "{UserRole.ADMIN.value}" or "{UserRole.USER.value}"'}), 400
                query = query.filter_by(role=role)
            
            paginated_users = query.order_by(User.created_at.desc()).paginate(
                page=page, per_page=per_page, error_out=False
            )
            
            return jsonify({
                'users': [user.to_dict() for user in paginated_users.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated_users.total,
                    'pages': paginated_users.pages
                }
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve users: {str(e)}'}), 500

    @staticmethod
    def get_user(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            return jsonify({'user': user.to_dict()}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve user: {str(e)}'}), 500

    @staticmethod
    def change_user_role(user_id):
        try:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            new_role = data.get('role')
            if not new_role:
                return jsonify({'error': 'Missing required field: role'}), 400
            
            if new_role not in [UserRole.ADMIN.value, UserRole.USER.value]:
                return jsonify({'error': f'Invalid role. Must be "{UserRole.ADMIN.value}" or "{UserRole.USER.value}"'}), 400
            
            user.role = new_role
            db.session.commit()
            return jsonify({
                'message': f'User role changed to {new_role}',
                'user': user.to_dict()
            }), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error changing role for user {user_id}: {str(e)}')
            return jsonify({'error': f'Failed to change user role: {str(e)}'}), 500

    @staticmethod
    def delete_user(user_id):
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if int(current_user_id) == user_id:
                return jsonify({'error': 'Cannot delete your own account'}), 403
            
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error deleting user {user_id}: {str(e)}')
            return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500

    @staticmethod
    def get_all_tasks():
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            completed = request.args.get('completed', None, type=lambda x: x.lower() == 'true' if x else None)
            user_id = request.args.get('user_id', None, type=int)
            
            if page < 1 or per_page < 1:
                return jsonify({'error': 'Page and per_page must be positive integers'}), 400
            
            query = Task.query
            if completed is not None:
                query = query.filter_by(completed=completed)
            if user_id:
                if not User.query.get(user_id):
                    return jsonify({'error': f'User with ID {user_id} not found'}), 404
                query = query.filter_by(user_id=user_id)
            
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
            return jsonify({'error': f'Failed to retrieve tasks: {str(e)}'}), 500

    @staticmethod
    def delete_any_task(task_id):
        try:
            task = Task.query.get(task_id)
            if not task:
                return jsonify({'error': 'Task not found'}), 404
            
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'}), 200
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Admin error deleting task {task_id}: {str(e)}')
            return jsonify({'error': f'Failed to delete task: {str(e)}'}), 500

    @staticmethod
    def get_system_stats():
        try:
            total_users = User.query.count()
            total_tasks = Task.query.count()
            completed_tasks = Task.query.filter_by(completed=True).count()
            incomplete_tasks = Task.query.filter_by(completed=False).count()
            admin_users = User.query.filter_by(role=UserRole.ADMIN.value).count()
            regular_users = User.query.filter_by(role=UserRole.USER.value).count()
            
            completion_rate = f"{(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0:.1f}%"
            
            return jsonify({
                'stats': {
                    'total_users': total_users,
                    'total_tasks': total_tasks,
                    'completed_tasks': completed_tasks,
                    'incomplete_tasks': incomplete_tasks,
                    'admin_users': admin_users,
                    'regular_users': regular_users,
                    'completion_rate': completion_rate
                }
            }), 200
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve statistics: {str(e)}'}), 500
