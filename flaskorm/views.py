from flask import render_template
from flask import jsonify, session
import functools
from myutils import Calender, get_password, Pagintor
from models import Curriculum, User, Leave, models
from main import app,csrf
import math

def loginCheck(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        username = request.cookies.get("username")
        id = request.cookies.get("id", 0)
        session_name = session.get("username")
        if id:
            user = User.query.get(int(id))
            if user:
                if user.user_name == username and session_name == username:
                    return func(*args, **kwargs)
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


from flask import request, redirect


@app.route("/register/", methods=["POST", "GET"])
@csrf.exempt
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

@csrf.exempt
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
                        response = redirect('/index/')
                        response.set_cookie("email", user.email)
                        response.set_cookie("username", user.user_name)
                        response.set_cookie("id", str(user.id))
                        session["username"] = user.user_name
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
    response = redirect('/index/')
    if request.cookies.get("id"):
        response.delete_cookie("id")
        response.delete_cookie("email")
        response.delete_cookie("username")
    if session.get("username"):
        session.pop("username")
    return response

@csrf.exempt
@app.route("/request_label/", methods=["POST", "GET"])
@loginCheck
def request_level():
    if request.method == "POST":
        form = request.form
        level = Leave()
        level.request_id = request.cookies.get("id")
        level.request_name = form.get("request_name")
        level.request_type = form.get("request_type")
        level.start_time = form.get("start_time")
        level.end_time = form.get("end_time")
        level.phone = form.get("phone")
        level.description = form.get("request_description")
        level.status = 0
        level.save()

        return redirect("/leave_list/1/")

    return render_template("request_leave.html")


@app.route("/leave_list/<int:page>/", methods=["POST", "GET"])
@loginCheck
def leave_list(page):
    # 0页  1-5
    # 1页  6-10
    # 2页  11-15
    # id = int(request.cookies.get("id"))
    # offsetnum = (page - 1) * page_num
    # leaves = Leave.query.filter_by(request_id=id).order_by(models.desc("id"))  # 获取该用户所有假条
    # page_total = math.ceil(leaves.count()/page_num)  # 总页数
    # page_list = range(1,page_total+1)  # 页表页码
    #
    # leaves = leaves.offset(offsetnum).limit(page_num) # 获取当前页的数据

    id = int(request.cookies.get("id"))
    leaves = Leave.query.filter_by(request_id=id).order_by(models.desc("id"))
    pagintor = Pagintor(leaves,3)

    page_list = pagintor.page_range # 总页码列表

    leaves = pagintor.page_data(page)

    return render_template("leave_list.html", **locals())


@app.route("/cancle_leave/", methods=["POST", "GET"])
@loginCheck
def cancle_leave():
    if request.method == "POST":
       id = request.form.get("id")
       id = int(id)
       leave = Leave.query.get(id)
       leave.delete()
    elif request.method == "GET":
        id = request.args.get("id")
        id = int(id)
        leave = Leave.query.get(id)
        leave.delete()

    return jsonify({"data":"删除成功"})





from forms import TaskForm

@app.route("/add_task/",methods=["GET","POST"])
def add_task():
    task = TaskForm()
    if request.method == "POST":
        if task.validate_on_submit(): # 有效的post请求
            from_data = task.data  # 校验成功

            time = from_data.get("time")
            public = from_data.get("public")
            description = from_data.get("description")
            name = from_data.get("name")
        else:
            error = task.errors #校验失败
            print(error)
    return render_template("add_task.html",**locals())

from forms import LoginForm


@app.route("/pwd/", methods=["GET", "POST"])
def pwd(): # 表单类详细使用
    #生成表单对象，传入模板
     form = LoginForm()
     if request.method == "POST":
         if form.validate_on_submit():
            #用户返回信息
            data = form.data
            print(data)
         else:
             print(form.errors)
     return render_template("pwd.html", form=form)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)
