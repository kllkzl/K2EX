from V2EX.main import main
from flask import render_template,redirect,g, request, flash, url_for, current_app
from flask_login import current_user, login_required
from mongoengine import connect
from V2EX.models import Reply, Subject, User
from .forms import CommentForm, SubmitArticlesForm
from datetime import datetime


@main.route('/')
@main.route('/index')
def index():
    connect('V2EX')
    subjects = Subject.objects().order_by('create_time')
    return render_template('index.html',subjects = subjects)


@main.route('/nodes/<tag>/')
def nodes(tag):
    connect('V2EX')
    subjects = Subject.objects(tag=tag).order_by('create_time')
    return render_template('index.html', subjects=subjects)

@main.route('/subjectdetails/<id>/', methods=['GET', 'POST'])
@login_required
def subjectdetails(id):
    form = CommentForm(request.form, follow=-1)
    connect('V2EX')
    subject = Subject.objects(id=id).first()

    if form.validate_on_submit():
        user = User.objects(username = current_user.username).first()
        reply = Reply(subject_id = subject.id,
                          content=form.content.data,
                          user= user) # 用current_user可能有问题

        reply_to = form.reply_to.data
        if reply_to :
            reply.reply_type = 'reply2' # 该回复是楼中楼
            reply.reply_to = reply_to
        subject.reply.append(reply)
        subject.reply_count += 1
        reply.save()
        subject.save()
        flash(u'提交评论成功！', 'success')
        return redirect(url_for('.subjectdetails', id=subject.id, page=-1))
    if form.errors:
        flash(u'发表评论失败', 'danger')

    '''page = request.args.get('page', 1, type=int)
    
    if page == -1:
        page = (subject.reply.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = subject.reply.paginate( # sort(key =subject.reply.create_time.asc() )
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    replys = pagination.items
    #article.add_view(article, db)'''
    replys = subject.reply
    subject.click_count += 1
    subject.save()
    return render_template('article_details.html', subject=subject, replys=replys,  form=form, endpoint='.subjectdetails', id=subject.id)
    '''return render_template('article_detials.html', subject=subject,
                           replys=replys, pagination=pagination, page=page,
                           form=form, endpoint='.subjectdetails', id=subject.id)'''

#--------主题管理------------
@main.route('/manage-subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    connect('V2EX')
    user = User.objects(username = current_user.username).first()
    subjects = Subject.objects(user=user).order_by('create_time')
    return render_template('manage_subjects.html', subjects=subjects)


article_types = {'开发语言': ['Python', 'Java', 'JavaScript'],
'Geek': ['Ruby on Rails', 'Tornado', 'MongoDB'],
'城市': ['上海', '杭州'],
'生活那些事': ['心灵有约', '缘分天空','郁闷小屋']}
types = []
for l1 in article_types.keys():
    for l2 in article_types[l1]:
        types.append((l2.lower(), l2))


@main.route('/new-subject/', methods=['GET', 'POST'])
@login_required
def new_subject():
    form = SubmitArticlesForm()
    form.tag.choices = types
    connect('V2EX')
    if form.validate_on_submit():
        tag = form.tag.data
        title = form.title.data
        content = form.content.data
        user = User.objects(username = current_user.username).first()
        subject = Subject(title=title, user=user, tag=tag, content=content)

        subject.save()
        flash(u'发表主题成功！', 'success')
        return redirect(url_for('main.subjectdetails', id=subject.id))
    if form.errors:
        flash(u'发表主题失败', 'danger')
    return render_template('submit_subject.html', form=form)


@main.route('/edit-subject/<id>/', methods=['GET', 'POST'])
@login_required
def edit_subject(id):
    connect('V2EX')
    subject = Subject.objects(id=id).first()
    form = SubmitArticlesForm()
    form.tag.choices = types

    if form.validate_on_submit():
        subject.tag = form.tag.data
        subject.title = form.title.data
        subject.content = form.content.data
        subject.update_time = datetime.utcnow()
        subject.save()
        flash(u'主题更新成功！', 'success')
        return redirect(url_for('main.subjectdetails', id=subject.id))
    form.title.data = subject.title
    form.content.data = subject.content
    form.tag.data = subject.tag
    return render_template('submit_subject.html', form=form)


@main.route('/delete-subject/<id>/', methods=['GET', 'POST'])
@login_required
def delete_subject(id):
    pass


# -------用户资料管理---------
@main.route('/userpage/<name>/', methods=['GET', 'POST'])
@login_required
def userpage(name):
    connect('V2EX')
    user = User.objects(username=name).first()
    subjects = Subject.objects(user=user).all()
    return render_template('userpage.html', subjects=subjects, user=user)


@main.route('/edit-userpage/', methods=['GET', 'POST'])
@login_required
def edit_userpage(name):
    pass


@main.route('/edit-follow/', methods=['GET', 'POST'])
@login_required
def follow():
    pass


@main.route('/edit-follow2/', methods=['GET', 'POST'])
@login_required
def unfollow(name):
    pass
#--------科技版块------------
@main.route('/java')
def tech_java():
    return 'haha'

@main.route('/python')
def tech_python():
    return 'haha'

@main.route('/ml')
def tech_ml():
    return 'haha'

#-------好玩版块------------
@main.route('/create')
def fun_create():
    return 'haha'

@main.route('/pi')
def fun_pi():
    return 'haha'

#------酷工作版块------------
@main.route('/hangzhou')
def job_hangzhou():
    return 'haha'

@main.route('/shanghai')
def job_shanghai():
    return 'haha'

