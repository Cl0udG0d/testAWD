from core.checkDown import check1
from models import *
from init import app

def job1(a, b):                          # 运行的定时任务的函数
    print(str(a) + ' ' + str(b))


def checkDown():
    with app.app_context():
        vulhubList=Vulhub.query.all()
        for vulhub in vulhubList:
            if vulhub.vulname==check1.check.__doc__:
                status=check1.check(vulhub.addr,vulhub.serviceport)
                vulhub.status=status
                db.session.commit()
    print("check service down :)")
    return

if __name__ == '__main__':
    checkDown()