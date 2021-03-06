import os
from random import random

import config
from flask import Flask
from exts import db
# from flask_apscheduler import APScheduler
from config import OneRoundSec
from models import *


app = Flask(__name__)
app.config.from_object(config)
# scheduler = APScheduler()                  # 实例化 APScheduler
# scheduler.init_app(app)                    # 把任务列表放入 flask
# scheduler.start()
db.init_app(app)

