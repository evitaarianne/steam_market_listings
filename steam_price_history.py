import requests
import json
import datetime
import os
import time
import csv
import pandas as pd

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
    "steamLoginSecure": "76561199772980047%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwM18yNThFMTJFQ18wRDMxQyIsICJzdWIiOiAiNzY1NjExOTk3NzI5ODAwNDciLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzUzNTE5OTgsICJuYmYiOiAxNzI2NjI0MDQwLCAiaWF0IjogMTczNTI2NDA0MCwgImp0aSI6ICIwMDE0XzI1OEUxMzA0XzZBNzI2IiwgIm9hdCI6IDE3MzUwOTIwNTIsICJydF9leHAiOiAxNzUzMjQyMTY2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNDkuMTQ1LjY4LjEzMSIsICJpcF9jb25maXJtZXIiOiAiNDkuMTQ1LjY4LjEzMSIgfQ.wlDskfz8G_puR4NdW-6X8XCBvPpw_f-0wQzPaMSHtWHr3XIg8rlNs9toPgqQIghNV1-JaANrSO9nBIrEpjETCw",
    "sessionid": "0b0b4c7bf2f3b37443ce096f",
    "browserid": "3358081979100829757",
    "timezoneOffset": "28800,0",
    "steamCountry": "PH%7C4820b4d68695a659fae175d42b4852f1",
}

OUTPUT_FILE = "./data_price_history/price_history.csv"
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def load_existing_data():
    """
    Load existing rows from the CSV file into a set for deduplication.
    """
    existing_rows = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header
            for row in reader:
                # Use tuple of relevant data as key
                existing_rows.add(tuple(row))
    return existing_rows

def scrape_and_save():
    print(f"Writing to file: {os.path.abspath(OUTPUT_FILE)}")
    file_exists = os.path.isfile(OUTPUT_FILE)
    
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "market_hash_name", "date", "price", "volume"])

        for url in URLS:
            try:
                print(f"Fetching data from {url}")
                response = requests.get(url, headers=HEADERS, cookies=COOKIES)
                print(f"Response Status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    market_hash_name = url.split("=")[-1]
                    prices = data.get("prices", [])

                    if not prices:
                        print(f"No prices data for {market_hash_name}")
                        continue

                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    for entry in prices:
                        writer.writerow([timestamp, market_hash_name, entry[0], entry[1], entry[2]])
                    print(f"Data for {market_hash_name} appended to {OUTPUT_FILE}")
                else:
                    print(f"Error {response.status_code}: Failed to fetch data from {url}")
            except Exception as e:
                print(f"An error occurred while fetching data from {url}: {e}")

        csvfile.flush()

def remove_duplicates():
    print(f"Removing duplicates from {OUTPUT_FILE}")
    if os.path.exists(OUTPUT_FILE):
        df = pd.read_csv(OUTPUT_FILE)
        
        if df.empty:
            print(f"{OUTPUT_FILE} is empty. Skipping deduplication.")
            return
        
        print("CSV Columns:", df.columns)
        
        required_columns = {"timestamp", "market_hash_name", "date", "price", "volume"}
        if not required_columns.issubset(df.columns):
            print(f"Missing required columns: {required_columns - set(df.columns)}")
            return

        deduplicated_df = df.sort_values(by="timestamp").drop_duplicates(
            subset=["market_hash_name", "date", "price", "volume"], keep="first"
        )
        deduplicated_df.to_csv(OUTPUT_FILE, index=False)
        print(f"Duplicates removed. Cleaned data saved to {OUTPUT_FILE}")
    else:
        print(f"{OUTPUT_FILE} does not exist. Skipping deduplication.")


if __name__ == "__main__":
    scrape_and_save()
    remove_duplicates()