from typing import cast
import requests
from bs4 import BeautifulSoup
from itertools import combinations_with_replacement
from time import sleep

url = "http://board.sejong.ac.kr/boardlist.do"

querystring = {"bbsConfigFK":"337"}
headers = {
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en,ko-KR;q=0.9,ko;q=0.8,en-US;q=0.7"
}

try:
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        response = BeautifulSoup(response.content, 'lxml')
        for target in response.find_all('tr'):
            print(" ".join(target.get_text().strip().replace("\n", " ").split()))
except Exception as e:
    print(e)