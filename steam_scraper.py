import requests
import json
import datetime
import os
import time

URLS = [
    "https://steamcommunity.com/market/listings/3188910/Ren/render?currency=1",
    "https://steamcommunity.com/market/listings/3188910/Aoshi/render?currency=1",
    "https://steamcommunity.com/market/listings/3188910/Jeanne/render?currency=1",
    "https://steamcommunity.com/market/listings/3188910/Minnie/render?currency=1",
    "https://steamcommunity.com/market/listings/3188910/Celia/render?currency=1",
    "https://steamcommunity.com/market/listings/3188910/Shizuku/render?currency=1",
]

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

OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_old_files(directory, hours=3):
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(hours=hours)

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        try:
            if filename.startswith("steam_market_") and filename.endswith(".json"):
                timestamp_str = filename.split("_")[-1].replace(".json", "") 
                file_time = datetime.datetime.strptime(timestamp_str, "%Y%m%d%H%M%S")

                print(f"Checking file: {filename}, timestamp: {file_time}")
                if file_time < cutoff:
                    os.remove(file_path)
                    print(f"Deleted old file: {file_path}")
                else:
                    print(f"File {filename} is not old enough to be deleted.")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")

def scrape_and_save():
    for url in URLS:
        try:
            response = requests.get(url, headers=HEADERS, cookies=COOKIES)
            if response.status_code == 200:
                data = response.json()
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                market_hash_name = url.split("/")[-2]  
                filename = f"{OUTPUT_DIR}/steam_market_{market_hash_name}_{timestamp}.json"
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"Data saved to {filename}")
            else:
                print(f"Error {response.status_code}: Failed to fetch data from {url}")
        except Exception as e:
            print(f"An error occurred while fetching data from {url}: {e}")

if __name__ == "__main__":
    clean_old_files(OUTPUT_DIR, hours=0.0167)  # ~1 minute
    scrape_and_save()