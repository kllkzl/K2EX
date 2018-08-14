# Configuration

class Config(object):
    DEBUG = True
    SECRET_KEY = 'Oh My V2EX Bless Nice Work By Kzl '
    WTF_CSRF_SECRET_KEY = 'random key for form'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Mail邮件配置
    MAIL_DEBUG = True
    MAIL_USERNAME = 'kllkzl@qq.com'
    MAIL_PASSWORD = 'niejsdnjrrljbied'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = 'True'
    MAIL_DEFAULT_SENDER = 'kllkzl@qq.com'
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/' +  'flaskbb.sqlite'

    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 5 # 每页评论回复数