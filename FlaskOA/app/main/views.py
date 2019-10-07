import os
import functools

from flask import render_template
from flask_restful import Resource
from flask import jsonify, session
from app.models import Curriculum, User, Leave, models

from . import main
from app import api
from .forms import TaskForm
from .forms import LoginForm
from app.myutils import Calender, get_password, Pagintor


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


@main.route("/index/")
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


@main.route("/userinfo/")
def userInfo():
    """
    用户中心，课程
    """
    caleda_month = Calender().calenda_month()
    return render_template("userinfo.html", **locals())


@main.errorhandler(404)
def handle_bad_request(e):
    return '页面找不到了!orz(´･_･`)', 404


@main.route("/users")
def users_api():
    # 返回json格式
    # return jsonify({"user":"zs","age":19})
    return jsonify(user="zs", age=19)


from flask import request, redirect


@main.route("/register/", methods=["POST", "GET"])
# @csrf.exempt
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


# @csrf.exempt
@main.route("/login/", methods=["POST", "GET"])
@main.route("/", methods=["POST", "GET"])
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


@main.route("/logout/", methods=["POST", "GET"])
def logout():
    response = redirect('/index/')
    if request.cookies.get("id"):
        response.delete_cookie("id")
        response.delete_cookie("email")
        response.delete_cookie("username")
    if session.get("username"):
        session.pop("username")
    return response


# @csrf.exempt
@main.route("/request_label/", methods=["POST", "GET"])
@loginCheck
def request_level():
    """
    请假功能，get请求返回页面，post请求，生成假条，保存到数据库
    """
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


@main.route("/leave_list/<int:page>/", methods=["POST", "GET"])
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
    pagintor = Pagintor(leaves, 3)

    page_list = pagintor.page_range  # 总页码列表

    leaves = pagintor.page_data(page)

    return render_template("leave_list.html", **locals())


@main.route("/cancle_leave/", methods=["POST", "GET"])
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

    return jsonify({"data": "删除成功"})





@main.route("/add_task/", methods=["GET", "POST"])
def add_task():
    task = TaskForm()
    if request.method == "POST":
        if task.validate_on_submit():  # 有效的post请求
            from_data = task.data  # 校验成功

            time = from_data.get("time")
            public = from_data.get("public")
            description = from_data.get("description")
            name = from_data.get("name")
        else:
            error = task.errors  # 校验失败
            print(error)
    return render_template("add_task.html", **locals())





@main.route("/pwd/", methods=["GET", "POST"])
def pwd():  # 表单类详细使用
    # 生成表单对象，传入模板
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # 用户返回信息
            data = form.data
            print(data)
        else:
            print(form.errors)
    return render_template("pwd.html", form=form)


from settings import STATIC_FILES_DIR


@main.route("/pic/", methods=["GET", "POST"])
def picture():
    if request.method == "POST":
        pic = request.files.get("photo")
        """
        print([i for i in dir(pic) if not i.startswith("_")])
        print("-"*20)
        print(pic.content_length)
        print("-" * 20)
        print(pic.content_type)
        print("-" * 20)
        print(pic.filename)
        print("-" * 20)
        print(pic.headers)
        print("-" * 20)
        print(pic.mimetype)
        print("-" * 20)
        print(pic.mimetype_params)
        print("-" * 20)
        print(pic.name)
        print("-" * 20)
        """
        filepath = "img/%s" % pic.filename
        savepath = os.path.join(STATIC_FILES_DIR, filepath)

        pic.save(savepath)

    return render_template("picture.html")


@api.resource("/Api/leave/")
class LeaveApi(Resource):

    def __init__(self):
        super(LeaveApi, self).__init__()
        self.result = {
            "version": '1.0',
            "method": "",
            "data": ""
        }

    def get(self):
        self.result["method"] = "get"
        data = request.args
        id = data.get("id")
        key = data.get("filter")
        value = data.get("value")

        if id:
            leave = Leave.query.get(int(id))
            self.result["data"] = self.save_data(leave)
        elif key and value:

            leaves = Leave.query.filter_by(request_type=value)

            res = []
            for leave in leaves:
                res.append(self.save_data(leave))
            self.result["data"] = res

        else:
            leaves = Leave.query.all()
            res = []
            for leave in leaves:
                res.append(self.save_data(leave))
            self.result["data"] = res

        return self.result

    def save_data(self, leave):
        resu = {
            "request_name": leave.request_name,
            "request_type": leave.request_type,
            "start_time": leave.start_time,
            "end_time": leave.end_time,
            "description": leave.description,
            "phone": leave.phone
        }
        return resu

    def post(self):
        self.result["method"] = "post"
        data = request.form

        request_id = data.get("request_id")
        request_name = data.get("request_name")
        request_type = data.get("request_type")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        description = data.get("description")
        phone = data.get("phone")

        leave = Leave()

        leave.request_id = request_id
        leave.request_name = request_name
        leave.request_type = request_type
        leave.start_time = start_time
        leave.end_time = end_time
        leave.description = description
        leave.phone = phone
        leave.save()

        self.result["data"] = self.save_data(leave)
        return self.result

    # def put(self):
    #     self.result["method"] = "put"
    #
    #     data = request.form
    #     id = data.get("id")
    #     leave = Leave.query.get(int(id))
    #     if leave:
    #         for key, v in data.items():
    #             if key != "id":
    #                 setattr(leave, key, v)
    #         leave.save()
    #
    #         self.result["data"] = self.save_data(leave)
    #     else:
    #         self.result["data"] = "没有这个id的数据"
    #
    #     return self.result

    def put(self):
        self.result["method"] = "put"

        data = request.form
        id = data.get("id")
        leaves = Leave.query.filter_by(id=int(id))
        if leaves.count() > 0:
            leaves.update(data)
            for leave in leaves:
                leave.save()
            self.result["data"] = self.save_data(leave)
        else:
            self.result["data"] = "没有id为%s的数据" %id
        return self.result

    def delete(self):
        self.result["method"] = "delete"
        data = request.form
        id = data.get("id")
        leave = Leave.query.get(int(id))
        leave.delete()

        self.result["data"] = "id为%s的数据，已经删除" % id
        return self.result


if __name__ == '__main__':
    main.run(host="127.0.0.1", port=8000, debug=True)
