import time
import re   
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_driver():
    """Configures an ethical, headless Chrome browser."""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # Identify as a standard desktop Chrome user
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def fetch_page_source(url):
    """Fetches the HTML of the target URL with human-like delays."""
    print(f"\n[+] Initializing connection to: {url}")
    driver = setup_driver()
    
    try:
        delay = random.uniform(2.0, 5.0)
        print(f"[+] Pacing request. Waiting {delay:.2f} seconds...")
        time.sleep(delay)
        
        driver.get(url)
        time.sleep(3) # Wait for JavaScript to load
        
        return driver.page_source
    finally:
        driver.quit()


def parse_flipkart_reviews(product_url, max_pages=3):
    """Transforms URL and extracts paginated reviews using a Persistent Session."""
    
    if "/p/" in product_url:
        base_review_url = product_url.replace("/p/", "/product-reviews/")
    else:
        base_review_url = product_url
        
    print(f"[*] Base URL for extraction: {base_review_url}")
    extracted_data = []
    
    print("\n[*] Booting up persistent browser session...")
    # 1. We boot the driver ONCE before the loop begins
    driver = setup_driver() 
    
    try:
        # --- PHASE 3: THE PAGINATION LOOP ---
        for page_num in range(1, max_pages + 1):
            print(f"\n--- Scraping Page {page_num} of {max_pages} ---")
            
            if "?" in base_review_url:
                page_url = f"{base_review_url}&page={page_num}"
            else:
                page_url = f"{base_review_url}?page={page_num}"
                
            # 2. Human-like delay before clicking to the next page
            delay = random.uniform(2.0, 4.0)
            print(f"[+] Pacing request. Waiting {delay:.2f} seconds...")
            time.sleep(delay)
            
            # 3. Fetch the page using the SAME persistent browser tab
            driver.get(page_url)
            time.sleep(3) # Wait for React/JS to render
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            anchor_blocks = soup.find_all(string=re.compile("Review for:"))
            print(f"[*] Found {len(anchor_blocks)} structural anchors on page {page_num}.")
            
            if len(anchor_blocks) == 0:
                print("[*] No reviews found or bot-wall hit. Stopping pagination.")
                break 
                
            for anchor in anchor_blocks:
                try:
                    parent_div = anchor.parent
                    
                    # Extract Text
                    review_text_div = parent_div.find_next_sibling('div')
                    if not review_text_div:
                        continue 
                    review_text = review_text_div.get_text(strip=True)
                    
                    # Extract Rating
                    rating_div = parent_div.find_previous_sibling('div')
                    rating = "N/A"
                    if rating_div:
                        rating_text = rating_div.get_text(separator=" ", strip=True)
                        match = re.search(r'(\d(\.\d)?)', rating_text)
                        if match:
                            rating = match.group(1)
                    
                    extracted_data.append({
                        "platform": "Flipkart",
                        "rating": rating,
                        "text": review_text
                    })
                    
                except Exception as e:
                    print(f"[!] Warning: Structural shift detected on a block. Skipping. ({e})")
                    
    finally:
        # 4. We securely close the browser only AFTER all pages are scraped
        driver.quit()
        print("\n[+] Browser session closed securely.")
            
    return extracted_data

# --- Test Execution ---
if __name__ == "__main__":
    # The HP Victus test link
    test_url = "https://www.flipkart.com/hp-victus-intel-core-i5-13th-gen-13420-h-16-gb-512-gb-ssd-windows-11-home-6-graphics-nvidia-geforce-rtx-3050-15-fa2196tx-gaming-laptop/p/itm44c5abe672c87?pid=COMHGWQESQN4BAHV"
    
    print("--- Starting Flipkart Extraction Engine ---")
    reviews = parse_flipkart_reviews(test_url)
    
    print("\n--- Extraction Results ---")
    for i, review in enumerate(reviews, 1):
        print(f"\nReview {i}:")
        print(f"Stars: {review['rating']}")
        print(f"Text: {review['text'][:100]}...") # Printing just the first 100 characters so it doesn't flood your terminal