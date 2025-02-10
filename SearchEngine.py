import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import itertools
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_javascript_rendered(website):
    """Determine if a website requires JavaScript by checking if essential content is missing."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(website, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # If no significant text is found, assume JavaScript is needed
        return len(soup.get_text(strip=True)) < 500  # Adjust threshold if necessary
    return True  # Assume JavaScript is required if request fails

def get_all_pages(base_url):
    """Finds and returns all category or pagination links on the main website."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("/") and not href.startswith("//"):
                links.add(base_url.rstrip("/") + href)
            elif base_url in href:
                links.add(href)
        return list(links)
    return [base_url]



class VinylStore:
    def __init__(self, name, locations, websites):
        self.name = name
        self.locations = locations if isinstance(locations, list) else [locations]
        self.websites = websites if isinstance(websites, list) else [websites]

    def search_artist(self, artist):
        """Search for an artist on the store's websites, handling JavaScript-rendered pages with Selenium."""
        options = Options()
        #options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service("/Users/jamesli/VSCode/Projects/VinylWebScraper/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        for base_website in self.websites:
            try:
                print(f"\n🔎 Checking website: {base_website}")

                all_pages = get_all_pages(base_website)
                print(f"📃 Found {len(all_pages)} pages to search.")

                

                
                for website in all_pages:
                    if is_javascript_rendered(website):
                        print(f"\nDetected JavaScript-based site: {website}. Using Selenium...")
                        driver.get(website)
                        time.sleep(5)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                    
                    else:
                        print(f"\nDetected static HTML site: {website}. Using requests...")
                        headers = {"User-Agent": "Mozilla/5.0"}
                        response = requests.get(website, headers=headers)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, "html.parser")
                        else:
                            continue
                    
                    if artist.lower() in soup.text.lower():
                        driver.quit()
                        return True

            except Exception as e:
                print(f"Error processing {base_website}: {e}")

        driver.quit()
        return False

def animate_search():
    states = ["Running", "rUnning", "ruNning", "runNing", "runnIng", "runniNg", "runninG"]
    for state in itertools.cycle(states):
        sys.stdout.write(f"\r{state}")
        sys.stdout.flush()
        time.sleep(0.3)
        if stop_animation:
            break
    sys.stdout.write("\r")

def search_vinyl_by_artist(artist):
    global stop_animation
    stop_animation = False
    import threading
    animation_thread = threading.Thread(target=animate_search)
    animation_thread.start()

    found_stores = []

    for store in vinyl_stores:
        if store.search_artist(artist):
            found_stores.append(store)

    stop_animation = True
    animation_thread.join()

    print(f"\nSearching for vinyl records by '{artist}' in Chicago record stores...\n")

    if found_stores:
        print(f"Vinyls by {artist} are available at:")
        for store in found_stores:
            print(f"- {store.name} ({', '.join(store.locations)})")
            print(f"  Websites: {', '.join(store.websites)}\n")
    else:
        print(f"No records found for {artist} in the indexed stores.")

