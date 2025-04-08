import pytest
from flask import url_for
from app import generate_unique_company_id
from models import Employee

def test_app_exists(app):
    """Check if the Flask app instance exists."""
    assert app is not None

def test_app_is_testing(app):
    """Check if the app is running in testing configuration."""
    assert app.config['TESTING'] is True
    assert app.config['DEBUG'] is False
    assert 'sqlite:///:memory:' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['MAIL_ENABLED'] is False

def test_index_renders_login_when_logged_out(client):
    """Test if accessing '/' renders the login page when not logged in."""
    response = client.get('/')
    assert response.status_code == 200

    assert b'GreenTech</h1>' in response.data
    assert b'Monitoring Dashboard Login' in response.data
    assert b'Email Address' in response.data
    assert b'Password' in response.data
    assert b'Log In</button>' in response.data

def test_index_redirects_when_logged_in(client, session, regular_user_data):
    """Test if accessing '/' redirects to dashboard WHEN logged in."""
    # --- Setup: Create and log in a user ---
    company_id = generate_unique_company_id()
    user = Employee(
        name=regular_user_data['name'],
        email=regular_user_data['email'],
        company_id=company_id
    )
    user.set_password(regular_user_data['password'])
    session.add(user)
    session.commit()

    client.post('/login', data={
        'email': regular_user_data['email'],
        'password': regular_user_data['password']
    })
    # --- End Setup ---

    # Now access '/' WHILE logged in
    response = client.get('/', follow_redirects=False)
    assert response.status_code == 200

    response_followed = client.get('/', follow_redirects=True)
    assert response_followed.status_code == 200
    assert b'Dashboard' in response_followed.data



def test_login_page_loads(client):
    """Test if the login page loads correctly."""
    response = client.get(url_for('login'))
    assert response.status_code == 200
    assert b'Email Address' in response.data
    assert b'Password' in response.data