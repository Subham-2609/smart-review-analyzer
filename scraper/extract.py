import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_driver():
    """Configures an ethical, headless Chrome browser."""
    chrome_options = Options()
    # Run in the background without opening a visible window
    chrome_options.add_argument("--headless")
    
    # Identify our bot transparently
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 SmartReviewBot/1.0")
    
    # Bypass simple security blocks
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def fetch_page_source(url):
    """Fetches the HTML of the target URL with human-like delays."""
    print(f"Initializing connection to: {url}")
    driver = setup_driver()
    
    try:
        # Introduce a randomized ethical delay (2 to 5 seconds)
        delay = random.uniform(2.0, 5.0)
        print(f"Pacing request. Waiting {delay:.2f} seconds...")
        time.sleep(delay)
        
        driver.get(url)
        
        # Wait a moment for JavaScript reviews to render
        time.sleep(3) 
        
        html = driver.page_source
        return html
        
    finally:
        driver.quit()
        print("Browser session closed securely.")

# --- Test Execution ---
if __name__ == "__main__":
    # We will use a generic test URL first before targeting specific products
    test_url = "https://example.com" 
    raw_html = fetch_page_source(test_url)
    
    soup = BeautifulSoup(raw_html, 'html.parser')
    print("\n--- Page Title Extracted ---")
    print(soup.title.text)