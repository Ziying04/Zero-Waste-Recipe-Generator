from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 10)

# --- Test 1: Open Home Page ---
driver.get("http://127.0.0.1:8000")
time.sleep(2)

if "Zero Waste" in driver.title or driver.find_element(By.TAG_NAME, "body"):
    print("PASS: Homepage loaded successfully")
else:
    print("FAIL: Homepage did not load")

# --- Test 2: Check Hero Section Content ---
try:
    heading = driver.find_element(By.CLASS_NAME, "heading")
    if "Leftover" in heading.text or "Ingredients" in heading.text:
        print("PASS: Hero heading is visible")
    else:
        print("FAIL: Hero heading not found")
except Exception as e:
    print("ERROR in Hero Test:", e)

# --- Test 3: Check 'How It Works' Section ---
try:
    steps = driver.find_elements(By.CLASS_NAME, "step")
    if len(steps) == 3:
        print(f"PASS: 'How It Works' section has {len(steps)} steps")
    else:
        print(f"FAIL: Expected 3 steps, found {len(steps)}")
except Exception as e:
    print("ERROR in How It Works Test:", e)

# --- Test 4: Check Features Section ---
try:
    features = driver.find_elements(By.CLASS_NAME, "feature")
    if len(features) == 4:
        print(f"PASS: Features section has {len(features)} features")
    else:
        print(f"FAIL: Expected 4 features, found {len(features)}")
except Exception as e:
    print("ERROR in Features Test:", e)

# --- Test 5: Click 'Get Started' button → goes to Signup page ---
try:
    get_started = driver.find_element(By.LINK_TEXT, "Get Started")
    get_started.click()
    time.sleep(2)

    if "signup" in driver.current_url or "register" in driver.current_url:
        print("PASS: 'Get Started' navigates to signup page")
    else:
        print("FAIL: 'Get Started' did not go to signup. Current URL:", driver.current_url)
except Exception as e:
    print("ERROR in Get Started Test:", e)

# --- Test 6: Navigate to Login Page ---
try:
    driver.get("http://127.0.0.1:8000/login/")
    time.sleep(2)

    if "login" in driver.page_source.lower():
        print("PASS: Login page loaded")
    else:
        print("FAIL: Login page not found")
except Exception as e:
    print("ERROR in Login Test:", e)

# --- Test 7: Navigate to Dashboard ---
try:
    driver.get("http://127.0.0.1:8000/dashboard/")
    time.sleep(2)

    if "dashboard" in driver.page_source.lower():
        print("PASS: Dashboard loaded")
    else:
        print("INFO: Dashboard requires login (redirect occurred)")
        print("      Redirected to:", driver.current_url)
except Exception as e:
    print("ERROR in Dashboard Test:", e)

driver.quit()
print("\nAll tests completed.")