import lxml # for using easy parser
import os
import requests
from bs4 import BeautifulSoup


def crawlingAndParsing(url: str):
  result = requests.get(url)
  result = BeautifulSoup(result.content, 'lxml')
  result = result.find('tbody')
  result = result.find_all('tr')
  return result


def makeingTargetList(result):
  country_info = [] # data set list
  for idx, country in enumerate(result):
    name = country.select('td')[0].get_text().strip().lower()
    temp_list = [name[0].upper(), name[1:]]
    name = ''.join(temp_list)
    currency = country.select('td')[2].get_text().strip()
    temp_list = [name, currency]
    if currency:
      print(f"# {idx} {name}")
      country_info.append(temp_list)
  return country_info
  
  
if __name__ == "__main__":
  os.system("clear")
  url = "https://www.iban.com/currency-codes"
  print("Hello! Pleas choose select a country by number: ")
  
  # result = BeautifulSoup(result.text, 'html.parser')
  # xpaht : /html/body/div[1]/div[2]/div/div/div/div/table/tbody
  country_info = makeingTargetList(crawlingAndParsing(url))
  
  while True:
    try:
      inputs = input("#: ")
      inputs = int(inputs)
      if inputs >= len(country_info):
        raise Exception('Choose a number from the list.')

      print(f"You chose {country_info[inputs][0]}\nThe currency code is {country_info[inputs][1]}")
      break
    except ValueError:
      print("That wasn't a number")
      continue
    except Exception as e:
      print(e)
      continue


