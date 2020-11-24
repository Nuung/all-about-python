from flask import Flask, render_template, request, redirect

app = Flask("Alba Scrapper")

@app.route("/")
def home():
    return render_template("potato.html") # render_template 가 templates폴더 찾아줌! 

@app.route("/report")
def report():
    # print(request.args.get('jobname'))
    # print(request.args) -> 리턴하는 자료구조가 dictionary임
    jobname = request.args.get('jobname') # 이걸 template에 넘기고 싶어!! 어떻게 해? 
    # return f"You are looking for a job in {jobname}" 
    
    if jobname: # None type 방지
        jobname = jobname.lower()
    else:
        return redirect("/")
    return render_template("report.html", searchingBy = jobname, something = "Test value")

######################################################################

@app.route("/contact") # 데코레이터라고 부른다! ~ '바로 아래에 있는 함수'만 본다
def contact():
    return "Contact to me, Nuung"

@app.route("/user/<username>") # url 파라미터를 이렇게 전달한다! 
def potato(username):
    return f"Hello!! {username} how r u today?"

app.run(host="127.0.0.1") # repl.it 에서 0.0.0.0 으로 작업해야함~ 