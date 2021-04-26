import random
from config import FLAG_END,FLAG_START
from models import *
from init import app

def getRandomStr():
    '''
    返回一个长度为8的随机字符串，其组成最终的flag
    :return:
    '''
    return ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',8))

def createFlagModel():
    '''
    生成一个随机的flag 其格式为 flag_start+ rand(8)*4 +flag_end
    用于生成每一轮每一个选手靶机的flag
    :return:
    '''
    flag=''.join("{}{}-{}-{}-{}{}".format(FLAG_START,getRandomStr(),getRandomStr(),getRandomStr(),getRandomStr(),FLAG_END))
    # print(flag)
    return flag

def createFlagIndex():
    teamList
    return

def saveFlag2Mysql():
    return

if __name__ == '__main__':
    createFlagIndex()