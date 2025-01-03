import requests
import datetime
import os
from bs4 import BeautifulSoup

# List of URLs to scrape
URLS = [
    "https://steamcommunity.com/market/listings/3188910/Ren",
    "https://steamcommunity.com/market/listings/3188910/Aoshi",
    "https://steamcommunity.com/market/listings/3188910/Jeanne",
    "https://steamcommunity.com/market/listings/3188910/Minnie",
    "https://steamcommunity.com/market/listings/3188910/Celia",
    "https://steamcommunity.com/market/listings/3188910/Shizuku",
    "https://steamcommunity.com/market/listings/3188910/Noelle",
    "https://steamcommunity.com/market/listings/3188910/Clara",
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

# Directory to save output files
OUTPUT_DIR = "./data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_and_save():
    for url in URLS:
        try:
            response = requests.get(url, headers=HEADERS, cookies=COOKIES)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                html_content = soup.prettify()
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                market_hash_name = url.split("/")[-1]  # Extract item name from URL
                filename = f"{OUTPUT_DIR}/steam_market_{market_hash_name}_{timestamp}.html"
                
                # Save the HTML content to a file
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(html_content)
                
                print(f"Data saved to {filename}")
            else:
                print(f"Error {response.status_code}: Failed to fetch data from {url}")
        except Exception as e:
            print(f"An error occurred while fetching data from {url}: {e}")

if __name__ == "__main__":
    scrape_and_save()
