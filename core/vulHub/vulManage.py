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
    commend="echo {} > flag.txt && docker cp ./flag.txt {}:/flag.txt".format(flag,dockerid)
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

def writeFlag2Vulhub():
    '''
    将 flag 写入到对应对应队伍的 docker 靶机中
    :return:
    '''
    with app.app_context():
        flaglist=Flag.query.all()
        for tempflag in flaglist:
            teamName=Team.query.filter(Team.id==tempflag.tid).first().teamname
            text="{}队伍靶机flag:{}已更新".format(teamName,tempflag.flag)
            ulog = ULog(text=text)
            db.session.add(ulog)
            tempVul=Vulhub.query.filter(Vulhub.tid==tempflag.tid).first()
            resetVulhubFlag(tempflag.flag, tempVul.dockerid)
    db.session.commit()
    print("docker flag更新成功")


if __name__ == '__main__':
    delVulhub()