import os


def resetVulhubFlag(flag,dockerid):
    commend="echo {} > flag.txt && docker cp ./flag.txt {}:/flag.txt && rm ./flag.txt".format(flag,dockerid)
    print(commend)
    os.system(commend)
    return

if __name__ == '__main__':
    resetVulhubFlag('flag{test_docker_2}','ab64c51efb59')
