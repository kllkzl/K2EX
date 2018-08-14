from mongoengine import *
from datetime import datetime


class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    password_hash = StringField(required=True)
    usertype = IntField(default=1) # 1 代表游民 ， 2 代表正式用户
    email = StringField(required=True, unique=True)
    img_url = StringField(default='/static/images/avatar.jpg')
    create_time = DateTimeField(default=datetime.utcnow(), required=True)
    followed = ListField(default=[])
    follower = ListField(default=[])
    token = StringField()
    token_expiration = StringField()


class Reply(Document):
    subject_id = ObjectIdField(required=True)
    user = ReferenceField(User)
    content = StringField(required=True)
    create_time = DateTimeField(default=datetime.utcnow(), required=True)
    disabled = BooleanField(default=False)
    reply_type = StringField(default='reply')
    reply_to = StringField(default='notReply')

    #def gravatar(self, size=20):
        #digest = md5(self.content.lower().encode('utf-8')).hexdigest()
        #return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    #def gravatar(self, size=40, default='identicon', rating='g'):




class Subject(Document):
    title = StringField(max_length=120, required=True)
    user = ReferenceField(User)
    create_time = DateTimeField(default=datetime.utcnow(), required=True)
    update_time = DateTimeField(default=datetime.utcnow(), required=False)
    tag = StringField(max_length=30)
    content = StringField()
    click_count = IntField(default=0)
    reply = ListField(EmbeddedDocumentField('Reply'),default=[])
    reply_count = IntField(default=0)


#--------TEST-----------#
def test_subject_reply():
    connect('test')
    user = User.objects.all().first()
    u2 = User(username = 'test2',password_hash = '666',email = 'test2@qq.com')
    u2.save()
    #b = Subject(title = 'Subject 3', user=User.objects.all().first(), tag = 'python', content = 'Hello', reply = [])
   # b.save()
    b = Subject.objects(title = 'Subject 3').first()
    r = Reply(subject_id = b.id,user=user, content='Reply')
    r.save()
    r2 = Reply(subject_id = b.id, user = u2, content = 'Reply2')
    r2.save()
    b.reply.append(r2)
    b.save()
    print(b.reply)
    x = Subject.objects.all().first()
    print(x.user.username)
    #print(b)

def test_tag():
    connect('V2EX')
    tag_search = 'python'
    cnt = Subject.objects(tag = 'java').count()
    print(cnt)

def test_subject2():
    connect('V2EX')
    sub1 = Subject(title = 'Subject 1', user=User.objects(username = 'kllkzl').first(), tag = 'python', content = 'Hello', reply = [])
    sub1.save()
    sub2 = Subject(title = 'Subject 2', user=User.objects(username = 'test1').first(), tag = 'python', content = 'Hello', reply = [])
    sub2.save()
    x = Subject.objects.all()
    print(x)

def test_user2():
    connect('V2EX')
    u1  = User(username = 'test3',password_hash = '666',email = 'test3@qq.com')
    u1.save()
    u2 = User(username='test4', password_hash='668890756', email='test4@qq.com')
    u2.save()
    x = User.objects.all()
    print(x)
if __name__ == '__main__':
    test_subject2()