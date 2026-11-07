import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://mlbbhub.com/counter"

# Put your target hero list here
HEROES = ["fanny", "masha", "gord", "gusion"] 

def scrape_mlbb_counters():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        all_data = []
        
        for idx, slug in enumerate(HEROES):
            url = f"{BASE_URL}/{slug}"
            print(f"[{idx+1}/{len(HEROES)}] Fetching counters for {slug}...")
            
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                
                # Wait for the counter section to load
                page.wait_for_selector("text=PROVEN COUNTERS", timeout=5000)
                
                # Extract counter items
                # We locate the left grid/container under 'PROVEN COUNTERS'
                counter_list = []
                
                # Target the parent container or counter card rows
                # From your screenshot, each item has a hero name and a score like '+3.0 pp'
                rows = page.locator("div:has-text('PROVEN COUNTERS') ~ div, table tr, .grid > div").all()
                
                # Alternative clean approach: query text elements matching the page layout
                # Grab all text blocks containing '+X.X pp'
                body_text = page.locator("body").inner_text()
                
                all_data.append({
                    "hero": slug,
                    "raw_text": body_text
                })
                
            except Exception as e:
                print(f"[!] Error fetching {slug}: {e}")
                
            time.sleep(0.5)

        with open("mlbb_raw_stats.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4)
            
        print("[+] Scraped raw data successfully!")
        browser.close()

if __name__ == "__main__":
    scrape_mlbb_counters()

        


