from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired
from V2EX.models import User
from flask_babel import _, lazy_gettext as _l
from mongoengine import connect
#from V2EX.extensions import photos


# 用户注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='用户名不能为空'), Length(6, 12, message='用户名只能在6~12个字符之间')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空'), Length(6, 20, message='密码只能在6~20个字符之间')])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    email = StringField('邮箱', validators=[Email(message='无效的邮箱格式')])
    submit = SubmitField('立即注册')

    # 自定义用户名验证器
    def validate_username(self, username):
        connect('V2EX')
        if User.objects(username = username.data).first():
            raise ValidationError('用户名已注册，请选用其它名称')

    # 自定义邮箱验证器
    def validate_email(self, email):
        connect('V2EX')
        if User.objects(email=email.data).first():
            raise  ValidationError('该邮箱已注册使用，请选用其它邮箱')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='no empty')])
    password = PasswordField('密码', validators=[DataRequired(message='no empty')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('邮箱'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('重置密码提交'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('密码'), validators=[DataRequired()])
    confirm = PasswordField('确认密码', validators=[EqualTo('password', message='两次密码不一致')])
    submit = SubmitField(_l('重置密码提交'))