from mongoengine import *
from datetime import datetime
# 连接数据库
connect('test')   # 连接本地blog数据库

class Tags(EmbeddedDocument):
    name = StringField()
    date = DateTimeField(default=datetime.now())


class Posts(Document):

    title = StringField(max_length=100, required=True)
    content = StringField(required=True)
    tags = ListField(EmbeddedDocumentField('Tags'), required=True)
    categories = ReferenceField('Categories')

class Categories(Document):
    name = StringField(max_length=30, required=True)
    artnum = IntField(default=0, required=True)
    date = DateTimeField(default=datetime.now(), required=True)



tag = Tags(name="Linuxzen")
post = Posts(title="Linuxzen.com", content="Linuxzen.com", tags=[tag])
tag = Tags(name="mysite")
post.tags.append(tag)
post.save()
tags = post.tags
for tag in tags:
    print(tag.name)