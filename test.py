import os


def resetVulhubFlag(flag,dockerid):
    commend="echo {} > flag.txt && docker cp ./flag.txt {}:/flag.txt && rm ./flag.txt".format(flag,dockerid)
    print(commend)
    os.system(commend)
    return

def checkIsDown():
    path="./vulhub/"
    filelist=os.listdir(path)
    for file in filelist:
        currdir=os.path.join(path,file)
        print(currdir)
        if os.path.isdir(currdir):
            checkfile=os.path.join(currdir,"check.py")
            import checkfile
            checkfile.check()
    print(filelist)
    return

if __name__ == '__main__':
    checkIsDown()
