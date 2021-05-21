import importlib
from models import *
from init import app
from config import OneRoundSec
from core.vulHub.vulManage import writeFlag2Vulhub
from core.flag.calculateTheScore import delTeamVulDownSource,calculateTheScoreIndex
from core.flag.createFlag import createFlagIndex

'''
    https://www.cnblogs.com/wanghui-garcia/p/11233515.html
'''
def job1(a, b):
    # 运行的定时任务的函数
    # 测试函数
    print(str(a) + ' ' + str(b))


def timeCount():
    '''
    时间递增 定时任务
    :return:
    '''
    with app.app_context():
        timeNow=app.config['TIMENOW']
        if timeNow==-1:
            pass
        else:
            app.config['TIMENOW']+=1
    # print(app.config['TIMENOW'])
    return

def checkOneVulhub(vulhub,ip,port):
    '''
    python 动态调用模块
    :param vulhub:
    :param ip:
    :param port:
    :return:
    '''
    model_filename = "core.checkDown." + vulhub
    modellib = importlib.import_module(model_filename)
    # print(modellib.test())
    return modellib.check(ip,port)

def checkDownMain():
    '''
    检测宕机函数
    :return:
    '''
    with app.app_context():
        vulhubList=Vulhub.query.all()
        for vulhub in vulhubList:
            status=checkOneVulhub(vulhub.vulname,vulhub.addr,vulhub.serviceport)
            vulhub.status = status
            db.session.commit()
    print("check service down :)")
    return

def newRoundFlush():
    '''
    新一轮刷新：
    1，攻击成功分数瓜分与扣分
    2，宕机扣分
    3，flag 数据库刷新与 容器刷新
    :return:
    '''
    nowround = int(app.config['TIMENOW'] / OneRoundSec) + 1
    # 扣除本轮靶机宕机队伍的分数
    # delTeamVulDownSource()
    # 对攻击成功的事件进行加减分处理
    calculateTheScoreIndex(nowround)
    # 创建flag
    createFlagIndex()
    # 将 flag 写入靶机
    writeFlag2Vulhub()
    return




if __name__ == '__main__':
    checkDownMain()