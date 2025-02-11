from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
from web_utils import get_all_pages, is_javascript_rendered
from bs4 import BeautifulSoup

def find_search_bar(driver, seller_name=""):
    """Detect and return the most relevant search bar with advanced debugging."""
    
    sys.stdout.flush()  # Force flush at start of function
    
    # Wait for page load
    WebDriverWait(driver, 10).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )
    print("✅ Page fully loaded")
    sys.stdout.flush()
    
    # First check for any search-related buttons that need to be clicked
    search_button_selectors = [
        ".search-toggle",  # Move this to first priority
        "button[aria-label*='search' i]",
        "[data-action='search']",
        ".search-icon",
        ".search-trigger",
        "#search-toggle",
        "[aria-label='Toggle search']",
        ".header-search-toggle"
    ]
    
    print("🔍 Looking for search toggle button...")
    sys.stdout.flush()
    
    search_toggle_success = False
    for selector in search_button_selectors:
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            print(f"✅ Found search trigger button: {selector}")
            sys.stdout.flush()
            
            button.click()
            time.sleep(1)  # Wait for search bar animation
            print("✅ Clicked search toggle button")
            sys.stdout.flush()
            search_toggle_success = True
            break
        except Exception as e:
            print(f"⚠️ Could not find/click {selector}: {str(e)}")
            sys.stdout.flush()
            continue
    
    # Try to find and interact with search input if toggle was successful
    if search_toggle_success:
        try:
            search_box = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='search']"))
            )
            print("✅ Found search box after toggle")
            sys.stdout.flush()
            return search_box
        except Exception as e:
            print(f"❌ Could not find search box after toggle: {str(e)}")
            sys.stdout.flush()
    
    # ✅ Reference Point 1: No Search Bar Found or Not Interactable
    print("⚠️ No search bar detected or not interactable. Determining alternative scraping method...")
    sys.stdout.flush()

    all_pages = get_all_pages(driver.current_url)

    if is_javascript_rendered(driver.current_url):
        print("⚡ JavaScript-based website detected. Using Selenium to extract content...")
        sys.stdout.flush()
        for website in all_pages:
            print(f"Checking page: {website}")
            sys.stdout.flush()
            driver.get(website)
            time.sleep(3)  # Allow page to load
            
    else:
        print("Static HTML website detected. Using Requests for scraping...")
        sys.stdout.flush()
        
        for website in all_pages:
            print(f"Checking page: {website}")
            sys.stdout.flush()
            
            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(website, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    # Continue with your existing parsing logic...
                else:
                    print(f"Failed to access {website}: Status code {response.status_code}")
                    sys.stdout.flush()
            except Exception as e:
                print(f"Error accessing {website}: {str(e)}")
                sys.stdout.flush()
                continue
    
    return None