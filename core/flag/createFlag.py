import random
from config import FLAG_END,FLAG_START
from models import *
from init import app

def getRandomStr():
    '''
    返回一个长度为8的随机字符串，其组成最终的flag
    :return:
    '''
    return ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',8))

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
    '''
    为每个队伍在 flag表中创建对应的flag信息
    :return:
    '''
    teamList=Team.query.all()
    for tempteam in teamList:
        tid=tempteam.id
        flag=createFlagModel()
        with app.app_context():
            tempFlag = Flag(tid=tid, flag=flag)
            db.session.add(tempFlag)
            db.session.commit()
    return

def updateFlagIndex():
    '''
    更新 flag 表中的每个 flag
    :return:
    '''
    flaglist=Flag.query.all()
    with app.app_context():
        for tempflag in flaglist:
            tempflag.flag=createFlagModel()
            db.session.commit()
    return

if __name__ == '__main__':
    createFlagIndex()