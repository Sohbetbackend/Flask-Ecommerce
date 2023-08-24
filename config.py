import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","") or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SECRET_KEY= os.environ.get("SECRET_KEY") or 'hfouewhfoiwefoquw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'tk']
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, 'static/product_images')
