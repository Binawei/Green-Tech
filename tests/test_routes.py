import pytest
from flask import url_for


def test_view_greenhouses_requires_login(client):
    response = client.get(url_for('view_greenhouses'), follow_redirects=False)
    assert response.status_code == 302
    assert url_for('login') in response.location

def test_dashboard_requires_login(client):
    response = client.get(url_for('dashboard'), follow_redirects=False)
    assert response.status_code == 302
    assert url_for('login') in response.location

def test_dashboard_loads_admin(logged_in_admin_client, test_greenhouse1, ongoing_issue_gh1):
    response = logged_in_admin_client.get(url_for('dashboard'))
    assert response.status_code == 200
    assert b'Welcome, Test Admin!' in response.data
    assert bytes(test_greenhouse1.name, 'utf-8') in response.data
    # Check for the text part
    assert b'Ongoing Issues:' in response.data

    assert b'<strong>1</strong>' in response.data
    assert b'id="issue-alert-modal"' not in response.data


def test_dashboard_loads_regular_user(logged_in_regular_client, test_greenhouse1):
    response = logged_in_regular_client.get(url_for('dashboard'))
    assert response.status_code == 200
    assert b'Welcome, Test User!' in response.data
    assert b'Employees' not in response.data
    assert bytes(test_greenhouse1.name, 'utf-8') in response.data
    assert b'id="issue-alert-modal"' not in response.data

def test_dashboard_alert_modal_appears(logged_in_user_gh1_client, ongoing_issue_gh1):
     response = logged_in_user_gh1_client.get(url_for('dashboard'))
     assert response.status_code == 200
     assert b'Welcome, User GH1!' in response.data
     # Check modal HTML is present in the response
     assert b'id="issue-alert-modal"' in response.data
     assert b'Issue Alert: GH Test Alpha' in response.data # Check title uses GH name
     assert bytes(ongoing_issue_gh1.description, 'utf-8') in response.data

def test_dashboard_alert_modal_not_appears_if_resolved(logged_in_user_gh1_client, resolved_issue_gh1):
     # user_gh1 is assigned to test_greenhouse1 which only has a resolved issue
     response = logged_in_user_gh1_client.get(url_for('dashboard'))
     assert response.status_code == 200
     assert b'id="issue-alert-modal"' not in response.data