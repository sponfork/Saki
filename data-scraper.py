import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://mlbbhub.com/counter"

def get_all_hero_slugs(page):
    print("[+] Fetching master hero list from mlbbhub.com/counter...")
    page.goto("https://mlbbhub.com/counter", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_selector("a[href*='/counter/']", timeout=15000)
    
    # Extract all unique hero slugs from counter links on the main page
    links = page.locator("a[href*='/counter/']").all()
    slugs = set()
    
    for link in links:
        href = link.get_attribute("href")
        if href and "/counter/" in href:
            slug = href.split("/counter/")[-1].strip("/")
            if slug:
                slugs.add(slug)
                
    return list(slugs)

def scrape_all_counters():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        hero_slugs = get_all_hero_slugs(page)
        print(f"[+] Found {len(hero_slugs)} total heroes to scrape.")
        
        all_raw_data = []
        
        for idx, slug in enumerate(hero_slugs):
            url = f"{BASE_URL}/{slug}"
            print(f"[{idx+1}/{len(hero_slugs)}] Scraping counter page: {url}")
            
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                page.wait_for_selector("text=PROVEN COUNTERS", timeout=5000)
                
                body_text = page.locator("body").inner_text()
                all_raw_data.append({
                    "hero": slug,
                    "raw_text": body_text
                })
            except Exception as e:
                print(f"[!] Error fetching {slug}: {e}")
                
            # Polite delay to prevent connection drops
            time.sleep(0.4)

        with open("mlbb_raw_stats.json", "w", encoding="utf-8") as f:
            json.dump(all_raw_data, f, indent=4)
            
        print(f"[+] Successfully saved raw data for {len(all_raw_data)} heroes to mlbb_raw_stats.json!")
        browser.close()

if __name__ == "__main__":
    scrape_all_counters()

        


