import lxml
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from operator import itemgetter # for sorting dict in list! 

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

base_url = "https://reddit.com"
subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

def deleteDuplication(result: list):
  seen = set()
  new_result = []
  for d in result:
      t = tuple(d.items())
      if t not in seen:
          seen.add(t)
          new_result.append(d)
  return new_result

def crawlingTarget(name: str):
  url = "https://www.reddit.com/r/{}/top/?t=month".format(name)
  
  try:
    res = requests.get(url, headers = headers)
    res = BeautifulSoup(res.content, 'lxml')
    res = res.find('div', { 'class': 'rpBJOHq2PR60pnwJlUyP0' })
    res = res.find_all('div')
  except Exception as e:
    print(e)
    return

  result = [] # set 
  for r in res:
    try:
      temp_list = {}
      # ad pass
      if r.find('span', { 'class':'_2oEYZXchPfHwcf9mTMGMg8' }):
        continue
      # temp = r.find('article')
      temp_list['url'] = (r.find('a', { 'class': 'SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE' }).get('href'))
      temp_list['text'] = (r.find('h3').get_text().strip())
      temp_list['vote'] = int(r.find('div', { 'class': '_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ' }).get_text().strip())
      temp_list['topic'] = "r/{}".format(name)
      result.append(temp_list)
    except Exception as e:
      print(e)
      continue

  return deleteDuplication(result)


############################ Routes ############################

app = Flask("DayEleven")

@app.route("/") # ?order_by=popular 기본 
def home():
  return render_template("home.html", datas = subreddits)

@app.route("/read") # ?order_by=popular 기본 
def read():
  result = []
  for key in request.args.keys():
    result.extend(crawlingTarget(key))
  
  return render_template("read.html", datas = sorted(result, key=itemgetter('vote'), reverse=True), subreddits = request.args.keys())

# app.run(host="0.0.0.0")
app.run(host="127.0.0.1")