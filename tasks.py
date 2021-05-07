from core.checkDown import check1
from models import *
from init import app
# from flask import current_app
def job1(a, b):                          # 运行的定时任务的函数
    print(str(a) + ' ' + str(b))

def timeCount():
    with app.app_context():
        timeNow=app.config['TIMENOW']
        if timeNow==-1:
            pass
        else:
            app.config['TIMENOW']+=1
    # print(app.config['TIMENOW'])
    return



def checkDown():
    with app.app_context():
        vulhubList=Vulhub.query.all()
        for vulhub in vulhubList:
            if vulhub.vulname==check1.check.__doc__:
                status=check1.check(vulhub.addr,vulhub.serviceport)
                vulhub.status=status
                db.session.commit()
    # print("check service down :)")
    return

if __name__ == '__main__':
    checkDown()