from models import *
from init import app


def checkFlagAlreadySubmit(sourcetid,flag,round):
    '''
    检测本轮 该队伍 是否提交过 该flag
    :param sourcetid:
    :param flag:
    :param round:
    :return:
    '''
    return AttackRecord.query.filter(AttackRecord.round == round).filer(AttackRecord.sourcetid==sourcetid).filter(AttackRecord.flag==flag).first() != None

def checkFlagIsTrue(flag):
    '''
    检测本轮 flag 表里面是否存在传入的这个flag
    :param flag:
    :return:
    '''
    return Flag.query.filter(Flag.flag==flag).first()==None

def checkFlagIndex(sourcetid,goaltid,round,flag):
    '''
    检测该队伍提交的flag是否正确
    并且将攻击成功的事件记录在数据表 AttackRecord 中
    正确返回 0
    错误返回 1
    该队伍已提交返回 2
    :param sourcetid:
    :param flag:
    :return:
    '''
    if checkFlagIsTrue(flag):
        return 1
    elif checkFlagAlreadySubmit(sourcetid,round,flag):
        return 2
    saveTeamAttackEvant(sourcetid, goaltid, round)
    return 0

def saveTeamAttackEvant(sourcetid,goaltid,round):
    '''
    该函数记录成功的攻击事件 存储在AttackRecord表中
    存储数据为 攻击队伍ID 被攻击队伍ID 当前是第几轮 round
    :param sourcetid:
    :param goaltid:
    :param round:
    :return:
    '''
    with app.app_context():
        event=AttackRecord(sourcetid=sourcetid,goaltid=goaltid,round=round)
        db.session.add(event)
        db.session.commit()


if __name__ == '__main__':
    saveTeamAttackEvant(1,2,1)