import pytest

from app import app as flask_app
from models import db as _db, Employee, Greenhouse
from config import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Session-wide test `Flask` application."""
    flask_app.config.from_object(TestingConfig)
    ctx = flask_app.app_context()
    ctx.push()
    yield flask_app
    ctx.pop()

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def default_password():
    """Provides a default password string for tests."""
    return "password123"

import pytest
import os
import datetime
from app import app as flask_app
# Import specific models needed
from models import db as _db, Employee, Greenhouse, Issue, EnvironmentalData
from config import TestingConfig
from app import generate_unique_company_id

# ... (app, client, runner, db, session, default_password fixtures) ...

# --- CORRECTED Data Fixtures ---
@pytest.fixture
def admin_user_data(): # Keep data fixtures separate
    return { 'name': "Test Admin", 'email': "admin@test.com"}

@pytest.fixture
def regular_user_data(): # Keep data fixtures separate
     return { 'name': "Test User", 'email': "user@test.com"}

@pytest.fixture
def admin_user(session, default_password):
    """Creates an admin user in the test DB."""
    admin = Employee() # Create instance first
    admin.name="Test Admin"
    admin.email="admin@test.com"
    admin.company_id=generate_unique_company_id()
    admin.is_admin=True
    admin.available=True
    admin.phone_number="111-111-1111"
    admin.set_password(default_password) # Set password via method
    session.add(admin)
    session.commit()
    return admin

@pytest.fixture
def regular_user(session, default_password):
    """Creates a regular user in the test DB."""
    user = Employee() # Create instance first
    user.name="Test User"
    user.email="user@test.com"
    user.company_id=generate_unique_company_id()
    user.is_admin=False
    user.available=True
    user.phone_number="222-222-2222"
    user.set_password(default_password)
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def test_greenhouse1(session):
    """Creates a greenhouse in the test DB."""
    gh = Greenhouse() # Create instance first
    gh.name="GH Test Alpha"
    gh.location="Lab A"
    # Don't set status if removed, or set default if kept
    # gh.status = "Operational"
    session.add(gh)
    session.commit()
    return gh

@pytest.fixture
def test_greenhouse2(session):
    """Creates a second greenhouse in the test DB."""
    gh = Greenhouse() # Create instance first
    gh.name="GH Test Beta"
    gh.location="Lab B"
    session.add(gh)
    session.commit()
    return gh

@pytest.fixture
def user_assigned_gh1(session, default_password, test_greenhouse1):
    """User specifically assigned only to test_greenhouse1"""
    user = Employee() # Create instance first
    user.name="User GH1"
    user.email="user_gh1@test.com"
    user.company_id=generate_unique_company_id()
    user.is_admin=False
    user.set_password(default_password)
    user.greenhouses.append(test_greenhouse1) # Assign relationship
    session.add(user)
    session.commit()
    return user

@pytest.fixture
def user_assigned_both(session, default_password, test_greenhouse1, test_greenhouse2):
    """User assigned to both test greenhouses"""
    user = Employee() # Create instance first
    user.name="User Both"
    user.email="user_both@test.com"
    user.company_id=generate_unique_company_id()
    user.is_admin=False
    user.set_password(default_password)
    user.greenhouses.append(test_greenhouse1) # Assign relationships
    user.greenhouses.append(test_greenhouse2)
    session.add(user)
    session.commit()
    return user


@pytest.fixture
def ongoing_issue_gh1(session, test_greenhouse1):
    """Create an ongoing issue for greenhouse 1"""
    issue = Issue() # Create instance first
    issue.greenhouse_id=test_greenhouse1.id
    issue.description="Alpha Temp High"
    issue.status="Ongoing"
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def resolved_issue_gh1(session, test_greenhouse1):
    """Create a resolved issue for greenhouse 1"""
    issue = Issue() # Create instance first
    issue.greenhouse_id=test_greenhouse1.id
    issue.description="Alpha Humidity Low (Resolved)"
    issue.status="Resolved"
    issue.created_at=datetime.datetime.utcnow() - datetime.timedelta(days=1)
    issue.resolved_at=datetime.datetime.utcnow()
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def ongoing_issue_gh2(session, test_greenhouse2):
    """Create an ongoing issue for greenhouse 2"""
    issue = Issue() # Create instance first
    issue.greenhouse_id=test_greenhouse2.id
    issue.description="Beta CO2 High"
    issue.status="Ongoing"
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def manual_data_gh1(session, test_greenhouse1):
    """Create manual env data for greenhouse 1"""
    data = EnvironmentalData() # Create instance first
    data.greenhouse_id=test_greenhouse1.id
    data.source='manual'
    data.temperature=26
    data.humidity=65
    data.co2=1100
    data.light_intensity=9000
    data.soil_ph=6.8
    data.soil_moisture=50
    session.add(data)
    session.commit()
    return data

@pytest.fixture
def manual_data_gh2(session, test_greenhouse2):
    """Create manual env data for greenhouse 2"""
    data = EnvironmentalData() # Create instance first
    data.greenhouse_id=test_greenhouse2.id
    # ... set attributes ...
    session.add(data)
    session.commit()
    return data

@pytest.fixture
def resolution_data_gh1(session, test_greenhouse1):
    """Create resolution env data for greenhouse 1"""
    data = EnvironmentalData() # Create instance first
    data.greenhouse_id=test_greenhouse1.id
    # ... set attributes ...
    session.add(data)
    session.commit()
    return data
# --- ADD THESE LOGGED-IN CLIENT FIXTURES ---
@pytest.fixture
def logged_in_admin_client(client, admin_user, default_password):
    """Provides a test client logged in as the admin user."""
    # Perform login POST request
    client.post('/', data={
        'email': admin_user.email,
        'password': default_password
    }, follow_redirects=True) # follow_redirects might not be needed just to set session
    yield client # Provide the client object (now with session cookies)
    # Logout after the test using this fixture finishes
    client.get('/logout')


@pytest.fixture
def logged_in_regular_client(client, regular_user, default_password):
    """Provides a test client logged in as the regular user."""
    client.post('/', data={
        'email': regular_user.email,
        'password': default_password
    }, follow_redirects=True)
    yield client
    client.get('/logout')


@pytest.fixture
def logged_in_user_gh1_client(client, user_assigned_gh1, default_password):
    """Client logged in as user assigned ONLY to GH1"""
    client.post('/', data={
        'email': user_assigned_gh1.email,
        'password': default_password
    }, follow_redirects=True)
    yield client
    client.get('/logout')


@pytest.fixture(scope='function')
def db(app):
    """Function-scoped test database. Creates/drops tables for each test."""
    if app.config['SQLALCHEMY_DATABASE_URI'] is None:
        raise ValueError("SQLALCHEMY_DATABASE_URI not set for testing in config")

    # --- Setup ---
    _db.create_all()

    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    yield db.session


@pytest.fixture
def admin_user_data():
    return {
        'name': "Test Admin",
        'email': "admin@test.com",
        'password': "password123",
        'is_admin': True,
        'available': True
    }

@pytest.fixture
def regular_user_data():
     return {
        'name': "Test User",
        'email': "user@test.com",
        'password': "password123",
        'is_admin': False,
        'available': True
    }