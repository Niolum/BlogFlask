import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))

DBUSER = os.environ['DBUSER']
DBPASS = os.environ['DBPASS']
DBHOST = os.environ['DBHOST']
DBNAME = os.environ['DBNAME']

CACHE_TYPE = os.environ['CACHE_TYPE']
CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']

WHITENOISE_MAX_AGE = os.environ['WHITENOISE_MAX_AGE']

database_url = f"postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/{DBNAME}"

SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.environ['SECRET_KEY']


class Config(object):
    CSRF_ENABLED = True
    DEBUG = False
    TESTING = False
    SECRET_KEY = SECRET_KEY
    CACHE_TYPE = CACHE_TYPE
    CACHE_REDIS_HOST = CACHE_REDIS_HOST
    CACHE_REDIS_PORT = CACHE_REDIS_PORT
    CACHE_REDIS_DB = CACHE_REDIS_DB
    CACHE_REDIS_URL = CACHE_REDIS_URL
    CACHE_DEFAULT_TIMEOUT = CACHE_DEFAULT_TIMEOUT
    SQLALCHEMY_DATABASE_URI = database_url
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "blog/static/media")
    ALLOWED_EXTENSIONS = {"png", "jpeg", "jpg"}


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True