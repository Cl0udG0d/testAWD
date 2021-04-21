import os

'''
配置文件：
    debug=true
    secret_key,session中的24位随机盐值
    MySQL数据库配置
    数据库名为autumnwater
        python3:https://blog.csdn.net/qq562029186/article/details/81325074
'''

DEBUG = True
# DEBUG = False
SECRET_KEY = os.urandom(24)

# HOSTNAME = 'mysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'autumnwater'
USERNAME = 'root'
PASSWORD = 'root'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                               DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False