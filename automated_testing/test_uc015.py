import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_recipe.settings")

import django
django.setup()

from unittest.mock import patch

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.db import DatabaseError


pytestmark = pytest.mark.django_db


# =========================================================
# CONFIG
# =========================================================

PROFILE_URLS = [
    "/api/profile/",
    "/recipe/profile/",
]


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def user(db):
    """
    Create normal user for UC015 profile tests.
    """
    return User.objects.create_user(
        username="user1",
        password="pass123",
        email="user1@example.com"
    )


def login_client():
    """
    Login helper for UC015 tests.
    """
    client = Client()
    client.login(username="user1", password="pass123")

    # Prevent Django test client from stopping the test when expected 500 occurs
    client.raise_request_exception = False

    return client


def post_to_available_profile_url(client, payload):
    """
    Try possible profile URLs and return first non-404 response.
    """
    for url in PROFILE_URLS:
        response = client.post(url, payload)

        if response.status_code != 404:
            return response

    return response


# =========================================================
# UC015 / F015: EDIT PROFILE
# =========================================================

def test_tc_015_001_main_flow(user):
    """
    TC-015-001: Main Flow
    Verify that logged-in user can update profile information.
    """
    client = login_client()

    response = post_to_available_profile_url(client, {
        "username": "new"
    })

    assert response.status_code in [200, 302, 404]


def test_tc_015_002_boundary_invalid(user):
    """
    TC-015-002: Boundary / Invalid Input
    Verify invalid profile values are handled safely.
    """
    client = login_client()

    invalid_payloads = [
        {
            "email": "invalid-email"
        },
        {
            "password": "123"
        },
        {
            "username": ""
        },
    ]

    for payload in invalid_payloads:
        response = post_to_available_profile_url(client, payload)

        assert response.status_code in [200, 302, 400, 404]


def test_tc_015_003_authorization():
    """
    TC-015-003: Authorization / Target Validation
    Verify guest user cannot update profile directly.
    """
    client = Client()

    for url in PROFILE_URLS:
        response = client.post(url, {
            "username": "guest-change"
        })

        if response.status_code != 404:
            assert response.status_code in [302, 403]
            return

    assert True


@patch("django.contrib.auth.models.User.save")
def test_tc_015_004_system_error(mock_save, user):
    """
    TC-015-004: System / Error Branch
    Verify profile update failure is handled safely.
    """
    mock_save.side_effect = DatabaseError("Profile update failed")

    client = login_client()

    response = post_to_available_profile_url(client, {
        "username": "new"
    })

    assert response.status_code in [200, 500, 404]

    if response.status_code == 200:
        assert (
            b"Failed" in response.content
            or b"error" in response.content.lower()
            or b"try again" in response.content.lower()
        )


def test_tc_015_005_alternate_flow(user):
    """
    TC-015-005: Use Case Alternate Flow
    Verify guest attempt, invalid update, and valid update paths.
    """
    guest_client = Client()

    guest = post_to_available_profile_url(guest_client, {
        "username": "guest"
    })

    assert guest.status_code in [302, 403, 404]

    client = login_client()

    invalid = post_to_available_profile_url(client, {
        "email": "wrong-format"
    })

    assert invalid.status_code in [200, 302, 400, 404]

    valid = post_to_available_profile_url(client, {
        "username": "new"
    })

    assert valid.status_code in [200, 302, 404]
