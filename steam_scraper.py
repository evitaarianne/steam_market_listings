{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bc01b27a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Data saved to ./data/steam_market_20241218190258.json\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import json\n",
    "import datetime\n",
    "import os\n",
    "\n",
    "URL = \"https://steamcommunity.com/market/listings/3188910/Aoshi/render?currency=1\"\n",
    "\n",
    "HEADERS = {\n",
    "    \"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/116.0.0.0 Safari/537.36\",\n",
    "    \"Referer\": \"https://steamcommunity.com/market/\",\n",
    "    \"Accept-Language\": \"en-US,en;q=0.9\",\n",
    "}\n",
    "COOKIES = {\n",
    "    \"steamLoginSecure\": \"76561199757649520%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MDAxNl8yNThCQURFMF8wMEJCNyIsICJzdWIiOiAiNzY1NjExOTk3NTc2NDk1MjAiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MzQ1Nzc5MjksICJuYmYiOiAxNzI1ODQ5OTQ0LCAiaWF0IjogMTczNDQ4OTk0NCwgImp0aSI6ICIwMDEyXzI1OEJBREVGXzBDODc5IiwgIm9hdCI6IDE3MzQ0ODk5NDMsICJydF9leHAiOiAxNzUyNzI1MDAxLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiNDkuMTQ1LjY0LjIxNyIsICJpcF9jb25maXJtZXIiOiAiNDkuMTQ1LjY0LjIxNyIgfQ.j-ts4zfMTzo1ySFwa9WC2TmNGdSSzblOxxIUvuICFeHpCjE855Pna_oFFM9Z5FIhkphK6CEa3heSd1SEscrwBQ\",\n",
    "    \"sessionid\": \"122d58839a40e0dc29498971\",\n",
    "    \"browserid\": \"3358081979100829757\",\n",
    "    \"timezoneOffset\": \"28800,0\",\n",
    "    \"steamCountry\": \"PH%7C445351b22ded0c8d5da3ef8e60a3c10c\",\n",
    "}\n",
    "\n",
    "OUTPUT_DIR = \"./data\"\n",
    "os.makedirs(OUTPUT_DIR, exist_ok=True)\n",
    "\n",
    "def scrape_and_save():\n",
    "    try:\n",
    "        response = requests.get(URL, headers=HEADERS, cookies=COOKIES)\n",
    "        if response.status_code == 200:\n",
    "            data = response.json()\n",
    "            timestamp = datetime.datetime.now().strftime(\"%Y%m%d%H%M%S\")\n",
    "            filename = f\"{OUTPUT_DIR}/steam_market_{timestamp}.json\"\n",
    "            with open(filename, \"w\") as file:\n",
    "                json.dump(data, file, indent=4)\n",
    "            print(f\"Data saved to {filename}\")\n",
    "        else:\n",
    "            print(f\"Error {response.status_code}: Failed to fetch data\")\n",
    "    except Exception as e:\n",
    "        print(\"An error occurred:\", e)\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    scrape_and_save()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3c967eee",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
