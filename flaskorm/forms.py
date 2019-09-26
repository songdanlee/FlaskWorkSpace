import wtforms
from wtforms.validators import ValidationError
from flask_wtf import FlaskForm
from wtforms import validators
from models import User


# 自定义检验函数
def keywords_valid(form, field):
    """

    :param form:  表单
    :param field:  字段
    这两个不用主动传参
    """
    data = field.data  # 获取input内容，value
    keywords = ["admin", "root", "管理员", "版主"]
    if data in keywords:
        raise ValidationError("不可以使用敏感词命名")


class TaskForm(FlaskForm):
    name = wtforms.StringField(

        render_kw={
            "class": "form-control",
            "placeholder": "任务名称"
        },
        validators=[
            validators.DataRequired("姓名不可以为空"),

            keywords_valid
        ]
    )

    description = wtforms.TextField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务描述"
        },
        validators=[
            validators.DataRequired("描述不可以为空"),
            validators.Length(min=5,message='长度必须大于5')]
    )

    time = wtforms.DateField(
        render_kw={
            "class": "form-control",
            "placeholder": "任务时间"
        }
    )

    public = wtforms.StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "公布任务人"
        }, validators=[
            validators.DataRequired("不可以为空"),
        ]

    )


class LoginForm(FlaskForm):
    '''管理员登陆表单'''
    account = wtforms.StringField(
        label="邮箱",
        validators=[
            validators.DataRequired("请输入邮箱！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            "required": "required"  # 前端加入判别
        }
    )
    # 密码
    pwd = wtforms.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！"
            # "required": "required"
        }
    )

    # 验证旧密码
    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["username"]
        admin = User.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")

    # 两次密码验证
    repwd = wtforms.PasswordField(
        label="管理员重复密码",
        validators=[
            validators.DataRequired("请输入管理员重复密码！"),
            validators.EqualTo('pwd', message="密码不一致！")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码！"
        }
    )

    # 文件上传
    url = wtforms.FileField(
        label="文件",
        validators=[
            validators.DataRequired("请上传文件！")
        ],
        description="文件",
    )

    # 文本框
    info = wtforms.TextAreaField(
        label="简介",
        validators=[
            validators.DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10

        }
    )

    # 选择框
    star = wtforms.SelectField(
        label="星级",
        validators=[
            validators.DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
        }
    )

    submit = wtforms.SubmitField(
        '登陆',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        email = field.data
        admin = User.query.filter_by(email=email).count()
        if admin == 0:
            raise ValidationError("邮箱不存在")
