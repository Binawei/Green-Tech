from datetime import datetime

import pytest
from models import Employee, Greenhouse, Issue, EnvironmentalData
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
    """Test assigning an employee to a greenhouse (Many-to-Many)."""
    gh = Greenhouse(name="Test GH Beta", location="Lab Bench 2")

    company_id = generate_unique_company_id()
    user = Employee(
        # Use data from the fixture dictionary
        name=regular_user_data['name'],
        email=regular_user_data['email'],
        company_id=company_id,
    )
    user.set_password(regular_user_data['password'])

    user.greenhouses.append(gh)

    session.add(user)
    session.commit()

    # --- Query back to check relationships ---
    queried_user = Employee.query.filter_by(email=regular_user_data['email']).first()
    queried_gh = Greenhouse.query.get(gh.id)

    assert queried_user is not None
    assert len(queried_user.greenhouses) == 1
    assert queried_user.greenhouses[0].id == gh.id
    assert queried_user.greenhouses[0].name == "Test GH Beta"

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


@pytest.fixture
def ongoing_issue_gh1(session, test_greenhouse1):
    """Create an ongoing issue for greenhouse 1"""
    issue = Issue(greenhouse_id=test_greenhouse1.id, description="Alpha Temp High", status="Ongoing")
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def resolved_issue_gh1(session, test_greenhouse1):
    """Create a resolved issue for greenhouse 1"""
    issue = Issue(
        greenhouse_id=test_greenhouse1.id,
        description="Alpha Humidity Low (Resolved)",
        status="Resolved",
        created_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        resolved_at=datetime.datetime.utcnow()
    )
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def ongoing_issue_gh2(session, test_greenhouse2):
    """Create an ongoing issue for greenhouse 2"""
    issue = Issue(greenhouse_id=test_greenhouse2.id, description="Beta CO2 High", status="Ongoing")
    session.add(issue)
    session.commit()
    return issue

@pytest.fixture
def manual_data_gh1(session, test_greenhouse1):
    """Create manual env data for greenhouse 1"""
    data = EnvironmentalData(
        greenhouse_id=test_greenhouse1.id, source='manual',
        temperature=26, humidity=65, co2=1100, light_intensity=9000, soil_ph=6.8, soil_moisture=50
    )
    session.add(data)
    session.commit()
    return data

@pytest.fixture
def manual_data_gh2(session, test_greenhouse2):
    """Create manual env data for greenhouse 2"""
    data = EnvironmentalData(
        greenhouse_id=test_greenhouse2.id, source='manual',
        temperature=21, humidity=45, co2=750, light_intensity=11000, soil_ph=6.2, soil_moisture=35
    )
    session.add(data)
    session.commit()
    return data

@pytest.fixture
def resolution_data_gh1(session, test_greenhouse1):
    """Create resolution env data for greenhouse 1"""
    data = EnvironmentalData(
        greenhouse_id=test_greenhouse1.id, source='resolution',
        temperature=22, humidity=50, co2=800, light_intensity=5000, soil_ph=6.5, soil_moisture=45
    )
    session.add(data)
    session.commit()
    return data