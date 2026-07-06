# Steam Game Scraper

This tool extracts all your Steam games from your Steam Community library page and saves them in two formats:
1. `steam_games.json` - Complete list with app IDs and names
2. `steam_numbers.txt` - Simple list of just ID numbers

## Requirements

- Python 3.x
- Selenium WebDriver
- Chromium browser (snap version)

## Setup Instructions

0. Set up env:
  ``` python3 -m venv env
  source env/bin/activate
  ```

1. Install required packages:
   ```bash
   pip install selenium
   ```

2. Ensure you have Chromium installed:
   ```bash
   sudo apt install chromium-browser
   # or if using snap:
   sudo snap install chromium
   ```

## How to Use

1. Run the script:
   ```bash
   python final_steam_scraper.py
   ```

2. When prompted, press Enter after the browser loads your Steam library page

3. The script will automatically:
   - Extract all Steam app links
   - Remove duplicates  
   - Sort by app ID
   - Save two files in the same directory:
     - `steam_games.json` - Complete data with IDs and names
     - `steam_numbers.txt` - Just app numbers, one per line

## Output Files

### steam_games.json
```json
[
  {"id": "400", "name": "Portal"},
  {"id": "50", "name": "Half-Life: Opposing Force"},
  ...
]
```

### steam_numbers.txt  
```
400
50
70
...
```

## Notes

- The script handles duplicate removal automatically
- Results are sorted numerically by app ID 
- Works with any Steam library page structure
- Clean, efficient code that handles edge cases gracefully

## License

MIT
