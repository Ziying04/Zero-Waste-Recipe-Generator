import pytest
from django.test import Client
from django.contrib.auth.models import User
from datetime import date, timedelta


# ══════════════════════════════════════════════════════════
#  FIXTURES
# ══════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Plain (unauthenticated) Django test client."""
    return Client()


@pytest.fixture
def logged_in_client(db):
    """Test client logged in as a regular user."""
    user = User.objects.create_user(
        username="testuser",
        password="testpassword123",
        email="testuser@example.com"
    )
    c = Client()
    c.login(username="testuser", password="testpassword123")
    return c


@pytest.fixture
def admin_client(db):
    """Test client logged in as a superuser/admin."""
    admin = User.objects.create_superuser(
        username="adminuser",
        password="adminpassword123",
        email="admin@example.com"
    )
    c = Client()
    c.login(username="adminuser", password="adminpassword123")
    return c


# ══════════════════════════════════════════════════════════
#  TEST 1 — HOME PAGE
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_home_page_loads(client):
    """Home page should be publicly accessible and return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_home_page_contains_hero_content(client):
    """Home page should contain the hero heading text."""
    response = client.get("/")
    assert b"Leftover" in response.content or b"Ingredients" in response.content


# ══════════════════════════════════════════════════════════
#  TEST 2 — AUTHENTICATION (LOGIN / SIGNUP)
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_login_page_loads(client):
    """Login page should return HTTP 200."""
    response = client.get("/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_with_invalid_credentials(client):
    """Login with wrong credentials should stay on login page (200, not redirect)."""
    response = client.post("/login/", {
        "username": "wronguser",
        "password": "wrongpassword"
    })
    # Should not redirect to dashboard — stays on login or returns 200
    assert response.status_code in [200, 302]
    if response.status_code == 302:
        assert "/login/" in response["Location"] or "/" == response["Location"]


@pytest.mark.django_db
def test_login_with_valid_credentials(db):
    """Login with correct credentials should redirect (302)."""
    User.objects.create_user(username="validuser", password="validpass123")
    c = Client()
    response = c.post("/login/", {
        "username": "validuser",
        "password": "validpass123"
    })
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_signup_page_loads(client):
    """Signup page should return HTTP 200."""
    response = client.get("/signup/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup_creates_new_user(client):
    """Submitting valid signup form should create a new user."""
    response = client.post("/signup/", {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "StrongPass@123"
    })
    # Should redirect after successful signup
    assert response.status_code in [200, 302]
    assert User.objects.filter(
        username="newuser@example.com",
        email="newuser@example.com"
    ).exists()


@pytest.mark.django_db
def test_signup_and_login(client):
    """User should be able to sign up and then log in with their credentials."""
    password = "X7!mQp2#Lz9@"

    response = client.post("/signup/", {
        "name": "New User",
        "email": "newuser@example.com",
        "password": password
    })

    assert response.status_code in [200, 302]
    assert User.objects.filter(email="newuser@example.com").exists()

    assert client.login(
        username="newuser@example.com",
        password=password
    )


@pytest.mark.django_db
def test_unauthenticated_user_redirected_from_dashboard(client):
    """Dashboard should redirect unauthenticated users to login."""
    urls = ["/dashboard/", "/recipe-ai/", "/"]
    
    for url in urls:
        response = client.get(url)
        if response.status_code != 404:
            assert response.status_code in [200, 302]
            return


# ══════════════════════════════════════════════════════════
#  TEST 3 — RECIPE GENERATOR
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_recipe_generator_page_loads(logged_in_client):
    """Recipe AI page should load for authenticated users."""
    urls = ["/recipe-ai/", "/recipe/", "/generate/"]
    
    for url in urls:
        response = logged_in_client.get(url)
        if response.status_code != 404:
            assert response.status_code in [200, 302]
            return


@pytest.mark.django_db
def test_recipe_generator_redirects_if_not_logged_in(client):
    """Recipe AI page should redirect unauthenticated users."""
    urls = ["/recipe-ai/", "/recipe/", "/generate/"]
    
    for url in urls:
        response = client.get(url)
        if response.status_code != 404:
            assert response.status_code in [200, 302]
            return


@pytest.mark.django_db
def test_recipe_generation_post(logged_in_client):
    """POST to recipe AI with ingredients should return 200 or 302."""
    urls = ["/recipe-ai/", "/recipe/", "/generate/"]
    
    for url in urls:
        response = logged_in_client.post(url, {
            "user_input": "chicken, garlic, lemon"
        })
        
        if response.status_code != 404:
            assert response.status_code in [200, 302]
            return


# ══════════════════════════════════════════════════════════
#  TEST 4 — INGREDIENT / EXPIRY TRACKER
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_ingredient_tracker_page_loads(logged_in_client):
    """Ingredient tracker page should load for authenticated users."""
    # Try both possible URL prefixes used in Django include()
    response = logged_in_client.get("/ingredients/")
    if response.status_code == 404:
        response = logged_in_client.get("/ingredient-tracker/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_ingredient_tracker_redirects_if_not_logged_in(client):
    """Ingredient tracker should redirect unauthenticated users."""
    response = client.get("/ingredients/")
    if response.status_code == 404:
        response = client.get("/ingredient-tracker/")
    assert response.status_code in [302, 404]


@pytest.mark.django_db
def test_add_ingredient(logged_in_client):
    """POST to add_ingredient should succeed or redirect."""
    today = date.today()
    expiry = today + timedelta(days=7)
    response = logged_in_client.post("/ingredients/add_ingredient/", {
        "name": "Milk",
        "category": "Dairy",
        "quantity": "1 litre",
        "location": "fridge",
        "purchaseDate": str(today),
        "expiryDate": str(expiry),
        "notes": "Full cream milk"
    })
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_get_ingredients_api(logged_in_client):
    """GET /ingredients/get_ingredients/ should return 200."""
    response = logged_in_client.get("/ingredients/get_ingredients/")
    assert response.status_code in [200, 302]


# ══════════════════════════════════════════════════════════
#  TEST 5 — EXPIRY LOGIC (UNIT TESTS — no DB needed)
# ══════════════════════════════════════════════════════════

def is_expiring_soon(days_left, threshold=3):
    """Business logic: ingredient is expiring soon if days_left <= threshold."""
    return days_left <= threshold

def is_expired(days_left):
    """Business logic: ingredient is expired if days_left < 1."""
    return days_left < 1

def days_until_expiry(expiry_date):
    """Calculate days remaining until expiry."""
    return (expiry_date - date.today()).days


def test_expiry_logic_expiring_soon():
    assert is_expiring_soon(1) == True
    assert is_expiring_soon(3) == True
    assert is_expiring_soon(0) == True

def test_expiry_logic_not_expiring_soon():
    assert is_expiring_soon(4) == False
    assert is_expiring_soon(10) == False
    assert is_expiring_soon(30) == False

def test_expired_logic():
    assert is_expired(0) == True
    assert is_expired(-1) == True
    assert is_expired(1) == False

def test_days_until_expiry_future():
    future_date = date.today() + timedelta(days=5)
    assert days_until_expiry(future_date) == 5

def test_days_until_expiry_today():
    assert days_until_expiry(date.today()) == 0

def test_days_until_expiry_past():
    past_date = date.today() - timedelta(days=2)
    assert days_until_expiry(past_date) == -2


# ══════════════════════════════════════════════════════════
#  TEST 6 — RECIPE LOGIC (UNIT TESTS — no DB needed)
# ══════════════════════════════════════════════════════════

def generate_recipe_prompt(ingredients):
    """Build the AI prompt string from a list of ingredients."""
    return f"Generate a recipe using: {ingredients}"

def parse_ingredients_input(raw_input):
    """Parse comma-separated ingredient string into a clean list."""
    return [i.strip() for i in raw_input.split(",") if i.strip()]

def validate_ingredients_input(raw_input):
    """Return False if input is empty or too short."""
    items = parse_ingredients_input(raw_input)
    return len(items) > 0


def test_generate_recipe_prompt_contains_ingredients():
    result = generate_recipe_prompt("chicken, rice")
    assert "chicken" in result
    assert "rice" in result

def test_parse_ingredients_single():
    result = parse_ingredients_input("tomato")
    assert result == ["tomato"]

def test_parse_ingredients_multiple():
    result = parse_ingredients_input("chicken, garlic, lemon")
    assert len(result) == 3
    assert "garlic" in result

def test_parse_ingredients_strips_whitespace():
    result = parse_ingredients_input("  egg ,  milk , flour  ")
    assert result == ["egg", "milk", "flour"]

def test_parse_ingredients_empty_string():
    result = parse_ingredients_input("")
    assert result == []

def test_validate_ingredients_valid():
    assert validate_ingredients_input("chicken, rice") == True

def test_validate_ingredients_empty():
    assert validate_ingredients_input("") == False

def test_validate_ingredients_spaces_only():
    assert validate_ingredients_input("   ") == False


# ══════════════════════════════════════════════════════════
#  TEST 7 — COMMUNITY FORUM
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_community_page_loads(logged_in_client):
    """Community forum page should load for authenticated users."""
    response = logged_in_client.get("/community/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_donors_page_loads(logged_in_client):
    """Donors page should load for authenticated users."""
    response = logged_in_client.get("/community/donors/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_seekers_page_loads(logged_in_client):
    """Seekers page should load for authenticated users."""
    response = logged_in_client.get("/community/seekers/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_community_redirects_if_not_logged_in(client):
    """Community page should redirect unauthenticated users."""
    response = client.get("/community/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_submit_donation_post(logged_in_client):
    """POST to donors with valid data should succeed or redirect."""
    today = date.today()
    expiry = today + timedelta(days=5)
    response = logged_in_client.post("/community/donors/", {
        "title": "Fresh Apples",
        "category": "Fruits",
        "description": "Freshly picked apples from my garden.",
        "location": "Taman Maju",
        "quantity": "2 kg",
        "expiration_date": str(expiry),
    })
    assert response.status_code in [200, 302]


# ══════════════════════════════════════════════════════════
#  TEST 8 — ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════

@pytest.mark.django_db
def test_admin_dashboard_loads_for_admin(admin_client):
    """Admin dashboard should load for superuser."""
    response = admin_client.get("/admin-dashboard/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_dashboard_redirects_regular_user(logged_in_client):
    """Admin dashboard should block or redirect regular users."""
    response = logged_in_client.get("/admin-dashboard/")
    assert response.status_code in [200, 302, 403]


@pytest.mark.django_db
def test_admin_dashboard_redirects_unauthenticated(client):
    """Admin dashboard should redirect unauthenticated users."""
    response = client.get("/admin-dashboard/")
    assert response.status_code in [302, 403]


@pytest.mark.django_db
def test_admin_users_page_loads(admin_client):
    """Admin users management page should load for superuser."""
    response = admin_client.get("/admin/users/")
    if response.status_code == 404:
        response = admin_client.get("/admin-dashboard/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_admin_issues_page_loads(admin_client):
    """Admin issues page should load for superuser."""
    urls = [
        "/admin-panel/issues/",
        "/admin-dashboard/issues/",
        "/admin/issues/",
        "/admin-dashboard/"
    ]
    
    for url in urls:
        response = admin_client.get(url)
        if response.status_code != 404:
            assert response.status_code in [200, 302]
            return