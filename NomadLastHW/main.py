import re
import csv
import lxml
import requests
import setting # config file
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request, Blueprint, abort
from exporter import save_to_file
from jinja2 import TemplateNotFound

"""
The website should also be able to export to .csv
You need to implement a fake db to make repeat searches faster.

These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q={python}
https://weworkremotely.com/remote-jobs/search?term={python}
https://remoteok.io/remote-dev+{python}-jobs

Good luck!
"""

db = {} # fake db 

# 공백 제거 함수
def no_space(text):
	text1 = re.sub('&nbsp; | &nbsp;| \n|\t|\r', '', text)
	text2 = re.sub('\n\n', '', text1)
	return text2

# delete Duplication in list 'dict'
def deleteDuplication(result: list):
  seen = set()
  new_result = []
  for d in result:
      t = tuple(d.items())
      if t not in seen:
          seen.add(t)
          new_result.append(d)
  return new_result

# write CSV file 
def writeCSVfile(job_lists: list, query: str):
  print(f"{query}.csv file is being made ---")
  
  with open('csv/' + query + '.csv', 'w', encoding='utf-8', newline='\n') as f:
    wr = csv.writer(f)
    for job_info in job_lists:
      wr.writerow(job_info.values())

  print(f"{query}.csv file is being made --- --- done without any exceptions")

#                                                                #
############################ Crawling ############################
#                                                                #

# STACK OVER FLOW
def stackoverflowCrawling(url: str):
  try:
    datas = [] # return
    res = requests.get(url, headers = setting.HEADERS)
    res = BeautifulSoup(res.content, 'lxml')
    res = res.find('div', {'class':'listResults'})
    result = res.find_all('div')[1:]
    for r in result:
      temp = {}
      try:
        if r.find('div', {'class':'grid'}):
          temp['url'] = (setting.BASE_URL[0] + r.find('a').get('href'))
          title = (r.find('a').get_text().strip())
          
          if title == "Undo":
            continue

          temp['title'] = title
          temp['company'] = (no_space(r.find('h3').get_text().strip()).split("\n")[0])
          
          icon = r.find('img').get('src')
          if not icon: 
            temp['icon'] = setting.DEFAULT_ICON
          else:
            temp['icon'] = icon
          datas.append(temp)
      except Exception as e:
        print(f"stackoverflowCrawling: {e}")
        continue

    return datas
  except Exception:
    return 

# WE WORK REMOTELY
def weworkremotelyCrawling(url: str):
  try:
    datas = [] # return
    res = requests.get(url, headers = setting.HEADERS)
    res = BeautifulSoup(res.content, 'lxml')
    res = res.find('article')
    result = res.find_all('li')
    for r in result:
      temp = {}
      try:
        temp['url'] = (setting.BASE_URL[1] + r.find('a').get('href'))
        temp['title'] = (r.find('span', {'class':'title'}).get_text().strip())
        temp['company'] = (r.find('span', {'class':'company'}).get_text().strip())
        icon = r.find('div', {'class':'flag-logo'}).get('style')
        icon = icon.split("background-image:url(")[-1].split(")")[0]
        if not icon: 
          temp['icon'] = setting.DEFAULT_ICON
        else:
          temp['icon'] = icon
        datas.append(temp)
      except Exception as e:
        print(f"weworkremotelyCrawling: {e}")
        continue

    return datas
  except Exception:
    return

# REMOTEOK
def remoteokCrawling(url: str):
  try:
    datas = [] # return
    res = requests.get(url, headers = setting.HEADERS)
    res = BeautifulSoup(res.content, 'lxml')
    res = res.find('table', {'id':'jobsboard'})
    # res = res.find('tbody')
    result = res.find_all('tr', {'class':'job'})
    for r in result:
      temp = {}
      try:
        temp['url'] = (setting.BASE_URL[2] + r.get('data-url'))
        temp['company'] = r.get('data-company')
        temp['title'] = (r.find('h2').get_text().strip())
        icon = r.find('img').get('src')
        if not icon: 
          temp['icon'] = setting.DEFAULT_ICON
        elif icon == "/assets/logo.png?1" or icon == "/assets/hot.gif":
          temp['icon'] = setting.DEFAULT_ICON
        else:
          temp['icon'] = icon
        datas.append(temp)
      except Exception as e:
        print(f"remoteokCrawling: {e}")
        continue
    
    return datas
  except Exception:
    return

#                                                              #
############################ Routes ############################
#                                                              #

app = Flask("DayThirteenAndFourteen")

@app.route("/") 
def index():
  return render_template("index.html")

@app.route("/search") 
def search():
  try:
    datas = []
    if request.args.get('query'):
      query = request.args.get('query').lower()

      if query not in db: # fake db에 처음 들어가는거면 크롤링 해야지 
        datas.extend(stackoverflowCrawling(setting.CRAWLING_URL[0].format(query)))
        datas.extend(weworkremotelyCrawling(setting.CRAWLING_URL[1].format(query)))
        datas.extend(remoteokCrawling(setting.CRAWLING_URL[2].format(query)))
        datas = deleteDuplication(datas)
        db[query] = datas
        writeCSVfile(datas, query)
      else: # 그게 아니면 fake db에서 불러오고 
        datas = db[query]

    # for data in datas:
      # print(data)
    return render_template("search.html", datas = datas, query = query)
  except Exception:
    return redirect("/")

@app.route('/export')
def export():
  try:
    query = request.args.get('query')
    if not query: # parameter check
      raise Exception()
    query = query.lower()

    jobs = db.get(query)
    if not jobs: # fake db check
      raise Exception()

    file_name = f"csv/{query}.csv"
    return send_file(file_name, mimetype='text/csv', attachment_filename=f"{query}.csv",# 다운받아지는 파일 이름. 
                      as_attachment = True)  

  except Exception:
    return redirect("/")

  

app.run(debug=True, use_reloader=True)