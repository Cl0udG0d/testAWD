import os


FLAG_START="BiuCtf{"
FLAG_END="}"

DEBUG = True
# DEBUG = False
SECRET_KEY = os.urandom(24)

# HOSTNAME = 'mysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'FanDu_AWD'
USERNAME = 'root'
PASSWORD = 'root'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                               DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False