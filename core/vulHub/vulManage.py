import os

from init import app
from models import *

def inputVulhubMsg(title,tid,addr,sshport,detail,sshname,sshpass,dockerid):
    with app.app_context():
        tempVul=Vulhub(tid=tid,title=title,addr=addr,sshport=sshport,sshname=sshname,sshpass=sshpass,dockerid=dockerid,detail=detail)
        db.session.add(tempVul)
        db.session.commit()
    return

def resetVulhubFlag(flag,dockerid):
    commend='{} > flag.txt || docker cp ./flag.txt {}:/flag.txt || rm ./flag.txt'.format(flag,dockerid)
    os.system(commend)
    return

def delVulhub():
    return

if __name__ == '__main__':
    delVulhub()