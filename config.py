import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['steve@delphicapital.co.uk']
    OP_ADMIN = ['natasha@twinningproject.org', 'steve@delphicapital.co.uk']
    POSTS_PER_PAGE = 100
    COMMENTS_PER_PAGE = 3
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'uploads')
    UPLOADS_AUTOSERVE = True
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    NOTIFICATION_DAYS = 14
    STOCK_LOW = 20
