import os
import requests

# checking page's status code is 200 or not
def isPageUp(url: str, status_code: int):
  if status_code == 200:
    print(f"{url} is up!")
  else:
    print(f"{url} is down!")

# crawling target url for status code
def crawlTargetUrl(input_string: list):
  for url in input_string:
    url = url.strip()
    if "http://" not in url:
      url = "http://" + url
    # try - catch for error
    try:
      result = requests.get(url)
      isPageUp(url, result.status_code)
    except Exception:
      print(url + " is down!")
      continue


if __name__ == "__main__":
  input_string = input("Welcome to IsItDown.py By Nuung!!\nPlease write a URL or URLs you want to check. (separated by comma)\n")
  crawlTargetUrl(input_string.split(","))

  # try again if u input 'y'
  while input("Do you want to start over? y/n ") == "y":
    try:
      os.system('clear')
    except Exception:
      os.system('cls')

    input_string = input("Welcome to IsItDown.py By Nuung!!\nPlease write a URL or URLs you want to check. (separated by comma)\n")
    crawlTargetUrl(input_string.split(","))