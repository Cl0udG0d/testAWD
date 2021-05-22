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
        tempSource=Team.query.filter(Team.id==tid).first()
        tempSource.source-=config.Suffer_Source
        db.session.commit()
    return

def addAttackTeamSource(tid,source):
    '''
    给攻击成功的队伍加分
    :param tid:
    :param round:
    :param source:
    :return:
    '''
    with app.app_context():
        tempSource=Team.query.filter(Team.id==tid).first()
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
    #被攻击
    sufferlist=AttackRecord.query.filter(AttackRecord.goaltid==tid).filter(AttackRecord.round==round).all()
    print(len(sufferlist))
    if len(sufferlist)==0:
        return
    else:
        source = int(config.Suffer_Source / len(sufferlist))
        #如果队伍本局被攻击成功，扣分
        if len(sufferlist)!=0:
            delSufferTeamSource(tid)
        #给攻击成功的队伍加分
        for sufferteam in sufferlist:
            sufferteam = db.session.merge(sufferteam)
            attacktid=sufferteam.sourcetid
            addAttackTeamSource(attacktid,source)

def checkVulhubDown(tid):
    '''
    检测某个队伍靶机宕机数量
    :param tid:
    :return:
    '''
    vulList=Vulhub.query.filter(Vulhub.tid==tid).all()
    downNum=0
    for tempVulhub in vulList:
        if not tempVulhub.status:
            downNum+=1
    return downNum

def delDownSource(tid,downNum):
    '''
    删除宕机靶机所属队伍的分数
    :param tid:
    :return:
    '''
    with app.app_context():
        tempSource = Team.query.filter(Team.id==tid).first()
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
    with app.app_context():
        teamlist = Team.query.all()
        for tempteam in teamlist:
            tempteam = db.session.merge(tempteam)
            tid=tempteam.id
            #攻击扣分
            getSufferNum(tid,round)
            #宕机扣分
            downNum=checkVulhubDown(tid)
            if downNum!=0:
                delDownSource(tid,downNum)
        db.session.commit()
    return

def delTeamVulDownSource():
    '''
    在一轮结束后，删除存在宕机靶机队伍对应的分数
    :return:
    '''
    with app.app_context():
        teamlist = Team.query.all()
        for tempteam in teamlist:
            tid = tempteam.id
            downNum = checkVulhubDown(tid)
            if downNum != 0:
                delDownSource(tid, downNum)
        db.session.commit()
    return

if __name__ == '__main__':
    calculateTheScoreIndex(1)