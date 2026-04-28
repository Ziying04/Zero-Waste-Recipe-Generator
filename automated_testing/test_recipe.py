import pytest
from django.test import Client

# --- Test 1: Home Page Loads ---
@pytest.mark.django_db
def test_home_page():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


# --- Test 2: Recipe Generation Logic (Mock) ---
def generate_recipe(ingredients):
    return f"Recipe using {ingredients}"

def test_generate_recipe():
    result = generate_recipe("chicken, rice")
    assert "chicken" in result


# --- Test 3: Ingredient Expiry Logic ---
def is_expiring(days_left):
    return days_left <= 2

def test_expiry_logic():
    assert is_expiring(1) == True
    assert is_expiring(5) == False


# --- Test 4: Dashboard Access (if login required) ---
@pytest.mark.django_db
def test_home_page():
    client = Client()
    response = client.get("/")
    assert response.status_code == 200


# --- Test Admin Dashboard ---
@pytest.mark.django_db
def test_admin_dashboard():
    client = Client()
    response = client.get("/admin-dashboard/")
    assert response.status_code in [200, 302]


# --- Test Seeker Dashboard ---
@pytest.mark.django_db
def test_seeker_dashboard():
    client = Client()
    response = client.get("/community/seekers/")
    assert response.status_code in [200, 302]


# --- Test Donor Dashboard ---
@pytest.mark.django_db
def test_donor_dashboard():
    client = Client()
    response = client.get("/community/donors/")
    assert response.status_code in [200, 302]

# --- Ingredien Tracker ---
@pytest.mark.django_db
def test_ingredient_tracker_page():
    client = Client()
    response = client.get("/ingredients/")
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_add_ingredient():
    client = Client()
    response = client.post("/ingredients/add_ingredient/", {
        "name": "Milk",
        "expiry_date": "2026-05-01"
    })
    assert response.status_code in [200, 302]

#--- Community Feature Test ---
@pytest.mark.django_db
def test_community_page():
    client = Client()
    response = client.get("/community/")
    assert response.status_code in [200, 302]

#--- Test Recipe Feature ---
@pytest.mark.django_db
def test_recipe_generator_page():
    client = Client()
    response = client.get("/api/generate/")
    assert response.status_code in [200, 302]


#@pytest.mark.django_db
#def test_recipe_ai():
#    client = Client()
#    response = client.post("/api/recipe_ai/", {
#        "ingredients": "chicken, rice"
#    })
#    assert response.status_code in [200, 302]

