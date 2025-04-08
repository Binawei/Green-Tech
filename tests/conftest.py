import pytest

from app import app as flask_app
from models import db as _db
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