from time import strftime, localtime

from init import app
from models import *

def saveTeamAttackEvant(sourcetid,goaltid,round,flag):
    '''
    该函数记录成功的攻击事件 存储在AttackRecord表中
    存储数据为 攻击队伍ID 被攻击队伍ID 当前是第几轮 round
    :param sourcetid:
    :param goaltid:
    :param round:
    :return:
    '''
    with app.app_context():
        sourceTeamName=Team.query.filter(Team.id==sourcetid).first().teamname
        goalTeamName=Team.query.filter(Team.id==goaltid).first().teamname
        text="{} 在{}轮 攻击 {} ,flag为{}".format(sourceTeamName,goalTeamName,round,flag)
        ulog = ULog(text=text)
        event=AttackRecord(sourcetid=sourcetid,goaltid=goaltid,round=round,flag=flag,atttime=strftime('%Y-%m-%d %H:%M:%S', localtime()))
        db.session.add(ulog)
        db.session.add(event)
        db.session.commit()

def getAuthorizationTid(Authorization):
    '''
    查询该 token 对应的队伍的 tid
    存在该token 返回 队伍id ，不存在则返回 -1
    :param Authorization:
    :return:
    '''
    team=Team.query.filter(Team.token == Authorization ).first()
    return team.id if team else -1

def getFlagTid(flag):
    '''
    查询该 flag 对应的受害者队伍 tid
    存在该 flag 返回tid ，不存在则返回 -1
    :param flag:
    :return:
    '''
    teampFlag=Flag.query.filter(Flag.flag==flag).first()
    return teampFlag.tid if teampFlag else -1


def authorizationSaveFlag(flag,Authorization,round):
    '''
    保存通过 curl 提交 flag 的本轮攻击记录函数
    并且将攻击成功的事件记录在数据表 AttackRecord 中
    正确返回 1
    错误返回 0
    该队伍已提交返回 2
    :param flag:
    :param Authorization:
    :return:
    '''
    sourcetid=getAuthorizationTid(Authorization)
    goaltid=getFlagTid(flag)
    if sourcetid==-1 or goaltid==-1:
        return 0
    if checkFlagAlreadySubmit(sourcetid,round,flag):
        return 2
    saveTeamAttackEvant(sourcetid,goaltid,round,flag)
    return 1

def checkFlagAlreadySubmit(sourcetid,flag,round):
    '''
    检测本轮 该队伍 是否提交过 该flag
    :param sourcetid:
    :param flag:
    :param round:
    :return:
    '''
    return AttackRecord.query.filter(AttackRecord.round == round).filter(AttackRecord.sourcetid==sourcetid).filter(AttackRecord.flag==flag).first() != None

def checkFlagIsTrue(flag):
    '''
    检测本轮 flag 表里面是否存在传入的这个flag
    :param flag:
    :return:
    '''
    return Flag.query.filter(Flag.flag==flag).first()==None

def checkFlagIndex(sourcetid,round,flag):
    '''
    检测该队伍提交的flag是否正确
    并且将攻击成功的事件记录在数据表 AttackRecord 中
    正确返回 1
    错误返回 0
    该队伍已提交返回 2
    :param sourcetid:
    :param flag:
    :return:
    '''
    with app.app_context():
        tempUlog=ULog(text="队伍id {} 在第{}轮提交flag {}".format(sourcetid,round,flag))
        db.session.add(tempUlog)
        db.session.commit()
    goaltid = getFlagTid(flag)
    if checkFlagIsTrue(flag):
        return "flag错误","error"
    elif checkFlagAlreadySubmit(sourcetid,round,flag):
        return "flag已提交","submitted"
    saveTeamAttackEvant(sourcetid, goaltid, round,flag)
    return "flag正确","success"




if __name__ == '__main__':
    authorizationSaveFlag()