import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_HOST = os.environ.get('DB_HOST')
    DB_NAME = os.environ.get('DB_NAME')
    
    DATABASE_URL = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + '/' +DB_NAME
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    ### SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    ###                          'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    LANGUAGES = ['en', 'es', 'zh']
    POSTS_PER_PAGE = 5
    PROMOTIONS_PER_PAGE = 2
    FEATURES_PER_PAGE = 1
    DISTRICTS_PER_PAGE = 3
    STORES_PER_PAGE = 5
    NEWPRODUCT_PER_PAGE = 4
    PRODUCT_PER_PAGE = 8
    PRODUCTBRAND_PER_PAGE = 6
