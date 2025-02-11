from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from web_utils import get_all_pages, is_javascript_rendered, extract_seller_name
from selenium_utils import find_search_bar
from bs4 import BeautifulSoup
import time
import requests
import sys
from functools import partial

print = partial(print, flush=True, file=sys.stdout)

class VinylStore:
    def __init__(self, name, locations, websites):
        self.name = name
        self.locations = locations if isinstance(locations, list) else [locations]
        self.websites = websites if isinstance(websites, list) else [websites]

    def search_artist(self, artist):
        """Use Selenium to search for an artist, falling back to page parsing if no search bar exists."""
        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0")

        service = Service("/Users/jamesli/VSCode/Projects/VinylWebScraper/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        for base_website in self.websites:
            try:
                print(f"\n🔎 Checking website: {base_website}")
                driver.get(base_website)
                time.sleep(3)

                # ✅ Step 1: Detect Search Bar
                search_bars = driver.find_elements(By.CSS_SELECTOR, "input[type='search'], input[name='q'], input[name='search'], input[placeholder*='Search'], input[aria-label*='search'], input[name='keywords'], input[class*='search'], input[class*='query']")

                if search_bars:
                    print(f"✅ Found {len(search_bars)} search bars.")

                    # ✅ Step 2: Handle Multiple Search Bars
                    if len(search_bars) > 1:
                        print("🔍 Multiple search bars detected. Selecting seller-specific one...")
                        
                        seller_name = extract_seller_name(base_website)
                        seller_specific_bars = [
                            bar for bar in search_bars if seller_name.lower() in bar.get_attribute("outerHTML").lower()
                        ]

                        # If there's a seller-specific search bar, use it
                        if seller_specific_bars:
                            search_box = seller_specific_bars[0]  # Prioritize the first seller-specific one
                            print(f"✅ Using seller-specific search bar for {seller_name}.")
                        else:
                            search_box = min(search_bars, key=lambda x: x.size["width"] * x.size["height"])  # Pick the smallest bar
                            print("🔍 No seller-specific search bar found. Using the smallest detected search bar.")

                    else:
                        search_box = search_bars[0]  # ✅ Only one search bar exists, use it.

                    # ✅ Step 3: Search for the Artist
                    print(f"🎵 Searching for '{artist}'...")
                    try:
                        search_box.click()
                        search_box.send_keys(artist)
                        search_box.send_keys(Keys.RETURN)
                        time.sleep(5)
                    except Exception as e:
                        print(f"⚠️ Search interaction failed: {str(e)}")
                        print("Falling back to alternative scraping method...")
                        
                        all_pages = get_all_pages(base_website)

                        if is_javascript_rendered(base_website):
                            print("⚡ JavaScript-based website detected. Using Selenium to extract content...")
                            for website in all_pages:
                                print(f"Checking page: {website}")
                                driver.get(website)
                                time.sleep(3)
                                soup = BeautifulSoup(driver.page_source, "html.parser")
                                if artist.lower() in soup.text.lower():
                                    print(f"🎵 Artist '{artist}' found on subpage: {website}")
                                    driver.quit()
                                    return True
                        else:
                            print("Static HTML website detected. Using Requests for scraping...")
                            for website in all_pages:
                                print(f"Checking page: {website}")
                                try:
                                    headers = {"User-Agent": "Mozilla/5.0"}
                                    response = requests.get(website, headers=headers)
                                    if response.status_code == 200:
                                        soup = BeautifulSoup(response.text, "html.parser")
                                        if artist.lower() in soup.text.lower():
                                            print(f"🎵 Artist '{artist}' found on subpage: {website}")
                                            driver.quit()
                                            return True
                                except Exception as e:
                                    print(f"Error accessing {website}: {str(e)}")
                                    continue
                        continue

                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    page_text = soup.text.lower()
                    
                    # Check for "no results" phrases first
                    no_results_phrases = [
                        f"no results found for {artist.lower()}",
                        f"no matches found for {artist.lower()}",
                        f"no items found for {artist.lower()}",
                        f"couldn't find anything for {artist.lower()}",
                        "no results found",
                        "no matches found",
                        "no items found",
                        "0 results",
                        "nothing found"
                    ]
                    
                    if any(phrase in page_text for phrase in no_results_phrases):
                        print(f"❌ No results found for '{artist}' on {base_website}")
                        continue
                        
                    # If no rejection phrases found, check for artist name
                    if artist.lower() in page_text:
                        print(f"Artist '{artist}' found on {base_website}!")
                        driver.quit()
                        return True

                    print(f"❌ Artist '{artist}' not found in search results. Falling back to page parsing...")

                # ✅ Reference Point 1: No Search Bar Found
                print("⚠️ No search bar detected. Determining alternative scraping method...")

                all_pages = get_all_pages(base_website)

                if is_javascript_rendered(base_website):
                    print("⚡ JavaScript-based website detected. Using Selenium to extract content...")
                    for website in all_pages:
                        print(f"Checking page: {website}")
                        driver.get(website)
                        time.sleep(3)  # Allow page to load
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        if artist.lower() in soup.text.lower():
                            print(f"🎵 Artist '{artist}' found on subpage: {website}")
                            driver.quit()
                            return True
                else:
                    print("Static HTML website detected. Using Requests for scraping...")
                    for website in all_pages:
                        print(f"Checking page: {website}")
                        try:
                            headers = {"User-Agent": "Mozilla/5.0"}
                            response = requests.get(website, headers=headers)
                            if response.status_code == 200:
                                soup = BeautifulSoup(response.text, "html.parser")
                                if artist.lower() in soup.text.lower():
                                    print(f"🎵 Artist '{artist}' found on subpage: {website}")
                                    driver.quit()
                                    return True
                            else:
                                print(f"Failed to access {website}: Status code {response.status_code}")
                        except Exception as e:
                            print(f"Error accessing {website}: {str(e)}")
                            continue

                print(f"❌ Artist '{artist}' not found through alternative scraping methods.")
                continue  # Move to next website if artist not found

            except Exception as e:
                print(f"⚠️ Error processing {base_website}: {e}")

        driver.quit()
        return False
