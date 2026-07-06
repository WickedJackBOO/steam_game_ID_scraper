import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import os
import json

# Configure Chromium for Selenium (snap version)
chrome_options = ChromeOptions()
chrome_options.binary_location = "/snap/bin/chromium"
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create the WebDriver (connects to Chromium via debug port)
driver = webdriver.Chrome(options=chrome_options)

print("Opening Steam library page...")
# Using a generic URL - user should replace with their own
driver.get("https://steamcommunity.com/id/YOUR_STEAM_ID/games/?tab=all")
print(f"Navigated to: https://steamcommunity.com/id/YOUR_STEAM_ID/games/?tab=all")

# Wait for the page to load fully
time.sleep(5)  # Give more time for complex page loading

# Prompt user before scraping
input("\nPress Enter when you're ready to scrape Steam app links...")

print("Scraping Steam apps...")

# Get all anchor elements and filter for Steam store links
steam_apps = []
try:
    anchors = driver.find_elements(By.TAG_NAME, "a")
    
    print(f"Found {len(anchors)} anchor elements on page")
    
    # Filter for Steam app links
    steam_links_found = 0
    for i, anchor in enumerate(anchors):
        href = anchor.get_attribute("href") or ""
        if "store.steampowered.com/app/" in href:
            try:
                # Extract the app number from URL like store.steampowered.com/app/526870
                parts = href.split("/app/")
                if len(parts) > 1:
                    app_number = parts[1].split("/")[0]
                    
                    # Get text content (game name)
                    name = anchor.text.strip()
                    
                    # Only add if we have a valid app number and name 
                    if app_number.isdigit() and name:
                        steam_apps.append((app_number, name))
                        steam_links_found += 1
                        print(f"Found Steam App: {app_number} Name: {name}")
                        
            except Exception as e:
                # Skip any errors with specific elements but continue processing others
                pass
    
    print(f"\nSuccessfully found {steam_links_found} Steam apps")
    
except Exception as e:
    print(f"Error getting links: {e}")

# Remove duplicates while preserving order
unique_apps = []
seen_ids = set()
for app_id, name in steam_apps:
    if app_id not in seen_ids:
        unique_apps.append({"id": app_id, "name": name})
        seen_ids.add(app_id)

print(f"\nAfter removing duplicates: {len(unique_apps)} unique apps")

# Sort by ID number
unique_apps.sort(key=lambda x: int(x["id"]))

# Save main JSON file with full info
try:
    # Use script's directory for output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "steam_games.json")
    
    with open(json_file_path, "w") as f:
        json.dump(unique_apps, f, indent=2)
    print(f"Successfully saved to {json_file_path}")
except Exception as e:
    print(f"Error saving main JSON: {e}")

# Save separate list with just numbers
try:
    # Use script's directory for output files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_file_path = os.path.join(script_dir, "steam_numbers.txt")
    
    with open(txt_file_path, "w") as f:
        for app in unique_apps:
            f.write(f"{app['id']}\n")
    print(f"Successfully saved to {txt_file_path}")
except Exception as e:
    print(f"Error saving numbers list: {e}")

# Close the driver
print("\nClosing browser...")
driver.quit()

print("Done!")