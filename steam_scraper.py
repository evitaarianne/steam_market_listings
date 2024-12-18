import requests
import json
import datetime
import os

# List of endpoints with names and URLs
URLS = [
    {"name": "Ren", "url": "https://steamcommunity.com/market/listings/3188910/Ren/render?currency=1"},
    {"name": "Aoshi", "url": "https://steamcommunity.com/market/listings/3188910/Aoshi/render?currency=1"},
    {"name": "Jeanne", "url": "https://steamcommunity.com/market/listings/3188910/Jeanne/render?currency=1"},
    {"name": "Minnie", "url": "https://steamcommunity.com/market/listings/3188910/Minnie/render?currency=1"},
    {"name": "Celia", "url": "https://steamcommunity.com/market/listings/3188910/Celia/render?currency=1"},
    {"name": "Shizuku", "url": "https://steamcommunity.com/market/listings/3188910/Shizuku/render?currency=1"},
]

# Headers and Cookies for Steam Requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://steamcommunity.com/market/",
    "Accept-Language": "en-US,en;q=0.9",
}
COOKIES = {
    "steamLoginSecure": "76561199757649520%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAxNl8yNThCQURFMF8wMEJCNyIsICJzdWIiOiAiNzY1NjExOTk3NTc2NDk1MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzQ1Nzc5MjksICJuYmYiOiAxNzI1ODQ5OTQ0LCAiaWF0IjogMTczNDQ4OTk0NCwgImp0aSI6ICIwMDEyXzI1OEJBREVGXzBDODc5IiwgIm9hdCI6IDE3MzQ0ODk5NDMsICJydF9leHAiOiAxNzUyNzI1MDAxLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNDkuMTQ1LjY0LjIxNyIsICJpcF9jb25maXJtZXIiOiAiNDkuMTQ1LjY0LjIxNyIgfQ.j-ts4zfMTzo1ySFwa9WC2TmNGdSSzblOxxIUvuICFeHpCjE855Pna_oFFM9Z5FIhkphK6CEa3heSd1SEscrwBQ",
    "sessionid": "122d58839a40e0dc29498971",
    "browserid": "3358081979100829757",
    "timezoneOffset": "28800,0",
    "steamCountry": "PH%7C445351b22ded0c8d5da3ef8e60a3c10c",
}

# Output directory for saved JSON files
OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Scrape data and save to JSON
def scrape_and_save():
    for endpoint in URLS:
        try:
            print(f"Fetching data for: {endpoint['name']}")
            response = requests.get(endpoint['url'], headers=HEADERS, cookies=COOKIES)
            if response.status_code == 200:
                data = response.json()
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{OUTPUT_DIR}/steam_market_{endpoint['name']}_{timestamp}.json"
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"Data saved to {filename}")
            else:
                print(f"Error {response.status_code} for {endpoint['name']}: Failed to fetch data")
        except Exception as e:
            print(f"An error occurred for {endpoint['name']}: {e}")

if __name__ == "__main__":
    scrape_and_save()