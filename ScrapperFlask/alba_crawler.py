import lxml
import os
import csv
import requests
from bs4 import BeautifulSoup

# http://norangtongdak.alba.co.kr/job/brand/?page=3&pagesize=50
# Place Title Time Pay Date

def crawlTargetUrl(target_url: str):
  job_total_list = []

  with (requests.get(target_url)) as req:
    target = BeautifulSoup(req.content, 'lxml')
    target = target.find('tbody')
    target = target.find_all('tr')
    for target_line in target:
      job_info = []
      try:
        job_info.append(target_line.find('td', {'class':'local'}).get_text().strip())
        job_info.append(target_line.find('span', {'class':'company'}).get_text().strip())
        job_info.append(target_line.find('span', {'class':'time'}).get_text().strip())
        job_info.append(target_line.find('td', {'class':'pay'}).get_text().strip())
        job_info.append(target_line.find('td', {'class':'regDate'}).get_text().strip())
        # print(job_info, target_url)
        job_total_list.append(job_info)
      except Exception as e: # 두번째 요약 보여주는 tr 태그는 pass시키자 
        # print(target_url, e)
        # job_total_list.append(job_info)
        continue

  return job_total_list

def writeCSVfile(job_total_list: list, main_company: str):
  print(f"{main_company}.csv file is being made ---")
  
  with open('./csv/' + main_company + '.csv', 'w', encoding='utf-8', newline='\n') as f:
    wr = csv.writer(f)
    for job_info in job_total_list:
      wr.writerow(job_info)

  print(f"{main_company}.csv file is being made --- --- done without any exceptions")

def main():
  # setting up 
  os.system("clear")
  alba_url = "http://www.alba.co.kr"
  r = requests.get(alba_url)
  results = BeautifulSoup(r.content, 'lxml')
  results = results.find('div', {'id':'MainSuperBrand'})
  results = results.find('ul', {'class':'goodsBox'})
  results = results.find_all('li')

  # crawl Main pages
  for result in results:
    try:
      target_url = result.find('a', {'class':'goodsBox-info'}).get('href')
      main_company = result.find('span', {'class':'company'}).get_text().strip()
      writeCSVfile(crawlTargetUrl(target_url), main_company)
    except Exception as e:
      print(result, e)
      continue

  # done
  print("--- Each site is done! Check out the CSV files ---")
  return "--- Each site is done! Check out the CSV files ---"

if __name__ == "__main__":
  main()