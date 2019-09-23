from flask import Flask
from flask import render_template
from myutils import Calender
app = Flask(__name__)


@app.route("/")
def index():
    name = "zs"
    return render_template("index.html",**locals())


@app.route("/base/")
def base():
    name = "zs"
    return render_template("base.html",**locals())

@app.route("/userinfo/")
def userInfo():
    caleda_month = Calender().calenda_month()
    return render_template("userinfo.html",**locals())






if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8000,debug=True)