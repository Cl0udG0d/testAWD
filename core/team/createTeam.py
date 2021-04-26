import random
import config
from init import app
from models import *

def getRandomStr(length):
    '''
    返回一个长度为 length 的随机字符串
    :return:
    '''
    return ''.join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',int(length)))


def getRandomToken():
    '''
    返回随机生成的团队 token 值 ,默认为 32位
    :return:
    '''
    return getRandomStr(config.TOKEN_LENGTH)

def getRandomPass():
    '''
    返回随机生成的团队 password 值,默认为 16位
    :return:
    '''
    return getRandomStr(config.PASSWORD_LENGTH)

def createTeam(teamname):
    '''
    创建一个队伍,存储其队伍名,密码,token
    :param teamname:
    :return:
    '''
    teampass=getRandomPass()
    token=getRandomToken()
    with app.app_context():
        tempTeam=Team(teamname=teamname,password=teampass,token=token)
        db.session.add(tempTeam)
        # 事务提交
        db.session.commit()
    return

if __name__ == '__main__':
    createTeam("team1")