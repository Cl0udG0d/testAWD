import os

from init import app
from models import *

def inputVulhubMsg(title,tid,addr,sshport,detail,sshname,sshpass,dockerid):
    '''
    输入 vulhub 的初始环境
    :param title:
    :param tid:
    :param addr:
    :param sshport:
    :param detail:
    :param sshname:
    :param sshpass:
    :param dockerid:
    :return:
    '''
    with app.app_context():
        tempVul=Vulhub(tid=tid,title=title,addr=addr,sshport=sshport,sshname=sshname,sshpass=sshpass,dockerid=dockerid,detail=detail)
        db.session.add(tempVul)
        db.session.commit()
    return

def resetVulhubFlag(flag,dockerid):
    '''
    重置指定 docker 根目录下的 flag
    :param flag:
    :param dockerid:
    :return:
    '''
    commend="echo {} > flag.txt && docker cp ./flag.txt {}:/flag.txt && rm ./flag.txt".format(flag,dockerid)
    # print(commend)
    os.system(commend)
    return

def delVulhub(dockerid):
    '''
    停止并删除指定 id 的 docker
    :param dockerid:
    :return:
    '''
    commend="docker stop {} && docker rmi {}".format(dockerid,dockerid)
    os.system(commend)
    return



if __name__ == '__main__':
    checkVulIsDown()