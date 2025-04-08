import pytest
from models import Employee, Greenhouse, Issue
from app import generate_unique_company_id

# Fixture 'session' is automatically injected from conftest.py

def test_create_employee(session, regular_user_data):
    """Test creating a basic employee."""
    company_id = generate_unique_company_id()
    user = Employee(
        name=regular_user_data['name'],
        email=regular_user_data['email'],
        company_id=company_id,
        is_admin=False,
        available=True
    )
    user.set_password(regular_user_data['password'])

    session.add(user)
    session.commit() # Commit within the test transaction

    assert user.id is not None
    assert user.name == regular_user_data['name']
    assert user.check_password(regular_user_data['password']) is True
    assert user.check_password("wrongpassword") is False
    assert user.is_admin is False

def test_create_greenhouse(session):
    """Test creating a greenhouse."""
    gh = Greenhouse(name="Test GH Alpha", location="Lab Bench 1")
    session.add(gh)
    session.commit()

    assert gh.id is not None
    assert gh.name == "Test GH Alpha"
    assert len(gh.issues) == 0

def test_greenhouse_employee_relationship(session, regular_user_data):
    """Test assigning an employee to a greenhouse."""
    gh = Greenhouse(name="Test GH Beta", location="Lab Bench 2")
    session.add(gh)
    session.commit() # Commit GH first to get its ID

    company_id = generate_unique_company_id()
    user = Employee(
        name=regular_user_data['name'],
        email=regular_user_data['email'],
        company_id=company_id,
        greenhouse_id=gh.id
    )
    user.set_password(regular_user_data['password'])
    session.add(user)
    session.commit()

    # Query back to check relationships
    queried_user = Employee.query.filter_by(email=regular_user_data['email']).first()
    queried_gh = Greenhouse.query.get(gh.id)

    assert queried_user is not None
    assert queried_user.assigned_greenhouse is not None
    assert queried_user.assigned_greenhouse.id == gh.id
    assert queried_user.assigned_greenhouse.name == "Test GH Beta"

    assert queried_gh is not None
    assert len(queried_gh.employees) == 1
    assert queried_gh.employees[0].email == regular_user_data['email']

def test_create_issue(session):
    """Test creating an issue associated with a greenhouse."""
    gh = Greenhouse(name="Test GH Gamma", location="Roof")
    session.add(gh)
    session.commit()

    issue = Issue(
        greenhouse_id=gh.id,
        description="Temperature too high!",
        status="Ongoing"
    )
    session.add(issue)
    session.commit()

    assert issue.id is not None
    assert issue.status == "Ongoing"
    assert issue.originating_greenhouse.id == gh.id

    queried_gh = Greenhouse.query.get(gh.id)
    assert len(queried_gh.issues) == 1
    assert queried_gh.issues[0].description == "Temperature too high!"