vinyl_stores = [

#VinylStore("Reckless Records", ["1379 N Milwaukee Ave, Chicago, IL 60622", "929 W Belmont Ave, Chicago, IL 60657", "26 E Madison St, Chicago, IL 60602"], "https://www.reckless.com"),
VinylStore("Pinwheel Records", "1722 W 18th St, Chicago, IL 60608", ["https://www.pinwheelrecords.com", "https://www.discogs.com/seller/pinwheelrecordschi/profile", "https://www.ebay.com/str/pinwheelrecords"]),
#VinylStore("Groove Distribution", "346 N Justine St, Chicago, IL 60607", "https://www.groovedis.com"),
#VinylStore("Loud Pizza Records", "2833 W Fullerton Ave, Chicago, IL 60647", "https://loudpizza.com/"),
#VinylStore("Rattleback Records", "5405 N Clark St, Chicago, IL 60640", "https://store.rattlebackrecords.com/"),
#VinylStore("Meteor Gem", "3542 S Halsted St, Chicago, IL 60609", "https://meteor-gem.com/?"),
#VinylStore("Let's Boogie Records and Tapes", "3321 S Halsted St, Chicago, IL 60608", ["https://www.letsboogierecords.com", "https://www.discogs.com/seller/lets_boogie_records/profile"]),
#VinylStore("Shady Rest Vintage and Vinyl", "1659 W 18th St, Chicago, IL 60608", "https://www.shadyrestchicago.com/"),
#VinylStore("Thrill Jockey Records", "2044 W Chicago Ave, Chicago, IL 60622", "https://www.thrilljockey.com"),
#VinylStore("Out of the Past Records", "4407 W Madison St, Chicago, IL 60624", ["https://www.outofthepastrecords.com", "https://outofthepastrecords.myshopify.com/"]),
#VinylStore("Dusty Groove", "1120 N Ashland Ave, Chicago, IL 60622", "https://www.dustygroove.com"),
#VinylStore("606 Records", "1808 S Allport St, Chicago, IL 60608", "https://www.606records.com"),
#VinylStore("Bric-A-Brac Records and Collectibles", "2845 N Milwaukee Ave, Chicago, IL 60618", ["https://www.bricabracrecords.com", "https://www.discogs.com/seller/bricabracrecords/profile"]),
#VinylStore("Gramaphone Records", "2843 N Clark St, Chicago, IL 60657", "https://www.gramaphonerecords.com"),
#VinylStore("Record Breakers", "2935 N Milwaukee Ave, Chicago, IL 60618", ["https://www.recordbreakerschi.com", "https://shop.recordbreakerschi.com/"]),
#VinylStore("Round Trip Records", "3455 W Foster Ave, Chicago, IL 60625", ["https://roundtriprecords.store/?", "https://www.discogs.com/seller/RoundTripRecords/profile"]),
#VinylStore("Tone Deaf Records", "4356 N Milwaukee Ave, Chicago, IL 60641", "https://www.tonedeafrecs.com"),
#VinylStore("Music Direct", "1811 W Bryn Mawr Ave, Chicago, IL 60660", "https://www.musicdirect.com"),
#VinylStore("Miyagi Records", "307 E Garfield Blvd, Chicago, IL 60637", "https://www.miyagirecords.com"),
#VinylStore("Bob's Blues & Jazz Mart", "3419 W Irving Park Rd, Chicago, IL 60618", ["https://www.discogs.com/user/bluesandjazzmart/collection", "https://www.ebay.com/str/bluesandjazzmart"]),
#VinylStore("Vintage Vinyl", "925 Davis St, Evanston, IL 60201", "https://www.vintagevinyl.com"),
#VinylStore("Shuga Records", "1272 N Milwaukee Ave, Chicago, IL 60622", "https://www.shugarecords.com"),

]                

#Broken For now
#VinylStore("Urban Outfitters", "1100 N State St, Chicago, IL 60610", "https://www.urbanoutfitters.com"),
#VinylStore("Interstellar Space", "2022 W Montrose Ave, Chicago, IL 60618", "https://www.interstellarspacerecords.com"),
#VinylStore("Val's Halla Records", "239 Harrison St, Oak Park, IL 60304", ["https://valshallarecords.com/sho/", "https://www.valshallarecords.com"]),
#VinylStore("Beverly Records", "11612 S Western Ave, Chicago, IL 60643", ["https://www.musicstack.com/my/index.cgi?seller=260354", "https://www.beverlyrecords.com"]),


#No Website/Facebook
#VinylStore("Animal Records", "4507 N Kedzie Ave, Chicago, IL 60625", "https://www.animalrecords.com"),
#VinylStore("Hip Cat Records", "2735 W Division St, Chicago, IL 60622", "https://www.hipcatrecords.com"),
#VinylStore("Squeezebox Books and Music", "1235 W Belmont Ave, Chicago, IL 60657", "https://www.squeezeboxbooksandmusic.com"),
#VinylStore("Laurie's Planet of Sound", "4639 N Lincoln Ave, Chicago, IL 60625", "https://www.lauriesplanetofsound.com"),
#VinylStore("Hyde Park Records", "1377 E 53rd St, Chicago, IL 60615", "https://www.hydeparkrecords.net"),
#VinylStore("Electric Jungle", "1768 W Greenleaf Ave, Chicago, IL 60626", "https://www.electricjunglechicago.com"),
#VinylStore("Dave's Records", "2604 N Clark St, Chicago, IL 60614", "https://www.facebook.com/davesrecordschicago")








# Example: User Input
artist_to_search = input("Enter the artist name: ")
search_vinyl_by_artist(artist_to_search)

