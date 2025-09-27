import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = "https://www.indeed.com/jobs?q=Data+Analyst&l=Lucknow"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 OPR/122.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Connection": "keep-alive"
    }

response = requests.get(URL, headers = headers)
print(response.status_code)
