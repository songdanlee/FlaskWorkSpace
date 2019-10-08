from flask import Flask
from flask import render_template
from flask import jsonify

from myutils import Calender
app = Flask(__name__)


@app.route("/")
@app.route("/index/")
def index():
    name = "zs"
    return render_template("index.html",**locals())



@app.route("/base/")
def base():
    # abort(401)让一个用户从索引页重定向到一个无法访问的页面（401 表示禁止访问）
    # return redirect("/index/") 重定向
    return render_template("base.html")

@app.route("/userinfo/")
def userInfo():
    caleda_month = Calender().calenda_month()
    return render_template("userinfo.html",**locals())

@app.errorhandler(404)
def handle_bad_request(e):

    return '页面找不到了!orz(´･_･`)', 404


@app.route("/users")
def users_api():
    # 返回json格式
    # return jsonify({"user":"zs","age":19})
    return jsonify(user="zs",age=19)



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=8000,debug=True)