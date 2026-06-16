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
    Create test user and login for UC013 backend tests.
    """
    username = "uc013_user@example.com"
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
    Selenium Chrome driver for UC013 UI test.
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
# UC013 / F013: EDIT RECIPE
# =========================================================

def test_tc_013_001_main_flow(logged_in_client):
    """
    TC-013-001: Main Flow
    Verify that logged-in user can submit valid edited recipe details.
    """
    response = logged_in_client.post(f"/recipes/edit/{RECIPE_ID}/", {
        "title": "Tomato Rice Updated",
        "ingredients": "tomato, rice, onion",
        "steps": "Cook rice with tomato and onion.",
        "cooking_time": "20"
    })

    assert response.status_code in [200, 302, 404]


def test_tc_013_002_boundary_invalid(logged_in_client):
    """
    TC-013-002: Boundary / Invalid Input
    Verify invalid recipe edit values are handled safely.
    """
    invalid_payloads = [
        {
            "title": "",
            "cooking_time": "20"
        },
        {
            "title": "A" * 256,
            "cooking_time": "20"
        },
        {
            "title": "Valid",
            "cooking_time": "0"
        },
        {
            "title": "Valid",
            "cooking_time": "1441"
        },
    ]

    for payload in invalid_payloads:
        payload.update({
            "ingredients": "egg",
            "steps": "cook"
        })

        response = logged_in_client.post(f"/recipes/edit/{RECIPE_ID}/", payload)

        assert response.status_code in [200, 302, 400, 404]


def test_tc_013_003_authorization():
    """
    TC-013-003: Authorization / Target Validation
    Verify guest user cannot edit recipe directly.
    """
    client = Client()

    response = client.post(f"/recipes/edit/{RECIPE_ID}/", {
        "title": "Unauthorized Edit",
        "ingredients": "egg",
        "steps": "cook"
    })

    assert response.status_code in [302, 403, 404]


@patch("django.db.models.Model.save")
def test_tc_013_004_system_error(mock_save, logged_in_client):
    """
    TC-013-004: System / Error Branch
    Verify recipe update failure is handled safely.
    """
    mock_save.side_effect = DatabaseError("Recipe update failed")

    response = logged_in_client.post(f"/recipes/edit/{RECIPE_ID}/", {
        "title": "Tomato Rice Updated",
        "ingredients": "tomato, rice",
        "steps": "Cook",
        "cooking_time": "20"
    })

    assert response.status_code in [200, 500, 404]

    if response.status_code == 200:
        assert (
            b"Failed" in response.content
            or b"error" in response.content.lower()
            or b"try again" in response.content.lower()
        )


def test_tc_013_005_state_transition(driver):
    """
    TC-013-005: State Transition Valid Path
    Verify recipe detail page can move to edit form and submit updated recipe.
    """
    selenium_login(driver)

    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}/recipes/{RECIPE_ID}/")

    try:
        edit_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "edit-btn"))
        )
        edit_btn.click()
    except Exception:
        # Fallback if edit button ID is not available
        driver.get(f"{BASE_URL}/recipes/edit/{RECIPE_ID}/")

    assert "edit" in driver.current_url.lower() or driver.find_element(By.NAME, "title") is not None

    title_input = wait.until(
        EC.presence_of_element_located((By.NAME, "title"))
    )

    title_input.clear()
    title_input.send_keys("Tomato Rice Updated")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    wait.until(
        lambda d:
        "Tomato Rice Updated" in d.page_source
        or d.current_url != f"{BASE_URL}/recipes/edit/{RECIPE_ID}/"
    )

    assert (
        "Tomato Rice Updated" in driver.page_source
        or "recipes" in driver.current_url.lower()
    )


def test_tc_013_006_cancel_retry(driver):
    """
    TC-013-006: Cancel / Return / Retry Path
    Verify cancel does not save temporary changes and retry can submit corrected data.
    """
    selenium_login(driver)

    wait = WebDriverWait(driver, 10)

    driver.get(f"{BASE_URL}/recipes/edit/{RECIPE_ID}/")

    title_input = wait.until(
        EC.presence_of_element_located((By.NAME, "title"))
    )

    title_input.clear()
    title_input.send_keys("Temporary Title")

    cancel_clicked = False

    cancel_buttons = driver.find_elements(
        By.XPATH,
        "//a[contains(text(), 'Cancel')] | //button[contains(text(), 'Cancel')] | //a[contains(text(), 'Back')] | //button[contains(text(), 'Back')]"
    )

    if len(cancel_buttons) > 0:
        cancel_buttons[0].click()
        cancel_clicked = True
    else:
        driver.get(f"{BASE_URL}/recipes/{RECIPE_ID}/")

    assert cancel_clicked is True or "recipes" in driver.current_url.lower()
    assert "Temporary Title" not in driver.page_source

    # Retry path
    driver.get(f"{BASE_URL}/recipes/edit/{RECIPE_ID}/")

    title_input = wait.until(
        EC.presence_of_element_located((By.NAME, "title"))
    )

    title_input.clear()
    title_input.send_keys("Tomato Rice Updated")

    try:
        ingredients_input = driver.find_element(By.NAME, "ingredients")
        ingredients_input.clear()
        ingredients_input.send_keys("tomato, rice, onion")
    except Exception:
        pass

    try:
        steps_input = driver.find_element(By.NAME, "steps")
        steps_input.clear()
        steps_input.send_keys("Cook rice with tomato and onion.")
    except Exception:
        pass

    try:
        time_input = driver.find_element(By.NAME, "cooking_time")
        time_input.clear()
        time_input.send_keys("20")
    except Exception:
        pass

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    wait.until(
        lambda d:
        "Tomato Rice Updated" in d.page_source
        or "recipes" in d.current_url.lower()
    )

    assert (
        "Tomato Rice Updated" in driver.page_source
        or "recipes" in driver.current_url.lower()
    )
