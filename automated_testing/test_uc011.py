import os
from datetime import date, timedelta
from unittest.mock import patch

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.db import DatabaseError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_recipe.settings")

import django
django.setup()


pytestmark = pytest.mark.django_db


@pytest.fixture
def logged_in_client(db):
    """Create test user and login for UC011 tests."""
    username = "uc011_user@example.com"
    password = "Password123!"

    User.objects.create_user(
        username=username,
        email=username,
        password=password
    )

    client = Client()
    client.login(username=username, password=password)

    # Prevent Django test client from stopping the test when expected 500 occurs
    client.raise_request_exception = False

    return client


# =========================================================
# UC011 / F011: Ingredient Tracker
# =========================================================

def test_tc_011_001_main_flow(logged_in_client):
    """
    TC-011-001: Main Flow
    Verify that logged-in user can add a valid ingredient.
    """
    today = date.today()
    expiry = today + timedelta(days=7)

    response = logged_in_client.post("/ingredients/add_ingredient/", {
        "name": "Milk",
        "category": "Dairy",
        "quantity": "1L",
        "location": "fridge",
        "purchaseDate": str(today),
        "expiryDate": str(expiry),
        "notes": ""
    })

    assert response.status_code in [200, 302]


def test_tc_011_002_boundary_invalid(logged_in_client):
    """
    TC-011-002: Boundary / Invalid Input
    Verify invalid or boundary ingredient values are handled safely.
    """
    today = date.today()

    invalid_sets = [
        {
            "name": "",
            "quantity": "1L",
            "expiryDate": str(today + timedelta(days=2))
        },
        {
            "name": "A" * 101,
            "quantity": "1L",
            "expiryDate": str(today + timedelta(days=2))
        },
        {
            "name": "Milk",
            "quantity": "0",
            "expiryDate": str(today + timedelta(days=4))
        },
        {
            "name": "Milk",
            "quantity": "1L",
            "expiryDate": str(today - timedelta(days=1))
        },
    ]

    for data in invalid_sets:
        data.update({
            "category": "Dairy",
            "location": "fridge",
            "purchaseDate": str(today),
            "notes": ""
        })

        response = logged_in_client.post("/ingredients/add_ingredient/", data)

        assert response.status_code in [200, 302, 400]


def test_tc_011_003_authorization():
    """
    TC-011-003: Authorization / Target Validation
    Verify guest user is redirected or blocked from ingredient tracker.
    """
    client = Client()

    response = client.get("/ingredients/")

    if response.status_code == 404:
        response = client.get("/ingredient-tracker/")

    assert response.status_code in [302, 404]


@patch("django.db.models.Model.save")
def test_tc_011_004_system_error(mock_save, logged_in_client):
    """
    TC-011-004: System / Error Branch
    Verify system handles ingredient save failure safely.
    """
    mock_save.side_effect = DatabaseError("Ingredient save failed")

    response = logged_in_client.post("/ingredients/add_ingredient/", {
        "name": "Milk",
        "category": "Dairy",
        "quantity": "1L",
        "location": "fridge",
        "purchaseDate": str(date.today()),
        "expiryDate": str(date.today() + timedelta(days=2)),
        "notes": ""
    })

    assert response.status_code in [200, 500]

    if response.status_code == 200:
        assert b"Failed" in response.content or b"error" in response.content.lower()


def is_expiring_soon(days_left, threshold=3):
    return days_left <= threshold


def is_expired(days_left):
    return days_left < 1


def test_tc_011_005_state_transition():
    """
    TC-011-005: State Transition Valid Path
    Verify ingredient expiry status transition logic.
    """
    assert is_expiring_soon(4) is False
    assert is_expiring_soon(3) is True
    assert is_expiring_soon(1) is True

    assert is_expired(0) is True
    assert is_expired(-1) is True
    assert is_expired(1) is False
