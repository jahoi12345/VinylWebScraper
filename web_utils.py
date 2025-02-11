import requests
from bs4 import BeautifulSoup

def extract_seller_name(url):
    """Extract seller username from Discogs or similar URLs."""
    url_parts = url.rstrip('/').split('/')
    if "seller" in url_parts:
        seller_index = url_parts.index("seller") + 1
        return url_parts[seller_index]
    return ""

def is_javascript_rendered(website):
    """Determine if a website requires JavaScript by checking if essential content is missing."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(website, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return len(soup.get_text(strip=True)) < 500
    return True

def get_all_pages(base_url):
    """Finds and returns all category or pagination links on the main website."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("/"):
                links.add(base_url.rstrip("/") + href)
            elif href.startswith("http") and base_url.split("//")[1].split("/")[0] in href:
                links.add(href)
        print(f"Found {len(links)} subpages to check")
        return list(links)
    return [base_url] 