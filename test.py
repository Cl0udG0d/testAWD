from init import app
from models import *
def calculateTheScoreIndex(round):
    '''
    获得所有的团队的 id
    传递至 getSufferNum,进行本轮被攻击扣分计算
    传递至 checkVulhubDown,进行本轮宕机扣分计算
    :param round:
    :return:
    '''
    with app.app_context():
        teamlist=Team.query.all()
        for tempteam in teamlist:
            tid=tempteam.id
            print(tid)

        db.session.commit()
    return

if __name__ == '__main__':
    calculateTheScoreIndex(1)