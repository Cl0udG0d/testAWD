import os


FLAG_START="BiuCtf{"
FLAG_END="}"

SSHPASS="123456"

TOKEN_LENGTH=32
PASSWORD_LENGTH=16

<<<<<<< HEAD
DEBUG = False
=======
Suffer_Source=50
CheckDown_Source=200

DEBUG = True
>>>>>>> 2d5622005fefca31c2a92a8d5965be3df19048c4
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