import lxml # for using easy parser
import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

# get Data from the url by request
def crawlingAndParsing(url: str):
  result = requests.get(url)
  result = BeautifulSoup(result.content, 'lxml')
  result = result.find('tbody')
  result = result.find_all('tr')
  return result

# Making List by crawling data
def makeingTargetList(result):
  country_info = [] # data set list
  for row in result:
    items = row.find_all("td")
    name = items[0].text
    code = items[2].text
    if name and code:
      if name != "No universal currency":
        country = {
          'name':name.capitalize(),
          'code': code
        }
        country_info.append(country)
  return country_info

# convertring currency
def convertingCurrency(country_one, country_two):
  print(f"How many {country_one['code']} do you want to convert to {country_two['code']}?")

  try: 
    choice = input("how many: ")
    choice = int(choice)
    url = "https://transferwise.com/gb/currency-converter/{}-to-{}-rate?amount={}".format(country_one['code'], country_two['code'], choice)
    result = requests.get(url)

    if result.status_code != 200:
      raise Exception("http://transferwise.com page dont have that currency code : {} or {}".format(country_one['code'], country_two['code']))

    result = BeautifulSoup(result.content, 'lxml')
    result = result.find('span', {"class": "text-success"}).get_text().strip()
    result = float(result)

    print(f"{format_currency(choice, country_one['code'])} is {format_currency(int(result * choice), country_two['code'])}")

  except ValueError:
    print("That wasn't a number")
    convertingCurrency(country_one, country_two)
  except Exception as e:
    print(e)


#################### MAIN ####################

if __name__ == "__main__":
  os.system("clear")
  url = "https://www.iban.com/currency-codes"
  print("Welcome to CurrencyConvert PRO 2000! \n")
  
  # 함수형 프로그래밍 흉내 
  country_info = makeingTargetList(crawlingAndParsing(url))
  # printing 
  for index, country in enumerate(country_info):
    print(f"#{index} {country['name']}")  

  while True:
    try:
      # input type1
      print("\nWhere are you from? Choose a country by number.\n")
      choice = input("#: ")
      choice = int(choice)
      if choice >= len(country_info):
        raise Exception('Choose a number from the list.')

      country_one = country_info[choice]
      print(f"country: {country_one['name']}, currency code: {country_one['code']}\n\nNow Choose another country\n")

      # input type2
      choice = input("#: ")
      choice = int(choice)
      if choice >= len(country_info):
        raise Exception('Choose a number from the list.')

      country_two = country_info[choice]
      print(f"country: {country_two['name']}, currency code: {country_two['code']}\n")

      #### input main ####
      convertingCurrency(country_one, country_two)
      break
    except ValueError:
      print("That wasn't a number")
      continue
    except Exception as e:
      print(e)
      continue
