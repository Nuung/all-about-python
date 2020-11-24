from flask import Flask

app = Flask("Alba Scrapper")

@app.route("/")
def home():
    return "Hello! Welcome to My world by Flask!!"

app.run(host="127.0.0.1")