# Vinyl Store Web Scraper

## Overview
This project is a web scraping tool designed to search for vinyl records by a specific artist across multiple Chicago-based record store websites. It uses Python with Selenium and BeautifulSoup to extract data from both static and JavaScript-rendered pages.

## Features
- Detects whether a website requires JavaScript to render essential content.
- Searches for an artist using store-specific search bars when available.
- Falls back to parsing all store pages if no search bar is detected.
- Provides debugging information for improved scraping performance.
- Supports multiple record stores and their respective websites.

## Requirements
To run this script, you need the following dependencies:

### Python Libraries:
- `requests`
- `beautifulsoup4`
- `selenium`
- `itertools`
- `sys`
- `functools`

### WebDriver:
- **ChromeDriver**: Required for Selenium. Ensure it's installed and placed in the correct directory.
- The script references `chromedriver` in `/Users/jamesli/VSCode/Projects/VinylWebScraper/chromedriver`, so update this path as needed.

## Installation
1. Clone the repository or download the script.
2. Install the required libraries using:
   ```sh
   pip install requests beautifulsoup4 selenium
   ```
3. Ensure ChromeDriver is installed and accessible from your script’s directory.

## Usage
1. Run the script in a terminal or command prompt:
   ```sh
   python TEST2.py
   ```
2. Enter the name of the artist you want to search for when prompted.
3. The script will attempt to locate the artist’s records across listed vinyl stores.
4. Results will be displayed with store names, locations, and links.

## How It Works
- **Extracts seller name:** Parses the URL to identify the seller when applicable.
- **Determines JavaScript dependency:** Uses BeautifulSoup to check if the content is fully loaded or if JavaScript is required.
- **Finds the search bar:** Locates and interacts with search bars using Selenium.
- **Scrapes alternative pages:** If no search bar is found, it scrapes all subpages of the website for relevant artist information.

## Configuring Store Listings
- Stores are defined using the `VinylStore` class, which takes `name`, `locations`, and `websites` as parameters.
- To add more stores, append them to the `vinyl_stores` list with their corresponding details.

## Example Store Definition
```python
VinylStore("606 Records", "1808 S Allport St, Chicago, IL 60608", "https://www.606records.com")
```

## Troubleshooting
- **Selenium WebDriver Errors:** Ensure that your ChromeDriver matches your Chrome version.
- **Timeouts in finding elements:** Increase `WebDriverWait` duration if elements take longer to load.
- **Websites blocking scraping:** Try adjusting headers to mimic a real browser request.

## Future Improvements
- Expand the list of stores.
- Implement caching for faster results.
- Add support for headless browsing to reduce resource usage.

## License
This project is licensed under the MIT License.

## Contributors
- **James Li** (Original Developer)

