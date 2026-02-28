import pytest
import json
from app import create_app
from app.models import db, User, Task

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def auth_header(client):
    """Get authorization header for a standard user."""
    # Register an initial user who will be admin
    client.post('/api/auth/register', json={
        'username': 'admin_init',
        'email': 'admin_init@example.com',
        'password': 'Password123'
    })
    # Register the test user who will be a regular user
    client.post('/api/auth/register', json={
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'Password123'
    })
    response = client.post('/api/auth/login', json={
        'username': 'test_user',
        'password': 'Password123'
    })
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_header(client):
    """Get authorization header for an admin user (first user)."""
    client.post('/api/auth/register', json={
        'username': 'admin_user',
        'email': 'admin@example.com',
        'password': 'Password123'
    })
    response = client.post('/api/auth/login', json={
        'username': 'admin_user',
        'password': 'Password123'
    })
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

class TestAuth:
    def test_register(self, client):
        response = client.post('/api/auth/register', json={
            'username': 'new_user',
            'email': 'new@example.com',
            'password': 'Password123'
        })
        assert response.status_code == 201
        assert 'User registered' in response.get_json()['message']

    def test_login(self, client):
        client.post('/api/auth/register', json={
            'username': 'login_user',
            'email': 'login@example.com',
            'password': 'Password123'
        })
        response = client.post('/api/auth/login', json={
            'username': 'login_user',
            'password': 'Password123'
        })
        assert response.status_code == 200
        assert 'access_token' in response.get_json()

    def test_get_profile(self, client, auth_header):
        response = client.get('/api/auth/profile', headers=auth_header)
        assert response.status_code == 200
        assert response.get_json()['user']['username'] == 'test_user'

class TestTasks:
    def test_create_task(self, client, auth_header):
        response = client.post('/api/tasks', json={
            'title': 'Test Task',
            'description': 'Test Description'
        }, headers=auth_header)
        assert response.status_code == 201
        assert response.get_json()['task']['title'] == 'Test Task'

    def test_get_tasks(self, client, auth_header):
        client.post('/api/tasks', json={'title': 'Task 1'}, headers=auth_header)
        client.post('/api/tasks', json={'title': 'Task 2'}, headers=auth_header)
        response = client.get('/api/tasks', headers=auth_header)
        assert response.status_code == 200
        assert len(response.get_json()['tasks']) == 2

    def test_update_task(self, client, auth_header):
        create_res = client.post('/api/tasks', json={'title': 'Old Title'}, headers=auth_header)
        task_id = create_res.get_json()['task']['id']
        response = client.put(f'/api/tasks/{task_id}', json={'title': 'New Title'}, headers=auth_header)
        assert response.status_code == 200
        assert response.get_json()['task']['title'] == 'New Title'

    def test_delete_task(self, client, auth_header):
        create_res = client.post('/api/tasks', json={'title': 'Delete Me'}, headers=auth_header)
        task_id = create_res.get_json()['task']['id']
        response = client.delete(f'/api/tasks/{task_id}', headers=auth_header)
        assert response.status_code == 200
        
        get_res = client.get(f'/api/tasks/{task_id}', headers=auth_header)
        assert get_res.status_code == 404

class TestAdmin:
    def test_admin_get_all_users(self, client, admin_header):
        response = client.get('/api/admin/users', headers=admin_header)
        assert response.status_code == 200
        assert len(response.get_json()['users']) >= 1

    def test_admin_stats(self, client, admin_header):
        response = client.get('/api/admin/stats', headers=admin_header)
        assert response.status_code == 200
        assert 'total_users' in response.get_json()['stats']

    def test_unauthorized_admin_access(self, client, auth_header):
        response = client.get('/api/admin/users', headers=auth_header)
        assert response.status_code == 403

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'
