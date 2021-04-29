from functools import wraps
from flask import session,redirect,url_for

def login_required(func):
    '''
    限制团队登录装饰器
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('teamid'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper

def admin_login_required(func):
    '''
    限制管理员登录装饰器
    :param func:
    :return:
    '''
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('adminid'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('adminLogin'))
    return wrapper

