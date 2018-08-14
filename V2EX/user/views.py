from flask import render_template,redirect,url_for,flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_babel import _
from mongoengine import *
from werkzeug.urls import url_parse
from V2EX.user import user
from V2EX.models import User
from V2EX import login_manager
from V2EX.email import send_mail
from .forms import *
from datetime import datetime



@user.route('/<name>')
def userpage(name):
    pass

#--------用户注册登录------------
# 用户注册
@user.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        connect('V2EX')
        u = User(username=form.username.data, email=form.email.data, usertype=1)
        u.set_password(form.password.data)
        token = u.get_auth_token()
        send_mail(u.email, '账户激活', 'activate', username=u.username, token=token)
        u.save()
        flash(_('恭喜您！注册成功！请登录邮箱进行认证！'))
        return redirect(url_for('user.login'))
    return render_template('user/register.html', title=_('Register'), form=form)


# 邮箱认证
@user.route('/activate/<token>')
def activate(token):
    user = User.verify_auth_token(token)
    if user:
        connect('V2EX')
        user.usertype = 2
        user.save()
        flash('激活成功')
        return redirect(url_for('user.login'))
    else:
        flash('激活失败')
        return redirect(url_for('main.index'))


# 用户登录
@user.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        connect('V2EX')
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('无效的用户名或密码'))
            return redirect(url_for('user.login'))
        user.last_login_time = datetime.utcnow()
        user.save()
        login_user(user, remember=form.remember_me.data)
        if user.usertype == 1:
            flash('登录成功！请前往邮箱进行用户激活！')
        else:
            flash('登录成功！')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('user/login.html', title=_('Sign In'), form=form)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))

