import os

# import importlib
#
# name='web_example'
# model_filename = "core.checkDown." + name
# # 根据指定的args.model来导入本地models文件夹中的相应args.model + '_model.py'模块
# # 假设如果args.model = cycle_gan，则导入模块models.cycle_gan_model
# modellib = importlib.import_module(model_filename)
# print(modellib.test())
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def aps_test():
    print("a")


scheduler = BlockingScheduler()

scheduler.add_job(func=aps_test, trigger='interval', seconds=5)

scheduler.start()