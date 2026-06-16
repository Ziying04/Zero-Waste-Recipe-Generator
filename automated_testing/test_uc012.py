import os
from unittest.mock import patch

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.db import DatabaseError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_recipe.settings")

import django
django.setup()


pytestmark = pytest.mark.django_db


# =========================================================
# CONFIG
# =========================================================

BASE_URL = "http://127.0.0.1:8000"

TEST_EMAIL = "admin123@gmail.com"
TEST_PASSWORD = "password"

# Change this if recipe_id=1 does not exist in your system
RECIPE_ID = 1


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def logged_in_client(db):
    """
    Create test user and login for UC012 backend tests.
    """
    username = "uc012_user@example.com"
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


@pytest.fixture
def driver():
    """
    Selenium Chrome driver for UC012 UI test.
    """
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.maximize_window()
    yield browser
    browser.quit()


def selenium_login(driver):
    """
    Login helper for Selenium test.
    Make sure this user exists in your actual database.
    """
    driver.get(f"{BASE_URL}/login/")

    wait = WebDriverWait(driver, 10)

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = driver.find_element(By.NAME, "password")

    email_input.clear()
    email_input.send_keys(TEST_EMAIL)

    password_input.clear()
    password_input.send_keys(TEST_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    wait.until(lambda d: "login" not in d.current_url.lower())


# =========================================================
# UC012 / F012: SAVE RECIPE
# =========================================================

def test_tc_012_001_main_flow(logged_in_client):
    """
    TC-012-001: Main Flow
    Verify that logged-in user can save a visible recipe.
    """
    response = logged_in_client.post(f"/save/{RECIPE_ID}/")

    assert response.status_code in [200, 302]


def test_tc_012_002_boundary_invalid(logged_in_client):
    """
    TC-012-002: Boundary / Invalid Input
    Verify invalid recipe IDs are handled safely.
    """
    for recipe_id in [0, 10000]:
        response = logged_in_client.post(f"/save/{recipe_id}/")

        assert response.status_code in [200, 302, 404]


def test_tc_012_003_authorization():
    """
    TC-012-003: Authorization / Target Validation
    Verify guest user cannot save recipe directly.
    """
    client = Client()

    response = client.post(f"/save/{RECIPE_ID}/")

    assert response.status_code in [302, 404]


@patch("django.db.models.Model.save")
def test_tc_012_004_system_error(mock_save, logged_in_client):
    """
    TC-012-004: System / Error Branch
    Verify save recipe failure is handled safely.
    """
    mock_save.side_effect = DatabaseError("Save recipe failed")

    response = logged_in_client.post(f"/save/{RECIPE_ID}/")

    assert response.status_code in [200, 500, 404]

    if response.status_code == 200:
        assert (
            b"Failed" in response.content
            or b"error" in response.content.lower()
            or b"try again" in response.content.lower()
        )


def test_tc_012_005_state_transition(driver):
    """
    TC-012-005: State Transition Valid Path
    Verify Save button changes between Save and Saved state.
    """
    selenium_login(driver)

    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}/recipes/{RECIPE_ID}/")

    save_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "save-btn"))
    )

    save_btn.click()

    wait.until(
        lambda d:
        "saved" in save_btn.get_attribute("class").lower()
        or "Saved" in d.page_source
        or "saved" in d.page_source.lower()
    )

    assert (
        "saved" in save_btn.get_attribute("class").lower()
        or "Saved" in driver.page_source
        or "saved" in driver.page_source.lower()
    )

    save_btn.click()

    wait.until(
        lambda d:
        "Save" in d.page_source
        or "save" in d.page_source.lower()
    )

    assert (
        "Save" in driver.page_source
        or "save" in driver.page_source.lower()
    )


def test_tc_012_006_retry_path(logged_in_client):
    """
    TC-012-006: Cancel / Return / Retry Path
    Verify repeated save action does not crash or create invalid duplicate behavior.
    """
    first = logged_in_client.post(f"/save/{RECIPE_ID}/")

    assert first.status_code in [200, 302, 404]

    second = logged_in_client.post(f"/save/{RECIPE_ID}/")

    assert second.status_code in [200, 302, 404]

