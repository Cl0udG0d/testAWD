import os

from concurrent.futures import ThreadPoolExecutor

MAXWORKERS=2
EXECUTOR = ThreadPoolExecutor(max_workers=MAXWORKERS)

FLAG_START="BiuCtf{"
FLAG_END="}"

SSHPASS="123456"

TOKEN_LENGTH=32
PASSWORD_LENGTH=16

Suffer_Source=50
CheckDown_Source=200
#每轮用的时间为 5*60=300秒
# OneRoundSec=5*60
OneRoundSec=30

STARTTIME=0
TIMENOW=-1
CURRENTROUND=1

DEBUG = True
# DEBUG = False
SECRET_KEY = os.urandom(24)

# HOSTNAME = 'mysql'
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'FanDu_AWD'
USERNAME = 'root'
# PASSWORD = '123mysql'
PASSWORD = 'root'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT,
                                                                               DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

SCHEDULER_API_ENABLED = True

CheckDownPath='./core/checkDown'