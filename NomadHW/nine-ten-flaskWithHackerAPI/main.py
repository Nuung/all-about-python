import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"
new = f"{base_url}/search_by_date?tags=story" # the newest stories.
popular = f"{base_url}/search?tags=story" # the most popular stories

# fake DB
db = {
  "new":[],
  "popular":[]
}
app = Flask("DayNine")

def crawling_main():
  res_new = requests.get(new).json()
  res_popular = requests.get(popular).json()
  
  # title, url, points, author, number of comments (obj id)
  for r in res_new['hits']:
    temp = {}
    temp["title"] = (r['title'])
    temp["url"] = (r['url'])
    temp["points"] = (r['points'])
    temp["author"] = (r['author'])
    temp["num_comments"] = (r['num_comments'])
    temp["objectID"] = (r['objectID'])
    db["new"].append(temp)

  for r in res_popular['hits']:
    temp = {}
    temp["title"] = (r['title'])
    temp["url"] = (r['url'])
    temp["points"] = (r['points'])
    temp["author"] = (r['author'])
    temp["num_comments"] = (r['num_comments'])
    temp["objectID"] = (r['objectID'])
    db["popular"].append(temp)


def crawling_detail(url: str):
  res = requests.get(url)
  res = res.json()
  item_info = {}
  item_info['title'] = res['title']
  item_info['url'] = res['url']
  item_info['points'] = res['points']
  item_info['author'] = res['author']

  comments = []
  for r in res['children']:
    if r['author']:
        temp = {}
        temp["author"] = (r['author'])
        temp["comment_text"] = (r['text'])
        comments.append(temp)
    else:
        continue
  item_info['comments'] = comments
  return item_info

# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

############################ Routes ############################
# static method
crawling_main()

@app.route("/") # ?order_by=popular 기본 
def home():
  order_by = request.args.get('order_by')
  if order_by:
    order_by = order_by.lower()
    if order_by == "popular":
      return render_template("index.html", datas = db["popular"], isNew = False)
    else: # == "new":
      return render_template("index.html", datas = db["new"], isNew = True)
  else:
    return render_template("index.html", datas = db["popular"], isNew = False)

@app.route("/<objectID>")
def detail(objectID):
  item_info = crawling_detail(make_detail_url(objectID))
  return render_template("detail.html", datas = item_info)

# app.run(host="0.0.0.0")
app.run()