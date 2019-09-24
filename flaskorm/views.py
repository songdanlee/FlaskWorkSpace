from flask import render_template
from flask import jsonify
from flask import make_response
from flaskorm.myutils import Calender, get_password
from flaskorm.models import Curriculum, User
from flaskorm import app

def loginCheck(func):
    def inner(*args,**kwargs):
        user = request.cookies.get("user")
        if user:
            return  func(*args,**kwargs)
        else:
            return redirect("/login/")
    return inner


@app.route("/index/")
@loginCheck
def index():
    # c = Curriculum.query.get(1)
    # c.c_name = "flask"
    # c.update()
    curriculum_list = Curriculum.query.all()

    return render_template("index.html", curriculum_list=curriculum_list)



def base():
    # abort(401)让一个用户从索引页重定向到一个无法访问的页面（401 表示禁止访问）
    # return redirect("/index/") 重定向
    return render_template("base.html")


@app.route("/userinfo/")
def userInfo():
    caleda_month = Calender().calenda_month()
    return render_template("userinfo.html", **locals())


@app.errorhandler(404)
def handle_bad_request(e):
    return '页面找不到了!orz(´･_･`)', 404


@app.route("/users")
def users_api():
    # 返回json格式
    # return jsonify({"user":"zs","age":19})
    return jsonify(user="zs", age=19)


from flask import request,redirect


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            if username:
                if email:
                    if password:
                        u = User()
                        u.user_name = username
                        u.email = email
                        u.password = get_password(password)
                        u.save()
                        sucmsg = "注册成功"
                    else:
                        errmsg = "密码为空"
                else:
                    errmsg = "邮箱为空"
            else:
                errmsg = "用户名为空"
        else:
            errmsg = "该邮箱已被注册"

    return render_template("register.html", **locals())


@app.route("/login/", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email:
            if password:
                user = User.query.filter_by(email=email).first()
                if user:
                    db_pass = user.password
                    if db_pass == get_password(password):
                        response = make_response(redirect('/index/'))

                        response.set_cookie("user",email)
                        return response
                    else:
                        errmsg = "密码不匹配"
                else:
                    errmsg = "邮箱未注册"
            else:
                errmsg = "密码为空"
        else:
            errmsg = "邮箱为空"

    return render_template("login.html", **locals())

@app.route("/logout/", methods=["POST", "GET"])
def logout():
    response = make_response(redirect('/index/'))
    if request.cookies.get("user"):
        response.delete_cookie("user")
    return response

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
