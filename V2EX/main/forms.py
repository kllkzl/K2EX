#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional


class CommentForm(Form):
    name = StringField(u'昵称', validators=[DataRequired()])
    content = TextAreaField(u'添加一条新回复', validators=[DataRequired(), Length(1, 1024)])
    reply_to = StringField()

class DeleteArticleForm(Form):
    subjectId = StringField(validators=[DataRequired()])


class DeleteArticlesForm(Form):
    subjectIds = StringField(validators=[DataRequired()])

class SubmitArticlesForm(Form):
    tag = SelectField(u'节点分类',coerce=str,  validators=[DataRequired()])
    title = StringField(u'主题标题' ) # validators=[DataRequired(), Length(1, 64)]
    content = TextAreaField(u'正文') #  validators=[DataRequired()]