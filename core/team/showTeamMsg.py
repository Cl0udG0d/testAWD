from models import *
from init import app

def getTeamPass(tid):
    '''
    返回 tid 对应的团队密码
    :param tid:
    :return:
    '''
    with app.app_context():
        tempTeam = Team.query.filter(Team.id == tid).first()
        return tempTeam.password

def getTeamToken(tid):
    '''
    返回 tid 对应的团队 token
    :param tid:
    :return:
    '''
    with app.app_context():
        tempTeam = Team.query.filter(Team.id == tid).first()
        return tempTeam.token

def getTeamAllMsg(tid):
    '''
    返回 tid 对应的团队 团队名,密码，token
    :param tid:
    :return:
    '''
    with app.app_context():
        tempTeam = Team.query.filter(Team.id == tid).first()
        return tempTeam.teamname,tempTeam.password,tempTeam.token

if __name__ == '__main__':
    print(getTeamPass('1'))