import requests
import json
import datetime
import os
import time

URLS = [
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Ren",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Aoshi",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Jeanne",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Minnie",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Celia",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Shizuku",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Noelle",
    "https://steamcommunity.com/market/pricehistory?appid=3188910&market_hash_name=Clara",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0 Safari/537.36",
    "Referer": "https://steamcommunity.com/market/",
    "Accept-Language": "en-US,en;q=0.9",
}
COOKIES = {
    "steamLoginSecure": "76561199772980047%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwM18yNThFMTJFQ18wRDMxQyIsICJzdWIiOiAiNzY1NjExOTk3NzI5ODAwNDciLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzUxNzkwNTMsICJuYmYiOiAxNzI2NDUyMDUyLCAiaWF0IjogMTczNTA5MjA1MiwgImp0aSI6ICIwMDE0XzI1OEUxMkUyX0RDNEQ2IiwgIm9hdCI6IDE3MzUwOTIwNTIsICJydF9leHAiOiAxNzUzMjQyMTY2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNDkuMTQ1LjY4LjEzMSIsICJpcF9jb25maXJtZXIiOiAiNDkuMTQ1LjY4LjEzMSIgfQ.lRq_DasAT0TekVtyNG5g3-kpfVGg5aDC_c_4Wk6M9Xl0yea1J6j2JSWWma82mAZ2QuLI79KcaRJ8lmgIXPTuCg",
    "sessionid": "4199d345365ba98db572156e",
    "browserid": "3358081979100829757",
    "timezoneOffset": "28800,0",
    "steamCountry": "PH%7C4820b4d68695a659fae175d42b4852f1",
}

OUTPUT_DIR = "./data_price_history"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_and_save():
    for url in URLS:
        try:
            response = requests.get(url, headers=HEADERS, cookies=COOKIES)
            if response.status_code == 200:
                data = response.json()
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                market_hash_name = url.split("=")[-1]  
                filename = f"{OUTPUT_DIR}/steam_market_{market_hash_name}_{timestamp}.json"
                with open(filename, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"Data saved to {filename}")
            else:
                print(f"Error {response.status_code}: Failed to fetch data from {url}")
        except Exception as e:
            print(f"An error occurred while fetching data from {url}: {e}")

if __name__ == "__main__":
    scrape_and_save()