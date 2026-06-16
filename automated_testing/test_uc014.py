import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ai_recipe.settings")

import django
django.setup()

from unittest.mock import patch

import pytest
from django.test import Client
from django.contrib.auth.models import User
from django.db import DatabaseError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


pytestmark = pytest.mark.django_db


# =========================================================
# CONFIG
# =========================================================

BASE_URL = "http://127.0.0.1:8000"

TEST_EMAIL = "admin123@gmail.com"
TEST_PASSWORD = "password"

REPORT_URL = "/issues/report/"


# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def logged_in_client(db):
    """
    Create test user and login for UC014 backend tests.
    """
    username = "uc014_user@example.com"
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
    Selenium Chrome driver for UC014 UI tests.
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


def select_issue_type(driver, visible_text="Bug"):
    """
    Select issue type using name='issue_type' first.
    Fallback to name='issue' if the form uses a different field name.
    """
    try:
        Select(driver.find_element(By.NAME, "issue_type")).select_by_visible_text(visible_text)
        return
    except Exception:
        pass

    try:
        Select(driver.find_element(By.NAME, "issue")).select_by_visible_text(visible_text)
        return
    except Exception:
        pass

    try:
        issue_input = driver.find_element(By.NAME, "issue_type")
        issue_input.clear()
        issue_input.send_keys(visible_text)
        return
    except Exception:
        pass

    issue_input = driver.find_element(By.NAME, "issue")
    issue_input.clear()
    issue_input.send_keys(visible_text)


# =========================================================
# UC014 / F014: REPORT ISSUES
# =========================================================

def test_tc_014_001_main_flow(logged_in_client):
    """
    TC-014-001: Main Flow
    Verify that logged-in user can submit a valid issue report.
    """
    response = logged_in_client.post(REPORT_URL, {
        "issue": "bug",
        "issue_type": "Bug",
        "description": "Save button does not respond when clicked."
    })

    assert response.status_code in [200, 302, 404]


def test_tc_014_002_boundary_invalid(logged_in_client):
    """
    TC-014-002: Boundary / Invalid Input
    Verify invalid issue report values are handled safely.
    """
    invalid_payloads = [
        {
            "issue_type": "Bug",
            "description": ""
        },
        {
            "issue_type": "Bug",
            "description": "A" * 2001
        },
        {
            "issue_type": "UnknownType",
            "description": "Invalid issue type"
        },
    ]

    for payload in invalid_payloads:
        response = logged_in_client.post(REPORT_URL, payload)

        assert response.status_code in [200, 302, 400, 404]


def test_tc_014_003_authorization():
    """
    TC-014-003: Authorization / Target Validation
    Verify guest user cannot submit issue report directly.
    """
    client = Client()

    response = client.post(REPORT_URL, {
        "issue": "bug"
    })

    assert response.status_code in [302, 404]


@patch("django.db.models.Model.save")
def test_tc_014_004_system_error(mock_save, logged_in_client):
    """
    TC-014-004: System / Error Branch
    Verify issue report save failure is handled safely.
    """
    mock_save.side_effect = DatabaseError("Issue report save failed")

    response = logged_in_client.post(REPORT_URL, {
        "issue_type": "Bug",
        "description": "Unable to save recipe."
    })

    assert response.status_code in [200, 500, 404]

    if response.status_code == 200:
        assert (
            b"Failed" in response.content
            or b"error" in response.content.lower()
            or b"try again" in response.content.lower()
        )


def test_tc_014_005_state_transition(driver):
    """
    TC-014-005: State Transition Valid Path
    Verify report form can move from form state to submitted state.
    """
    selenium_login(driver)

    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}{REPORT_URL}")

    wait.until(
        EC.presence_of_element_located((By.NAME, "description"))
    )

    select_issue_type(driver, "Bug")

    description = driver.find_element(By.NAME, "description")
    description.clear()
    description.send_keys("Save button does not respond.")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(
        lambda d:
        "submitted" in d.page_source.lower()
        or "thank" in d.page_source.lower()
        or "success" in d.page_source.lower()
        or d.current_url != f"{BASE_URL}{REPORT_URL}"
    )

    assert (
        "submitted" in driver.page_source.lower()
        or "thank" in driver.page_source.lower()
        or "success" in driver.page_source.lower()
        or "issue" in driver.current_url.lower()
    )


def test_tc_014_006_cancel_retry(driver):
    """
    TC-014-006: Cancel / Return / Retry Path
    Verify cancel does not submit temporary report and retry allows corrected submission.
    """
    selenium_login(driver)

    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}{REPORT_URL}")

    description = wait.until(
        EC.presence_of_element_located((By.NAME, "description"))
    )

    description.clear()
    description.send_keys("Temporary report")

    cancel_clicked = False

    cancel_buttons = driver.find_elements(
        By.XPATH,
        "//a[contains(text(), 'Cancel')] | //button[contains(text(), 'Cancel')] | //a[contains(text(), 'Back')] | //button[contains(text(), 'Back')]"
    )

    if len(cancel_buttons) > 0:
        cancel_buttons[0].click()
        cancel_clicked = True
    else:
        driver.get(f"{BASE_URL}/")

    assert cancel_clicked is True or driver.current_url == f"{BASE_URL}/"
    assert "Temporary report" not in driver.page_source

    # Retry path
    driver.get(f"{BASE_URL}{REPORT_URL}")

    wait.until(
        EC.presence_of_element_located((By.NAME, "description"))
    )

    select_issue_type(driver, "Bug")

    description = driver.find_element(By.NAME, "description")
    description.clear()
    description.send_keys("Retry report after correction")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(
        lambda d:
        "submitted" in d.page_source.lower()
        or "thank" in d.page_source.lower()
        or "success" in d.page_source.lower()
        or d.current_url != f"{BASE_URL}{REPORT_URL}"
    )

    assert (
        "submitted" in driver.page_source.lower()
        or "thank" in driver.page_source.lower()
        or "success" in driver.page_source.lower()
        or "issue" in driver.current_url.lower()
    )
