from init import app
from models import *
import config


def delSufferTeamSource(tid):
    '''
    减去被攻击队伍的分数
    :param tid:
    :return:
    '''
    with app.app_context():
        tempSource=Source.query.filter(tid=tid).first()
        tempSource.source-=config.Suffer_Source
        db.session.commit()
    return

def addAttackTeamSource(tid,round,source):
    '''
    给攻击成功的队伍加分
    :param tid:
    :param round:
    :param source:
    :return:
    '''
    attacklist=AttackRecord.query.filter(goaltid=tid).filter(round=round).all()
    for team in attacklist:
        attacktid=team.tid
        with app.app_context():
            tempSource=Source.query.filter(tid=attacktid).first()
            tempSource.source+=source
            db.session.commit()
    return

def getSufferNum(tid,round):
    '''
    获取某队伍在某一轮中被攻击的次数,并且进行受害队伍的扣分,攻击成功队伍的加分
    :param tid:
    :param round:
    :return:
    '''
    sufferlist=AttackRecord.query.filter(goaltid=tid,round=round).all()
    if len(sufferlist)==0:
        return
    else:
        source = config.Suffer_Source / len(sufferlist)
        delSufferTeamSource(tid)
        addAttackTeamSource(tid,round,source)

def checkVulhubDown(tid):
    '''
    检测某个队伍靶机宕机数量
    :param tid:
    :return:
    '''
    vulList=Vulhub.query.filter(tid=tid).all()
    downNum=0
    for tempVulhub in vulList:
        if tempVulhub.status:
            downNum+=1
    return downNum

def delDownSource(tid,downNum):
    '''
    删除宕机靶机所属队伍的分数
    :param tid:
    :return:
    '''
    with app.app_context():
        tempSource = Source.query.filter(tid=tid).first()
        tempSource.source -=config.CheckDown_Source*downNum
        db.session.commit()
    return

def calculateTheScoreIndex(round):
    '''
    获得所有的团队的 id
    传递至 getSufferNum,进行本轮被攻击扣分计算
    传递至 checkVulhubDown,进行本轮宕机扣分计算
    :param round:
    :return:
    '''
    teamlist=Team.query.all()
    for tempteam in teamlist:
        tid=tempteam.id
        getSufferNum(tid,round)
        downNum=checkVulhubDown(tid)
        if downNum!=0:
            delDownSource(tid,downNum)
    return

if __name__ == '__main__':
    calculateTheScoreIndex()