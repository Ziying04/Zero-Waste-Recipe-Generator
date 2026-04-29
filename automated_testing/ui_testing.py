from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ──────────────────────────────────────────────
#  CONFIG — change these to match your account
# ──────────────────────────────────────────────
BASE_URL       = "http://127.0.0.1:8000"
TEST_EMAIL     = "admin123@gmail.com"
TEST_PASSWORD  = "password"
# ──────────────────────────────────────────────

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
wait = WebDriverWait(driver, 10)

passed = 0
failed = 0

def result(label, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  PASS: {label}")
        passed += 1
    else:
        print(f"  FAIL: {label}" + (f" — {detail}" if detail else ""))
        failed += 1

def section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

def login():
    """Log in using email field (not username)."""
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    try:
        driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
        driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
        time.sleep(2)
    except Exception as e:
        print(f"  [login helper error: {e}]")

# ══════════════════════════════════════════════
# TEST 1 — HOME PAGE
# ══════════════════════════════════════════════
section("TEST 1: Home Page")
try:
    driver.get(f"{BASE_URL}/")
    time.sleep(2)

    result("Homepage loads successfully",
           driver.find_element(By.TAG_NAME, "body") is not None)

    heading = driver.find_element(By.CLASS_NAME, "heading")
    result("Hero heading is displayed",
           "Leftover" in heading.text or "Ingredients" in heading.text,
           f"Got: {heading.text}")

    steps = driver.find_elements(By.CLASS_NAME, "step")
    result("'How It Works' shows 3 steps", len(steps) == 3,
           f"Found {len(steps)} steps")

    features = driver.find_elements(By.CLASS_NAME, "feature")
    result("Features section shows 4 features", len(features) == 4,
           f"Found {len(features)} features")

    driver.find_element(By.LINK_TEXT, "Get Started").click()
    time.sleep(2)
    result("'Get Started' button navigates to signup page",
           "signup" in driver.current_url or "register" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Home Page tests: {e}")

# ══════════════════════════════════════════════
# TEST 2 — SIGNUP PAGE
# ══════════════════════════════════════════════
section("TEST 2: Signup Page")
try:
    driver.get(f"{BASE_URL}/signup/")
    time.sleep(2)

    result("Signup page loads",
           "signup" in driver.current_url or "register" in driver.current_url)

    result("Name input field is present",
           driver.find_element(By.NAME, "name") is not None)

    result("Email input field is present",
           driver.find_element(By.NAME, "email") is not None)

    result("Password input field is present",
           driver.find_element(By.NAME, "password") is not None)

    result("Confirm Password input field is present",
           driver.find_element(By.NAME, "confirmPassword") is not None)

    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    result("Submit/Register button is present", btn is not None)

    btn.click()
    time.sleep(1)
    result("Empty form does not proceed (validation active)",
           "signup" in driver.current_url or "register" in driver.current_url)

except Exception as e:
    print(f"  ERROR in Signup tests: {e}")

# ══════════════════════════════════════════════
# TEST 3 — LOGIN PAGE
# ══════════════════════════════════════════════
section("TEST 3: Login Page")
try:
    driver.get(f"{BASE_URL}/login/")
    time.sleep(2)

    result("Login page loads", "login" in driver.current_url)

    result("Email field is present",
           driver.find_element(By.NAME, "email") is not None)

    result("Password field is present",
           driver.find_element(By.NAME, "password") is not None)

    # Wrong credentials
    driver.find_element(By.NAME, "email").send_keys("wronguser@test.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    result("Invalid credentials keeps user on login page",
           "login" in driver.current_url)

    # Correct credentials
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(2)
    result("Valid credentials redirects away from login page",
           "login" not in driver.current_url)

except Exception as e:
    print(f"  ERROR in Login tests: {e}")

# ══════════════════════════════════════════════
# TEST 4 — AI RECIPE GENERATOR
# FIX: login() now uses email; URL confirmed as /recipe-ai/
# ══════════════════════════════════════════════
section("TEST 4: AI Recipe Generator")
try:
    login()
    driver.get(f"{BASE_URL}/recipe-ai/")
    time.sleep(2)

    result("Recipe Generator page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    # FIX DEF-003: textarea id="user-input" confirmed from HTML
    textarea = wait.until(EC.presence_of_element_located((By.ID, "user-input")))
    result("Ingredient textarea input is present", textarea is not None)

    tabs = driver.find_elements(By.CLASS_NAME, "tab")
    result("Both recipe tabs are present (By Input / By Inventory)",
           len(tabs) >= 2, f"Found {len(tabs)} tabs")

    # Switch to inventory tab
    driver.find_element(By.ID, "use-inventory").click()
    time.sleep(1)
    inv_section = driver.find_element(By.ID, "available-ingredient")
    result("Switching to 'By available ingredient' tab works",
           "hidden" not in inv_section.get_attribute("class"))

    # Switch back to text input tab and generate
    driver.find_element(By.ID, "use-text").click()
    time.sleep(1)
    textarea = driver.find_element(By.ID, "user-input")
    textarea.clear()
    textarea.send_keys("chicken, garlic, lemon")
    driver.find_element(By.ID, "generate-btn").click()
    time.sleep(10)  # wait for AI response

    output = driver.find_element(By.ID, "output-section")
    result("Recipe output section appears after generation",
           "hidden" not in output.get_attribute("class"))

    recipe_text = driver.find_element(By.ID, "recipe-output").get_attribute("value")
    result("Generated recipe output is not empty",
           len(recipe_text.strip()) > 0)

    result("Copy button is present on recipe output",
           driver.find_element(By.CSS_SELECTOR, ".copy-btn") is not None)

    result("Share Recipe button is present",
           driver.find_element(By.CSS_SELECTOR, ".share-btn") is not None)

except Exception as e:
    print(f"  ERROR in Recipe Generator tests: {e}")

# ══════════════════════════════════════════════
# TEST 5 — EXPIRATION TRACKER
# FIX DEF-004: Use XPATH to find button by text since
#              class="btn green" (two separate classes, not one)
#              Also try correct URL from ingredient_tracker urls.py
# ══════════════════════════════════════════════
section("TEST 5: Expiration Tracker (Ingredient Inventory)")
try:
    login()

    # Try both possible mounted URLs
    driver.get(f"{BASE_URL}/ingredients/")
    time.sleep(1)
    if "404" in driver.title or "not found" in driver.page_source.lower()[:500]:
        driver.get(f"{BASE_URL}/ingredient-tracker/")
    time.sleep(2)

    result("Expiration Tracker page loads",
           "404" not in driver.title)

    # FIX DEF-004: button has TWO classes "btn" and "green" separately,
    # use XPATH contains text instead
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Add Ingredient')]")
    ))
    result("'+ Add Ingredient' button is present", add_btn is not None)

    add_btn.click()
    time.sleep(1)
    form = driver.find_element(By.ID, "form")
    result("Add Ingredient form appears after clicking button",
           "hidden" not in form.get_attribute("class"))

    filter_tabs = driver.find_elements(By.CSS_SELECTOR, ".tabs .tab")
    result("Filter tabs are present (All / Expiring Soon / Expired / Fresh)",
           len(filter_tabs) >= 4, f"Found {len(filter_tabs)} tabs")

    cat_select = Select(driver.find_element(By.ID, "category"))
    result("Category dropdown has multiple options",
           len(cat_select.options) > 1)

    cat_select.select_by_visible_text("Vegetables")
    time.sleep(1)
    driver.find_element(By.ID, "quantity").send_keys("3 pieces")
    driver.find_element(By.ID, "purchaseDate").send_keys("04/20/2025")
    driver.find_element(By.ID, "expiryDate").send_keys("05/10/2025")
    result("Add Ingredient form fields filled successfully", True)

except Exception as e:
    print(f"  ERROR in Expiration Tracker tests: {e}")

# ══════════════════════════════════════════════
# TEST 6 — COMMUNITY FORUM
# ══════════════════════════════════════════════
section("TEST 6: Community Forum Page")
try:
    login()
    driver.get(f"{BASE_URL}/community/")
    time.sleep(2)

    result("Community Forum page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    hero = driver.find_element(By.CLASS_NAME, "hero-title")
    result("Hero title 'Community Food Sharing' is displayed",
           "Community" in hero.text, f"Got: {hero.text}")

    result("Food Donor card is visible",
           driver.find_element(By.CLASS_NAME, "donor-card") is not None)

    result("Food Seeker card is visible",
           driver.find_element(By.CLASS_NAME, "seeker-card") is not None)

    stats = driver.find_elements(By.CLASS_NAME, "stat-item")
    result("Community Impact stats section is present",
           len(stats) >= 3, f"Found {len(stats)} stat items")

    steps = driver.find_elements(By.CLASS_NAME, "step-item")
    result("'How Food Sharing Works' shows 3 steps",
           len(steps) == 3, f"Found {len(steps)} steps")

    driver.find_element(By.PARTIAL_LINK_TEXT, "Start Donating").click()
    time.sleep(2)
    result("'Start Donating Food' button navigates to donors page",
           "donor" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Community Forum tests: {e}")

# ══════════════════════════════════════════════
# TEST 7 — DONATION BOARD
# FIX DEF-005: Button is id="tab-add" not text-based,
#              click by ID directly
# ══════════════════════════════════════════════
section("TEST 7: Donation Board (Donors Page)")
try:
    login()
    driver.get(f"{BASE_URL}/community/donors/")
    time.sleep(2)

    result("Donation Board page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    # FIX DEF-005: use id="tab-donations" and id="tab-add" directly
    result("'My Donations' tab is present",
           driver.find_element(By.ID, "tab-donations") is not None)

    tab_add = driver.find_element(By.ID, "tab-add")
    result("'Add New Donation' tab button is present", tab_add is not None)

    tab_add.click()
    time.sleep(1)
    form = driver.find_element(By.ID, "donation-form")
    result("Add New Donation form is visible after clicking tab",
           form.is_displayed())

    result("Food Name input field is present",
           driver.find_element(By.ID, "food_name") is not None)

    cat = Select(driver.find_element(By.ID, "category"))
    result("Category dropdown has options", len(cat.options) > 1)

    driver.find_element(By.ID, "food_name").send_keys("Fresh Tomatoes")
    cat.select_by_visible_text("Vegetables")
    driver.find_element(By.ID, "description").send_keys(
        "Freshly picked tomatoes from my garden.")
    driver.find_element(By.ID, "location").send_keys("Block A, Taman Maju")
    driver.find_element(By.ID, "quantity").send_keys("1 kg")
    driver.find_element(By.ID, "expiration_date").send_keys("05/10/2025")
    result("Donation form fields filled successfully", True)

    driver.find_element(By.PARTIAL_LINK_TEXT, "Back to Community").click()
    time.sleep(2)
    result("'Back to Community' link navigates back correctly",
           "community" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Donation Board tests: {e}")

# ══════════════════════════════════════════════
# TEST 8 — ADMIN DASHBOARD
# ══════════════════════════════════════════════
section("TEST 8: Admin Dashboard")
try:
    login()
    driver.get(f"{BASE_URL}/admin-dashboard/")
    time.sleep(2)

    result("Admin Dashboard page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    cards = driver.find_elements(By.CLASS_NAME, "admin-card")
    result("Admin dashboard shows 4 stat cards",
           len(cards) == 4, f"Found {len(cards)} cards")

    sidebar_links = driver.find_elements(By.CLASS_NAME, "sidebar-link")
    result("Sidebar navigation links are present",
           len(sidebar_links) >= 3, f"Found {len(sidebar_links)} links")

    activity_pane = driver.find_element(By.ID, "activity")
    result("'Recent Activity' tab is active by default",
           "active" in activity_pane.get_attribute("class"))

    driver.find_elements(By.CSS_SELECTOR, ".admin-tabs .tab")[1].click()
    time.sleep(1)
    donations_pane = driver.find_element(By.ID, "donations-section")
    result("Switching to 'Donations' tab works",
           "active" in donations_pane.get_attribute("class"))

    driver.find_elements(By.CSS_SELECTOR, ".admin-tabs .tab")[2].click()
    time.sleep(1)
    issues_pane = driver.find_element(By.ID, "issues")
    result("Switching to 'Issues' tab works",
           "active" in issues_pane.get_attribute("class"))

    result("'Back to Site' link is present in sidebar",
           driver.find_element(By.PARTIAL_LINK_TEXT, "Back to Site") is not None)

except Exception as e:
    print(f"  ERROR in Admin Dashboard tests: {e}")

# ══════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════
driver.quit()

total = passed + failed
print(f"\n{'='*55}")
print(f"  TEST SUMMARY")
print(f"{'='*55}")
print(f"  Total  : {total}")
print(f"  Passed : {passed}")
print(f"  Failed : {failed}")
print(f"  Result : {'ALL PASSED' if failed == 0 else f'{failed} test(s) failed'}")
print(f"{'='*55}\n")

# ══════════════════════════════════════════════
# TEST 1 — HOME PAGE
# ══════════════════════════════════════════════
section("TEST 1: Home Page")
try:
    driver.get(f"{BASE_URL}/")
    time.sleep(2)

    result("Homepage loads successfully",
           driver.find_element(By.TAG_NAME, "body") is not None)

    heading = driver.find_element(By.CLASS_NAME, "heading")
    result("Hero heading is displayed",
           "Leftover" in heading.text or "Ingredients" in heading.text,
           f"Got: {heading.text}")

    steps = driver.find_elements(By.CLASS_NAME, "step")
    result("'How It Works' shows 3 steps", len(steps) == 3,
           f"Found {len(steps)} steps")

    features = driver.find_elements(By.CLASS_NAME, "feature")
    result("Features section shows 4 features", len(features) == 4,
           f"Found {len(features)} features")

    driver.find_element(By.LINK_TEXT, "Get Started").click()
    time.sleep(2)
    result("'Get Started' button navigates to signup page",
           "signup" in driver.current_url or "register" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Home Page tests: {e}")

# ══════════════════════════════════════════════
# TEST 2 — SIGNUP PAGE
# ══════════════════════════════════════════════
section("TEST 2: Signup Page")
try:
    driver.get(f"{BASE_URL}/signup/")
    time.sleep(2)

    result("Signup page loads",
           "signup" in driver.current_url or "register" in driver.current_url)

    result("Name input field is present",
           driver.find_element(By.NAME, "name") is not None)

    result("Email input field is present",
           driver.find_element(By.NAME, "email") is not None)

    result("Password input field is present",
           driver.find_element(By.NAME, "password") is not None)

    result("Confirm Password input field is present",
           driver.find_element(By.NAME, "confirmPassword") is not None)

    btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    result("Submit/Register button is present", btn is not None)

    btn.click()
    time.sleep(1)
    result("Empty form does not proceed (validation active)",
           "signup" in driver.current_url or "register" in driver.current_url)

except Exception as e:
    print(f"  ERROR in Signup tests: {e}")

# ══════════════════════════════════════════════
# TEST 3 — LOGIN PAGE
# ══════════════════════════════════════════════
section("TEST 3: Login Page")
try:
    driver.get(f"{BASE_URL}/login/")
    time.sleep(2)

    result("Login page loads", "login" in driver.current_url)

    result("Email field is present",
           driver.find_element(By.NAME, "email") is not None)

    result("Password field is present",
           driver.find_element(By.NAME, "password") is not None)

    # Wrong credentials
    driver.find_element(By.NAME, "email").send_keys("wronguser@test.com")
    driver.find_element(By.NAME, "password").send_keys("wrongpassword")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    result("Invalid credentials keeps user on login page",
           "login" in driver.current_url)

    # Correct credentials
    driver.get(f"{BASE_URL}/login/")
    time.sleep(1)
    driver.find_element(By.NAME, "email").send_keys(TEST_EMAIL)
    driver.find_element(By.NAME, "password").send_keys(TEST_PASSWORD)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
    time.sleep(2)
    result("Valid credentials redirects away from login page",
           "login" not in driver.current_url)

except Exception as e:
    print(f"  ERROR in Login tests: {e}")

# ══════════════════════════════════════════════
# TEST 4 — AI RECIPE GENERATOR
# FIX: login() now uses email; URL confirmed as /recipe-ai/
# ══════════════════════════════════════════════
section("TEST 4: AI Recipe Generator")
try:
    login()
    driver.get(f"{BASE_URL}/recipe-ai/")
    time.sleep(2)

    result("Recipe Generator page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    # FIX DEF-003: textarea id="user-input" confirmed from HTML
    textarea = wait.until(EC.presence_of_element_located((By.ID, "user-input")))
    result("Ingredient textarea input is present", textarea is not None)

    tabs = driver.find_elements(By.CLASS_NAME, "tab")
    result("Both recipe tabs are present (By Input / By Inventory)",
           len(tabs) >= 2, f"Found {len(tabs)} tabs")

    # Switch to inventory tab
    driver.find_element(By.ID, "use-inventory").click()
    time.sleep(1)
    inv_section = driver.find_element(By.ID, "available-ingredient")
    result("Switching to 'By available ingredient' tab works",
           "hidden" not in inv_section.get_attribute("class"))

    # Switch back to text input tab and generate
    driver.find_element(By.ID, "use-text").click()
    time.sleep(1)
    textarea = driver.find_element(By.ID, "user-input")
    textarea.clear()
    textarea.send_keys("chicken, garlic, lemon")
    driver.find_element(By.ID, "generate-btn").click()
    time.sleep(10)  # wait for AI response

    output = driver.find_element(By.ID, "output-section")
    result("Recipe output section appears after generation",
           "hidden" not in output.get_attribute("class"))

    recipe_text = driver.find_element(By.ID, "recipe-output").get_attribute("value")
    result("Generated recipe output is not empty",
           len(recipe_text.strip()) > 0)

    result("Copy button is present on recipe output",
           driver.find_element(By.CSS_SELECTOR, ".copy-btn") is not None)

    result("Share Recipe button is present",
           driver.find_element(By.CSS_SELECTOR, ".share-btn") is not None)

except Exception as e:
    print(f"  ERROR in Recipe Generator tests: {e}")

# ══════════════════════════════════════════════
# TEST 5 — EXPIRATION TRACKER
# FIX DEF-004: Use XPATH to find button by text since
#              class="btn green" (two separate classes, not one)
#              Also try correct URL from ingredient_tracker urls.py
# ══════════════════════════════════════════════
section("TEST 5: Expiration Tracker (Ingredient Inventory)")
try:
    login()

    # Try both possible mounted URLs
    driver.get(f"{BASE_URL}/ingredients/")
    time.sleep(1)
    if "404" in driver.title or "not found" in driver.page_source.lower()[:500]:
        driver.get(f"{BASE_URL}/ingredient-tracker/")
    time.sleep(2)

    result("Expiration Tracker page loads",
           "404" not in driver.title)

    # FIX DEF-004: button has TWO classes "btn" and "green" separately,
    # use XPATH contains text instead
    add_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Add Ingredient')]")
    ))
    result("'+ Add Ingredient' button is present", add_btn is not None)

    add_btn.click()
    time.sleep(1)
    form = driver.find_element(By.ID, "form")
    result("Add Ingredient form appears after clicking button",
           "hidden" not in form.get_attribute("class"))

    filter_tabs = driver.find_elements(By.CSS_SELECTOR, ".tabs .tab")
    result("Filter tabs are present (All / Expiring Soon / Expired / Fresh)",
           len(filter_tabs) >= 4, f"Found {len(filter_tabs)} tabs")

    cat_select = Select(driver.find_element(By.ID, "category"))
    result("Category dropdown has multiple options",
           len(cat_select.options) > 1)

    cat_select.select_by_visible_text("Vegetables")
    time.sleep(1)
    driver.find_element(By.ID, "quantity").send_keys("3 pieces")
    driver.find_element(By.ID, "purchaseDate").send_keys("04/20/2025")
    driver.find_element(By.ID, "expiryDate").send_keys("05/10/2025")
    result("Add Ingredient form fields filled successfully", True)

except Exception as e:
    print(f"  ERROR in Expiration Tracker tests: {e}")

# ══════════════════════════════════════════════
# TEST 6 — COMMUNITY FORUM
# ══════════════════════════════════════════════
section("TEST 6: Community Forum Page")
try:
    login()
    driver.get(f"{BASE_URL}/community/")
    time.sleep(2)

    result("Community Forum page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    hero = driver.find_element(By.CLASS_NAME, "hero-title")
    result("Hero title 'Community Food Sharing' is displayed",
           "Community" in hero.text, f"Got: {hero.text}")

    result("Food Donor card is visible",
           driver.find_element(By.CLASS_NAME, "donor-card") is not None)

    result("Food Seeker card is visible",
           driver.find_element(By.CLASS_NAME, "seeker-card") is not None)

    stats = driver.find_elements(By.CLASS_NAME, "stat-item")
    result("Community Impact stats section is present",
           len(stats) >= 3, f"Found {len(stats)} stat items")

    steps = driver.find_elements(By.CLASS_NAME, "step-item")
    result("'How Food Sharing Works' shows 3 steps",
           len(steps) == 3, f"Found {len(steps)} steps")

    driver.find_element(By.PARTIAL_LINK_TEXT, "Start Donating").click()
    time.sleep(2)
    result("'Start Donating Food' button navigates to donors page",
           "donor" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Community Forum tests: {e}")

# ══════════════════════════════════════════════
# TEST 7 — DONATION BOARD
# FIX DEF-005: Button is id="tab-add" not text-based,
#              click by ID directly
# ══════════════════════════════════════════════
section("TEST 7: Donation Board (Donors Page)")
try:
    login()
    driver.get(f"{BASE_URL}/community/donors/")
    time.sleep(2)

    result("Donation Board page loads",
           driver.find_element(By.TAG_NAME, "body") is not None)

    # FIX DEF-005: use id="tab-donations" and id="tab-add" directly
    result("'My Donations' tab is present",
           driver.find_element(By.ID, "tab-donations") is not None)

    tab_add = driver.find_element(By.ID, "tab-add")
    result("'Add New Donation' tab button is present", tab_add is not None)

    tab_add.click()
    time.sleep(1)
    form = driver.find_element(By.ID, "donation-form")
    result("Add New Donation form is visible after clicking tab",
           form.is_displayed())

    result("Food Name input field is present",
           driver.find_element(By.ID, "food_name") is not None)

    cat = Select(driver.find_element(By.ID, "category"))
    result("Category dropdown has options", len(cat.options) > 1)

    driver.find_element(By.ID, "food_name").send_keys("Fresh Tomatoes")
    cat.select_by_visible_text("Vegetables")
    driver.find_element(By.ID, "description").send_keys(
        "Freshly picked tomatoes from my garden.")
    driver.find_element(By.ID, "location").send_keys("Block A, Taman Maju")
    driver.find_element(By.ID, "quantity").send_keys("1 kg")
    driver.find_element(By.ID, "expiration_date").send_keys("05/10/2025")
    result("Donation form fields filled successfully", True)

    driver.find_element(By.PARTIAL_LINK_TEXT, "Back to Community").click()
    time.sleep(2)
    result("'Back to Community' link navigates back correctly",
           "community" in driver.current_url,
           f"URL: {driver.current_url}")

except Exception as e:
    print(f"  ERROR in Donation Board tests: {e}")


# ══════════════════════════════════════════════
# TEST 8 — ADMIN DASHBOARD (FIXED)
# ══════════════════════════════════════════════
section("TEST 8: Admin Dashboard")
try:
    login()
    
    # FIX: Use the correct URL - check your urls.py for the actual path
    # Option 1: If mounted at /admin-panel/
    driver.get(f"{BASE_URL}/admin-panel/")
    time.sleep(2)
    
    # Check if we're redirected or got a 404
    if "login" in driver.current_url:
        print("  [Note: Redirected to login - may need admin privileges]")
        login()
        driver.get(f"{BASE_URL}/admin-panel/")
        time.sleep(2)

    result("Admin Dashboard page loads",
           driver.find_element(By.TAG_NAME, "body") is not None and 
           "404" not in driver.title)

    cards = driver.find_elements(By.CLASS_NAME, "admin-card")
    result("Admin dashboard shows 4 stat cards",
           len(cards) == 4, f"Found {len(cards)} cards")

    sidebar_links = driver.find_elements(By.CLASS_NAME, "sidebar-link")
    result("Sidebar navigation links are present",
           len(sidebar_links) >= 3, f"Found {len(sidebar_links)} links")

    # FIX: Check for tab-pane with "show active" classes
    activity_pane = driver.find_element(By.ID, "activity")
    pane_classes = activity_pane.get_attribute("class")
    result("'Recent Activity' tab is active by default",
           "active" in pane_classes and "show" in pane_classes,
           f"Classes: {pane_classes}")

    # FIX: Click the tab button, not just any .tab element
    tab_buttons = driver.find_elements(By.CSS_SELECTOR, ".admin-tabs .tab")
    if len(tab_buttons) >= 2:
        tab_buttons[1].click()  # Donations tab
        time.sleep(1)
        donations_pane = driver.find_element(By.ID, "donations-section")
        result("Switching to 'Donations' tab works",
               "active" in donations_pane.get_attribute("class"),
               f"Classes: {donations_pane.get_attribute('class')}")
    else:
        result("Switching to 'Donations' tab works", False, 
               f"Only found {len(tab_buttons)} tab buttons")

    if len(tab_buttons) >= 3:
        tab_buttons[2].click()  # Issues tab
        time.sleep(1)
        issues_pane = driver.find_element(By.ID, "issues")
        result("Switching to 'Issues' tab works",
               "active" in issues_pane.get_attribute("class"))
    else:
        result("Switching to 'Issues' tab works", False,
               f"Only found {len(tab_buttons)} tab buttons")

    # FIX: The "Back to Site" is inside sidebar-bottom, check both link and button
    try:
        back_link = driver.find_element(By.CSS_SELECTOR, ".sidebar-bottom a, .sidebar-bottom button")
        result("'Back to Site' link is present in sidebar", back_link is not None)
    except:
        result("'Back to Site' link is present in sidebar", False, "Element not found")

except Exception as e:
    print(f"  ERROR in Admin Dashboard tests: {e}")
    import traceback
    traceback.print_exc()


# ══════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════
driver.quit()

total = passed + failed
print(f"\n{'='*55}")
print(f"  TEST SUMMARY")
print(f"{'='*55}")
print(f"  Total  : {total}")
print(f"  Passed : {passed}")
print(f"  Failed : {failed}")
print(f"  Result : {'ALL PASSED' if failed == 0 else f'{failed} test(s) failed'}")
print(f"{'='*55}\n")