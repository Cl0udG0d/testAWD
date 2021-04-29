import os

'''
    本机部署靶场 -> web端填写靶机信息  ssh链接用户名密码等 ,docker id等-> 定时checkdown和更新flag
'''

def checkVulhubBeat():
    '''
    依次检测当前项目目录的 vulhub文件夹下的靶场环境是否符合标准
    读取记录并执行符合标准的靶场
    :return:
    '''
    return


def checkVulhubSSHConnect(username,password):
    '''
    检测靶机 ssh 是否能连接
    :param username:
    :param password:
    :return:
    '''
    return