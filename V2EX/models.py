from mongoengine import *
from datetime import datetime
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
from V2EX import db, login_manager
import jwt
from time import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
import uuid

'''article_types = dict('开发语言': ['Python', 'Java', 'JavaScript'],
'Geek': ['Ruby on Rails', 'Tornado', 'MongoDB'],
'城市': ['上海', '杭州'],
'生活那些事': ['心灵有约', '缘分天空','郁闷小屋'])'''

class User(UserMixin,Document):
    username = StringField(max_length=50, required=True, unique=True)
    password_hash = StringField(required=True)
    usertype = IntField(default=1) # 1 代表游民 ， 2 代表正式用户
    email = StringField(required=True, unique=True)
    about_me = StringField(default=u'这个人很懒，什么也没留下~~')
    img_url = StringField(default='/static/images/avatar.jpg')
    big_img_url = StringField(default='/static/images/big.jpg')
    create_time = DateTimeField(default=datetime.now(), required=True)
    last_login_time = DateTimeField(default=datetime.now(), required=True)
    followed = ListField(default=[])
    follower = ListField(default=[])
    token = StringField()
    token_expiration = StringField()

    #def __repr__(self):
        #return '<User {}>'.format(self.username)

    def get_id(self):
        return self.get_auth_token()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, username):
        if not self.is_following(username):
            self.followed.append(username)

    def unfollow(self, username):
        if self.is_following(username):
            self.followed.remove(username)

    def is_following(self, username):
        return (username in self.followed)

    def get_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        connect('V2EX')
        user = User.objects(username = data['username']).first()
        return user

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.username, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            username = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.objects(username=username)

    '''POST部分暂无
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())



    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n
    '''

@login_manager.user_loader
def load_user(token):
    return User.verify_auth_token(token)



class Reply(Document):
    subject_id = ObjectIdField(required=True)
    user = ReferenceField(User)
    content = StringField(required=True)
    create_time = DateTimeField(default=datetime.utcnow(), required=True)
    disabled = BooleanField(default=False)
    reply_type = StringField(default='reply')
    reply_to = StringField(default='notReply')

    def gravatar(self, size=20):
        digest = md5(self.content.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

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
def test_subject():
    connect('V2EX')
    r = Reply(content = 'Reply')
    b = Subject(title = 'Subject 2', tag = 'python', content = 'Hello', reply = [r])
    r2 = Reply(content = 'Reply2')
    b.reply.append(r2)
    print(b.reply)
    b.save()
    x = Subject.objects().first()
    print(x.id)
    print(x)

def test_tag():
    connect('V2EX')
    tag_search = 'python'
    cnt = Subject.objects(tag = 'java').count()
    print(cnt)

if __name__ == '__main__':
    test_subject()