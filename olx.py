from playwright.sync_api import sync_playwright
import pandas as pd
import time

def fetch_olx_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("Loading page...")
            page.goto(url, timeout=60000)
            
            # Wait for page to load completely
            print("Waiting for page to load...")
            page.wait_for_timeout(10000)
            
            # Try to wait for listings to appear
            try:
                page.wait_for_selector("[data-aut-id='itemBox']", timeout=30000)
                print("Listings found!")
            except:
                print("Standard listings selector not found, trying alternative...")
            
            # Multiple selector strategies for titles
            title_selectors = [
                "[data-aut-id='itemTitle']",
                "._2tW1I",
                ".EKdUR",
                "[data-testid='listing-title']",
                "h2 a",
                ".title",
                "a[data-aut-id='itemTitle']"
            ]
            
            # Multiple selector strategies for prices
            price_selectors = [
                "[data-aut-id='itemPrice']",
                "._89yzn",
                ".notranslate",
                "[data-testid='listing-price']",
                ".price",
                "span[data-aut-id='itemPrice']"
            ]
            
            titles = []
            prices = []
            
            # Try different selectors for titles
            for selector in title_selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        titles = [el.text_content().strip() for el in elements if el.text_content()]
                        if titles:
                            print(f"Found {len(titles)} titles using selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # Try different selectors for prices
            for selector in price_selectors:
                try:
                    elements = page.locator(selector).all()
                    if elements:
                        prices = [el.text_content().strip() for el in elements if el.text_content()]
                        if prices:
                            print(f"Found {len(prices)} prices using selector: {selector}")
                            break
                except Exception as e:
                    continue
            
            # If no specific selectors work, try a more general approach
            if not titles or not prices:
                print("Trying general approach...")
                
                # Look for listing containers
                listing_containers = page.locator("[data-aut-id='itemBox'], .EKdUR, ._1kVFD").all()
                
                if listing_containers:
                    print(f"Found {len(listing_containers)} listing containers")
                    titles = []
                    prices = []
                    
                    for container in listing_containers:
                        try:
                            # Try to find title within container
                            title_el = container.locator("a, h2, h3, .title").first
                            title = title_el.text_content().strip() if title_el else "N/A"
                            titles.append(title)
                            
                            # Try to find price within container
                            price_el = container.locator("[data-aut-id='itemPrice'], .price, .notranslate").first
                            price = price_el.text_content().strip() if price_el else "N/A"
                            prices.append(price)
                            
                        except Exception as e:
                            titles.append("N/A")
                            prices.append("N/A")
            
            print(f"Final results: {len(titles)} titles, {len(prices)} prices")
            
            # Debug: Print first few results
            if titles and prices:
                print("Sample data:")
                for i in range(min(3, len(titles), len(prices))):
                    print(f"  Title: {titles[i][:50]}...")
                    print(f"  Price: {prices[i]}")
                    print("  ---")
            
            # Create listings ensuring equal lengths
            min_length = min(len(titles), len(prices))
            if min_length > 0:
                listings = [{"Title": titles[i], "Price": prices[i]} for i in range(min_length)]
            else:
                print("No data found. Let's check what's on the page...")
                # Save page content for debugging
                content = page.content()
                with open("debug_page.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print("Page content saved to debug_page.html")
                listings = []
            
        except Exception as e:
            print(f"Error occurred: {e}")
            listings = []
        
        finally:
            browser.close()
        
        return listings

def main():
    url = "https://www.olx.in/items/q-car-cover"
    print(f"Scraping: {url}")
    
    listings = fetch_olx_data(url)
    
    if listings:
        df = pd.DataFrame(listings)
        df.to_csv("olx_car_covers.csv", index=False)
        print(f"Successfully scraped {len(listings)} listings and saved to olx_car_covers.csv")
        print("\nFirst few entries:")
        print(df.head())
    else:
        print("No listings found. Check the debug_page.html file to see what was loaded.")

if __name__ == "__main__":
    main()

