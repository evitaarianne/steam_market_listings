import requests
import json
import datetime
import os
import time
import csv
import psycopg2
from psycopg2.extras import execute_values

SUPABASE_DB_HOST = "aws-0-us-west-1.pooler.supabase.com"
SUPABASE_DB_NAME = "postgres"
SUPABASE_DB_USER = "postgres.usgsakbuekmtvgfcimfy"
SUPABASE_DB_PASSWORD = "cec!mhv2rqv3nah.WRH"
SUPABASE_DB_PORT = 6543

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
    "steamLoginSecure": "76561199772980047%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAwM18yNThFMTJFQ18wRDMxQyIsICJzdWIiOiAiNzY1NjExOTk3NzI5ODAwNDciLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzU2OTA3MTIsICJuYmYiOiAxNzI2OTY0MjU5LCAiaWF0IjogMTczNTYwNDI1OSwgImp0aSI6ICIwMDE0XzI1OEUxMzQ3XzZFNTZEIiwgIm9hdCI6IDE3MzUwOTIwNTIsICJydF9leHAiOiAxNzUzMjQyMTY2LCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNDkuMTQ1LjY4LjEzMSIsICJpcF9jb25maXJtZXIiOiAiNDkuMTQ1LjY4LjEzMSIgfQ.AuwcTaxkye0wPsJfFIDBHBh2olsegN8gdEPxUqLqrZP2Pamtm8epr09llUsSKZ7fuGTNWKhjq1Nh9Ct16okBAg",
    "sessionid": "dcf9b86768e2fce8594dc29d",
    "browserid": "3358081979100829757",
    "timezoneOffset": "28800,0",
    "steamCountry": "PH%7C4820b4d68695a659fae175d42b4852f1",
}

def connect_to_db():
    """Establish connection to Supabase Postgres database."""
    return psycopg2.connect(
        host=SUPABASE_DB_HOST,
        database=SUPABASE_DB_NAME,
        user=SUPABASE_DB_USER,
        password=SUPABASE_DB_PASSWORD,
        port=SUPABASE_DB_PORT
    )

def insert_data_to_db(data):
    """Insert scraped data into Supabase database."""
    insert_query = """
    INSERT INTO price_history (timestamp, market_hash_name, date, price, volume)
        VALUES %s
        ON CONFLICT (market_hash_name, date, price, volume) DO NOTHING;
    """
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        execute_values(cursor, insert_query, data)
        connection.commit()
        print("Data successfully inserted into the database.")
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

def scrape_and_save_to_db():
    all_data = []
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
                    all_data.append((timestamp, market_hash_name, entry[0], entry[1], entry[2]))
                print(f"Data for {market_hash_name} fetched successfully.")
            else:
                print(f"Error {response.status_code}: Failed to fetch data from {url}")
        except Exception as e:
            print(f"An error occurred while fetching data from {url}: {e}")

    if all_data:
        insert_data_to_db(all_data)

if __name__ == "__main__":
    scrape_and_save_to_db()